# Challenge — Construire une mémoire d’agent gouvernée

## Contexte

Tu construis un assistant IA pour une équipe support B2B.

L’assistant doit aider les utilisateurs à créer des tickets et à obtenir des réponses personnalisées.

Il doit se souvenir de certaines préférences utilisateur, mais ne doit jamais stocker de secrets ou d’informations temporaires inutiles.

## Objectif

Étendre le lab `memory_agent.py` pour ajouter une couche de gouvernance mémoire.

## Fonctionnalités attendues

### 1. Politique de mémoire

Créer une classe ou une fonction `MemoryPolicy`.

Elle doit décider si une information extraite peut être stockée.

La décision doit contenir :

```json
{
  "allowed": true,
  "reason": "explicit_preference",
  "memory_type": "preference"
}
```

### 2. Catégories interdites

La politique doit refuser au minimum :

- mots de passe ;
- tokens d’API ;
- numéros de carte ;
- informations médicales temporaires ;
- émotions temporaires ;
- données de ticket qui appartiennent seulement au state courant.

### 3. Expiration

Ajouter un champ optionnel `expires_at` sur les faits mémorisés.

Les préférences stables peuvent ne pas expirer.

Les faits contextuels doivent expirer ou ne pas être stockés.

### 4. Journal d’audit

Ajouter un journal en mémoire indiquant :

- user_id ;
- texte source ;
- décision ;
- raison ;
- clé mémoire ;
- timestamp.

### 5. Tests

Ajouter au moins 5 tests :

1. une préférence explicite est stockée ;
2. un secret est refusé ;
3. une donnée de state n’est pas stockée en mémoire longue ;
4. l’audit contient la décision ;
5. `forget_user` supprime aussi l’audit utilisateur.

## Contraintes

- Pas d’appel réseau.
- Pas de dépendance externe.
- Code Python exécutable.
- Tests déterministes.
- Pas de modification de l’arborescence.

## Livrable attendu

Un fichier Python modifié et une suite de tests.

Le code doit rester compréhensible par un AI Backend Engineer junior.

## Critères d’évaluation

Le challenge est réussi si :

- la mémoire longue est sélective ;
- les données interdites sont refusées ;
- l’audit est exploitable ;
- les tests couvrent les cas sensibles ;
- l’oubli utilisateur est complet ;
- le design reste simple.
