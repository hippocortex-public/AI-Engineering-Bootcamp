# 07_DECISIONS.md

# Project Decisions

Version: 1.1
Status: Frozen

## Decision 001 — Bootcamp orientation

The bootcamp is oriented toward AI Engineering, AI Backend Engineering and AI Solution Architecture.

## Decision 002 — Markdown as source of truth

Markdown files are the canonical source. Notebooks are generated artifacts.

## Decision 003 — Repository structure is frozen

The repository structure must not change unless explicitly requested by the project owner.

## Decision 004 — Corrections are stored locally per day

All corrections are stored in:

```text
book/weekXX/dayYY/corriges/
```

Mandatory correction files:

```text
exercises_solution.md
interview_solution.md
challenge_solution.md
review.md
```

## Decision 005 — Teacher notebook is mandatory

Every generated training day must produce two notebooks:

```text
notebooks/weekXX/Sx_Jy_<slug>.ipynb
notebooks/weekXX/teacher/Sx_Jy_<slug>_teacher.ipynb
```

## Decision 006 — Deliverable-first generation

The GPT must generate complete deliverables as files when content is too large for the conversation.

## Decision 007 — No spontaneous restructuring

The GPT must not propose new folders, file types or content categories unless the user explicitly requests it.

## Decision 008 — Day completeness

A day is incomplete if any mandatory source, correction, directory or notebook artifact is missing.
