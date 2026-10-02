# Rapport de validation — S5 J7 Déploiement

Date : 2 octobre 2026. Python 3.12.

## Exécuté dans l'environnement de génération

- 40 tests pytest réussis, aucun échec.
- Logique de quota Lua exécutée dans fakeredis avec support Lua.
- Concurrence et partage entre instances testés en mémoire.
- API, permissions, cache avec révocation et changements documentaires testés.
- Contrat de requête PostgreSQL tenant/paramètres vérifié avec des doubles de connexion.
- Décisions de promotion/rollback vérifiées avec callbacks simulés.
- Lecture YAML et contrôles statiques Compose/Dockerfile réalisés.
- Syntaxe Python et scripts shell de bootstrap vérifiés.
- Génération de secrets testée dans un répertoire temporaire : permissions Unix,
  refus d'écrasement et absence de valeurs dans stdout/stderr.
- Résolution pip de requirements.lock vérifiée sans installation de l'image.
- Schémas nbformat validés ; 4 cellules Python étudiant et 6 cellules enseignant
  exécutées séquentiellement avec assertions réussies.
- Génération des notebooks reproductible depuis le Markdown et corrections absentes
  du notebook étudiant, présentes avec notes de revue dans l'enseignant.
- Roadmap conservée à l'identique.

Un avertissement de dépréciation Starlette/AnyIO apparaît sans échec de test.

## Non exécuté : Docker absent

- `docker compose config` et validation par le moteur Compose.
- Build de l'image, montage réel des secrets et lancement des conteneurs.
- Bootstrap PostgreSQL et connexions réelles DB/Redis.
- Les neuf contrôles smoke_test.py contre la stack.
- Mise à jour et rollback réels d'image.
- Exécution du workflow GitHub Actions ou d'un scan Trivy.

Le parsing YAML n'est pas une validation complète de Compose. Les tests de connexion
simulés et fakeredis ne certifient pas le bootstrap ou la persistance réels.
Les cellules notebooks ont été exécutées dans Python, sans revendiquer une session
complète par le protocole Jupyter. Aucun vrai fournisseur LLM ou cloud n'est utilisé.

## Validation à effectuer sur votre machine

Depuis `book/week05/day07/labs/`, suivre README.md : tests Python, secrets,
`docker compose config -q`, build, `up --wait`, smoke_test.py, puis exercice de rollback.
Conserver les volumes et les secrets pendant ces vérifications.
