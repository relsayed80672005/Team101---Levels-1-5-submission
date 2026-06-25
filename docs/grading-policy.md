# Gradebook From Hell Grading Policy

This document is the source of truth for expected application behavior. Students should write tests against these numbered requirements.

## 1. Core grading

1. `CORE-01` Final numeric course grade is computed from category percentages multiplied by category weights. Within each category, points are summed across included assignments before the category percentage is calculated.
2. `CORE-02` Letter grades use these exact boundaries with no upward rounding: `A` for `93.00-100.00`, `A-` for `90.00-92.99`, `B+` for `87.00-89.99`, `B` for `83.00-86.99`, `B-` for `80.00-82.99`, `C+` for `77.00-79.99`, `C` for `73.00-76.99`, `C-` for `70.00-72.99`, `D+` for `67.00-69.99`, `D` for `63.00-66.99`, `D-` for `60.00-62.99`, and `F` below `60.00`.
3. `CORE-03` A missing grade on a non-excused assignment counts as zero earned points for that assignment.
4. `CORE-04` An excused assignment is excluded from both earned points and possible points for the affected student.
5. `CORE-05` The lowest quiz score is dropped only when a student has at least four non-excused quiz scores contributing to the course grade.
6. `CORE-06` Extra credit may raise a student’s numeric course grade, but the final numeric course grade reported to users must never exceed `100.00`.
7. `CORE-07` Course percentages are rounded to two decimal places for display only. Ranking and letter-grade decisions must use the unrounded numeric course grade.
8. `CORE-08` If multiple grade rows exist for the same student and assignment, the most recent row in the grades CSV replaces earlier rows for calculation purposes.
9. `CORE-09` For pass/fail assignments, `PASS` means full assignment credit and `FAIL` means zero assignment credit.

## 2. CSV and import

10. `CSV-01` Student email addresses are normalized by trimming leading and trailing whitespace and converting to lowercase during import.
11. `CSV-02` Duplicate students are detected by normalized email address. Duplicates must be reported as validation issues.
12. `CSV-03` Assignment IDs must be unique within the assignments CSV. Duplicate IDs must be reported as validation issues.
13. `CSV-04` A numeric score greater than the assignment’s `max_points` is invalid unless the assignment is marked as extra credit.
14. `CSV-05` Negative numeric scores are invalid.
15. `CSV-06` A CSV file that contains a header row but no data rows must produce a validation issue instead of silently succeeding.
16. `CSV-07` Malformed rows must be reported as validation issues, and the importer should continue processing the rest of the file instead of crashing.
17. `CSV-08` Grade rows referencing unknown students or unknown assignments must be reported as validation issues.

## 3. Reporting

18. `REPORT-01` `student-report` prints the student name, normalized email, status, final numeric grade, letter grade, and one line per assignment.
19. `REPORT-02` `rank` orders students by descending final numeric grade. Ties are broken by normalized email in ascending alphabetical order.
20. `REPORT-03` `category-report` shows the average percentage for each category across included students, not the average raw points.
21. `REPORT-04` `final-grades` includes active and inactive students but excludes withdrawn students.
22. `REPORT-05` The class median is the standard statistical median of the included final numeric grades. For an even number of students, it is the mean of the two middle grades.
23. `REPORT-06` The class average excludes withdrawn students.
24. `REPORT-07` Percentage values shown in text reports are formatted to exactly two decimal places.

## 4. Policy and rule behavior

25. `POLICY-01` The total of all non-extra-credit category weights must equal exactly `100`.
26. `POLICY-02` Late penalty is `10%` of the student’s earned score per day late, capped at `3` late days, and applies only when the assignment has a due date.
27. `POLICY-03` If an assignment has a minimum score floor, the floor is applied after late penalties are calculated.
28. `POLICY-04` Pass/fail grade values are case-insensitive. `PASS` and `pass` are equivalent, and `FAIL` and `fail` are equivalent.
29. `POLICY-05` Extra credit assignments must be in the `EXTRA_CREDIT` category and have weight `0`.
30. `POLICY-06` Excused assignments are exempt from late penalties and from the missing-as-zero rule.
31. `POLICY-07` Withdrawn students do not receive a final course letter grade in reports that exclude them.
32. `POLICY-08` If an assignment has no due date, no lateness penalty is applied.

## 5. State and workflow

33. `STATE-01` Loading the same three CSV files multiple times into the same in-memory gradebook state must not duplicate students, assignments, grades, or validation issues.
34. `STATE-03` Withdrawn students remain visible to validation and audit workflows but are excluded from ranking and aggregate reporting.
35. `STATE-04` The `validate` command exits with a non-zero status code when validation issues are present and `0` when no validation issues are present.
36. `STATE-05` The `audit` command includes invalid grade records, duplicate grade rows, and policy violations in its output.
37. `STATE-06` Supported student status values are `active`, `inactive`, and `withdrawn`. Unknown status values produce a validation issue and default to `active`.
38. `STATE-07` An excused grade row may omit the numeric score field.
39. `STATE-08` Each call to the top-level loader returns a fresh `GradebookData` snapshot that can be tested independently of previous loads.
