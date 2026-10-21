# Lab J7 — Projet intégré et revue d’architecture

Depuis la racine du dépôt :

```bash
python3 book/week07/day07/labs/run.py
```

Résultat attendu : **published=1, rejected=1, expired=1, publication_count=1**.

Le script exécute le scénario du jour contre une base en mémoire et ferme la connexion. Il ne crée aucun message externe. Inspecter `examples/week07/demo.py` et la méthode correspondante dans `workflow.py` pour relier la sortie à la transition étudiée.

## Travail à réaliser

1. Exécuter le scénario et expliquer chaque champ retourné.
2. Réaliser l’exercice 2 du jour avec une entrée différente.
3. Justifier l’absence de publication non autorisée.

Pour le parcours n8n, suivre [le guide d’installation](../../../../docs/week07/QUICKSTART.md). J1 configure la réception; J2 ajoute le scheduler; J3 teste les doublons; J4 observe les reprises et erreurs; J5 étudie le port de génération; J6 importe le workflow de décision; J7 exécute la checklist d’intégration.

Le scénario J4 utilise une horloge virtuelle. Les tests de reprise sont rapides et n’attendent pas réellement les délais. Le projet HTTP utilise une base fichier pour démontrer la persistance après redémarrage.
