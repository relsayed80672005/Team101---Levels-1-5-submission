# Instructor Answer Key

This file is for instructors only. It maps the seeded defects to requirement IDs and suggests how to test and fix them.

## Running instructor reference tests

After students complete the lab, instructors can run the reference suite with:

```bash
python -m pytest tests/instructor_reference
```

These tests are expected to fail against the starting repository because the seeded bugs are still present.

## Seeded functional bugs

| Bug ID | Requirement | Category | Description | Likely module | Expected behavior | Suggested test idea | Suggested fix direction |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BUG-01 | CORE-02 | Core grading | Letter grades round before threshold checks, so boundary scores can move upward incorrectly. | `gradebook/calculator.py` | Thresholds use raw numeric grade without upward rounding. | Check a grade like `89.5` stays a `B`. | Compare directly against numeric thresholds instead of `round()`. |
| BUG-02 | CORE-03 | Core grading | Missing grades are treated as full possible points instead of zero earned points. | `gradebook/calculator.py` | Missing non-excused work contributes `0/max_points`. | Student with missing homework should lose credit. | Return `0, max_points` for missing non-excused records. |
| BUG-03 | CORE-05 | Core grading | Quiz drop happens when only two quizzes are present. | `gradebook/calculator.py` | Lowest quiz is dropped only when there are at least three quizzes. | Build a fixture with two quizzes and verify no drop. | Change the eligibility threshold. |
| BUG-04 | CORE-06 | Core grading | Extra credit can push final grade above `100`. | `gradebook/calculator.py` | Final reported numeric grade is capped at `100`. | Use a high-performing student with bonus points. | Clamp the final numeric grade. |
| BUG-05 | CORE-08 | Core grading | Duplicate grade rows keep the first row instead of the latest correction. | `gradebook/calculator.py` | Later grade row wins. | Provide two rows for the same student and assignment. | Overwrite existing mapping on later rows. |
| BUG-06 | CSV-01 | CSV/import | Email normalization lowercases but does not trim whitespace. | `gradebook/students.py` | Leading and trailing whitespace is removed before storage. | Import a student with surrounding spaces in email. | Use `strip().lower()`. |
| BUG-07 | CSV-02 | CSV/import | Duplicate detection misses emails that differ only by whitespace because normalization is incomplete. | `gradebook/students.py` | Duplicates use normalized email addresses. | Two rows that differ only by case and spaces should collide. | Fix normalization before duplicate checks. |
| BUG-08 | CSV-04 | CSV/import | Scores above `max_points` are accidentally accepted for regular assignments. | `gradebook/policies.py` | Non-extra-credit scores greater than `max_points` produce validation issues. | Include `101/100` on a normal assignment. | Remove the premature return and honor extra-credit exception only where allowed. |
| BUG-09 | CSV-06 | CSV/import | Header-only CSV files produce no validation issue. | `gradebook/importer.py` | Header-only files should emit `CSV-06`. | Create temporary CSVs with only headers. | Add validation when `DictReader` has headers but zero data rows. |
| BUG-10 | CSV-07 | CSV/import | A malformed student row raises instead of being reported and skipped. | `gradebook/importer.py` | Import continues after malformed rows. | Feed a short row or bad date. | Catch row-level exceptions and continue. |
| BUG-11 | REPORT-02 | Reporting | Rankings sort ascending by grade instead of descending and include withdrawn students indirectly through status filtering choices. | `gradebook/reports.py` | Highest grade should rank first, ties by email asc. | Assert the top-ranked email for sample data. | Reverse primary numeric sort and exclude withdrawn students. |
| BUG-12 | REPORT-03 | Reporting | Category report uses average raw earned points instead of average category percentages. | `gradebook/reports.py` | Show average percentage per category. | Compare quiz line against percent-based expectation. | Average `summary.average_percent`. |
| BUG-13 | REPORT-05 | Reporting | Even-sized median uses the lower middle value instead of averaging the two middle values. | `gradebook/calculator.py` | Standard statistical median for even sample sizes. | Four included students should average middle two grades. | Compute mean of the two middle entries. |
| BUG-14 | REPORT-07 | Reporting | Report percentages are formatted with one decimal place instead of exactly two. | `gradebook/reports.py` | All displayed percentages use two decimals. | Match output against `NN.NN%` formatting. | Change formatter to `:.2f`. |
| BUG-15 | POLICY-01 | Policy/rule | Weight validation expects a total of `1.0` instead of `100`. | `gradebook/policies.py` | Non-extra-credit category weights total `100`. | Sample assignments should validate cleanly at `100`. | Compare to `100`, not `1.0`. |
| BUG-16 | POLICY-02 | Policy/rule | Late penalty subtracts from assignment max points and does not cap at three days. | `gradebook/policies.py` | Penalty is `10%` of earned score per day, max three days. | Compare one-day and four-day late cases. | Base penalty on earned score and clamp late days. |
| BUG-17 | POLICY-03 | Policy/rule | Minimum score floor is applied after penalty logic incorrectly for some cases because the penalty basis is wrong. | `gradebook/policies.py` | Floor should be applied after correct late penalty calculation. | Use exam with floor plus late days. | Fix late-penalty sequence and floor application. |
| BUG-18 | POLICY-04 | Policy/rule | Pass/fail parsing is case-sensitive, so uppercase `PASS` is invalid. | `gradebook/grades.py` | Pass/fail tokens are case-insensitive. | Use `PASS` in sample data. | Normalize token before lookup. |
| BUG-19 | STATE-01 | State/workflow | Re-loading into the same storage object appends grade rows and validation issues instead of replacing or deduplicating state. | `gradebook/storage.py` | Re-import should be idempotent. | Load the same files twice into one storage instance. | Reset or merge state deterministically. |
| BUG-20 | STATE-02 | State/workflow | Duplicate grade rows remain in raw state and calculations treat the earliest row as authoritative. | `gradebook/calculator.py` | Later grade row is the corrected record. | Assert the corrected score is used. | Overwrite earlier grade rows during consolidation. |
| BUG-21 | STATE-03 | State/workflow | Withdrawn students are excluded from some reports but still appear in ranking output. | `gradebook/reports.py` | Withdrawn students are excluded from ranking and aggregates. | Check `rank` output for withdrawn email absence. | Filter withdrawn status consistently. |
| BUG-22 | STATE-05 | State/workflow | Audit output skips grade-sourced validation issues, so invalid grade records are omitted. | `gradebook/reports.py` | Audit should include invalid grade rows and policy issues. | Look for unknown student or unknown assignment in audit text. | Include grade-source issues in the audit report. |
