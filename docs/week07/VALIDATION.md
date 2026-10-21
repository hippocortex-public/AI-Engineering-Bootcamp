# Rapport de validation — Semaine 7

Date : 12 octobre 2026. Python utilisé : 3.12.14.

## Contrôles exécutés

| Contrôle | Résultat |
|---|---|
| Complétude des 7 journées selon standard v1.1 | Conforme |
| Notebooks élèves / enseignants | 7 + 7 |
| Régénération Markdown vers notebooks | Octets identiques |
| Cellules Python exécutées séquentiellement | 21 réussies |
| Liens relatifs des journées | Résolus |
| Tests métier et HTTP unittest | 15 réussis |
| Scénario HTTP contre le serveur en processus séparé | Réussi |
| Exports n8n : JSON, connexions, absence de credentials | 3 conformes statiquement |
| Labs spécifiques J1 à J7 | Exécutés, sorties attendues |

Les cellules ont été exécutées comme du Python dans un namespace neuf pour chaque notebook, avec les assertions actives. Aucun kernel Jupyter et aucune validation nbformat par bibliothèque dédiée n’ont été utilisés. Les notebooks suivent le format JSON nbformat 4.5.

Les tests couvrent réception répétée, collision, contrat invalide, absence de publication prématurée, approbation idempotente, refus, hash/identité, expiration, backoff borné, dead letter/replay, sortie générateur invalide, reprise après fermeture/réouverture, absence de régénération d’un brouillon en attente et rollback transactionnel d’une publication échouée. Les tests HTTP vérifient également les rôles et les codes de réponse.

## Vérifications locales restantes

Docker n’est pas disponible dans l’environnement de génération. L’image n8n n’a pas été démarrée, les exports n’ont pas été importés dans l’éditeur et le parcours n8n n’a pas été exécuté. Suivre QUICKSTART.md, configurer les credentials, activer les trois workflows puis lancer `python3 -m examples.week07.smoke_http --n8n` pour cette vérification.

## Limites du démonstrateur

Générateur à règles simulé, publication locale simulée, identité de relecture à token partagé, serveur séquentiel, stockage SQLite et absence d’outbox distribuée. Aucun résultat ne prouve les performances ou la sécurité d’un modèle réel. Les limites et extensions sont expliquées dans ARCHITECTURE.md.

## Commandes de reproduction

```bash
python3 scripts/validate_week07.py
python3 -m unittest discover -s tests/week07 -v
python3 -m examples.week07.demo 7
```
