from __future__ import annotations

from .importer import load_gradebook_data
from .models import GradebookData


class InMemoryStorage:
    def __init__(self) -> None:
        self.data = GradebookData()

    def load(self, students_path: str, assignments_path: str, grades_path: str) -> GradebookData:
        fresh = load_gradebook_data(students_path, assignments_path, grades_path)
        self.data.students.update(fresh.students)
        self.data.assignments.update(fresh.assignments)
        self.data.grades.extend(fresh.grades)
        self.data.validation_issues.extend(fresh.validation_issues)
        return self.data
