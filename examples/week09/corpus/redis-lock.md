# Verrou Redis et propriétaire

Le verrou du lab possède un jeton aléatoire de propriétaire et une expiration. Libérer le verrou seulement si le jeton stocké correspond à celui de l’appelant. Une suppression aveugle peut libérer le verrou d’un autre processus.

Une expiration ne garantit pas que le premier travailleur a cessé ses effets. Pour protéger une ressource externe contre un travailleur retardataire, étudier un fencing token et une validation côté ressource.
