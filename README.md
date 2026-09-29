# Text-to-SQL with Clarification Engine

A natural-language-to-SQL system that detects ambiguous questions and asks
clarifying follow-ups before generating a query — instead of silently
guessing wrong.

## Project Status
- [x] Phase 0 — Environment setup
- [x] Phase 1 — Basic text-to-SQL
- [x] Phase 2 — Schema-aware generation + self-correction + eval set (100% execution-match accuracy on 8-question eval set)
- [x] Phase 3 — Clarification engine (detects ambiguous questions, asks follow-ups)
- [ ] Phase 4 — Advanced (retrieval, eval framework, fine-tuning, UI)

## Demo: the clarification engine in action

A key design goal of this project is refusing to guess when a question is
genuinely ambiguous. Here's a real run:

**Input:**

`Show me the top customers`

**System response:**

That's a bit ambiguous (the term 'top' isn't defined — it could refer to
total spending, number of invoices, or quantity of items purchased. No
time range is specified either).

Clarifying question: What metric should be used to determine the top customers?
Options: Total spending, Number of invoices, Quantity of items purchased
Your answer: Total spending

**Generated SQL (after clarification):**

```sql
SELECT c.FirstName, c.LastName, SUM(i.Total) AS TotalSpending
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
GROUP BY c.CustomerId, c.FirstName, c.LastName
ORDER BY TotalSpending DESC
LIMIT 5;
```

**Result:**

| FirstName | LastName | TotalSpending |
|---|---|---|
| Helena | Holý | 49.62 |
| Richard | Cunningham | 47.62 |
| Luis | Rojas | 46.62 |
| Ladislav | Kovács | 45.62 |
| Hugh | O'Reilly | 45.62 |

Without the clarification step, a naive text-to-SQL system would have
silently picked one interpretation of "top" — possibly the wrong one for
what the user actually wanted.

## Architecture

```
Question
   |
   v
Schema Linker  --> narrows the full DB schema to relevant tables
   |
   v
Clarifier      --> detects metric/time/entity/aggregation ambiguity
   |                  |
   |                  v
   |            (if ambiguous) ask follow-up, merge answer into question
   v
SQL Generator  --> few-shot prompted, schema-aware
   |
   v
Executor       --> runs SQL, retries with error feedback on failure (max 2x)
   |
   v
Result
```

## Tech stack

- **LLM:** OpenRouter (free-tier models, OpenAI-compatible API)
- **Database:** SQLite (Chinook sample dataset)
- **Language:** Python 3.13
- **Evaluation:** custom execution-match harness (`src/eval.py`)

## Setup

1. Clone this repo and enter it:
   ```bash
   git clone https://github.com/MendaPujitha/text2sql-clarify.git
   cd text2sql-clarify
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\Activate.ps1
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Get a free OpenRouter API key: https://openrouter.ai/keys

5. Copy `.env.example` to `.env` and fill in your key:
   ```bash
   copy .env.example .env
   ```

6. Download the sample database (Chinook — free, SQLite, music-store schema)
   and place it in `data/chinook.db`:
   - https://github.com/lerocha/chinook-database/releases (get
     `Chinook_Sqlite.sqlite`, rename to `chinook.db`)

7. Verify your setup:
   ```bash
   python src/check_setup.py
   ```

## Running the project

```bash
python src/main.py
```

## Running the eval set

```bash
python src/eval.py
```

Runs 8 question/expected-SQL pairs, executes both the generated and
expected queries, and reports execution-match accuracy.

## Project Structure

```
text2sql-clarify/
├── src/
│   ├── check_setup.py     # Phase 0: environment verification
│   ├── llm_client.py      # OpenRouter API client
│   ├── schema_linker.py   # Phase 2: keyword-based schema filtering
│   ├── sql_generator.py   # Phase 1-2: few-shot + self-correction
│   ├── clarifier.py       # Phase 3: ambiguity detection
│   ├── executor.py        # SQL execution against SQLite
│   ├── eval.py            # Phase 2: evaluation harness
│   └── main.py            # CLI entry point
├── data/                  # chinook.db + eval_set.json
├── notebooks/             # experimentation
├── tests/
├── requirements.txt
└── README.md
```

## Limitations & future work

- Schema linking uses keyword matching, not embeddings — works well for
  small schemas but would need a vector-based approach (e.g. sentence
  embeddings + FAISS) to scale to databases with 50+ tables.
- No protection yet against destructive SQL (DROP/DELETE) — a production
  version would add a guardrail layer before execution.
- Currently a CLI; a Streamlit or FastAPI front-end would make it demoable
  without a terminal.

## Why this project
Built as a portfolio piece to demonstrate NL understanding, SQL generation,
ambiguity handling, and evaluation methodology — the kind of end-to-end
system design AI Engineer interviews probe for.
