# Review formateur

## Points à vérifier

- L'apprenant distingue trace, span, event et metric.
- Les spans ont des parents cohérents.
- Les erreurs d'outil ne sont pas masquées.
- La redaction est activée par défaut.
- Le rapport de santé est lisible.
- Le lab est exécuté jusqu'aux tests.

## Erreurs fréquentes

1. Tout mettre dans des logs plats.
2. Oublier les relations parent/enfant.
3. Stocker les données sensibles en clair.
4. Marquer toute la trace `failed` alors qu'un fallback sûr existe.
5. Confondre métrique et événement.
6. Instrumenter seulement le modèle et pas les outils.
7. Ne pas capturer les guardrails.

## Critères de réussite

L'apprenant doit pouvoir expliquer :

- comment reconstruire un run ;
- comment savoir quel outil a échoué ;
- comment masquer les données sensibles ;
- comment calculer la latence ;
- comment exporter les traces ;
- comment utiliser l'observabilité pour améliorer un agent.

## Extension proposée

Brancher l'export JSON du lab vers un collecteur OpenTelemetry pédagogique ou un tableau de bord local.
