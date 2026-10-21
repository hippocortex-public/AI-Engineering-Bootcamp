from pathlib import Path
import argparse
from copy import deepcopy
import json
import tempfile
from .knowledge import (Store,HashEmbedding,chunk_document,cosine,rerank,answer,
                         retrieval_metrics,digest,ContractError)
CORPUS=Path(__file__).resolve().parent/'corpus'


def documents():
    metadata=json.loads((CORPUS/'documents.json').read_text())
    return [{**doc,'text':(CORPUS/doc['source']).read_text()} for doc in metadata]


def populated(path=':memory:'):
    store=Store(path)
    try:
        for doc in documents():store.ingest(doc)
        return store
    except Exception:
        store.close();raise


def doc_ranking(chunks):
    return list(dict.fromkeys(c['doc_id'] for c in chunks))


def evaluate_retrieval(store,k=3):
    queries=json.loads((CORPUS/'queries.json').read_text())
    rows=[]
    for query in queries:
        for mode in ('lexical','vector','hybrid','reranked'):
            hits=store.search(query['question'],query['tenant'],mode='hybrid' if mode=='reranked' else mode,top_k=12)
            if mode=='reranked':hits=rerank(query['question'],hits)
            ranked=doc_ranking(hits)
            rows.append({'query_id':query['id'],'mode':mode,'ranked_docs':ranked[:k],
                         **retrieval_metrics(ranked,set(query['relevant']),k)})
    summaries={}
    for mode in ('lexical','vector','hybrid','reranked'):
        group=[r for r in rows if r['mode']==mode]
        summaries[mode]={metric:sum(r[metric] for r in group)/len(group) for metric in ('recall_at_k','mrr_at_k','ndcg_at_k')}
    unanswerable=json.loads((CORPUS/'unanswerable.json').read_text())
    refusals=[{'id':q['id'],'status':answer(store,q['question'],q['tenant'])['status']} for q in unanswerable]
    return {'queries':len(queries),'k':k,'summaries':summaries,'cases':rows,'unanswerable':refusals,
            'corpus_hash':digest(documents()),'qrels_hash':digest(queries),
            'embedding':store.embedding.fingerprint,
            'scope':'small fictional corpus; no claim of neural semantic quality or production reliability'}


def scenario(day):
    docs=documents()
    if day==1:
        chunks=chunk_document(docs[0],24,4)
        assert all(docs[0]['text'][c['start']:c['end']]==c['text'] for c in chunks)
        return {'chunks':len(chunks),'offsets_valid':True,'sample':chunks[0]}
    if day==2:
        model=HashEmbedding()
        a=model.encode('Kafka paiement');b=model.encode('paiement Kafka');c=model.encode('jardin tulipe')
        return {'fingerprint':model.fingerprint,'dimension':len(a),'same_bag_cosine':cosine(a,b),'different_terms_cosine':cosine(a,c)}
    if day==3:
        with tempfile.TemporaryDirectory() as tmp:
            path=str(Path(tmp)/'index.sqlite')
            store=populated(path)
            before=store.search('paiement Kafka','team-a',top_k=3)
            store.close()
            reopened=Store(path)
            try:
                after=reopened.search('paiement Kafka','team-a',top_k=3)
                assert [c['chunk_id'] for c in before]==[c['chunk_id'] for c in after]
                return {'persistent':True,'documents':doc_ranking(after),'cross_tenant':any(c['tenant']!='team-a' for c in after)}
            finally:reopened.close()
    store=populated()
    try:
        if day==4:
            query='Comment rejouer un paiement avec Kafka ?'
            return {mode:doc_ranking(store.search(query,'team-a',mode,top_k=5)) for mode in ('lexical','vector','hybrid')}
        if day==5:
            query='Quel TTL pour le cache Redis des livres ?'
            candidates=store.search(query,'team-a',top_k=12)
            return {'before':doc_ranking(candidates)[:3],'after':doc_ranking(rerank(query,candidates))[:3],
                    'note':'reclassement lexical heuristique, pas CrossEncoder'}
        if day==6:
            store.remember('team-a','alice','s1','style','Préférer une réponse courte',ttl=60,now=1000)
            visible=store.recall('team-a','alice','s1',now=1001)
            isolated=store.recall('team-a','bob','s1',now=1001)
            expired=store.recall('team-a','alice','s1',now=1060)
            return {'own_notes':len(visible),'other_user_notes':len(isolated),'at_expiry_notes':len(expired)}
        if day==7:
            question='Comment rejouer un paiement avec Kafka ?'
            response=answer(store,question,'team-a')
            return {'question':question,'response':response,'retrieval_evaluation':evaluate_retrieval(store)}
        raise ContractError('Jour attendu de 1 à 7')
    finally:store.close()


def main():
    parser=argparse.ArgumentParser(description='Recherche et réponses extractives sur corpus fictif')
    parser.add_argument('--day',type=int,choices=range(1,8),default=7)
    parser.add_argument('--question')
    parser.add_argument('--tenant',default='team-a')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    try:
        if args.question is not None:
            store=populated()
            try:result=answer(store,args.question,args.tenant)
            finally:store.close()
        else:result=scenario(args.day)
        output=json.dumps(result,ensure_ascii=False,allow_nan=False,indent=2)+'\n'
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(output)
        print(output,end='')
        return 1 if result.get('status')=='abstain' else 0
    except (ContractError,ValueError,OSError) as exc:
        print('Entrée invalide : '+str(exc),file=__import__('sys').stderr);return 2

if __name__=='__main__':raise SystemExit(main())
