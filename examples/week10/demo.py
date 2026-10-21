import argparse
import json
from pathlib import Path
from .nlp import (ContractError,artifact,classify,classification_metrics,digest,embedding_report,entities,
                  extract,process,read_data,specialized,span_metrics,subset,summarize,summary_overlap,trained)


def scenario(day):
    examples=read_data('examples.json')
    if day==1:
        bundle=trained();test=subset(read_data('tickets.json'),'test')
        return {'baseline':classification_metrics(bundle['vectorizer'],bundle['baseline'],test,bundle['baseline_threshold']),
                'ood':[{'id':row['id'],**classify(row['text'],bundle,'baseline')} for row in read_data('ood.json')],
                'provenance':bundle['provenance']}
    if day==2:
        rows=[{'id':r['id'],'fields':extract(r['text']),'expected':r['expected'],'expected_status':r['expected_status']} for r in examples]
        correct=sum(field['value']==r['expected'][key] for r in rows for key,field in r['fields'].items())
        return {'records':rows,'value_matches':correct,'status_matches':sum(field['status']==r['expected_status'][key] for r in rows for key,field in r['fields'].items()),'field_count':len(rows)*4,
                'note':'Exact values on fictional examples; inspect ambiguous/missing statuses separately'}
    if day==3:
        return {'records':[{'id':r['id'],**summarize(r['text']),'reference_overlap':summary_overlap(summarize(r['text'])['summary'],r['summary_reference'])} for r in examples],
                'note':'Extractive, no LLM generation; sentence selection is not a factuality evaluation'}
    if day==4:
        predictions=[{'id':r['id'],'entities':entities(r['text'])} for r in examples]
        return {'predictions':predictions,'metrics':span_metrics(examples,predictions),'method':'gazetteer + email regex, not learned NER'}
    if day==5:
        bundle=trained();test=subset(read_data('tickets.json'),'test')
        before=classification_metrics(bundle['vectorizer'],bundle['baseline'],test,bundle['baseline_threshold'])
        after=classification_metrics(bundle['vectorizer'],bundle['adapted'],test,bundle['adapted_threshold'])
        base=artifact(bundle,'baseline');adapted=artifact(bundle,'adapted')
        return {'selected_epochs':bundle['selected_epochs'],'selection':bundle['selection'],
                'baseline':before,'adapted':after,'vocabulary_unchanged':base['vocabulary']==adapted['vocabulary'],
                'head_weights_changed':base['coef']!=adapted['coef'],'method':'continued linear-head training, frozen TF-IDF; not LLM LoRA'}
    if day==6:
        _,details=specialized()
        return {'retrieval':embedding_report(),'training':details,'method':'supervised NCA on train TF-IDF; no pretrained neural model'}
    if day==7:
        return {'records':[{'id':r['id'],**process(r['text'])} for r in examples],
                'classifier_evaluation':scenario(5),'ner_evaluation':scenario(4)['metrics'],
                'embedding_evaluation':scenario(6),'dataset_hash':digest(read_data('tickets.json')),
                'scope':'fictional local corpus; trained algorithms, no production quality claim or external action'}
    raise ContractError('Jour attendu de 1 à 7')


def main():
    parser=argparse.ArgumentParser(description='NLP appliqué hors ligne sur tickets fictifs')
    parser.add_argument('--day',type=int,choices=range(1,8),default=7)
    parser.add_argument('--text')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    try:
        result=process(args.text) if args.text is not None else scenario(args.day)
        output=json.dumps(result,ensure_ascii=False,allow_nan=False,indent=2)+'\n'
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(output)
        print(output,end='')
        return 1 if args.text is not None and result['requires_review'] else 0
    except (ContractError,ValueError,OSError) as exc:
        print('Entrée invalide : '+str(exc),file=__import__('sys').stderr);return 2

if __name__=='__main__':raise SystemExit(main())
