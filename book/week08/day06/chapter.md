# S8 J6 — Sécurité des agents et contrôles de permissions


## 1. Protéger la frontière d’action
Un système agentique reçoit des textes, documents ou résultats d’outils susceptibles de contenir des consignes hostiles. Un contenu peut demander de changer de tenant, divulguer des données ou publier sans autorisation. Cette instruction ne devient pas une permission parce qu’un modèle l’a reformulée.

Les références OWASP consultées distinguent notamment injection de prompt et excès d’autonomie. Le cours applique ces idées à une frontière précise : un contrôleur décide si une action proposée est autorisée, sans exécuter d’outil. Il ne prétend pas empêcher toutes les injections ni démontrer la résistance d’un modèle.

## 2. Trois objets de confiance différents
Le texte non fiable est une donnée métier. L’acteur vient, en architecture réelle, d’un mécanisme d’authentification serveur. Le grant vient d’un service de validation de confiance. Dans le lab, acteur et grant sont des fixtures explicitement injectées par le test. La fonction authorize n’est pas un endpoint public et n’authentifie pas ces objets.

Si un client pouvait envoyer librement role=reviewer et approved=true, le contrôle perdrait son sens. Pour un raccord HTTP réel, dériver le sujet et les rôles d’un contexte vérifié; stocker ou signer l’approbation côté service et vérifier sa portée, son expiration et son usage. Ces mécanismes ne sont pas implémentés dans ce lab.

## 3. Réduire l’espace des actions
Le contrôleur n’admet que read_ticket et publish_draft. Un outil execute_shell est refusé avant toute exécution. Les arguments possèdent exactement ticket_id et tenant; un champ url supplémentaire est rejeté. L’identifiant respecte T suivi d’un tiret et de trois chiffres.

La comparaison du tenant de l’acteur avec celui de la ressource refuse un passage inter-tenant. Cette règle suppose que le tenant de la ressource soit résolu côté serveur. Accepter une simple déclaration du client permettrait de contourner l’isolation. Une architecture réelle ajouterait un lookup autorisé et des contrôles d’accès au niveau du stockage.

## 4. Lier la validation à l’effet
La lecture est accordée aux rôles reader et reviewer. La publication demande le rôle reviewer et un grant approuvé dont action_hash correspond exactement au tenant, à l’outil et aux arguments. Modifier le ticket après validation invalide le grant. Le hash ne signe pas l’acteur et ne fournit pas de mécanisme anti-rejeu.

S7 traitait l’expiration et l’idempotence d’une décision de publication locale. Ce jour ne duplique pas son moteur : il teste une politique de permissions indépendante. Le projet final ne doit pas annoncer que cette politique seule gère une approbation durable ou un effet externe unique.

## 5. Cas positifs et négatifs
La suite contient deux opérations permises et six refus attendus : tenant voisin, outil inconnu, approbation absente, rôle insuffisant, action modifiée et argument supplémentaire. Les textes adversariaux sont présents dans les fixtures, mais le contrôleur ne les interprète pas. Modifier le texte ne change pas une permission.

Un système qui refuse tout réussirait les seuls tests négatifs. Les cas positifs vérifient que le comportement autorisé reste possible. Inversement, des cas nominaux ne prouvent pas la séparation des tenants. Conserver les deux populations et des raisons de décision explicites.

## 6. Limites et campagne réelle
Le résultat « huit cas passent » signifie que ce contrôleur traite les huit objets comme prévu. Aucun modèle n’a reçu les textes et aucun outil n’a été appelé. Une campagne réelle aurait besoin d’un environnement isolé, de comptes et ressources fictifs, d’un générateur de propositions du modèle et d’une vérification des effets observés.

Tester aussi les chemins indirects : documents récupérés, sortie d’outil et mémoire partagée. Empêcher une exécution dangereuse par contrôle applicatif reste utile même si le modèle propose cette exécution. Ne pas déduire d’un refus de l’API que le prompt a résisté à l’attaque; ce sont deux résultats différents.

## À retenir
L’identité, les droits et les approbations proviennent d’une frontière de confiance. Une proposition IA reste une donnée soumise à cette frontière.
