# Gradebook From Hell Lab Instructions

## Overview

This repository contains a Python command-line gradebook application with intentional defects.

Your job is to treat the grading policy as the source of truth, write tests against that policy, expose defects, fix the code, and protect each fix with a test.

You are not searching for bugs at random. Your primary task is to translate requirements into executable unit tests. Bugs are discovered as a consequence of testing the requirements.

## Source of truth

Use [grading-policy.md](./grading-policy.md) as the authoritative requirements document.

## Your task

You should:

1. Get the project to build and run.
2. Read the policy requirements.
3. Write unit tests for each requirement group.
4. Run the tests and identify defects.
5. Fix the implementation defects.
6. Keep each fix protected by a regression test.

Before fixing a defect, first write a test that demonstrates the defect.

## Levels

### Level 0: Build and run the app

The repository intentionally contains a few setup issues. Your first task is to get:

- the CLI running
- `pytest` collecting tests

Do not over-engineer this step. Fix only what is necessary to get the project into a runnable state.

### Level 1: Core grading

Focus on:

- weighted averages
- grade boundaries
- missing and excused work
- dropped quizzes
- corrected grades

### Level 2: CSV and import

Focus on:

- normalization
- duplicate handling
- invalid values
- empty files
- malformed rows

### Level 3: Reporting

Focus on:

- student report output
- rankings
- category summaries
- class average and median
- output formatting

### Level 4: Policy and rule behavior

Focus on:

- late penalties
- grade floors
- pass/fail handling
- category weight validation

### Level 5: State and workflow

Focus on:

- repeated imports
- corrected grade replacement
- withdrawn student handling
- validation and audit workflow

## Deliverables

Submit:

- a working application
- a `pytest` suite covering the requirements you tested
- tests named after requirement IDs where practical
- a brief summary of the defects your team fixed

## Suggested workflow

1. Start with one requirement group at a time.
2. Read one requirement.
3. Write a test.
4. Watch it fail or pass.
5. Only then inspect the implementation.
6. Name tests after requirement IDs, for example `test_core_02_letter_boundary`.
7. Prefer small focused tests over large end-to-end tests.
8. Fix one defect at a time.
9. Re-run the relevant tests after each fix.

## Useful commands

```bash
python -m gradebook --help
python -m gradebook validate sample_data/students.csv sample_data/assignments.csv sample_data/grades.csv
python -m gradebook final-grades sample_data/students.csv sample_data/assignments.csv sample_data/grades.csv
python -m pytest
```
