# Lab — Monitoring d’une API IA

## Objectif

Construire une mini-API FastAPI instrumentée pour exposer :

- `/health`
- `/metrics`
- `/alerts`
- `/chat`

Le fournisseur LLM est simulé pour rendre le lab reproductible.

## Installation

Depuis ce dossier :

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Lancer les tests

```bash
python -m pytest -q
```

## Lancer l’API

```bash
python -m uvicorn monitoring_ai_service.app:app --reload
```

## Tester manuellement

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Explique le monitoring IA en trois phrases."}'
```
