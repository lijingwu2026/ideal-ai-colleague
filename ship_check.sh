#!/usr/bin/env bash
# ship_check.sh — publish precondition for ideal-ai-colleague. Exit 0 = safe to publish, 1 = blocked.
# Optional: SHIPCHECK_IDENTITY='term1|term2' greps for private identity terms you must not ship.
set -u
cd "$(dirname "$0")" || exit 2
fail=0
ok()  { printf '  ok   %s\n' "$1"; }
bad() { printf '  FAIL %s\n' "$1"; fail=1; }

echo "[1/5] required files"
for f in README.md CLAUDE.md output-styles/colleague-voice.md ADOPT.md AGENTS.md EVIDENCE.md TESTING.md \
         abtest.py examples/changing_values.py LICENSE .claude-plugin/marketplace.json .claude-plugin/plugin.json; do
  [ -f "$f" ] && ok "$f" || bad "missing $f"
done

echo "[2/5] code compiles"
if python3 -m py_compile abtest.py examples/changing_values.py 2>/dev/null; then ok "python"; else bad "python does not compile"; fi
rm -rf __pycache__ examples/__pycache__

echo "[3/5] secrets (gitleaks, fail-closed)"
if command -v gitleaks >/dev/null 2>&1; then
  if gitleaks dir . >/dev/null 2>&1; then ok "no leaks"; else bad "gitleaks found leaks (run: gitleaks dir . -v)"; fi
else
  bad "gitleaks not installed — cannot pass without it"
fi

echo "[4/5] local paths and wiki links"
if grep -rnI --exclude=ship_check.sh -E '/Users/|/home/|\[\[' . ; then bad "local path or wiki link found"; else ok "none"; fi

echo "[5/5] identity terms and placeholders"
if [ -n "${SHIPCHECK_IDENTITY:-}" ]; then
  if grep -rnIiE --exclude=ship_check.sh "$SHIPCHECK_IDENTITY" . ; then bad "identity term found"; else ok "no identity terms"; fi
else
  echo "  skip identity grep (SHIPCHECK_IDENTITY unset)"
fi
if grep -rnI --exclude=ship_check.sh -E '<raw URL>|\[Lijing: why\?\]|RERUN_|\[Opus re-run' . ; then bad "unfilled placeholder"; else ok "no placeholders"; fi

[ "$fail" -eq 0 ] && echo "SHIP-CHECK PASS" || echo "SHIP-CHECK BLOCKED"
exit "$fail"
