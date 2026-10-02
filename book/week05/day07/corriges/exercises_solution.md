# Corrigés des exercices

## 1. Santé et readiness

PostgreSQL peut accepter des connexions mais refuser le compte applicatif après une
rotation incomplète ; tester ce compte sans imprimer son secret. Le serveur peut
également fonctionner avec un schéma absent ou d'une version différente ; vérifier
le bootstrap ou la migration et la table de version.

Redis peut être indisponible alors que PostgreSQL fonctionne. Examiner son healthcheck
et sa configuration, sans exposer les mots de passe. La liveness doit constater le
processus, pour ne pas créer une boucle de redémarrage liée à une dépendance externe.

## 2. Mot de passe et bootstrap

Les scripts d'initialisation ne sont exécutés que sur un volume vide. Le rôle SQL
conserve donc l'ancien mot de passe, tandis que l'API lit le nouveau fichier. Modifier
le script n'applique pas non plus une évolution sur une base existante.

Planifier la rotation : mettre à jour le rôle via un accès privilégié protégé,
mettre à jour le secret distribué aux consommateurs, redémarrer/recharger ceux-ci,
puis vérifier une connexion et la readiness. Organiser le chevauchement si requis
pour éviter l'interruption. Le compte applicatif ne peut pas réaliser lui-même cette
administration. Pour le schéma, utiliser une migration versionnée ; conserver et
tester une sauvegarde. Ne pas supprimer des données pour contourner la procédure.

## 3. Rollback et schéma

Non : l'ancienne image dépend d'une colonne supprimée. Un rollback d'image seul
échoue ou réintroduit des erreurs. Corriger vers l'avant ou restaurer selon un plan
explicite avec conséquences sur les données.

Expand/contract : ajouter la nouvelle colonne de façon compatible ; permettre aux
deux versions de fonctionner ; migrer/backfiller ; déployer les lecteurs/écrivains
nouveaux ; vérifier qu'aucun ancien consommateur ne reste ; supprimer l'ancienne
colonne dans une release ultérieure. La phase destructive ferme la fenêtre de
rollback simple et doit être traitée comme telle.

## 4. Partage du quota

```python
import fakeredis
from deployment_ai_service.auth import Principal
from deployment_ai_service.storage import RedisBackend, RateLimited

client = fakeredis.FakeRedis(decode_responses=True)
alice = Principal("alice", "alpha", frozenset({"chat:write"}))
first, second = RedisBackend(client, limit=1), RedisBackend(client, limit=1)
first.consume(alice)
try:
    second.consume(alice)
except RateLimited:
    print("Quota partagé : deuxième appel refusé")
else:
    raise AssertionError("Quota contourné")
```

Deux clients Redis connectés à des serveurs distincts ne partageraient pas le même
état. Le test fakeredis exécute la logique Lua sans prouver la configuration réseau
et la persistance de Redis dans le conteneur.

## 5. Checklist de livraison

| Élément | Preuve |
|---|---|
| Image | Commit associé, digest/identifiant conservé, résultat du scan |
| Configuration | Valeurs non sensibles relues et chemins de secrets validés |
| Schéma | Version compatible lue avec le compte applicatif |
| Sauvegarde | Identifiant du backup et résultat du test de restauration |
| Readiness | 200 observé après remplacement et lors de la montée en charge |
| Métier | Smoke tests auth, document, cache et métriques réussis |
| Isolation | Même ressource beta refusée sous identité alpha |
| Exploitation | Erreurs, latence et logs surveillés sur une fenêtre définie |
| Rollback | Image précédente disponible, compatibilité et procédure de retour testées |

Un bon diagnostic exige des preuves complémentaires : une seule sonde ou un seul
smoke test ne couvre pas tous les comportements.
