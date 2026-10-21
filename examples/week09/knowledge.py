"""Recherche locale réelle sur corpus pédagogique; aucune API générative."""
from __future__ import annotations
from collections import Counter
import hashlib
import json
import math
import re
import sqlite3
import time
import unicodedata

STOP=set('a au aux avec ce ces cet cette comment dans de des du en et est faire il je la le les leur ma mes mon ne nos nous on ou par pas pour pourquoi que quel quelle quelles quels qui sa se ses son sur un une vos vous'.split())


class ContractError(ValueError):
    pass


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode()).hexdigest()


def tokens(text):
    if not isinstance(text,str):raise ContractError('Texte requis')
    normalized=''.join(c for c in unicodedata.normalize('NFKD',text.lower()) if not unicodedata.combining(c))
    return [t for t in re.findall(r'[a-z0-9_]+',normalized) if t not in STOP]


def positive_int(value,name):
    if type(value) is not int or value<1:raise ContractError('Entier positif requis : '+name)
    return value


def finite(value,name):
    if type(value) not in (int,float) or not math.isfinite(value):raise ContractError('Nombre fini requis : '+name)
    return value


def validate_doc(doc):
    expected={'doc_id','tenant','version','title','source','text'}
    if not isinstance(doc,dict) or set(doc)!=expected:raise ContractError('Contrat documentaire invalide')
    for name in ('doc_id','tenant','title','source','text'):
        if not isinstance(doc[name],str) or not doc[name].strip():raise ContractError('Champ vide : '+name)
    for name in ('doc_id','tenant'):
        if not re.fullmatch(r'[a-zA-Z0-9_-]{1,100}',doc[name]):raise ContractError('Identifiant invalide')
    positive_int(doc['version'],'version')
    return doc


def chunk_document(doc,max_words=48,overlap=8):
    validate_doc(doc);positive_int(max_words,'max_words')
    if type(overlap) is not int or not 0<=overlap<max_words:raise ContractError('Overlap invalide')
    chunks=[]
    # Les séparations de paragraphes sont conservées dans les offsets originaux.
    for paragraph in re.finditer(r'\S(?:[^\n]|\n(?!\s*\n))*',doc['text']):
        words=list(re.finditer(r'\S+',paragraph.group()))
        offset=0
        while offset<len(words):
            end=min(offset+max_words,len(words))
            start_char=paragraph.start()+words[offset].start()
            end_char=paragraph.start()+words[end-1].end()
            identity={'tenant':doc['tenant'],'doc_id':doc['doc_id'],'version':doc['version'],
                      'start':start_char,'end':end_char,'text':doc['text'][start_char:end_char]}
            chunks.append({'chunk_id':digest(identity)[:24],**identity,'title':doc['title'],'source':doc['source']})
            if end==len(words):break
            offset=end-overlap
    return chunks


class HashEmbedding:
    """Projection signée de comptes de mots : baseline lexicale, non sémantique."""
    def __init__(self,dimension=128):
        self.dimension=positive_int(dimension,'dimension')
        self.fingerprint=f'hashbow-sha256-v1:dim={dimension}:tokens=nfkd-stop-v1'

    def encode(self,text):
        result=[0.0]*self.dimension
        for term,count in Counter(tokens(text)).items():
            h=hashlib.sha256(term.encode()).digest()
            bucket=int.from_bytes(h[:8],'big')%self.dimension
            sign=1 if h[8]%2 else -1
            result[bucket]+=sign*count
        norm=math.sqrt(sum(v*v for v in result))
        return [v/norm for v in result] if norm else result


def validate_vector(vector,dimension):
    if not isinstance(vector,list) or len(vector)!=dimension:raise ContractError('Dimension incompatible')
    for value in vector:finite(value,'vector')
    return vector


def cosine(left,right):
    if not left or len(left)!=len(right):raise ContractError('Vecteurs incompatibles')
    validate_vector(left,len(left));validate_vector(right,len(right))
    a=math.sqrt(sum(x*x for x in left));b=math.sqrt(sum(x*x for x in right))
    return sum(x*y for x,y in zip(left,right))/(a*b) if a and b else 0.0


def rank_bm25(query,chunks,k1=1.2,b=.75):
    finite(k1,'k1');finite(b,'b')
    if k1<=0 or not 0<=b<=1:raise ContractError('Paramètres BM25 invalides')
    terms=set(tokens(query))
    if not chunks or not terms:return []
    bags=[Counter(tokens(c['text'])) for c in chunks]
    lengths=[sum(bag.values()) for bag in bags]
    avg=sum(lengths)/len(lengths)
    if not avg:return []
    scored=[]
    for chunk,bag,length in zip(chunks,bags,lengths):
        score=0.0
        for term in terms:
            df=sum(term in candidate for candidate in bags)
            idf=math.log(1+(len(chunks)-df+.5)/(df+.5))
            tf=bag[term]
            score+=idf*tf*(k1+1)/(tf+k1*(1-b+b*length/avg)) if tf else 0
        if score>0:scored.append({**chunk,'score':score})
    return sorted(scored,key=lambda c:(-c['score'],c['chunk_id']))


def rrf(rankings,constant=60):
    positive_int(constant,'rrf constant')
    scores={};items={}
    for ranking in rankings:
        seen=set()
        for rank,item in enumerate(ranking,1):
            key=item['chunk_id']
            if key in seen:raise ContractError('Candidat dupliqué dans une liste')
            seen.add(key);items[key]=item
            scores[key]=scores.get(key,0)+1/(constant+rank)
    return sorted(({**items[key],'score':score} for key,score in scores.items()),key=lambda c:(-c['score'],c['chunk_id']))


def rerank(query,candidates):
    """Heuristique query/document, pas un CrossEncoder appris."""
    terms=set(tokens(query))
    if not terms:return []
    result=[]
    for item in candidates:
        content=set(tokens(item['text']))
        coverage=len(terms&content)/len(terms)
        title_coverage=len(terms&set(tokens(item['title'])))/len(terms)
        result.append({**item,'retrieval_score':item['score'],'score':coverage+.1*title_coverage,'term_coverage':coverage})
    return sorted(result,key=lambda c:(-c['score'],-c['retrieval_score'],c['chunk_id']))


class Store:
    """SQLite persistant + calcul exact Python. Aucun index ANN."""
    def __init__(self,path=':memory:',embedding=None):
        self.embedding=embedding or HashEmbedding()
        self.db=sqlite3.connect(path);self.db.row_factory=sqlite3.Row
        self.db.executescript('''
        CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY,value TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS documents (
          tenant TEXT NOT NULL,doc_id TEXT NOT NULL,version INTEGER NOT NULL,body TEXT NOT NULL,
          PRIMARY KEY(tenant,doc_id));
        CREATE TABLE IF NOT EXISTS chunks (
          chunk_id TEXT PRIMARY KEY,tenant TEXT NOT NULL,doc_id TEXT NOT NULL,body TEXT NOT NULL,vector TEXT NOT NULL);
        CREATE INDEX IF NOT EXISTS chunks_tenant ON chunks(tenant);
        CREATE TABLE IF NOT EXISTS memory (
          tenant TEXT,user_id TEXT,session_id TEXT,note_id TEXT,content TEXT,expires_at REAL,
          doc_id TEXT,doc_version INTEGER,PRIMARY KEY(tenant,user_id,session_id,note_id));
        ''')
        expected=digest({'fingerprint':self.embedding.fingerprint,'dimension':self.embedding.dimension})
        row=self.db.execute("SELECT value FROM metadata WHERE key='embedding'").fetchone()
        if row and row['value']!=expected:
            self.db.close();raise ContractError('Modèle ou dimension incompatible : reconstruire un index distinct')
        with self.db:self.db.execute("INSERT OR IGNORE INTO metadata VALUES ('embedding',?)",(expected,))

    def close(self):self.db.close()

    def ingest(self,doc,max_words=48,overlap=8):
        validate_doc(doc)
        chunks=chunk_document(doc,max_words,overlap)
        encoder=getattr(self.embedding,'encode_document',self.embedding.encode)
        vectors=[validate_vector(encoder(c['text']),self.embedding.dimension) for c in chunks]
        serialized=json.dumps(doc,sort_keys=True,ensure_ascii=False)
        old=self.db.execute('SELECT version,body FROM documents WHERE tenant=? AND doc_id=?',(doc['tenant'],doc['doc_id'])).fetchone()
        if old and doc['version']<old['version']:raise ContractError('Retour à une version antérieure interdit')
        if old and doc['version']==old['version']:
            if serialized!=old['body']:raise ContractError('Même version pour un autre contenu')
            # Même version mais nouveau chunking : reconstruction atomique explicite.
        with self.db:
            self.db.execute('DELETE FROM chunks WHERE tenant=? AND doc_id=?',(doc['tenant'],doc['doc_id']))
            self.db.execute('INSERT OR REPLACE INTO documents VALUES (?,?,?,?)',(doc['tenant'],doc['doc_id'],doc['version'],serialized))
            for c,v in zip(chunks,vectors):
                self.db.execute('INSERT INTO chunks VALUES (?,?,?,?,?)',(c['chunk_id'],c['tenant'],c['doc_id'],json.dumps(c,ensure_ascii=False),json.dumps(v,allow_nan=False)))
        return len(chunks)

    def delete_document(self,tenant,doc_id):
        with self.db:
            self.db.execute('DELETE FROM chunks WHERE tenant=? AND doc_id=?',(tenant,doc_id))
            self.db.execute('DELETE FROM documents WHERE tenant=? AND doc_id=?',(tenant,doc_id))
            self.db.execute('DELETE FROM memory WHERE tenant=? AND doc_id=?',(tenant,doc_id))

    def scoped_rows(self,tenant):
        if not isinstance(tenant,str) or not tenant:raise ContractError('Périmètre documentaire requis')
        return self.db.execute('SELECT body,vector FROM chunks WHERE tenant=? ORDER BY chunk_id',(tenant,)).fetchall()

    def search(self,query,tenant,mode='hybrid',top_k=5,candidate_k=12):
        positive_int(top_k,'top_k');positive_int(candidate_k,'candidate_k')
        if candidate_k<top_k:raise ContractError('candidate_k doit couvrir top_k')
        if mode not in ('lexical','vector','hybrid'):raise ContractError('Mode inconnu')
        rows=self.scoped_rows(tenant)
        chunks=[json.loads(r['body']) for r in rows]
        if not tokens(query):return []
        lexical=rank_bm25(query,chunks)[:candidate_k]
        query_encoder=getattr(self.embedding,'encode_query',self.embedding.encode)
        query_vector=validate_vector(query_encoder(query),self.embedding.dimension)
        vector=[]
        for row,chunk in zip(rows,chunks):
            score=cosine(query_vector,json.loads(row['vector']))
            if score>0:vector.append({**chunk,'score':score})
        vector=sorted(vector,key=lambda c:(-c['score'],c['chunk_id']))[:candidate_k]
        ranked=lexical if mode=='lexical' else vector if mode=='vector' else rrf([lexical,vector])
        return ranked[:top_k]

    def citation_valid(self,citation,tenant):
        if not isinstance(citation,dict):return False
        if any(not isinstance(citation.get(key),str) for key in ('chunk_id','doc_id','text','source')):return False
        if any(type(citation.get(key)) is not int for key in ('version','start','end')):return False
        row=self.db.execute('SELECT body FROM chunks WHERE tenant=? AND chunk_id=?',(tenant,citation.get('chunk_id'))).fetchone()
        if not row:return False
        current=json.loads(row['body'])
        return all(citation.get(key)==current[key] for key in ('doc_id','version','start','end','text','source'))

    def remember(self,tenant,user_id,session_id,note_id,content,ttl,now=None,doc_id=None):
        now=time.time() if now is None else finite(now,'now')
        finite(ttl,'ttl')
        if ttl<=0:raise ContractError('TTL positif requis')
        if any(not isinstance(v,str) or not v.strip() for v in (tenant,user_id,session_id,note_id,content)):
            raise ContractError('Périmètre et contenu mémoire requis')
        version=None
        if doc_id is not None:
            doc=self.db.execute('SELECT version FROM documents WHERE tenant=? AND doc_id=?',(tenant,doc_id)).fetchone()
            if not doc:raise ContractError('Source mémoire inconnue')
            version=doc['version']
        with self.db:self.db.execute('INSERT OR REPLACE INTO memory VALUES (?,?,?,?,?,?,?,?)',
                                     (tenant,user_id,session_id,note_id,content,now+ttl,doc_id,version))

    def recall(self,tenant,user_id,session_id,now=None):
        now=time.time() if now is None else finite(now,'now')
        rows=self.db.execute('''SELECT m.* FROM memory m LEFT JOIN documents d
            ON m.tenant=d.tenant AND m.doc_id=d.doc_id
            WHERE m.tenant=? AND m.user_id=? AND m.session_id=? AND m.expires_at>?
            AND (m.doc_id IS NULL OR m.doc_version=d.version) ORDER BY m.note_id''',(tenant,user_id,session_id,now))
        return [dict(row) for row in rows]

    def forget(self,tenant,user_id,session_id,note_id):
        with self.db:self.db.execute('DELETE FROM memory WHERE tenant=? AND user_id=? AND session_id=? AND note_id=?',
                                     (tenant,user_id,session_id,note_id))


def context_pack(candidates,word_budget=100):
    positive_int(word_budget,'word_budget')
    result=[];used=0
    for c in candidates:
        count=len(c['text'].split())
        if used+count<=word_budget:
            result.append(c);used+=count
    return result


def answer(store,question,tenant,top_k=3,word_budget=100,min_coverage=.6):
    positive_int(top_k,'top_k')
    finite(min_coverage,'min_coverage')
    if not 0<min_coverage<=1:raise ContractError('Seuil de couverture invalide')
    candidates=store.search(question,tenant,top_k=12,candidate_k=12)
    ranked=rerank(question,candidates)
    supported=[c for c in ranked if c['term_coverage']>=min_coverage and not c['text'].lstrip().startswith('#')]
    packed=context_pack(supported[:top_k],word_budget)
    if not packed:
        return {'status':'abstain','answer':'Aucun passage suffisamment étayé dans le corpus autorisé.',
                'citations':[],'mode':'extractive; no LLM'}
    citations=[{key:c[key] for key in ('chunk_id','doc_id','version','start','end','text','source')} for c in packed]
    assert all(store.citation_valid(c,tenant) for c in citations)
    text='\n\n'.join(f'[{i}] {c["text"]}' for i,c in enumerate(citations,1))
    return {'status':'supported_extract','answer':text,'citations':citations,'mode':'extractive; no LLM',
            'note':'Passages reproduits, pas une synthèse générative ni une preuve de justesse du document'}


def retrieval_metrics(ranked_doc_ids,relevant,k=3):
    positive_int(k,'k')
    if not isinstance(relevant,set) or not relevant:raise ContractError('Qrels positifs requis')
    if len(ranked_doc_ids)!=len(set(ranked_doc_ids)):raise ContractError('Documents classés dupliqués')
    selected=ranked_doc_ids[:k]
    recall=len(set(selected)&relevant)/len(relevant)
    reciprocal=next((1/i for i,doc in enumerate(selected,1) if doc in relevant),0.0)
    dcg=sum(1/math.log2(i+1) for i,doc in enumerate(selected,1) if doc in relevant)
    ideal=sum(1/math.log2(i+1) for i in range(1,min(len(relevant),k)+1))
    return {'recall_at_k':recall,'mrr_at_k':reciprocal,'ndcg_at_k':dcg/ideal,'k':k}
