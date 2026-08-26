# Challenge — Registry de support client contrôlé

## Contexte

Tu construis un assistant support interne pour une entreprise SaaS. L’agent doit pouvoir rechercher des politiques, classifier une demande et créer un ticket si nécessaire.

## Objectif

Étendre le lab pour créer un registre d’outils de support client.

## Outils à implémenter

### `classify_issue`

Arguments :

- `message` : string obligatoire.

Sortie attendue :

```json
{
  "category": "billing|technical|security|other",
  "confidence": 0.0
}
```

### `search_policy`

Réutilise ou adapte l’outil existant.

### `create_ticket`

Arguments :

- `title` : string obligatoire ;
- `category` : string obligatoire, enum `billing`, `technical`, `security`, `other` ;
- `priority` : string optionnel, enum `low`, `medium`, `high`.

Contraintes :

- outil sensible ;
- scope requis : `ticket:write` ;
- approbation humaine obligatoire.

## Critères d’acceptation

- le manifest n’expose pas les handlers Python ;
- `create_ticket` est masqué par défaut ;
- un appel sans scope est bloqué ;
- un appel sans approbation est bloqué ;
- un appel avec scope et approbation réussit ;
- les arguments invalides retournent un statut `failed` ;
- chaque appel produit une trace lisible.

## Variante avancée

Ajoute une méthode `list_tools_for_agent(agent_role)` qui filtre les outils selon le rôle :

- `support_reader` : lecture seulement ;
- `support_operator` : lecture + création de ticket avec approbation ;
- `admin` : tous les outils.
