from gradebook.importer import load_gradebook_data
from gradebook.reports import build_student_report, build_validation_report


def test_validate_report_contains_header() -> None:
    data = load_gradebook_data("sample_data/students.csv", "sample_data/assignments.csv", "sample_data/grades.csv")
    text = build_validation_report(data)
    assert "Validation" in text


def test_student_report_finds_alice() -> None:
    data = load_gradebook_data("sample_data/students.csv", "sample_data/assignments.csv", "sample_data/grades.csv")
    report = build_student_report(data, "alice@njit.edu")
    assert "Alice Nguyen" in report
    assert "Assignments:" in report
