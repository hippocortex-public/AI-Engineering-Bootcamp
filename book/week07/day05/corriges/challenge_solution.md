# Solution du challenge

Créer deux moteurs avec drafter injecté : {category:unsafe,draft:x}, puis {category:general,draft:x*2001}. Après ingest/process, vérifier dead_letter et COUNT(publications)=0. Le contrôle s’exerce après le générateur, avant tout stockage de proposition valide.
