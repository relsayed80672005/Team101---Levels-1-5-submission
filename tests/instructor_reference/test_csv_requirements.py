from gradebook.importer import import_students, load_gradebook_data


def test_csv_01_email_normalized_with_trim_and_lowercase() -> None:
    students, _ = import_students("sample_data/students.csv")
    assert "erin@njit.edu" in students


def test_csv_02_duplicate_students_after_normalization_flagged(tmp_path) -> None:
    path = tmp_path / "students.csv"
    path.write_text(
        "student_id,first_name,last_name,email,status,section\n"
        "1,Alice,N,alice@njit.edu,active,A\n"
        "2,Alice,N, ALICE@njit.edu ,active,A\n",
        encoding="utf-8",
    )
    students, issues = import_students(path)
    assert students
    assert any(issue.requirement_id == "CSV-02" for issue in issues)


def test_csv_04_score_greater_than_max_invalid() -> None:
    data = load_gradebook_data("sample_data/students.csv", "sample_data/assignments.csv", "sample_data/grades.csv")
    assert any(issue.requirement_id == "CSV-04" for issue in data.validation_issues)


def test_csv_06_empty_csv_after_header_reports_issue(tmp_path) -> None:
    students = tmp_path / "students.csv"
    assignments = tmp_path / "assignments.csv"
    grades = tmp_path / "grades.csv"
    students.write_text("student_id,first_name,last_name,email,status,section\n", encoding="utf-8")
    assignments.write_text("assignment_id,name,category,max_points,weight,due_date,drop_lowest_eligible,is_extra_credit,late_penalty_per_day,min_score_floor,grading_mode\n", encoding="utf-8")
    grades.write_text("student_email,assignment_id,score,status,days_late,notes\n", encoding="utf-8")
    data = load_gradebook_data(students, assignments, grades)
    assert any(issue.requirement_id == "CSV-06" for issue in data.validation_issues)


def test_csv_07_malformed_rows_become_issues_not_crash(tmp_path) -> None:
    students = tmp_path / "students.csv"
    students.write_text(
        "student_id,first_name,last_name,email,status,section\n"
        "1,Alice,N,alice@njit.edu,active\n",
        encoding="utf-8",
    )
    imported, issues = import_students(students)
    assert imported == {}
    assert any(issue.requirement_id == "CSV-07" for issue in issues)
