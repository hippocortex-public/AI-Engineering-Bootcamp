# 04_CONTENT_STANDARD.md

# Content Standard Specification

Version: 1.1
Status: Frozen

## Core principle

Every training day is a complete learning unit.

A day is not complete unless it contains student-facing content, corrections, diagrams, labs, a student notebook and a teacher notebook.

## Mandatory day files

```text
README.md
learning_objectives.md
chapter.md
exercises.md
interview.md
challenge.md
references.md
```

## Mandatory day directories

```text
corriges/
diagrams/
assets/
labs/
```

## Mandatory correction files

```text
corriges/
├── exercises_solution.md
├── interview_solution.md
├── challenge_solution.md
└── review.md
```

## Notebook generation standard

Every day must generate two notebooks:

```text
notebooks/weekXX/Sx_Jy_<slug>.ipynb
notebooks/weekXX/teacher/Sx_Jy_<slug>_teacher.ipynb
```

The student notebook excludes corrections.

The teacher notebook includes:

- exercises solutions;
- interview solutions;
- challenge solutions;
- review notes.

## Labs standard

The `labs/` folder is mandatory for every day.

If no lab is required, it must contain a `README.md` explaining that no lab is required.

## Completion rule

A day is complete only when all mandatory source files, correction files, directories and notebooks exist.
