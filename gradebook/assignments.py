from __future__ import annotations

from datetime import date

from .models import Assignment, ValidationIssue


def parse_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y"}


def parse_optional_date(value: str) -> date | None:
    text = value.strip()
    if not text:
        return None
    return date.fromisoformat(text)


def build_assignment(row: dict[str, str], row_number: int) -> tuple[Assignment | None, list[ValidationIssue]]:
    issues: list[ValidationIssue] = []
    assignment_id = row.get("assignment_id", "").strip()
    name = row.get("name", "").strip()
    category = row.get("category", "").strip().upper()
    if not assignment_id or not name or not category:
        issues.append(
            ValidationIssue(
                requirement_id="CSV-07",
                message="Assignment row missing required fields.",
                row_number=row_number,
                source="assignments",
            )
        )
        return None, issues
    try:
        max_points = float(row.get("max_points", "0"))
        weight = float(row.get("weight", "0"))
    except ValueError:
        issues.append(
            ValidationIssue(
                requirement_id="CSV-07",
                message="Assignment points or weight not numeric.",
                row_number=row_number,
                source="assignments",
            )
        )
        return None, issues
    assignment = Assignment(
        assignment_id=assignment_id,
        name=name,
        category=category,
        max_points=max_points,
        weight=weight,
        due_date=parse_optional_date(row.get("due_date", "")),
        drop_lowest_eligible=parse_bool(row.get("drop_lowest_eligible", "")),
        is_extra_credit=parse_bool(row.get("is_extra_credit", "")),
        late_penalty_per_day=float(row.get("late_penalty_per_day", "0.10") or "0.10"),
        min_score_floor=float(row["min_score_floor"]) if row.get("min_score_floor", "").strip() else None,
        grading_mode=(row.get("grading_mode", "").strip() or "points").lower(),
    )
    return assignment, issues


def find_duplicate_assignments(assignments: list[Assignment]) -> list[ValidationIssue]:
    seen: set[str] = set()
    issues: list[ValidationIssue] = []
    for index, assignment in enumerate(assignments, start=2):
        if assignment.assignment_id in seen:
            issues.append(
                ValidationIssue(
                    requirement_id="CSV-03",
                    message=f"Duplicate assignment_id found: {assignment.assignment_id}",
                    row_number=index,
                    source="assignments",
                )
            )
        seen.add(assignment.assignment_id)
    return issues
