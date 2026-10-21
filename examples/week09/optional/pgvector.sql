-- Extension PostgreSQL optionnelle; non exécutée dans la validation de ce paquet.
-- Le schéma utilise la dimension 128 de HashEmbedding pour la démonstration.
-- Pour un modèle neuronal, créer un index distinct avec sa dimension et son fingerprint.
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE IF NOT EXISTS s9_chunks (
    tenant text NOT NULL,
    chunk_id text NOT NULL,
    doc_id text NOT NULL,
    version integer NOT NULL CHECK (version > 0),
    model_fingerprint text NOT NULL,
    content text NOT NULL,
    embedding vector(128) NOT NULL,
    PRIMARY KEY (tenant, chunk_id)
);
CREATE INDEX IF NOT EXISTS s9_chunks_tenant ON s9_chunks (tenant);
-- Requête paramétrée, pas de concaténation de tenant ou de vecteur :
-- SELECT chunk_id, content, 1 - (embedding <=> %(query_vector)s::vector) AS score
-- FROM s9_chunks
-- WHERE tenant = %(tenant)s AND model_fingerprint = %(model)s
-- ORDER BY embedding <=> %(query_vector)s::vector LIMIT %(top_k)s;
-- Commencer sans index ANN pour établir une baseline exacte.
-- Étudier séparément :
-- CREATE INDEX s9_chunks_hnsw ON s9_chunks USING hnsw (embedding vector_cosine_ops);
-- Les filtres avec ANN demandent des mesures de rappel et éventuellement des scans itératifs.
-- Un WHERE tenant n'est pas une authentification : ajouter des droits et une RLS adaptée au service.
