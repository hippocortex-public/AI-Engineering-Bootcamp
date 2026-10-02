#!/bin/sh
set -eu
export BOOTCAMP_APP_PASSWORD="$(cat /run/secrets/db_app_password)"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<'SQL'
\getenv app_password BOOTCAMP_APP_PASSWORD
CREATE ROLE bootcamp_app LOGIN PASSWORD :'app_password';
REVOKE ALL ON SCHEMA public FROM PUBLIC;
CREATE TABLE schema_version (version integer NOT NULL);
INSERT INTO schema_version VALUES (1);
CREATE TABLE documents (
  tenant_id text NOT NULL,
  document_id text NOT NULL,
  content text NOT NULL,
  PRIMARY KEY (tenant_id, document_id)
);
INSERT INTO documents VALUES
('alpha', 'alpha-guide', 'Guide privé du tenant alpha.'),
('beta', 'beta-guide', 'Contenu privé du tenant beta.');
GRANT CONNECT ON DATABASE bootcamp TO bootcamp_app;
GRANT USAGE ON SCHEMA public TO bootcamp_app;
GRANT SELECT ON schema_version, documents TO bootcamp_app;
SQL
unset BOOTCAMP_APP_PASSWORD
