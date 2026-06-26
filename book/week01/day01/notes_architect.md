# Notes d'architecte — Day 1

## Décision

Ne pas utiliser automatiquement un LLM pour tous les problèmes.

## Raisonnement

Un LLM est puissant mais coûteux, probabiliste et parfois difficile à contrôler.

Pour une FAQ stable avec peu de questions, une solution à règles ou un moteur de recherche classique peut être plus robuste.

## Critères de décision

| Critère | Règles | LLM |
|---|---|---|
| Coût | Faible | Variable |
| Latence | Très faible | Plus élevée |
| Maintenance | Bonne si petit domaine | Bonne si domaine large |
| Risque d'erreur | Faible si couvert | Hallucinations possibles |
| Flexibilité | Faible | Élevée |
