# Limiter le débit du fournisseur

Le fournisseur fictif du lab accepte soixante appels par minute. Un limiteur de débit doit prendre en compte les appels initiaux et les reprises. Une file Kafka peut absorber une pointe sans augmenter le quota du fournisseur.

Après un refus temporaire du fournisseur, respecter le délai de reprise prévu par le contrat. Mesurer la longueur de la file et l’âge de l’événement le plus ancien avant d’ajouter des consommateurs.
