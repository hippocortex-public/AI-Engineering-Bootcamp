# Expiration du cache Redis

Dans le lab, le cache Redis des livres expire après six cents secondes. Définir un TTL évite de conserver indéfiniment une valeur périmée. Invalider le cache après une modification du livre lorsque le besoin métier exige une lecture fraîche.

Une expiration de cache n’est pas une suppression de la donnée métier dans PostgreSQL. La politique de conservation de la base et celle du cache doivent être distinctes.
