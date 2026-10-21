# Démarrage — Semaine 9

Python 3.11 ou plus récent. Depuis la racine du dépôt décompressé ou après intégration. Aucune dépendance pip pour le parcours obligatoire; aucun accès réseau ou clé LLM nécessaire.

## 1. Projet complet

```bash
python3 -m examples.week09.demo --day 7
python3 -m examples.week09.demo --question "Comment rejouer un paiement avec Kafka ?"
python3 -m examples.week09.demo --question "Quelle météo demain à Oslo ?"
```

La question du corpus retourne des extraits et citations, code 0. La question météo retourne abstain, code 1 : c’est une abstention attendue, pas une panne. Une entrée/option invalide retourne 2. Le CLI expose --tenant pour expérimenter les filtres, mais n’authentifie aucun utilisateur; ne pas l’exposer comme un service public.

Écrire une réponse dans un fichier :

```bash
python3 -m examples.week09.demo --question "Comment rejouer un paiement avec Kafka ?" --output /tmp/s9-answer.json
```

Les citations donnent le document, sa version, les offsets de caractères et le texte exact. Aucun message externe ni appel d’outil métier n’est envoyé.

## 2. Journées

```bash
python3 book/week09/day01/labs/run.py
python3 -m examples.week09.demo --day 2
python3 -m examples.week09.demo --day 3
python3 -m examples.week09.demo --day 4
python3 -m examples.week09.demo --day 5
python3 -m examples.week09.demo --day 6
```

Chaque journée possède son propre labs/run.py. Les scénarios utilisent des bases en mémoire ou des bases temporaires automatiquement fermées. Le scénario J3 vérifie une fermeture/réouverture d’un index fichier.

## 3. Conserver un index local

Pour construire un index fichier de travail, sans le remplacer si vous souhaitez conserver vos expériences :

```python
from examples.week09.demo import populated

store = populated('/tmp/s9-knowledge.sqlite')
try:
    hits = store.search('paiement Kafka', 'team-a', mode='hybrid', top_k=3)
    print([(c['doc_id'], c['version'], c['score']) for c in hits])
finally:
    store.close()
```

populated réingère la version distribuée du corpus. Après une mise à jour locale de source en version supérieure, cette réingestion refusera la version antérieure. Pour seulement rouvrir l’index sans réingérer, utiliser Store('/tmp/s9-knowledge.sqlite'). Pour changer de modèle, créer un autre fichier; ne pas mélanger les espaces.

## 4. Notebooks et tests

```bash
python3 scripts/generate_week09_notebooks.py
python3 scripts/validate_week09.py
python3 -m unittest discover -s tests/week09 -v
```

Ouvrir Jupyter depuis le dépôt ou un sous-dossier. Le notebook enseignant exécute le lab avant les cellules de correction. L’affichage Mermaid dépend du lecteur; les fichiers .mmd restent disponibles. Le générateur ne nécessite pas nbformat; il produit le JSON nbformat 4.5 depuis les Markdown.

## 5. Rapports

```bash
python3 scripts/make_week09_reports.py
```

Les rapports JSON et Markdown comparent lexical, vector, hybrid et reranked sur huit requêtes positives, ainsi que deux cas d’abstention. q8 est une paraphrase difficile à conserver dans l’analyse. Les qrels sont documentaires; les chunks d’une même source sont dédupliqués avant les métriques. Le score de ce minuscule corpus n’établit pas une qualité de production.

## 6. Extensions

Lire `examples/week09/optional/README.md` pour les modèles locaux et pgvector. Aucun modèle n’est téléchargé par les adaptateurs. La version de dépendance résolue, les artefacts des modèles et le serveur choisi doivent être verrouillés et testés pour cette expérience. La requête SQL est un exemple de référence, pas un adaptateur PostgreSQL déjà validé.
