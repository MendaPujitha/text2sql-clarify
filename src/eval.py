"""
Phase 2: Evaluation harness.

Runs every (question, expected_sql) pair in data/eval_set.json through the
generator, executes both the generated SQL and the expected SQL, and
compares results (execution-match accuracy -- more robust than comparing
raw SQL strings, since two different queries can be equally correct).

Run with:
    python src/eval.py
"""
import json
import os

from executor import get_schema, run_sql
from schema_linker import relevant_tables
from sql_generator import generate_sql_with_retry

EVAL_SET_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "eval_set.json")


def load_eval_set():
    with open(EVAL_SET_PATH, "r") as f:
        return json.load(f)


def results_match(rows_a, rows_b) -> bool:
    """Order-insensitive comparison of result rows."""
    return sorted(map(str, rows_a)) == sorted(map(str, rows_b))


def run_eval():
    eval_set = load_eval_set()
    full_schema = get_schema()

    passed = 0
    failed_cases = []

    for i, case in enumerate(eval_set, start=1):
        question = case["question"]
        expected_sql = case["expected_sql"]

        try:
            expected_columns, expected_rows = run_sql(expected_sql)
        except Exception as e:
            print(f"[{i}] SKIPPED (expected_sql itself failed to run): {e}")
            continue

        try:
            schema = relevant_tables(full_schema, question)
            generated_sql, gen_columns, gen_rows = generate_sql_with_retry(
                schema, question, run_sql
            )
            is_match = results_match(expected_rows, gen_rows)
        except Exception as e:
            generated_sql = None
            is_match = False
            print(f"[{i}] ERROR generating/running SQL: {e}")

        status = "PASS" if is_match else "FAIL"
        print(f"[{i}] {status} -- \"{question}\"")
        if not is_match:
            print(f"      expected SQL: {expected_sql}")
            print(f"      generated SQL: {generated_sql}")
            failed_cases.append(question)
        else:
            passed += 1

    total = len(eval_set)
    accuracy = passed / total * 100 if total else 0
    print(f"\nExecution-match accuracy: {passed}/{total} ({accuracy:.1f}%)")

    if failed_cases:
        print("\nFailed questions:")
        for q in failed_cases:
            print(f"  - {q}")


if __name__ == "__main__":
    run_eval()