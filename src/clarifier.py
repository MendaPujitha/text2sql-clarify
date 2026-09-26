"""
Phase 3: Clarification engine.

Before generating SQL, checks whether a question is ambiguous given the
schema (unclear metric, time range, entity, or aggregation). If so, returns
a clarifying question instead of guessing. The user's answer is merged into
the original question before SQL generation proceeds.
"""
import json
import re

from llm_client import ask_llm

CLARIFY_SYSTEM_PROMPT = (
    "You are an assistant that checks whether a natural language question "
    "can be answered unambiguously against a given database schema. "
    "Look specifically for: "
    "1) Metric ambiguity (e.g. 'top' -- by what measure?), "
    "2) Time range ambiguity (e.g. 'recent' -- what period?), "
    "3) Entity ambiguity (a term could map to more than one table/column), "
    "4) Aggregation ambiguity (sum vs count vs average unclear). "
    "Respond with ONLY a JSON object, no markdown, no explanation, in this "
    "exact shape: "
    '{"ambiguous": true or false, "reason": "short reason or empty string", '
    '"clarifying_question": "a single clear follow-up question, or empty string", '
    '"options": ["short option 1", "short option 2"] or []}'
)


def clean_json(raw_output: str) -> str:
    """Strip markdown code fences if the model adds them despite instructions."""
    cleaned = re.sub(r"^```json\s*|^```\s*|```$", "", raw_output.strip(), flags=re.MULTILINE)
    return cleaned.strip()


def check_ambiguity(schema: str, question: str) -> dict:
    """
    Returns a dict:
      {"ambiguous": bool, "reason": str, "clarifying_question": str, "options": list}
    Falls back to {"ambiguous": False, ...} if the model's response can't be
    parsed, so a parsing hiccup never blocks the user from getting an answer.
    """
    prompt = f"Database schema:\n{schema}\n\nQuestion: {question}\n\nJSON:"

    raw = ask_llm(prompt, system=CLARIFY_SYSTEM_PROMPT)

    try:
        parsed = json.loads(clean_json(raw))
        return {
            "ambiguous": bool(parsed.get("ambiguous", False)),
            "reason": parsed.get("reason", ""),
            "clarifying_question": parsed.get("clarifying_question", ""),
            "options": parsed.get("options", []),
        }
    except (json.JSONDecodeError, AttributeError):
        # If the model didn't return valid JSON, fail safe: treat as
        # unambiguous rather than blocking the user.
        return {"ambiguous": False, "reason": "", "clarifying_question": "", "options": []}


def merge_clarification(question: str, clarifying_question: str, answer: str) -> str:
    """Fold the user's clarification answer into the original question."""
    return (
        f"{question}\n"
        f"(Clarification -- \"{clarifying_question}\": {answer})"
    )