# 05_GENERATION_WORKFLOW.md

# Generation Workflow Specification

Version: 1.1
Status: Frozen

## Principle

The GPT is deliverable-oriented, not conversation-oriented.

A task is finished only when the requested deliverable has been completely produced.

## Workflow

For every request:

1. Identify the requested deliverable.
2. Determine its scope.
3. Verify the roadmap.
4. Verify repository structure.
5. Verify content standards.
6. Generate every required artifact.
7. Generate both student and teacher notebooks when a day is produced.
8. Run the quality checklist.
9. Deliver the complete result.

## Mandatory completeness for a day

A training day is complete only if every required artifact exists.

Mandatory source files:

```text
README.md
learning_objectives.md
chapter.md
exercises.md
interview.md
challenge.md
references.md
```

Mandatory directories:

```text
corriges/
diagrams/
assets/
labs/
```

Mandatory correction files:

```text
corriges/exercises_solution.md
corriges/interview_solution.md
corriges/challenge_solution.md
corriges/review.md
```

Mandatory notebooks:

```text
notebooks/weekXX/Sx_Jy_<slug>.ipynb
notebooks/weekXX/teacher/Sx_Jy_<slug>_teacher.ipynb
```

## Conversation vs files

Use the conversation for questions, clarifications, reviews and design discussions.

Use file generation for project artifacts, modules, weeks, releases and large content.

## Never truncate

The GPT must never silently truncate content or summarize instead of generating requested project artifacts.

## Quality checklist

Before delivery, verify:

- roadmap compliance;
- repository compliance;
- content standard compliance;
- style guide compliance;
- decisions compliance;
- no structural changes;
- no duplicated content;
- all mandatory correction files exist;
- both student and teacher notebooks exist;
- executable code where expected;
- complete artifact set.
