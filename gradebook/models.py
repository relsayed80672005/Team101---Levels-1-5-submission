from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Iterable


class StudentStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    WITHDRAWN = "withdrawn"


class GradeStatus(str, Enum):
    RECORDED = "recorded"
    MISSING = "missing"
    EXCUSED = "excused"


@dataclass(slots=True)
class Student:
    student_id: str
    first_name: str
    last_name: str
    email: str
    status: StudentStatus = StudentStatus.ACTIVE
    section: str = "main"

    @property
    def display_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()


@dataclass(slots=True)
class Assignment:
    assignment_id: str
    name: str
    category: str
    max_points: float
    weight: float
    due_date: date | None = None
    drop_lowest_eligible: bool = False
    is_extra_credit: bool = False
    late_penalty_per_day: float = 0.10
    min_score_floor: float | None = None
    grading_mode: str = "points"


@dataclass(slots=True)
class GradeRecord:
    student_email: str
    assignment_id: str
    score: float | None = None
    grade_status: GradeStatus = GradeStatus.RECORDED
    days_late: int = 0
    raw_value: str = ""
    notes: str = ""
    source_row: int = 0


@dataclass(slots=True)
class ValidationIssue:
    requirement_id: str
    message: str
    row_number: int | None = None
    severity: str = "error"
    source: str = ""


@dataclass(slots=True)
class CategorySummary:
    category: str
    weight: float
    earned_points: float
    possible_points: float
    average_percent: float


@dataclass(slots=True)
class StudentComputation:
    student: Student
    numeric_grade: float
    letter_grade: str
    category_summaries: list[CategorySummary] = field(default_factory=list)
    missing_assignments: list[str] = field(default_factory=list)


@dataclass(slots=True)
class GradebookData:
    students: dict[str, Student] = field(default_factory=dict)
    assignments: dict[str, Assignment] = field(default_factory=dict)
    grades: list[GradeRecord] = field(default_factory=list)
    validation_issues: list[ValidationIssue] = field(default_factory=list)

    def copy(self) -> "GradebookData":
        return GradebookData(
            students=dict(self.students),
            assignments=dict(self.assignments),
            grades=list(self.grades),
            validation_issues=list(self.validation_issues),
        )

    def active_students(self) -> list[Student]:
        return [student for student in self.students.values() if student.status == StudentStatus.ACTIVE]

    def all_categories(self) -> list[str]:
        categories = {assignment.category for assignment in self.assignments.values()}
        return sorted(categories)

    def issues_for_source(self, source: str) -> list[ValidationIssue]:
        return [issue for issue in self.validation_issues if issue.source == source]

    def grade_records_for_student(self, email: str) -> list[GradeRecord]:
        return [record for record in self.grades if record.student_email == email]

    def extend_issues(self, issues: Iterable[ValidationIssue]) -> None:
        self.validation_issues.extend(issues)
