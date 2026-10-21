"""NLP appliqué : apprentissage réel et baselines explicites sur corpus fictif."""
from __future__ import annotations
from copy import deepcopy
from collections import Counter
from decimal import Decimal
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import re
import unicodedata
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score,confusion_matrix,f1_score
from sklearn.neighbors import NeighborhoodComponentsAnalysis
from sklearn.preprocessing import normalize
from threadpoolctl import threadpool_limits

DATA=Path(__file__).resolve().parent/'data'
LABELS=['acces','deploiement','performance']
SEED=17


class ContractError(ValueError):pass


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode()).hexdigest()


def text_required(text):
    if not isinstance(text,str) or not text.strip() or len(text)>20000:raise ContractError('Texte non vide limité à 20000 caractères requis')
    return text


def positive_int(value,name):
    if type(value) is not int or value<1:raise ContractError('Entier positif requis : '+name)
    return value


def read_data(name):return json.loads((DATA/name).read_text(encoding='utf-8'))


def validate_dataset(rows):
    if not isinstance(rows,list) or not rows:raise ContractError('Dataset vide')
    ids=set();group_split={};texts=set()
    for row in rows:
        if not isinstance(row,dict) or set(row)!={'id','group_id','split','label','text'}:raise ContractError('Contrat de ligne invalide')
        for key in ('id','group_id'):
            if not isinstance(row[key],str) or not row[key]:raise ContractError('Identifiant requis')
        if row['id'] in ids:raise ContractError('Identifiant dupliqué')
        ids.add(row['id'])
        if row['split'] not in ('train','adapt','validation','test') or row['label'] not in LABELS:raise ContractError('Split ou classe invalide')
        text_required(row['text'])
        normalized=' '.join(unicodedata.normalize('NFKC',row['text']).casefold().split())
        if normalized in texts:raise ContractError('Texte dupliqué entre observations')
        texts.add(normalized)
        group=row['group_id']
        if group in group_split and group_split[group]!=row['split']:raise ContractError('Groupe partagé entre splits')
        group_split[group]=row['split']
    for split in ('train','adapt','validation','test'):
        if {r['label'] for r in rows if r['split']==split}!=set(LABELS):raise ContractError('Classes manquantes dans '+split)
    return rows


def subset(rows,split):return [r for r in rows if r['split']==split]


def require_partition(rows,expected):
    if not rows or any(r['split']!=expected for r in rows):raise ContractError('Partition attendue : '+expected)
    return rows


def vectorizer():
    return TfidfVectorizer(lowercase=True,strip_accents='unicode',ngram_range=(1,2),sublinear_tf=True,norm='l2')


def fit_initial(train):
    require_partition(train,'train')
    if {r['label'] for r in train}!=set(LABELS):raise ContractError('Classes d’entraînement incomplètes')
    vec=vectorizer();matrix=vec.fit_transform([r['text'] for r in train])
    head=SGDClassifier(loss='log_loss',alpha=.001,max_iter=1500,tol=1e-5,random_state=SEED)
    head.fit(matrix,[r['label'] for r in train])
    return vec,head


def adapt_head(vec,base,adapt,epochs):
    require_partition(adapt,'adapt');positive_int(epochs,'epochs')
    model=deepcopy(base)
    matrix=vec.transform([r['text'] for r in adapt])
    labels=[r['label'] for r in adapt]
    for _ in range(epochs):model.partial_fit(matrix,labels)
    return model


def classification_metrics(vec,model,rows,threshold=.5):
    if not rows:raise ContractError('Évaluation sans observations')
    if type(threshold) not in (float,int) or not math.isfinite(threshold) or not 0<=threshold<=1:raise ContractError('Seuil invalide')
    matrix=vec.transform([text_required(r['text']) for r in rows])
    probabilities=model.predict_proba(matrix)
    best=probabilities.max(axis=1)
    predictions=model.classes_[probabilities.argmax(axis=1)]
    usable=np.asarray(matrix.getnnz(axis=1)>0)
    accepted=(best>=threshold)&usable
    gold=[r['label'] for r in rows]
    return {'count':len(rows),'labels':list(LABELS),'accuracy_argmax':float(accuracy_score(gold,predictions)),
            'macro_f1_argmax':float(f1_score(gold,predictions,labels=LABELS,average='macro',zero_division=0)),
            'confusion_matrix':confusion_matrix(gold,predictions,labels=LABELS).tolist(),
            'threshold':threshold,'coverage':float(accepted.mean()),
            'selective_accuracy':float(np.mean(np.asarray(gold)[accepted]==predictions[accepted])) if accepted.any() else None,
            'cases':[{'id':r['id'],'gold':r['label'],'predicted':str(p),'accepted':bool(a),'max_probability':float(c)}
                     for r,p,a,c in zip(rows,predictions,accepted,best)]}


def choose_threshold(vec,head,validation):
    require_partition(validation,'validation')
    candidates=[classification_metrics(vec,head,validation,t) for t in (.34,.5,.65,.8,.9)]
    valid=[r for r in candidates if r['selective_accuracy'] is not None and r['selective_accuracy']>=.9]
    if not valid:raise ContractError('Aucun seuil candidat ne satisfait la contrainte de validation')
    chosen=max(valid,key=lambda r:(r['coverage'],-r['threshold']))
    return chosen['threshold'],[{'threshold':r['threshold'],'coverage':r['coverage'],'selective_accuracy':r['selective_accuracy']} for r in candidates]


def train_bundle(rows):
    validate_dataset(rows)
    train=subset(rows,'train');adapt=subset(rows,'adapt');validation=subset(rows,'validation')
    vec,base=fit_initial(train)
    candidates=[]
    for epochs in (1,3,8):
        head=adapt_head(vec,base,adapt,epochs)
        metrics=classification_metrics(vec,head,validation,0)
        candidates.append((metrics['macro_f1_argmax'],epochs,head))
    _,epochs,adapted=max(candidates,key=lambda item:(item[0],-item[1]))
    baseline_threshold,baseline_trials=choose_threshold(vec,base,validation)
    adapted_threshold,adapted_trials=choose_threshold(vec,adapted,validation)
    return {'vectorizer':vec,'baseline':base,'adapted':adapted,'selected_epochs':epochs,
            'baseline_threshold':baseline_threshold,'adapted_threshold':adapted_threshold,
            'selection':[{'epochs':e,'validation_macro_f1':score} for score,e,_ in candidates],
            'threshold_trials':{'baseline':baseline_trials,'adapted':adapted_trials},
            'provenance':{'train_hash':digest(train),'adapt_hash':digest(adapt),'validation_hash':digest(validation),
                          'seed':SEED,'vectorizer_fit':'train only','head_selection':'validation only'}}


@lru_cache(maxsize=1)
def trained():
    return train_bundle(read_data('tickets.json'))


def classify(text,bundle=None,variant='adapted'):
    text_required(text);bundle=trained() if bundle is None else bundle
    if variant not in ('baseline','adapted'):raise ContractError('Version inconnue')
    matrix=bundle['vectorizer'].transform([text]);head=bundle[variant]
    probabilities=head.predict_proba(matrix)[0];best=int(np.argmax(probabilities))
    threshold=bundle[variant+'_threshold']
    accepted=matrix.nnz>0 and float(probabilities[best])>=threshold
    return {'label':str(head.classes_[best]) if accepted else None,'status':'classified' if accepted else 'review',
            'max_probability':float(probabilities[best]),'threshold':threshold,
            'note':'Probabilité du classifieur non calibrée; pas une garantie métier'}


def artifact(bundle,variant='adapted'):
    if variant not in ('baseline','adapted'):raise ContractError('Version inconnue')
    vec=bundle['vectorizer'];head=bundle[variant]
    body={'schema_version':1,'variant':variant,'vocabulary':{k:int(v) for k,v in vec.vocabulary_.items()},
          'idf':vec.idf_.tolist(),'classes':head.classes_.tolist(),'coef':head.coef_.tolist(),'intercept':head.intercept_.tolist(),
          'threshold':bundle[variant+'_threshold'],'provenance':bundle['provenance'],
          'representation':{'ngram_range':[1,2],'strip_accents':'unicode','sublinear_tf':True,'norm':'l2','lowercase':True}}
    return {**body,'content_hash':digest(body)}


def predict_artifact(saved,text):
    text_required(text)
    if not isinstance(saved,dict) or 'content_hash' not in saved:raise ContractError('Artefact invalide')
    body={k:v for k,v in saved.items() if k!='content_hash'}
    try:
        if saved['content_hash']!=digest(body) or saved['schema_version']!=1:raise ContractError('Intégrité de contenu invalide')
        if saved['classes']!=LABELS:raise ContractError('Ordre de classes incompatible')
        expected={'ngram_range':[1,2],'strip_accents':'unicode','sublinear_tf':True,'norm':'l2','lowercase':True}
        if saved['representation']!=expected:raise ContractError('Représentation incompatible')
        vocabulary=saved['vocabulary'];size=len(vocabulary)
        if not size or set(vocabulary.values())!=set(range(size)) or any(type(v) is not int for v in vocabulary.values()):
            raise ContractError('Vocabulaire invalide')
        idf=np.asarray(saved['idf'],dtype=float);weights=np.asarray(saved['coef'],dtype=float);bias=np.asarray(saved['intercept'],dtype=float)
        if idf.shape!=(size,) or weights.shape!=(3,size) or bias.shape!=(3,) or not all(np.isfinite(v).all() for v in (idf,weights,bias)):
            raise ContractError('Poids invalides')
        threshold=saved['threshold']
        if type(threshold) not in (int,float) or not math.isfinite(threshold) or not 0<=threshold<=1:raise ContractError('Seuil invalide')
        vec=vectorizer();vec.set_params(vocabulary=vocabulary);vec.idf_=idf
        matrix=vec.transform([text]);scores=np.asarray(matrix@weights.T).ravel()+bias
        # SGDClassifier log_loss multiclasses utilise un schéma one-vs-rest.
        scores=np.clip(scores,-700,700);probabilities=1/(1+np.exp(-scores));probabilities/=probabilities.sum()
        index=int(probabilities.argmax());accepted=matrix.nnz>0 and float(probabilities[index])>=threshold
        return {'label':LABELS[index] if accepted else None,'status':'classified' if accepted else 'review',
                'max_probability':float(probabilities[index]),'threshold':threshold}
    except (KeyError,TypeError,ValueError,OverflowError) as exc:
        raise ContractError(str(exc)) from exc


FIELD_PATTERNS={
 'ticket_id':re.compile(r'\bINC-\d{3,6}\b'),
 'environment':re.compile(r'\b(?:production|preprod|recette|prod|test|dev)\b',re.I),
 'http_status':re.compile(r'\bHTTP\s+([1-5]\d{2})\b',re.I),
 'duration_ms':re.compile(r'\b(?:latence|durée)\s+(?:est\s+)?(?:de\s+)?(?P<number>\d+(?:[,.]\d+)?)\s*(?P<unit>ms|s)\b',re.I)}


def extract(text):
    text_required(text);result={}
    for field,pattern in FIELD_PATTERNS.items():
        evidence=[];values=[]
        for match in pattern.finditer(text):
            if field=='http_status':value=int(match.group(1))
            elif field=='environment':value='prod' if match.group().lower()=='production' else match.group().lower()
            elif field=='duration_ms':
                amount=Decimal(match.group('number').replace(',','.'))*(1000 if match.group('unit').lower()=='s' else 1)
                value=format(amount.normalize(),'f')
            else:value=match.group()
            values.append(value);evidence.append({'start':match.start(),'end':match.end(),'text':match.group(),'value':value})
        unique={json.dumps(v,sort_keys=True) for v in values}
        status='missing' if not unique else 'present' if len(unique)==1 else 'ambiguous'
        result[field]={'status':status,'value':values[0] if status=='present' else None,'evidence':evidence}
    return result


def sentence_spans(text):
    text_required(text)
    segments=[];start=0
    for match in re.finditer(r'(?<=[.!?])\s+|\n+',text):
        segments.append((start,match.start()));start=match.end()
    segments.append((start,len(text)))
    spans=[]
    for left,right in segments:
        while left<right and text[left].isspace():left+=1
        while right>left and text[right-1].isspace():right-=1
        if left<right:spans.append({'start':left,'end':right,'text':text[left:right]})
    return spans


def summarize(text,max_sentences=2,word_budget=45):
    positive_int(max_sentences,'max_sentences');positive_int(word_budget,'word_budget')
    spans=sentence_spans(text)
    try:
        matrix=vectorizer().fit_transform([s['text'] for s in spans])
        centroid=np.asarray(matrix.mean(axis=0)).ravel();norm=np.linalg.norm(centroid)
        scores=np.asarray(matrix@(centroid/norm)).ravel() if norm else np.zeros(len(spans))
    except ValueError:
        scores=np.zeros(len(spans))
    ranked=sorted(range(len(spans)),key=lambda i:(-float(scores[i]),spans[i]['start']))
    chosen=[];used=0
    for index in ranked:
        words=len(spans[index]['text'].split())
        if words+used<=word_budget:
            chosen.append({**spans[index],'score':float(scores[index])});used+=words
        if len(chosen)>=max_sentences:break
    chosen.sort(key=lambda s:s['start'])
    return {'summary':' '.join(s['text'] for s in chosen),'sentences':chosen,'word_count':used,
            'status':'extract' if chosen else 'budget_exhausted','method':'TF-IDF sentence/centroid, extractive'}


GAZETTEER={'SERVICE':['Paiement API','Catalogue API'],'TECH':['PostgreSQL','Kubernetes','Docker','Kafka','Redis'],
           'ENV':['production','preprod','recette','prod','test','dev']}


def entities(text):
    text_required(text);candidates=[]
    for label,terms in GAZETTEER.items():
        for term in terms:
            for match in re.finditer(r'(?<!\w)'+re.escape(term)+r'(?!\w)',text,re.I):
                candidates.append({'start':match.start(),'end':match.end(),'text':match.group(),'label':label})
    for match in re.finditer(r'(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}(?!\w)',text):
        candidates.append({'start':match.start(),'end':match.end(),'text':match.group(),'label':'EMAIL'})
    selected=[]
    for candidate in sorted(candidates,key=lambda c:(-(c['end']-c['start']),c['start'],c['label'])):
        if not any(candidate['start']<s['end'] and s['start']<candidate['end'] for s in selected):selected.append(candidate)
    return sorted(selected,key=lambda c:c['start'])


def span_metrics(gold,predicted):
    def keys(rows):return {(r['id'],s['start'],s['end'],s['label']) for r in rows for s in r['entities']}
    left=keys(gold);right=keys(predicted);tp=len(left&right)
    precision=tp/len(right) if right else 0.0;recall=tp/len(left) if left else 0.0
    return {'true_positive':tp,'false_positive':len(right-left),'false_negative':len(left-right),
            'precision':precision,'recall':recall,'f1':2*precision*recall/(precision+recall) if precision+recall else 0.0,
            'protocol':'exact document/start/end/label spans'}


def mask_entities(text,spans):
    text_required(text)
    ordered=sorted(spans,key=lambda s:s['start']);end=0
    for span in ordered:
        if type(span.get('start')) is not int or type(span.get('end')) is not int or not 0<=span['start']<span['end']<=len(text):raise ContractError('Span invalide')
        if span['start']<end or text[span['start']:span['end']]!=span['text']:raise ContractError('Spans incohérents')
        if not isinstance(span.get('label'),str) or not span['label']:raise ContractError('Label requis')
        end=span['end']
    result=text
    for span in reversed(ordered):result=result[:span['start']]+f'[{span["label"]}]'+result[span['end']:]
    return result


def specialize(bundle,train):
    require_partition(train,'train')
    matrix=bundle['vectorizer'].transform([r['text'] for r in train]).toarray()
    projection=NeighborhoodComponentsAnalysis(n_components=min(8,matrix.shape[0],matrix.shape[1]),init='pca',
                                              max_iter=40,tol=1e-5,random_state=SEED)
    with threadpool_limits(limits=1),warnings.catch_warnings(record=True) as caught:
        projection.fit(matrix,[r['label'] for r in train])
    return projection,{'iterations':int(projection.n_iter_),'warnings':[str(w.message) for w in caught],
                       'train_hash':digest(train),'feature_hash':digest({'vocabulary':bundle['vectorizer'].vocabulary_,'idf':bundle['vectorizer'].idf_.tolist()})}


@lru_cache(maxsize=1)
def specialized():
    bundle=trained();return specialize(bundle,subset(read_data('tickets.json'),'train'))


def embedding_report(bundle=None,projection=None):
    bundle=trained() if bundle is None else bundle
    if projection is None:projection,_=specialized()
    rows=read_data('tickets.json');index=subset(rows,'train');queries=subset(rows,'test')
    vec=bundle['vectorizer'];left=vec.transform([r['text'] for r in index]).toarray();right=vec.transform([r['text'] for r in queries]).toarray()
    result={}
    for mode,a,b in [('tfidf',left,right),('supervised_nca',projection.transform(left),projection.transform(right))]:
        similarities=normalize(b)@normalize(a).T
        cases=[]
        for row,scores in zip(queries,similarities):
            ranked=sorted(range(len(index)),key=lambda i:(-float(scores[i]),index[i]['id']))[:3]
            relevant=sum(r['label']==row['label'] for r in index)
            hits=[index[i]['label']==row['label'] for i in ranked]
            cases.append({'id':row['id'],'gold_topic':row['label'],'ranked_ids':[index[i]['id'] for i in ranked],
                          'precision_at_3':sum(hits)/3,'recall_at_3':sum(hits)/relevant,
                          'mrr_at_3':next((1/r for r,hit in enumerate(hits,1) if hit),0.0)})
        result[mode]={'dimension':a.shape[1],'cases':cases,**{k:float(np.mean([c[k] for c in cases])) for k in ('precision_at_3','recall_at_3','mrr_at_3')}}
    return {'queries':len(queries),'index_documents':len(index),'relevance':'same topic label proxy, not human semantic qrels','modes':result}


def process(text):
    classification=classify(text);fields=extract(text)
    review=classification['status']=='review' or fields['ticket_id']['status']!='present' or any(f['status']=='ambiguous' for f in fields.values())
    return {'classification':classification,'fields':fields,'summary':summarize(text),
            'entities':entities(text),'requires_review':review,'scope':'analysis only, no action or external publication'}


def summary_overlap(summary,reference):
    text_required(reference)
    if not isinstance(summary,str):raise ContractError('Résumé texte requis')
    left=Counter(re.findall(r'\w+',unicodedata.normalize('NFKC',summary).casefold()))
    right=Counter(re.findall(r'\w+',unicodedata.normalize('NFKC',reference).casefold()))
    common=sum((left&right).values())
    precision=common/sum(left.values()) if left else 0.0
    recall=common/sum(right.values()) if right else 0.0
    return {'precision':precision,'recall':recall,'f1':2*precision*recall/(precision+recall) if precision+recall else 0.0,
            'note':'token multiset overlap, not factuality or ROUGE'}
