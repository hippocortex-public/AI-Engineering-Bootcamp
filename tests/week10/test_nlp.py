from copy import deepcopy
import json
import math
from pathlib import Path
import subprocess
import sys
import unittest
import numpy as np
from examples.week10.nlp import (ContractError,LABELS,adapt_head,artifact,classify,classification_metrics,choose_threshold,
 digest,embedding_report,entities,extract,fit_initial,mask_entities,predict_artifact,process,read_data,
 sentence_spans,span_metrics,specialized,subset,summarize,summary_overlap,train_bundle,trained,validate_dataset)


class LearningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=read_data('tickets.json');cls.bundle=trained()

    def test_partitions_disjoint_and_balanced(self):
        validate_dataset(self.rows)
        self.assertEqual({s:len(subset(self.rows,s)) for s in ('train','adapt','validation','test')},
                         {'train':36,'adapt':12,'validation':12,'test':12})
        self.assertEqual(len({r['group_id'] for r in self.rows}),72)

    def test_shared_group_and_duplicate_text_rejected(self):
        for mutation in ('group','text'):
            rows=deepcopy(self.rows);train=next(r for r in rows if r['split']=='train');test=next(r for r in rows if r['split']=='test')
            if mutation=='group':test['group_id']=train['group_id']
            else:test['text']=train['text']
            with self.assertRaises(ContractError):validate_dataset(rows)

    def test_missing_label_and_duplicate_id_rejected(self):
        rows=deepcopy(self.rows);rows[1]['id']=rows[0]['id']
        with self.assertRaises(ContractError):validate_dataset(rows)
        rows=[r for r in self.rows if not(r['split']=='train' and r['label']=='acces')]
        with self.assertRaises(ContractError):validate_dataset(rows)

    def test_test_only_word_never_fits_vocabulary_or_weights(self):
        rows=deepcopy(self.rows)
        for row in rows:
            if row['split']=='test':row['text']+=' marqueuruniquetest'
        bundle=train_bundle(rows)
        self.assertNotIn('marqueuruniquetest',bundle['vectorizer'].vocabulary_)
        self.assertEqual(bundle['vectorizer'].vocabulary_,self.bundle['vectorizer'].vocabulary_)
        np.testing.assert_allclose(bundle['baseline'].coef_,self.bundle['baseline'].coef_,rtol=1e-12)
        self.assertEqual(bundle['selected_epochs'],self.bundle['selected_epochs'])

    def test_partition_guard_blocks_test_training(self):
        with self.assertRaises(ContractError):fit_initial(subset(self.rows,'test'))
        with self.assertRaises(ContractError):adapt_head(self.bundle['vectorizer'],self.bundle['baseline'],subset(self.rows,'test'),1)

    def test_adaptation_changes_weights_not_features_or_base(self):
        before=deepcopy(self.bundle['baseline'].coef_)
        candidate=adapt_head(self.bundle['vectorizer'],self.bundle['baseline'],subset(self.rows,'adapt'),1)
        self.assertFalse(np.array_equal(candidate.coef_,before))
        np.testing.assert_array_equal(self.bundle['baseline'].coef_,before)
        self.assertEqual(candidate.coef_.shape[1],len(self.bundle['vectorizer'].vocabulary_))

    def test_epoch_validation(self):
        for epochs in (0,-1,True):
            with self.assertRaises(ContractError):adapt_head(self.bundle['vectorizer'],self.bundle['baseline'],subset(self.rows,'adapt'),epochs)

    def test_metrics_label_order_and_coverage(self):
        report=classification_metrics(self.bundle['vectorizer'],self.bundle['baseline'],subset(self.rows,'test'),.5)
        self.assertEqual(report['labels'],LABELS)
        self.assertEqual(sum(map(sum,report['confusion_matrix'])),12)
        self.assertTrue(0<=report['macro_f1_argmax']<=1)
        self.assertTrue(0<=report['coverage']<=1)

    def test_zero_features_require_review(self):
        result=classify('quasar nébuleuse intergalactique',self.bundle)
        self.assertEqual(result['status'],'review');self.assertIsNone(result['label'])
        for text in ('',None,' '):
            with self.assertRaises(ContractError):classify(text,self.bundle)

    def test_no_acceptance_selective_accuracy_is_none(self):
        report=classification_metrics(self.bundle['vectorizer'],self.bundle['baseline'],subset(self.rows,'test'),1.0)
        self.assertEqual(report['coverage'],0);self.assertIsNone(report['selective_accuracy'])

    def test_threshold_selection_fails_if_no_candidate_is_eligible(self):
        class UniformHead:
            classes_=np.asarray(LABELS)
            def predict_proba(self,matrix):
                return np.full((matrix.shape[0],3),1/3)
        with self.assertRaises(ContractError):
            choose_threshold(self.bundle['vectorizer'],UniformHead(),subset(self.rows,'validation'))

    def test_invalid_metrics_threshold(self):
        for threshold in (True,float('nan'),-1,1.1):
            with self.assertRaises(ContractError):classification_metrics(self.bundle['vectorizer'],self.bundle['baseline'],subset(self.rows,'test'),threshold)

    def test_artifacts_reproduce_both_variants(self):
        for variant in ('baseline','adapted'):
            saved=json.loads(json.dumps(artifact(self.bundle,variant)))
            for row in subset(self.rows,'test'):
                loaded=predict_artifact(saved,row['text']);live=classify(row['text'],self.bundle,variant)
                self.assertEqual(loaded['label'],live['label'])
                self.assertAlmostEqual(loaded['max_probability'],live['max_probability'],places=12)

    def test_artifact_hash_and_rehashed_shape_guard(self):
        saved=artifact(self.bundle);saved['coef'][0][0]+=.1
        with self.assertRaises(ContractError):predict_artifact(saved,'jeton expiré')
        saved=artifact(self.bundle);saved['coef'][0].pop()
        body={k:v for k,v in saved.items() if k!='content_hash'};saved['content_hash']=digest(body)
        with self.assertRaises(ContractError):predict_artifact(saved,'jeton expiré')

    def test_deterministic_training_in_fixed_environment(self):
        repeat=train_bundle(self.rows)
        np.testing.assert_allclose(repeat['baseline'].coef_,self.bundle['baseline'].coef_,rtol=1e-12)
        self.assertEqual(repeat['selected_epochs'],self.bundle['selected_epochs'])


class ExtractionTests(unittest.TestCase):
    def test_values_statuses_and_offsets(self):
        for row in read_data('examples.json'):
            for name,field in extract(row['text']).items():
                self.assertEqual(field['value'],row['expected'][name])
                self.assertEqual(field['status'],row['expected_status'][name])
                self.assertTrue(all(row['text'][e['start']:e['end']]==e['text'] for e in field['evidence']))

    def test_duration_decimal_units(self):
        for text,value in [('latence de 1,5 s','1500'),('durée de 250 ms','250'),('latence de 0,25 ms','0.25')]:
            self.assertEqual(extract(text)['duration_ms']['value'],value)

    def test_ambiguity_and_repeated_identical_value(self):
        self.assertEqual(extract('HTTP 503 puis HTTP 503')['http_status']['status'],'present')
        result=extract('HTTP 401 puis HTTP 503')['http_status']
        self.assertEqual(result['status'],'ambiguous');self.assertIsNone(result['value']);self.assertEqual(len(result['evidence']),2)

    def test_missing_is_not_ambiguous_and_mention_not_assertion(self):
        self.assertEqual(extract('Aucun code disponible')['http_status']['status'],'missing')
        self.assertEqual(extract('Aucun HTTP 500 observé')['http_status']['value'],500)

    def test_environment_normalization(self):
        result=extract('production et prod')['environment']
        self.assertEqual(result['status'],'present');self.assertEqual(result['value'],'prod')
        self.assertEqual(extract('preprod')['environment']['value'],'preprod')


class SummaryTests(unittest.TestCase):
    def test_offsets_order_and_budget(self):
        for row in read_data('examples.json'):
            result=summarize(row['text'],max_sentences=2,word_budget=25)
            self.assertLessEqual(result['word_count'],25);self.assertLessEqual(len(result['sentences']),2)
            self.assertEqual([s['start'] for s in result['sentences']],sorted(s['start'] for s in result['sentences']))
            for span in result['sentences']:self.assertEqual(row['text'][span['start']:span['end']],span['text'])

    def test_decimals_and_email_not_split_internally(self):
        text='La durée est 1.5 s. Contact alice@example.invalid. Fin.'
        parts=sentence_spans(text)
        self.assertEqual(len(parts),3)
        self.assertIn('1.5',parts[0]['text']);self.assertIn('alice@example.invalid',parts[1]['text'])

    def test_budget_exhausted_is_explicit(self):
        result=summarize('Une phrase longue sans espace disponible.',word_budget=1)
        self.assertEqual(result['status'],'budget_exhausted');self.assertEqual(result['summary'],'')

    def test_summary_empty_vocabulary_and_invalid_limits(self):
        self.assertTrue(summarize('a !')['sentences'])
        for kwargs in ({'word_budget':0},{'max_sentences':True}):
            with self.assertRaises(ContractError):summarize('Phrase de test.',**kwargs)

    def test_overlap_is_defined_for_empty_prediction(self):
        self.assertEqual(summary_overlap('a b','a c')['f1'],.5)
        self.assertEqual(summary_overlap('','a c')['f1'],0)


class NERTests(unittest.TestCase):
    def test_exact_gold_spans(self):
        gold=read_data('examples.json');pred=[{'id':r['id'],'entities':entities(r['text'])} for r in gold]
        metrics=span_metrics(gold,pred)
        self.assertEqual(metrics['true_positive'],12);self.assertEqual(metrics['false_positive'],0)

    def test_boundary_label_and_document_mismatches(self):
        gold=[{'id':'x','entities':[{'start':0,'end':5,'label':'TECH'}]}]
        for document,span in [('x',{'start':0,'end':4,'label':'TECH'}),('x',{'start':0,'end':5,'label':'SERVICE'}),('y',{'start':0,'end':5,'label':'TECH'})]:
            report=span_metrics(gold,[{'id':document,'entities':[span]}])
            self.assertEqual(report['false_positive'],1);self.assertEqual(report['false_negative'],1)

    def test_longest_form_and_boundaries(self):
        spans=entities('production et Paiement API. Redislike est un autre nom.')
        self.assertEqual([(s['text'],s['label']) for s in spans],[('production','ENV'),('Paiement API','SERVICE')])

    def test_unknown_name_and_negated_mention(self):
        self.assertEqual(entities('Facturation Mobile'),[])
        self.assertEqual(entities('Ne pas utiliser Redis.')[0]['text'],'Redis')

    def test_mask_right_to_left_and_invalid_spans(self):
        text='Paiement API utilise Redis.'
        spans=entities(text)
        self.assertEqual(mask_entities(text,spans),'[SERVICE] utilise [TECH].')
        wrong=deepcopy(spans);wrong[0]['text']='Autre'
        with self.assertRaises(ContractError):mask_entities(text,wrong)
        with self.assertRaises(ContractError):mask_entities(text,spans+[spans[0]])


class EmbeddingTests(unittest.TestCase):
    def test_specialization_uses_train_and_finite_components(self):
        projection,info=specialized()
        self.assertEqual(projection.components_.shape[0],8)
        self.assertTrue(np.isfinite(projection.components_).all())
        self.assertEqual(info['train_hash'],digest(subset(read_data('tickets.json'),'train')))

    def test_retrieval_has_no_self_test_neighbor_and_correct_recall_denominator(self):
        report=embedding_report()
        self.assertEqual(report['queries'],12);self.assertEqual(report['index_documents'],36)
        for mode in report['modes'].values():
            for case in mode['cases']:
                self.assertTrue(all('-train-' in value for value in case['ranked_ids']))
                self.assertLessEqual(case['recall_at_3'],.25)
                self.assertAlmostEqual(case['recall_at_3'],case['precision_at_3']/4)


class IntegrationTests(unittest.TestCase):
    def test_ambiguous_ticket_requires_review(self):
        row=read_data('examples.json')[3];result=process(row['text'])
        self.assertTrue(result['requires_review'])
        self.assertEqual(result['fields']['http_status']['status'],'ambiguous')
        self.assertEqual(result['scope'],'analysis only, no action or external publication')

    def test_missing_ticket_identifier_requires_review(self):
        self.assertTrue(process('Le jeton est expiré et la connexion est refusée.')['requires_review'])

    def test_cli_success_review_and_invalid(self):
        for args,code in [(['--text','INC-204 retourne HTTP 401 car le jeton a expiré.'],0),
                          (['--text','quasar nébuleuse intergalactique'],1),(['--text',''],2)]:
            p=subprocess.run([sys.executable,'-m','examples.week10.demo',*args],capture_output=True,text=True)
            self.assertEqual(p.returncode,code,p.stderr)

if __name__=='__main__':unittest.main()
