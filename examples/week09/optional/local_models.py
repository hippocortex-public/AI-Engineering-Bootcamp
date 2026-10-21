"""Adaptateurs optionnels non exécutés dans la validation standard.
Requiert sentence-transformers et des modèles déjà présents sur disque.
"""
from pathlib import Path
import hashlib
import math
from ..knowledge import ContractError


def artifact_hash(directory):
    root=Path(directory).resolve()
    if not root.is_dir():raise ContractError('Répertoire de modèle local requis')
    digest=hashlib.sha256()
    for path in sorted(p for p in root.rglob('*') if p.is_file()):
        digest.update(path.relative_to(root).as_posix().encode())
        content=hashlib.sha256()
        with path.open('rb') as handle:
            for block in iter(lambda:handle.read(1024*1024),b''):content.update(block)
        digest.update(content.digest())
    return digest.hexdigest()


class LocalSentenceEmbedding:
    def __init__(self,directory):
        from sentence_transformers import SentenceTransformer
        self.model=SentenceTransformer(str(Path(directory).resolve()),local_files_only=True,trust_remote_code=False,device='cpu')
        self.dimension=self.model.get_sentence_embedding_dimension()
        self.fingerprint='sentence-transformers-local:'+artifact_hash(directory)

    def encode(self,text):return self.encode_document(text)
    def encode_document(self,text):return self.model.encode_document(text,normalize_embeddings=True).tolist()
    def encode_query(self,text):return self.model.encode_query(text,normalize_embeddings=True).tolist()


class LocalCrossEncoder:
    def __init__(self,directory):
        from sentence_transformers import CrossEncoder
        self.model=CrossEncoder(str(Path(directory).resolve()),local_files_only=True,trust_remote_code=False,device='cpu')
        self.fingerprint='cross-encoder-local:'+artifact_hash(directory)

    def rerank(self,query,candidates):
        if not candidates:return []
        scores=self.model.predict([(query,c['text']) for c in candidates])
        if len(scores)!=len(candidates):raise ContractError('Nombre de scores inattendu')
        result=[]
        for item,value in zip(candidates,scores):
            score=float(value)
            if not math.isfinite(score):raise ContractError('Score invalide')
            result.append({**item,'retrieval_score':item['score'],'score':score})
        return sorted(result,key=lambda c:(-c['score'],c['chunk_id']))
