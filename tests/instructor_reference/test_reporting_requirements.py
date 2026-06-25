from gradebook.importer import load_gradebook_data
from gradebook.reports import build_category_report, build_final_grades_report, build_rank_report


def test_report_02_rank_descending_with_email_tiebreak() -> None:
    data = load_gradebook_data("sample_data/students.csv", "sample_data/assignments.csv", "sample_data/grades.csv")
    report = build_rank_report(data)
    lines = report.splitlines()
    assert lines[1].startswith("1. alice@njit.edu")


def test_report_03_category_report_uses_percent_average() -> None:
    data = load_gradebook_data("sample_data/students.csv", "sample_data/assignments.csv", "sample_data/grades.csv")
    report = build_category_report(data)
    quiz_line = next(line for line in report.splitlines() if line.startswith("QUIZ"))
    assert "%" in quiz_line and "average=1" not in quiz_line


def test_report_05_even_median_averages_middle_two() -> None:
    data = load_gradebook_data("sample_data/students.csv", "sample_data/assignments.csv", "sample_data/grades.csv")
    report = build_final_grades_report(data)
    assert "Class median: 88.79%" in report


def test_report_07_percent_format_uses_two_decimals() -> None:
    data = load_gradebook_data("sample_data/students.csv", "sample_data/assignments.csv", "sample_data/grades.csv")
    report = build_final_grades_report(data)
    assert ".00%" in report or ".25%" in report or ".50%" in report or ".75%" in report
