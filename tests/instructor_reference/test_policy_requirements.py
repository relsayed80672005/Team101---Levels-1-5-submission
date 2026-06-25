from gradebook.calculator import compute_all_students
from gradebook.importer import load_gradebook_data


def test_policy_01_weights_total_100_not_1() -> None:
    data = load_gradebook_data("sample_data/students.csv", "sample_data/assignments.csv", "sample_data/grades.csv")
    assert not any(issue.requirement_id == "POLICY-01" for issue in data.validation_issues)


def test_policy_02_late_penalty_uses_earned_score_and_caps_at_3_days() -> None:
    data = load_gradebook_data("sample_data/students.csv", "sample_data/assignments.csv", "sample_data/grades.csv")
    bob = next(result for result in compute_all_students(data) if result.student.email == "bob@njit.edu")
    assert bob.numeric_grade > 40


def test_policy_03_floor_applies_after_penalty() -> None:
    data = load_gradebook_data("sample_data/students.csv", "sample_data/assignments.csv", "sample_data/grades.csv")
    bob = next(result for result in compute_all_students(data) if result.student.email == "bob@njit.edu")
    assert bob.numeric_grade < 70


def test_policy_04_pass_fail_is_case_insensitive() -> None:
    data = load_gradebook_data("sample_data/students.csv", "sample_data/assignments.csv", "sample_data/grades.csv")
    assert not any("PASS" in issue.message for issue in data.validation_issues)
