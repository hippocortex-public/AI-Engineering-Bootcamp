# Contributing

Ce projet est conçu comme un dépôt pédagogique professionnel.

## Conventions

- Les contenus pédagogiques vivent dans `book/`.
- Le code Python vit dans `mini_framework/` ou `ai_platform/`.
- Les notebooks sont générés à partir des sources Markdown.
- Les décisions d'architecture sont documentées dans `docs/decisions/`.

## Qualité

Avant chaque commit :

```bash
ruff check .
pytest
```
