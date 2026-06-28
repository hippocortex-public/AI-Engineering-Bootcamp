# 03_REPOSITORY_STRUCTURE.md

# Repository Structure Specification

Version: 1.1
Status: Frozen

## Root structure

```text
ai-engineering-bootcamp/
├── README.md
├── ROADMAP.md
├── BOOTCAMP_STATUS.md
├── CHANGELOG.md
├── pyproject.toml
├── requirements.txt
├── mkdocs.yml
├── specifications/
├── book/
├── notebooks/
├── docs/
├── templates/
├── standards/
├── examples/
├── tests/
├── scripts/
├── mini_framework/
└── ai_platform/
```

## Day structure

```text
book/
└── weekXX/
    └── dayYY/
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

## Notebook structure

```text
notebooks/
└── weekXX/
    ├── Sx_Jy_<slug>.ipynb
    └── teacher/
        └── Sx_Jy_<slug>_teacher.ipynb
```

The teacher notebook is mandatory.

## Corrections

Corrections are local to each day and are never stored globally.
