# S8 J2 — Benchmarks reproductibles et variabilité


## 1. Évaluer et mesurer ne répondent pas à la même question
Le jour 1 teste un contrat fonctionnel : une réponse, une structure ou une action respecte-t-elle l’attente ? Le benchmark ajoute le temps, la variabilité et les conditions d’exécution. Une version peut être correcte mais trop lente, ou plus rapide tout en violant un refus critique. Les deux familles de preuves doivent rester visibles.

Le fil rouge reprend les douze cas de J1. Chaque cas possède trois essais par version, soit trente-six observations. Les durées et tokens sont fabriqués pour le cours; aucun fournisseur n’a été mesuré. Les répétitions exercent l’agrégateur. Elles ne constituent pas des observations indépendantes de qualité : la sortie de J1 est réutilisée pour les trois essais d’un même cas.

## 2. Fixer le protocole avant les résultats
Décrire le corpus, les identifiants, le nombre de répétitions, la concurrence, le matériel, les paramètres et la politique de cache. Le fichier workload.json conserve une grille de cas et trois répétitions. Son empreinte relie les deux versions au même protocole. Les configurations de modèle diffèrent volontairement; leur empreinte doit être tracée sans interdire la comparaison de versions.

Le code refuse une observation manquante, une paire case_id/repeat dupliquée ou un mélange de configurations dans un même lot. En test réel, consigner les erreurs plutôt que supprimer les requêtes échouées. Un timeout fait partie du comportement du système et du coût de l’utilisateur. Écarter toutes les erreurs réduit artificiellement la latence observée.

## 3. Choisir un quantile et le documenter
Le lab utilise nearest-rank : trier N valeurs et prendre celle de rang plafond(p × N), avec des rangs démarrant à 1. Pour trente-six essais, le p95 est la trente-cinquième valeur. Le maximum reste nécessaire : le candidat possède un timeout à 2200 ms alors que son p95 est de 461 ms. Le p95 ne signifie donc pas « aucune requête au-delà de cette durée ».

La baseline a un p95 de 601 ms. Comparer les mêmes cas donne ici un gain de 140 ms pour le candidat. Ce résultat est une propriété des fixtures. On ne peut pas en déduire qu’un modèle commercial ou une architecture serait plus rapide. Sur de petits effectifs, un quantile évolue par sauts; augmenter le nombre de cas et de répétitions avant de tirer une conclusion générale.

## 4. Mesure séquentielle et charge concurrente
Le débit affiché divise le nombre d’essais par la somme de leurs durées synthétiques. C’est un débit de replay séquentiel, sans coût du client ni du réseau. Ce n’est pas la capacité maximale du serveur. Un test concurrent exige une mesure de temps murale, une politique d’arrivée, le nombre de requêtes en vol et des métriques de saturation.

Distinguer un modèle fermé, où un nombre fixe de clients attend la fin avant de recommencer, d’un modèle ouvert qui génère des arrivées selon un débit cible. Un client saturé peut ne plus produire les arrivées prévues. Un résultat sans explication de la charge ne permet pas d’évaluer ce biais. Le lab ne fournit pas de générateur de charge concurrente.

## 5. Comparaison et décision
Afficher taux d’erreur, effectifs et maximum avec les quantiles. Pour la qualité, conserver une comparaison appariée sur les mêmes cas et inspecter les régressions. Pour des mesures réelles, répartir l’ordre des versions afin de limiter un effet d’échauffement ou de disponibilité du fournisseur. Conserver tous les essais; ne pas publier uniquement le meilleur.

Le candidat de ce cours est plus rapide et moins cher, mais demeure refusé à cause de c09. La règle critique de J1 ne disparaît pas dans une moyenne pondérée vitesse/qualité. Les seuils du projet sont pédagogiques, à justifier pour un besoin réel.

## À retenir
Un benchmark utile contient un protocole reproductible, des observations complètes et des limites. Un p95 faible ne compense pas un échec critique ni un maximum caché.
