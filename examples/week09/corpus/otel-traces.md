# Corrélation des traces et journaux

Pour corréler les traces et les journaux, conserver trace_id et span_id dans les événements de diagnostic. Propager un contexte entre services permet de relier les opérations du même parcours. Un identifiant créé indépendamment dans chaque service ne suffit pas.

Ne pas placer le texte complet des tickets ni les credentials dans les métriques. Utiliser des dimensions bornées pour les compteurs et maîtriser les droits de lecture des journaux.
