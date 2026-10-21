# Validation — Semaine 10

Date : 20 octobre 2026. Python exécuté : 3.12.14.

| Contrôle | Résultat |
|---|---|
| Journées conformes au standard v1.1 | 7 complètes |
| Notebooks élève / enseignant | 7 + 7 |
| Cellules Python exécutées | 21 réussies |
| Régénération Markdown vers notebooks | Octets identiques |
| Tests unittest | 35 réussis |
| Labs | 7 exécutés |
| Liens relatifs des journées | Résolus |
| Rapports et artefacts de référence | 11 générés |
| Aller-retour des classifieurs JSON | Équivalence d’inférence vérifiée |
| Script LoRA optionnel | Syntaxe compilée, non exécuté |

## Environnement

NumPy 2.3.5, SciPy 1.17.0, scikit-learn 1.8.0, joblib 1.5.3 et threadpoolctl 3.6.0. Les dépendances S10 sont épinglées dans examples/week10/requirements.txt; elles n’écrasent aucun fichier de dépendances partagé du dépôt.

Les entraînements de tête et de projection ont été exécutés sur CPU, sans poids préentraînés ni API externe. Les données sont fictives; aucun incident ou email personnel réel n’a été utilisé.

## Méthode

scripts/validate_week10.py vérifie la structure et les liens, régénère les notebooks et compare leurs octets, exécute les cellules séquentiellement dans un namespace neuf par notebook, compile les modules puis lance les sept scénarios et la suite unittest. Le JSON nbformat 4.5 est vérifié par le script; aucun kernel Jupyter ni validation par la bibliothèque nbformat n’a été utilisé. Les diagrammes Mermaid n’ont pas été rendus graphiquement dans cet environnement.

## Tests significatifs

Séparation des groupes et doublons, partition obligatoire avant fit, mot du test absent du vocabulaire et des poids, adaptation sans mutation de baseline, seuils invalides ou aucun seuil admissible, métriques avec zéro accepté, rechargement JSON et refus d’artefacts incohérents, unités et preuves d’extraction, conflits de champs, résumé sous budget et phrases exactes, frontières de NER, masquage cohérent, index train distinct du test et règles de revue/CLI.

## Résultats et portée

Baseline et tête adaptée ont le même macro-F1 sur les douze tickets test, même si les poids changent. La NCA réduit la représentation à huit dimensions et améliore le voisinage par thème dans cette expérience. Le rappel utilise douze documents pertinents par catégorie; son plafond à k=3 est 0,25.

Les quatre textes annotés suffisent pour démontrer seize champs et douze spans connus, pas la robustesse linguistique générale. La NER est à règles; le résumé est extractif avec un proxy de recouvrement lexical. Aucune mesure de factualité générative, anonymisation exhaustive ou fiabilité hors distribution n’est annoncée.

PyTorch, Transformers, PEFT et le modèle BERT ne sont pas installés dans cette validation. Le script LoRA exige un environnement et des artefacts locaux verrouillés; aucun score LoRA ni résultat GPU n’est fourni. Aucun service n’a été déployé et aucun effet métier externe n’est exécuté.

## Reproduire

```bash
python scripts/validate_week10.py
python scripts/make_week10_reports.py
```
