"""
Phase 1: CLI entry point.

Run with:
    python src/main.py
"""
from executor import get_schema, run_sql
from sql_generator import generate_sql


def main():
    print("Text-to-SQL (Phase 1) -- type a question, or 'quit' to exit.\n")

    schema = get_schema()

    while True:
        question = input("Ask a question about the database: ").strip()
        if question.lower() in ("quit", "exit"):
            break
        if not question:
            continue

        try:
            sql = generate_sql(schema, question)
            print(f"\nGenerated SQL:\n  {sql}\n")

            columns, rows = run_sql(sql)
            print("Result:")
            print("  " + " | ".join(columns))
            for row in rows[:20]:
                print("  " + " | ".join(str(v) for v in row))
            if len(rows) > 20:
                print(f"  ... ({len(rows) - 20} more rows)")
            print()
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()
