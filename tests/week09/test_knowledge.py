from copy import deepcopy
from pathlib import Path
import json
import math
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from examples.week09.knowledge import (ContractError, HashEmbedding, Store, answer, chunk_document,
    context_pack,cosine,rank_bm25,rerank,retrieval_metrics,rrf,tokens)
from examples.week09.demo import documents,populated,evaluate_retrieval


def doc(text='Kafka paiement',tenant='team-a',doc_id='doc-1',version=1):
    return {'doc_id':doc_id,'tenant':tenant,'version':version,'title':'Titre de test','source':'test.md','text':text}


class ChunkTests(unittest.TestCase):
    def test_windows_progress_without_final_duplicate(self):
        chunks=chunk_document(doc('zero un deux trois quatre cinq six sept huit neuf'),4,1)
        self.assertEqual([c['text'] for c in chunks],['zero un deux trois','trois quatre cinq six','six sept huit neuf'])

    def test_unicode_offsets_and_paragraphs(self):
        source=doc('Été à Paris.\n\nDeuxième paragraphe : Kafka et paiement.\n')
        chunks=chunk_document(source,4,1)
        self.assertTrue(chunks)
        for chunk in chunks:
            self.assertEqual(source['text'][chunk['start']:chunk['end']],chunk['text'])
            self.assertLessEqual(len(chunk['text'].split()),4)
        self.assertTrue(any('Été' in c['text'] for c in chunks))

    def test_stability_and_versioned_ids(self):
        left=chunk_document(doc());right=chunk_document(doc())
        self.assertEqual(left,right)
        self.assertNotEqual(left[0]['chunk_id'],chunk_document(doc(version=2))[0]['chunk_id'])

    def test_invalid_chunk_configuration(self):
        for maximum,overlap in [(0,0),(4,4),(4,-1),(True,0),(4,True)]:
            with self.subTest(maximum=maximum,overlap=overlap),self.assertRaises(ContractError):
                chunk_document(doc(),maximum,overlap)

    def test_invalid_document(self):
        for patch in [{'text':''},{'version':True},{'version':0},{'doc_id':'../bad'}]:
            with self.assertRaises(ContractError):chunk_document({**doc(),**patch})


class RankingTests(unittest.TestCase):
    def test_normalization_and_empty_terms(self):
        self.assertEqual(tokens('ÉVÉNEMENT événement'),['evenement','evenement'])
        self.assertEqual(tokens('le et une'),[])

    def test_embedding_is_deterministic_and_not_order_sensitive(self):
        model=HashEmbedding()
        a=model.encode('Kafka paiement');b=model.encode('paiement Kafka')
        self.assertEqual(a,b);self.assertAlmostEqual(sum(v*v for v in a),1)
        output=subprocess.check_output([sys.executable,'-c',"import json; from examples.week09.knowledge import HashEmbedding; print(json.dumps(HashEmbedding().encode('Kafka paiement')))"],text=True)
        self.assertEqual(json.loads(output),a)

    def test_cosine_and_zero(self):
        self.assertAlmostEqual(cosine([1,0],[1,1]),1/math.sqrt(2))
        self.assertEqual(cosine([0,0],[1,1]),0)

    def test_invalid_vectors(self):
        for left,right in [([1,0],[1]),([True],[1]),([float('nan')],[1]),([],[])]:
            with self.assertRaises(ContractError):cosine(left,right)

    def test_bm25_does_not_return_zero_match(self):
        chunks=[{'chunk_id':'a','text':'kafka paiement'},{'chunk_id':'b','text':'redis cache'}]
        self.assertEqual([c['chunk_id'] for c in rank_bm25('kafka',chunks)],['a'])
        self.assertEqual(rank_bm25('astronomie',chunks),[])

    def test_rrf_scores_and_duplicate_guard(self):
        a={'chunk_id':'A','score':100};b={'chunk_id':'B','score':.01};c={'chunk_id':'C','score':1}
        result=rrf([[a,b,c],[b,a]])
        values={item['chunk_id']:item['score'] for item in result}
        self.assertAlmostEqual(values['A'],1/61+1/62);self.assertEqual(values['A'],values['B'])
        self.assertAlmostEqual(values['C'],1/63)
        with self.assertRaises(ContractError):rrf([[a,a]])

    def test_reranker_cannot_create_absent_candidate(self):
        candidates=[{'chunk_id':'a','title':'','text':'Redis cache','score':.01}]
        self.assertEqual([c['chunk_id'] for c in rerank('Kafka paiement',candidates)],['a'])
        self.assertEqual(rerank('Kafka paiement',candidates)[0]['term_coverage'],0)

    def test_context_budget_keeps_whole_passages(self):
        candidates=[{'text':'a b c d e'},{'text':'a b c'},{'text':'d e'}]
        self.assertEqual(context_pack(candidates,4),[candidates[1]])
        self.assertEqual(context_pack(candidates,5),[candidates[0]])

    def test_retrieval_metrics_known_values(self):
        result=retrieval_metrics(['B','C','A'],{'A','C'},2)
        self.assertEqual(result['recall_at_k'],.5);self.assertEqual(result['mrr_at_k'],.5)
        self.assertAlmostEqual(result['ndcg_at_k'],(1/math.log2(3))/(1+1/math.log2(3)))
        self.assertEqual(retrieval_metrics(['Z'],{'A'},3)['mrr_at_k'],0)

    def test_metrics_require_nonempty_qrels_and_unique_docs(self):
        with self.assertRaises(ContractError):retrieval_metrics(['A'],set())
        with self.assertRaises(ContractError):retrieval_metrics(['A','A'],{'A'})


class StoreTests(unittest.TestCase):
    def setUp(self):self.store=populated()
    def tearDown(self):self.store.close()

    def test_tenant_filter_before_top_one(self):
        for mode in ('lexical','vector','hybrid'):
            hits=self.store.search('paiement Kafka','team-a',mode,top_k=1)
            self.assertTrue(hits);self.assertEqual(hits[0]['tenant'],'team-a')
            self.assertNotIn('MARQUEUR_PRIVE_FICTIF_B',hits[0]['text'])
        self.assertEqual(self.store.search('paiement Kafka',"team-a' OR 1=1--"),[])

    def test_persistence_across_reopen(self):
        with tempfile.TemporaryDirectory() as directory:
            path=str(Path(directory)/'index.sqlite')
            store=populated(path);before=store.search('cache Redis','team-a');store.close()
            store=Store(path)
            try:self.assertEqual(store.search('cache Redis','team-a'),before)
            finally:store.close()

    def test_dimension_and_model_fingerprint_rejected(self):
        class OtherModel(HashEmbedding):
            def __init__(self):super().__init__(128);self.fingerprint='other-model-same-dimension'
        with tempfile.TemporaryDirectory() as directory:
            path=str(Path(directory)/'index.sqlite');store=Store(path);store.ingest(doc());store.close()
            for encoder in [HashEmbedding(64),OtherModel()]:
                with self.assertRaises(ContractError):Store(path,embedding=encoder)

    def test_reingestion_has_no_duplicate_chunks(self):
        source=documents()[0]
        before=len(self.store.scoped_rows('team-a'));self.store.ingest(source)
        self.assertEqual(len(self.store.scoped_rows('team-a')),before)

    def test_same_version_changed_content_refused(self):
        source=documents()[0]
        with self.assertRaises(ContractError):self.store.ingest({**source,'text':'Contenu changé'})
        self.assertTrue(any('rejouer un paiement' in json.loads(r['body'])['text'] for r in self.store.scoped_rows('team-a')))

    def test_update_invalidates_old_citation_and_rejects_downgrade(self):
        source=documents()[0]
        hit=self.store.search('paiement Kafka','team-a',top_k=1)[0]
        self.store.ingest({**source,'version':2,'text':'Procédure Kafka paiement version récente.'})
        self.assertFalse(self.store.citation_valid(hit,'team-a'))
        with self.assertRaises(ContractError):self.store.ingest(source)
        current=[json.loads(r['body']) for r in self.store.scoped_rows('team-a') if json.loads(r['body'])['doc_id']==source['doc_id']]
        self.assertTrue(current);self.assertTrue(all(c['version']==2 for c in current))

    def test_encoding_failure_does_not_delete_existing_document(self):
        class Failing(HashEmbedding):
            failing=False
            def encode(self,text):
                if self.failing:raise ContractError('Simulation encodage en panne')
                return super().encode(text)
        encoder=Failing();store=Store(embedding=encoder)
        try:
            store.ingest(doc());old=store.search('paiement','team-a')
            encoder.failing=True
            with self.assertRaises(ContractError):store.ingest(doc('Nouveau paiement',version=2))
            encoder.failing=False
            self.assertEqual(store.search('paiement','team-a'),old)
        finally:store.close()

    def test_sql_transaction_rolls_back_document_and_chunks(self):
        source=documents()[0];old=self.store.search('paiement Kafka','team-a')
        self.store.db.execute("CREATE TRIGGER fail_insert BEFORE INSERT ON chunks BEGIN SELECT RAISE(ABORT, 'simulated'); END")
        with self.assertRaises(sqlite3.IntegrityError):self.store.ingest({**source,'version':2,'text':'Nouveau paiement Kafka'})
        self.assertEqual(self.store.search('paiement Kafka','team-a'),old)
        row=self.store.db.execute('SELECT version FROM documents WHERE tenant=? AND doc_id=?',('team-a',source['doc_id'])).fetchone()
        self.assertEqual(row['version'],1)

    def test_document_delete_does_not_touch_other_tenant(self):
        self.store.delete_document('team-a','kafka-replay')
        self.assertFalse(any(c['doc_id']=='kafka-replay' for c in self.store.search('paiement Kafka','team-a')))
        self.assertTrue(self.store.search('paiement Kafka','team-b'))

    def test_search_contracts_and_empty_query(self):
        self.assertEqual(self.store.search('le et une','team-a'),[])
        for kwargs in [{'top_k':0},{'top_k':5,'candidate_k':2},{'mode':'unknown'}]:
            with self.assertRaises(ContractError):self.store.search('Kafka','team-a',**kwargs)

    def test_forged_wrong_tenant_and_stale_citations(self):
        citation=self.store.search('paiement Kafka','team-a',top_k=1)[0]
        self.assertTrue(self.store.citation_valid(citation,'team-a'))
        self.assertFalse(self.store.citation_valid(citation,'team-b'))
        for patch in [{'text':'inventé'},{'version':99},{'version':True},{'start':999},{'source':'other.md'}]:
            self.assertFalse(self.store.citation_valid({**citation,**patch},'team-a'))

    def test_answer_is_exact_extract_and_abstains_when_needed(self):
        result=answer(self.store,'Comment rejouer un paiement avec Kafka ?','team-a')
        self.assertEqual(result['status'],'supported_extract')
        self.assertTrue(result['citations'])
        for index,c in enumerate(result['citations'],1):
            self.assertTrue(self.store.citation_valid(c,'team-a'))
            self.assertIn(f'[{index}] '+c['text'],result['answer'])
        self.assertNotIn('MARQUEUR_PRIVE_FICTIF_B',result['answer'])
        self.assertEqual(answer(self.store,'Quelle météo demain à Oslo ?','team-a')['status'],'abstain')
        self.assertEqual(answer(self.store,'Comment rejouer un paiement avec Kafka ?','team-a',word_budget=1)['status'],'abstain')

    def test_evaluation_retains_paraphrase_failure_and_negative_cases(self):
        report=evaluate_retrieval(self.store)
        self.assertEqual(report['queries'],8)
        q8=next(c for c in report['cases'] if c['query_id']=='q8' and c['mode']=='lexical')
        self.assertEqual(q8['recall_at_k'],0)
        self.assertEqual(answer(self.store,'Retenter un encaissement depuis le journal distribué','team-a')['status'],'abstain')
        self.assertTrue(all(c['status']=='abstain' for c in report['unanswerable']))


class MemoryTests(unittest.TestCase):
    def setUp(self):self.store=populated()
    def tearDown(self):self.store.close()
    def note(self,**kwargs):
        self.store.remember('team-a','alice','s1','n1','Texte mémoire',ttl=60,now=1000,**kwargs)

    def test_isolation_and_expiry_boundary(self):
        self.note()
        self.assertEqual(len(self.store.recall('team-a','alice','s1',now=1059.999)),1)
        for scope in [('team-b','alice','s1'),('team-a','bob','s1'),('team-a','alice','s2')]:
            self.assertEqual(self.store.recall(*scope,now=1001),[])
        self.assertEqual(self.store.recall('team-a','alice','s1',now=1060),[])
        self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM memory').fetchone()[0],1)

    def test_update_invalidates_derived_note(self):
        self.note(doc_id='kafka-replay')
        self.assertTrue(self.store.recall('team-a','alice','s1',now=1001))
        self.store.ingest({**documents()[0],'version':2,'text':'Politique actualisée'})
        self.assertEqual(self.store.recall('team-a','alice','s1',now=1001),[])

    def test_delete_and_reingest_does_not_resurrect_memory(self):
        self.note(doc_id='kafka-replay')
        self.store.delete_document('team-a','kafka-replay');self.store.ingest(documents()[0])
        self.assertEqual(self.store.recall('team-a','alice','s1',now=1001),[])

    def test_forget_uses_complete_scope(self):
        self.note();self.store.forget('team-a','bob','s1','n1')
        self.assertTrue(self.store.recall('team-a','alice','s1',now=1001))
        self.store.forget('team-a','alice','s1','n1')
        self.assertEqual(self.store.recall('team-a','alice','s1',now=1001),[])

    def test_invalid_ttl_and_unknown_source(self):
        for value in [0,-1,float('nan'),True]:
            with self.assertRaises(ContractError):self.store.remember('team-a','alice','s1','n','note',value,now=1000)
        with self.assertRaises(ContractError):self.note(doc_id='unknown')

    def test_memory_is_not_a_documentary_citation(self):
        self.store.remember('team-a','alice','s1','n','MARQUEUR_MEMOIRE_FICTIF paiement Kafka',60)
        result=answer(self.store,'paiement Kafka','team-a')
        self.assertNotIn('MARQUEUR_MEMOIRE_FICTIF',result['answer'])


class CLITests(unittest.TestCase):
    def test_cli_answer_abstention_and_bad_argument(self):
        for args,expected in [(['--question','paiement Kafka'],0),(['--question','météo Oslo'],1),(['--day','9'],2)]:
            process=subprocess.run([sys.executable,'-m','examples.week09.demo',*args],capture_output=True,text=True)
            self.assertEqual(process.returncode,expected,process.stderr)

if __name__=='__main__':unittest.main()
