"""
Phase 2: Schema-aware SQL generation with few-shot examples and
self-correction on execution errors.
"""
import re

from llm_client import ask_llm

SYSTEM_PROMPT = (
    "You are an expert SQL generator. Given a database schema and a "
    "natural language question, output ONLY the SQL query needed to "
    "answer it. Do not include explanations, markdown formatting, or "
    "code fences. Output raw SQL only."
)

# Phase 2: few-shot examples -- consistently the single biggest accuracy
# improvement for free. Swap these for examples drawn from your own schema
# if you change databases.
FEW_SHOT_EXAMPLES = [
    (
        "How many customers are there?",
        "SELECT COUNT(*) FROM Customer;",
    ),
    (
        "List the top 5 best-selling tracks by quantity sold",
        "SELECT t.Name, SUM(il.Quantity) AS total_sold "
        "FROM Track t JOIN InvoiceLine il ON t.TrackId = il.TrackId "
        "GROUP BY t.TrackId ORDER BY total_sold DESC LIMIT 5;",
    ),
    (
        "Which customers are from Brazil?",
        "SELECT FirstName, LastName FROM Customer WHERE Country = 'Brazil';",
    ),
]


def build_few_shot_block() -> str:
    lines = []
    for question, sql in FEW_SHOT_EXAMPLES:
        lines.append(f"Q: {question}\nSQL: {sql}")
    return "\n\n".join(lines)


def build_prompt(schema: str, question: str, error_context: str = "") -> str:
    prompt = (
        f"Database schema:\n{schema}\n\n"
        f"Examples:\n{build_few_shot_block()}\n\n"
        f"Question: {question}\n"
    )
    if error_context:
        prompt += (
            f"\nYour previous attempt failed with this error:\n{error_context}\n"
            f"Fix the query and try again.\n"
        )
    prompt += "\nSQL query:"
    return prompt


def clean_sql(raw_output: str) -> str:
    """Strip markdown code fences if the model adds them despite instructions."""
    cleaned = re.sub(r"^```sql\s*|^```\s*|```$", "", raw_output.strip(), flags=re.MULTILINE)
    return cleaned.strip().rstrip(";") + ";"


def generate_sql(schema: str, question: str, error_context: str = "") -> str:
    prompt = build_prompt(schema, question, error_context)
    raw = ask_llm(prompt, system=SYSTEM_PROMPT)
    return clean_sql(raw)


def generate_sql_with_retry(schema: str, question: str, run_sql_fn, max_retries: int = 2):
    """
    Phase 2: self-correction loop. Generates SQL, tries executing it via
    run_sql_fn(sql) -> (columns, rows). If it errors, the error message is
    fed back to the LLM for a fix, up to max_retries times.

    Returns (sql, columns, rows). Raises the last error if all retries fail.
    """
    error_context = ""
    last_error = None

    for attempt in range(max_retries + 1):
        sql = generate_sql(schema, question, error_context)
        try:
            columns, rows = run_sql_fn(sql)
            return sql, columns, rows
        except Exception as e:
            last_error = e
            error_context = f"SQL: {sql}\nError: {e}"

    raise last_error