from pathlib import Path

from gradebook.calculator import _letter_grade, compute_student_grade
from gradebook.importer import load_gradebook_data


DATA_DIR = Path("sample_data")


def load_data():
    return load_gradebook_data(DATA_DIR / "students.csv", DATA_DIR / "assignments.csv", DATA_DIR / "grades.csv")


def test_core_02_letter_boundaries() -> None:
    assert _letter_grade(89.5) == "B"


def test_core_03_missing_counts_as_zero() -> None:
    data = load_data()
    result = compute_student_grade(data, data.students["erin@njit.edu"])
    assert "HW2" in result.missing_assignments


def test_core_05_drop_lowest_only_with_three_quizzes() -> None:
    data = load_data()
    result = compute_student_grade(data, data.students["bob@njit.edu"])
    quiz_summary = next(summary for summary in result.category_summaries if summary.category == "QUIZ")
    assert quiz_summary.possible_points == 40


def test_core_06_extra_credit_cap() -> None:
    data = load_data()
    result = compute_student_grade(data, data.students["alice@njit.edu"])
    assert result.numeric_grade <= 100


def test_core_08_corrected_grade_replaces_previous_score() -> None:
    data = load_data()
    result = compute_student_grade(data, data.students["erin@njit.edu"])
    quiz_summary = next(summary for summary in result.category_summaries if summary.category == "QUIZ")
    assert quiz_summary.earned_points == 19
