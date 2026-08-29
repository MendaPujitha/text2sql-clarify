"""
Phase 0: Environment verification.

Run this after completing README setup steps to confirm everything
is wired up correctly before moving to Phase 1.

    python src/check_setup.py
"""
import os
import sqlite3
import sys

from dotenv import load_dotenv

load_dotenv()

CHECK = "  [OK] "
FAIL = "  [FAIL] "


def check_python_version() -> bool:
    ok = sys.version_info >= (3, 10)
    print(f"{CHECK if ok else FAIL}Python version: {sys.version.split()[0]}")
    return ok


def check_dependencies() -> bool:
    required = ["requests", "dotenv", "sqlglot"]
    all_ok = True
    for pkg in required:
        try:
            __import__(pkg)
            print(f"{CHECK}Package available: {pkg}")
        except ImportError:
            print(f"{FAIL}Missing package: {pkg} (run: pip install -r requirements.txt)")
            all_ok = False
    return all_ok


def check_api_key() -> bool:
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    if openrouter_key and openrouter_key != "your_openrouter_api_key_here":
        print(f"{CHECK}OPENROUTER_API_KEY is set")
        return True
    if groq_key and groq_key != "your_groq_api_key_here":
        print(f"{CHECK}GROQ_API_KEY is set")
        return True
    if gemini_key and gemini_key != "your_gemini_api_key_here":
        print(f"{CHECK}GEMINI_API_KEY is set")
        return True
    print(f"{FAIL}No valid API key found in .env (or set up Ollama locally instead)")
    return False


def check_database() -> bool:
    db_path = os.getenv("DB_PATH", "data/chinook.db")
    if not os.path.exists(db_path):
        print(f"{FAIL}Database not found at {db_path} (see README step 6)")
        return False
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        print(f"{CHECK}Database connected: {db_path} ({len(tables)} tables found)")
        return len(tables) > 0
    except sqlite3.Error as e:
        print(f"{FAIL}Database error: {e}")
        return False


def main():
    print("Checking Phase 0 setup...\n")
    results = [
        check_python_version(),
        check_dependencies(),
        check_api_key(),
        check_database(),
    ]
    print()
    if all(results):
        print("All checks passed. You're ready for Phase 1.")
    else:
        print("Some checks failed. Fix the items above before continuing.")
        sys.exit(1)


if __name__ == "__main__":
    main()
