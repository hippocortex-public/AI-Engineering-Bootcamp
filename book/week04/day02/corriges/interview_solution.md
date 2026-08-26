# Corrigé — Questions d’entretien

## Question 1

Un agent ne doit pas appeler directement le SDK fournisseur parce que cela crée un couplage fort. Il devient difficile à tester, à remplacer, à observer et à exécuter en CI. Le SDK doit être encapsulé dans un `ModelClient`.

## Question 2

Un `Agent` définit un comportement et un contrat d’exécution. Un `ModelClient` abstrait l’appel au modèle. Un `Runner` orchestre une ou plusieurs exécutions, éventuellement avec workflow, mémoire et observabilité.

## Question 3

Un `AgentResult` permet de transporter le texte, le statut, l’usage, les traces et les métadonnées. Une chaîne simple est insuffisante pour orchestrer ou diagnostiquer un système agentique.

## Question 4

On injecte un faux `ModelClient` déterministe. Il retourne une réponse prévisible sans appel réseau. Cela permet de tester le contrat logiciel de l’agent indépendamment de la variabilité LLM.

## Question 5

Une trace minimale doit indiquer les étapes importantes : validation, construction du prompt, appel modèle, statut final. Elle doit aussi être suffisamment stable pour être testée.

## Question 6

Si l’agent gère tout, il devient un composant monolithique. Les responsabilités sont mélangées, les tests deviennent fragiles, et les évolutions futures sont coûteuses.

## Question 7

Il faut partir des besoins immédiats et définir des contrats simples. L’abstraction doit accepter l’extension, mais ne doit pas anticiper toutes les fonctionnalités futures dans son implémentation actuelle.

## Question 8

Les guardrails simples empêchent les erreurs évidentes, clarifient le contrat et protègent l’exécution. Même sans politique sécurité complète, ils améliorent la robustesse du framework.
