from gradebook.calculator import compute_student_grade
from gradebook.importer import load_gradebook_data
from gradebook.reports import build_audit_report, build_category_report, build_rank_report
from gradebook.storage import InMemoryStorage


def test_state_01_reimport_does_not_duplicate_records() -> None:
    storage = InMemoryStorage()
    first = storage.load("sample_data/students.csv", "sample_data/assignments.csv", "sample_data/grades.csv")
    first_grade_count = len(first.grades)
    first_issue_count = len(first.validation_issues)
    second = storage.load("sample_data/students.csv", "sample_data/assignments.csv", "sample_data/grades.csv")
    assert len(second.grades) == first_grade_count
    assert len(second.validation_issues) == first_issue_count


def test_state_02_latest_grade_row_wins() -> None:
    data = load_gradebook_data("sample_data/students.csv", "sample_data/assignments.csv", "sample_data/grades.csv")
    result = compute_student_grade(data, data.students["erin@njit.edu"])
    quiz_summary = next(summary for summary in result.category_summaries if summary.category == "QUIZ")
    assert quiz_summary.earned_points == 19


def test_state_03_withdrawn_students_excluded_from_rank_and_category_reports() -> None:
    data = load_gradebook_data("sample_data/students.csv", "sample_data/assignments.csv", "sample_data/grades.csv")
    assert "derek@njit.edu" not in build_rank_report(data)
    assert "derek@njit.edu" not in build_category_report(data)


def test_state_05_audit_includes_invalid_grade_records() -> None:
    data = load_gradebook_data("sample_data/students.csv", "sample_data/assignments.csv", "sample_data/grades.csv")
    audit = build_audit_report(data)
    assert "ghost@njit.edu" in audit or "NOPE" in audit
