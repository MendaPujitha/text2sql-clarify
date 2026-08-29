# Text-to-SQL with Clarification Engine

A natural-language-to-SQL system that detects ambiguous questions and asks
clarifying follow-ups before generating a query — instead of silently
guessing wrong.

## Project Status
- [x] Phase 0 — Environment setup
- [ ] Phase 1 — Basic text-to-SQL
- [ ] Phase 2 — Schema-aware generation + self-correction
- [ ] Phase 3 — Clarification engine
- [ ] Phase 4 — Advanced (retrieval, eval framework, fine-tuning, UI)

## Setup (Phase 0)

1. Clone this repo and enter it:
   ```bash
   git clone https://github.com/<you>/text2sql-clarify.git
   cd text2sql-clarify
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Get a free LLM API key (pick one):
   - **Groq** (recommended — fast, generous free tier): https://console.groq.com/keys
   - **Google AI Studio (Gemini)**: https://aistudio.google.com/apikey
   - Or skip API keys entirely and run **Ollama** locally: https://ollama.com
     then `ollama pull qwen2.5-coder`

5. Copy `.env.example` to `.env` and fill in your key:
   ```bash
   cp .env.example .env
   ```

6. Download the sample database (Chinook — free, SQLite, music-store schema)
   and place it in `data/chinook.db`:
   - https://github.com/lerocha/chinook-database (get `Chinook_Sqlite.sqlite`
     from the Releases page, rename to `chinook.db`)

7. Verify your setup:
   ```bash
   python src/check_setup.py
   ```
   You should see all green checkmarks before moving to Phase 1.

## Project Structure
```
text2sql-clarify/
├── src/
│   ├── check_setup.py     # Phase 0: environment verification
│   ├── schema_linker.py   # Phase 2
│   ├── sql_generator.py   # Phase 1-2
│   ├── clarifier.py       # Phase 3
│   └── executor.py        # Phase 1
├── data/                  # sample DB + eval set (chinook.db goes here)
├── notebooks/             # experimentation
├── tests/
├── eval_results.json
├── requirements.txt
└── README.md
```

## Why this project
Built as a portfolio piece to demonstrate NL understanding, SQL generation,
ambiguity handling, and evaluation methodology — the kind of end-to-end
system design AI Engineer interviews probe for.
