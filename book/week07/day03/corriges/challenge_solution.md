# Solution du challenge

Le payload canonique contient ticket_id : modifier ce champ avec le même event_id entraîne Conflict. Avec event_id neuf, le job est accepté. Cette différence montre que déduplication technique et politique métier par ticket sont distinctes.
