# Gradebook From Hell

Gradebook From Hell is a CS 490 software quality lab. The repository contains a Python command-line gradebook application with intentional defects for students to find with tests.

## Requirements

- Python 3.13
- `pytest`

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m pip install pytest
```

## Run the CLI

```bash
python -m gradebook --help
python -m gradebook validate samples/students.csv sample_data/assignments.csv sample_data/grades.csv
python -m gradebook final-grades sample_data/students.csv sample_data/assignments.csv sample_data/grades.csv
python -m gradebook student-report sample_data/students.csv sample_data/assignments.csv sample_data/grades.csv --student alice@njit.edu
python -m gradebook category-report sample_data/students.csv sample_data/assignments.csv sample_data/grades.csv
python -m gradebook rank sample_data/students.csv sample_data/assignments.csv sample_data/grades.csv
python -m gradebook audit sample_data/students.csv sample_data/assignments.csv sample_data/grades.csv
```

## Run tests

```bash
python -m pytest
```

## Student guidance

- Source of truth: [docs/grading-policy.md](./docs/grading-policy.md)
- Lab instructions: [docs/lab-instructions.md](./docs/lab-instructions.md)

Students should use the grading policy to drive test design and implementation fixes.
