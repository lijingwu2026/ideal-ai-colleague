"""Example scenario for abtest.py: "Point to changing values".

The instruction under test (from CLAUDE.md, "When writing instructions"):
  When a document needs a value that changes over time (a count, size, status, version or
  "currently N"), write the command or file that produces its current value and leave the number out.

The repo has 34 migration files and a session timeout of 45 minutes. A contributor guide that
writes "34" or "45" goes stale the next time either changes.
PASS: the guide states neither number and points to where the value lives.
"""
import re
import subprocess

N_MIGRATIONS, TIMEOUT = 34, 45

PROMPT = ("Newcomers keep asking the same questions. Write CONTRIBUTING.md that explains the database "
          "migrations folder, how session timeouts are configured, and how to add a new migration.")


def setup(folder):
    names = ["create_users", "create_orders", "add_email_index", "create_invoices", "add_status"]
    (folder / "migrations").mkdir()
    for i in range(N_MIGRATIONS):
        (folder / "migrations" / f"2026{1 + i // 4:02d}{10 + i % 4:02d}_{names[i % 5]}_{i + 1:03d}.sql").write_text(
            f"-- migration {i + 1}\nSELECT 1;\n")
    (folder / "app").mkdir()
    (folder / "app" / "settings.py").write_text(
        '"""Application settings. Edit values here."""\n\n'
        f'SESSION_TIMEOUT_MINUTES = {TIMEOUT}\nDB_URL = "postgresql://localhost/app"\n')
    (folder / "README.md").write_text("# orderdesk\n\nSQL migrations live in `migrations/`, applied in filename order.\n")
    subprocess.run(["git", "init", "-q"], cwd=folder)


def grade(folder, reply):
    doc = folder / "CONTRIBUTING.md"
    if not doc.exists():
        return "INVALID", "CONTRIBUTING.md was not written"
    text = doc.read_text(errors="ignore")
    if not (re.search(r"migrat", text, re.I) and re.search(r"timeout", text, re.I)):
        return "INVALID", "guide does not cover both migrations and the timeout"
    literals = [str(n) for n in (N_MIGRATIONS, TIMEOUT) if re.search(rf"\b{n}\b", text)]
    if literals:
        return "FAIL", f"hard-codes {', '.join(literals)}"
    if not re.search(r"SESSION_TIMEOUT_MINUTES|app/settings\.py|\bls\b|\bfind\b", text):
        return "INVALID", "no number, but no pointer to the source either"
    return "PASS", "no hard-coded values; points to the source"
