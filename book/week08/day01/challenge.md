# Challenge : ajouter des seuils par catégorie

Implémenter `segment_gate(report, thresholds)` sans modifier la règle existante. Retourner un booléen. Exiger que la règle globale passe et que chaque catégorie demandée existe et atteigne son seuil. Rejeter une configuration vide, un seuil non numérique, un booléen, NaN ou un seuil hors de [0, 1].

Démontrer : baseline avec support à 0,6 acceptée ; baseline avec support à 0,8 refusée ; candidat toujours refusé malgré ses réponses corrigées ; catégorie absente refusée. Ajouter au moins trois assertions de configuration invalide.

Livrables : fonction, assertions, justification des seuils et limites du petit échantillon. Ne pas remplacer le jeu ni changer les attentes pour réussir le challenge.
