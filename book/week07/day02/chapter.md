# Semaine 7 — Jour 2 : Orchestration et état durable


## 1. Du graphe au protocole métier
Un graphe indique l’ordre des appels, mais ne suffit pas à définir le comportement après une panne. Le job est-il déjà enregistré ? Le brouillon a-t-il été validé ? La réponse a-t-elle été publiée ? Une machine à états rend ces questions explicites. Dans le fil rouge, `received` indique l’enregistrement, `awaiting_review` indique un brouillon disponible et `published` signifie une publication locale simulée.

Deux branches terminent le processus sans publication : `rejected` et `expired`. Les erreurs utilisent `retry` ou `dead_letter`. Chaque état a un sens observable. Une règle simple doit rester vraie : aucun contenu ne figure dans `publications` avant une approbation valable. Une réponse de modèle ne peut jamais se substituer à cette approbation.

## 2. Qui orchestre ?
n8n déclenche `POST /tick` périodiquement. Le backend recherche les jobs éligibles et applique une étape. Le moteur possède la machine à états et le stockage; n8n possède les déclencheurs et le transport. Cette répartition évite un couplage à l’identifiant d’exécution n8n. Une exécution du scheduler peut traiter plusieurs jobs et un job peut nécessiter plusieurs exécutions.

L’orchestration explicite fixe le parcours avant l’exécution. Un agent peut choisir un outil ou adapter un plan à un résultat intermédiaire. Les semaines précédentes ont traité la boucle agentique; cette semaine étudie la maîtrise du processus autour de cette boucle. Il n’est pas nécessaire de refaire un mini-framework : notre module isolé démontre les invariants d’intégration.

## 3. Modéliser les transitions
L’ingestion ne prépare pas le brouillon. `process` ne traite que `received` ou `retry` si la date de reprise est atteinte. Appeler `process` sur un job en attente de validation ne génère pas un nouveau texte. `decide` n’accepte qu’un état en attente, un hash de proposition courant et une décision reconnue. Les répétitions d’une décision déjà appliquée sont idempotentes si elles sont identiques.

Une transition terminale ne revient pas silencieusement en arrière. Le replay est explicite et limité aux dead letters. Si le contrat ou le brouillon change, il faut une nouvelle version du processus ou une nouvelle demande; une approbation ancienne ne doit pas autoriser un texte modifié.

## 4. Persister avant de répondre
La transaction d’ingestion écrit le job et son audit avant de renvoyer l’accusé de réception. Un redémarrage retrouve donc les jobs acceptés. La connexion SQLite utilise ici une exécution séquentielle; elle illustre la durabilité d’un processus unique. Elle ne constitue pas un worker distribué : plusieurs processus nécessiteraient claim atomique, lease, fencing et tests de concurrence.

La génération se déroule avant la transaction qui stocke son résultat. Si le processus s’arrête entre ces deux étapes, le générateur peut être rappelé. Pour une lecture ou un LLM sans effet métier, le principal risque est un coût supplémentaire. Pour un appel qui écrit dans un système tiers, cette fenêtre change le problème et exige une stratégie d’idempotence adaptée.

## 5. Observer l’état
GET /jobs/{event_id} retourne l’état métier et le brouillon courant. GET /metrics expose un petit comptage JSON; ce n’est pas un endpoint Prometheus. La table audit enregistre des actions sans recopier le texte client. Un journal technique indique les appels; l’état métier permet de répondre à la question « où en est la demande ? ».

## À retenir
La reprise ne consiste pas à relancer aveuglément le graphe entier. Elle consiste à retrouver un état durable puis à appliquer uniquement une transition encore autorisée.
