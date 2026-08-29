"""
Phase 1: Basic text-to-SQL generation.

Takes a natural language question + a schema description, asks the LLM
to produce a SQL query.
"""
import re

from llm_client import ask_llm

SYSTEM_PROMPT = (
    "You are an expert SQL generator. Given a database schema and a "
    "natural language question, output ONLY the SQL query needed to "
    "answer it. Do not include explanations, markdown formatting, or "
    "code fences. Output raw SQL only."
)


def build_prompt(schema: str, question: str) -> str:
    return (
        f"Database schema:\n{schema}\n\n"
        f"Question: {question}\n\n"
        f"SQL query:"
    )


def clean_sql(raw_output: str) -> str:
    """Strip markdown code fences if the model adds them despite instructions."""
    cleaned = re.sub(r"^```sql\s*|^```\s*|```$", "", raw_output.strip(), flags=re.MULTILINE)
    return cleaned.strip().rstrip(";") + ";"


def generate_sql(schema: str, question: str) -> str:
    prompt = build_prompt(schema, question)
    raw = ask_llm(prompt, system=SYSTEM_PROMPT)
    return clean_sql(raw)
