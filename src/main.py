"""
Phase 2: CLI entry point with schema linking and self-correction.

Run with:
    python src/main.py
"""
from executor import get_schema, run_sql
from schema_linker import relevant_tables
from sql_generator import generate_sql_with_retry


def main():
    print("Text-to-SQL (Phase 2) -- type a question, or 'quit' to exit.\n")

    full_schema = get_schema()

    while True:
        question = input("Ask a question about the database: ").strip()
        if question.lower() in ("quit", "exit"):
            break
        if not question:
            continue

        try:
            schema = relevant_tables(full_schema, question)
            sql, columns, rows = generate_sql_with_retry(schema, question, run_sql)

            print(f"\nGenerated SQL:\n  {sql}\n")
            print("Result:")
            print("  " + " | ".join(columns))
            for row in rows[:20]:
                print("  " + " | ".join(str(v) for v in row))
            if len(rows) > 20:
                print(f"  ... ({len(rows) - 20} more rows)")
            print()
        except Exception as e:
            print(f"\nError after retries: {e}\n")


if __name__ == "__main__":
    main()