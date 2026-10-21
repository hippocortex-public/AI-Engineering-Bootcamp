# Lab LoRA optionnel — modèle BERT local

Ce script est fourni pour prolonger J5; il n’a pas été exécuté dans la validation standard. PyTorch, Transformers, PEFT et les poids BERT ne sont pas disponibles dans l’environnement de génération. L’apprentissage obligatoire de J5 adapte réellement une tête linéaire; il n’est pas présenté comme un fine-tuning de LLM.

Préparer un environnement séparé avec torch, transformers et peft, conserver les versions effectivement résolues dans un verrou de votre expérience et un modèle/tokenizer BERT local adapté au français. Vérifier la licence et les ressources nécessaires. Le code exige local_files_only=True et trust_remote_code=False et ne télécharge aucun modèle.

Depuis la racine :

```bash
python3 -m examples.week10.optional.train_lora --base-model /chemin/vers/bert-local --output /tmp/s10-lora-experiment --epochs 3
```

Le script cible explicitement l’architecture BERT, avec modules query/value et une tête classifier sauvegardée. Il refuse une autre architecture plutôt que supposer les mêmes noms de couches. Il optimise uniquement les paramètres entraînables et conserve le meilleur adaptateur selon le macro-F1 de validation. Aucun exemple de test n’entre dans l’optimisation ni la sélection; le script ne fait pas l’évaluation finale du test.

Les quelques tickets fictifs permettent de vérifier un protocole, pas d’obtenir un modèle prêt à déployer. Pour une expérience réelle : verrouiller base-model et tokenizer par artefacts immuables, enregistrer les versions logicielles, contrôler la licence/données, étudier les gradients/ressources puis utiliser un jeu réservé après sélection. Un chemin local n’atteste pas à lui seul le contenu des poids; ajouter une empreinte des artefacts pour une traçabilité complète.

L’API a été confrontée à la documentation primaire PEFT; la compatibilité d’exécution reste à vérifier sur votre installation. Aucun résultat LoRA ni benchmark GPU n’est annoncé dans cette archive.
