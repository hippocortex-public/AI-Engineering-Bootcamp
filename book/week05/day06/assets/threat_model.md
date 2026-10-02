# Modèle de menace du lab

## Actifs et frontières

Actifs : documents des tenants, identités et clés, capacité d'invocation, disponibilité,
journaux d'audit. Frontières : client → API, principal → ressource, modèle → outil,
processus → configuration et collecte de logs.

| Menace | Contrôle livré | Vérification | Limite |
|---|---|---|---|
| Clé absente/forgée | Authentification explicite | Tests 401 | Pas d'IdP |
| Usurpation de tenant | Principal serveur + ACL | Tests des trois voies | Données en mémoire |
| Invocation dangereuse | Allowlist + scopes | Outils inconnus refusés | Aucun vrai agent |
| Arguments malveillants | Schéma strict | Champs supplémentaires refusés | Pas de parser de fichiers |
| Rafale authentifiée | Quota atomique local | Concurrence et 429 | Pas distribué |
| Fuite de secrets | Logs minimaux + erreurs génériques | Captures et marqueurs | Proxy/APM hors lab |
| Configuration ouverte | Démarrage refusé | Tests env invalide | Révocation au redémarrage |
| Injection indirecte | Données sans exécution ; accès contrôlés | Document d'attaque | Modèle simulé |

## Hypothèses explicites

Le serveur et la configuration d'identités sont de confiance. Un accès administrateur
au processus compromet ces hypothèses. Les scopes s'appliquent dans le tenant de
l'identité. Le lab ne fournit ni limitation anonyme réseau, ni restriction d'egress,
ni isolation système pour l'exécution de code, laquelle est absente.
