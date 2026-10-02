# Corrigé des questions d'entretien

1. La clé LLM authentifie le backend chez le fournisseur. Elle ne prouve pas qui
   utilise l'API et ne porte pas la politique de vos tenants.
2. À chaque accès à une ressource, avec une règle centralisée et un tenant issu de
   l'identité validée. Les chemins alternatifs et le cache doivent appliquer la
   même règle ; un filtrage de l'interface ou du prompt est insuffisant.
3. Non. Un prompt est une consigne au modèle, pas une frontière déterministe. Le
   backend doit contrôler données et capacités, même si le modèle suit l'injection.
4. Le modèle peut halluciner ou être manipulé. Le dispatcher vérifie l'autorité de
   l'appelant et les arguments avant chaque invocation effective.
5. Une clé globale ou trop large peut mélanger les tenants ou les ACL. Une réponse
   mise en cache peut survivre à une révocation. Partitionner et revalider.
6. Le quota compte des appels ; le budget borne une consommation variable. Borner
   contexte/sortie, réserver et rapprocher les consommations réelles.
7. Indexer le quota sur le tenant et le sujet, pas sur la clé. Une nouvelle clé du
   même principal partage le compteur existant.
8. Sujet, tenant, route normalisée, décision/statut, corrélation et horodatage dans
   une collecte protégée. Éviter clés, prompts et documents bruts ; limiter la
   conservation et la cardinalité des métriques.
9. Le décodage extrait des champs non authentifiés. Valider cryptographie et claims
   attendus, notamment émetteur, audience et expiration, avant de les utiliser.
10. Externaliser quotas, secrets et audit ; configurer TLS, proxy de confiance,
    limite de corps, limitation avant authentification et délais d'exécution.
    Vérifier l'isolation SQL/cache et la révocation. Tester le fournisseur réel.

## Mise en situation corrigée

Contenir le chemin de fuite : désactiver temporairement le cache ou la fonction de
contexte en cause selon le diagnostic, préserver l'audit et limiter l'exposition.
Vérifier le tenant établi et la version d'ACL à chaque étape, la clé de cache et les
requêtes SQL. Ne pas recopier le contenu divulgué dans un ticket ou les logs généraux.

Ajouter des tests alpha/beta par voie directe, RAG/chat, outil et cache hit ; vérifier
révocation et traitements asynchrones. La gestion d'incident et les communications
suivent ensuite le processus de l'organisation. Une réponse HTTP 200 et un bon
SLO de latence ne prouvent pas l'isolation des données.
