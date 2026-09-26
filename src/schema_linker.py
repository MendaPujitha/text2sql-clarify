"""
Phase 2: Schema linking.

Given a full schema description and a question, return only the tables
that are likely relevant. Simple keyword-overlap approach -- no embeddings
needed yet (that comes in Phase 4). This keeps prompts smaller and more
accurate as a database grows to many tables.
"""
import re


def parse_schema_into_tables(schema: str) -> dict:
    """
    Turn the flat schema string (one line per table, from executor.get_schema)
    into {table_name: full_line} so we can filter by table later.
    """
    tables = {}
    for line in schema.strip().split("\n"):
        match = re.match(r"Table (\w+):", line)
        if match:
            tables[match.group(1)] = line
    return tables


def relevant_tables(schema: str, question: str, min_tables: int = 2) -> str:
    """
    Return a schema string containing only tables whose name or column
    names share a keyword with the question. Falls back to the full
    schema if fewer than `min_tables` match (keeps small DBs unaffected;
    matters more once you have 20+ tables).
    """
    tables = parse_schema_into_tables(schema)
    question_words = set(re.findall(r"[a-zA-Z]+", question.lower()))

    matched = []
    for name, line in tables.items():
        table_words = set(re.findall(r"[a-zA-Z]+", line.lower()))
        if question_words & table_words:
            matched.append(line)

    if len(matched) < min_tables:
        return schema  # not enough signal to safely narrow down; use everything

    return "\n".join(matched)