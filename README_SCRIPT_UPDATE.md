# Script update — notebooks generation

Remplacer le fichier existant :

```text
scripts/build_notebooks.py
```

par la version fournie dans ce paquet.

## Nouvelle structure supportée

```text
book/
└── week01/
    └── day02/
        ├── README.md
        ├── learning_objectives.md
        ├── chapter.md
        ├── exercises.md
        ├── interview.md
        ├── challenge.md
        ├── references.md
        ├── corriges/
        │   ├── exercises_solution.md
        │   ├── interview_solution.md
        │   ├── challenge_solution.md
        │   └── review.md
        ├── diagrams/
        ├── assets/
        └── labs/
```

## Générer les notebooks étudiant

```bash
python scripts/build_notebooks.py
```

Pour un jour précis :

```bash
python scripts/build_notebooks.py --week week01 --day day02
```

## Générer les notebooks formateur avec corrigés

```bash
python scripts/build_notebooks.py --teacher
```

Pour un jour précis :

```bash
python scripts/build_notebooks.py --week week01 --day day02 --teacher
```

## Sorties

Mode étudiant :

```text
notebooks/week01/S1_J2_<slug>.ipynb
```

Mode formateur :

```text
notebooks/week01/teacher/S1_J2_<slug>_teacher.ipynb
```
