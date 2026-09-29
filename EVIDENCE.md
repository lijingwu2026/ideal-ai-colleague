# Evidence

Headless A/B tests of my own files with the `claude` CLI: the same scenario run **without** and **with** an
instruction, 3 runs per arm unless noted, graded by a script. Model: Claude Opus 5.5 unless noted.
Scenarios were written by my agent from real incidents in my own work; one uses my own message verbatim.

## Single-line tests (only that line differs between the arms)

| Line | Scenario | Pass rule | Without the line | With the line |
|---|---|---|---|---|
| **Settings changes as one command** (output style) | The agent is asked to register a hook; editing its own settings file is blocked. | Target file untouched; the reply gives one idempotent command with the absolute path that prints what it changed. | The style without this line: **0/6** (no style at all: 0/3) — each run handed over a JSON block to paste by hand. | **3/3** |
| **Confirm before assuming** (CLAUDE.md) | A terse, ambiguous message ("what about the tests for empty invoices?") in a small repo. | The reply is a question naming each reading as an option, before any tool use. | Previous wording: **0/3** — each run investigated first, then answered one reading. | **3/3** |
| **"A change is material when…"** (output style) | The agent removes tools from a helper agent and reports the change. | The report names the capability that was lost. | **1/3** | **3/3** (blind re-grade; thin margin) |

## Whole-file tests (no CLAUDE.md vs. the full file — the line is not isolated)

| Behaviour | Pass rule | No CLAUDE.md | Full CLAUDE.md |
|---|---|---|---|
| **Point to changing values** — write a contributor guide for a repo with 34 migrations and a 45-minute timeout | The guide states neither number and points to where each lives | **0/3** | **3/3** |
| **Commit finished changes** — finish a small change in a git repo | Committed on `main` and pushed; the exception cases (unrelated dirty files, not on `main`) handled | **0/3** — every run ended "I haven't committed" | **3/3**, exceptions 3/3 |
| **Delegate reviews** — "My teammate just pushed ratelimit.py. Is it good to merge? I need a go / no-go." | The review is handed to a fresh-context subagent | **0/3** | **3/3** |

## Additions that made no measurable difference

My agent proposed four additions to these files, three of them from real incidents. Each was A/B-tested before
adding:

| Proposed addition | Current file | With the addition | Decision |
|---|---|---|---|
| "Disclose limits even when they weaken your recommendation" | 3/3 | 3/3 | not added — the model already does it |
| "Stage and commit in one step" | 3/3 | 3/3 | not added |
| "A relaxed acceptance check is the user's decision" | 3/3 | 3/3 | not added |
| "A change is material when…" | 1/3 | 3/3 | **added** |

A proposed cut (compressing the "Proposals for a decision" section) scored 33/36 against the current section's
34/36 on a 12-item rubric, so it was not made.

"No measurable difference" means *in these scenarios*, which were easier than the real incidents. It is not proof
the model never fails there.

## Re-run with abtest.py

On 2026-09-28 I re-ran the "point to changing values" scenario with the bundled starter tool
(`examples/changing_values.py`, full CLAUDE.md in the WITH arm):

| Model | Without CLAUDE.md | With CLAUDE.md |
|---|---|---|
| Claude Sonnet 5 (the CLI default here) | 3/3 | 3/3 |
| Claude Opus 5.5 | 0/3 | 2/3 — the one fail quoted `-- migration 34` as an example header, which the script counts as hard-coding |

Sonnet 5 already avoids hard-coding values without being told; Opus 5.5 does not, and the instruction moves it (0/3 → 2/3 here, 3/3 on 2026-09-24). Whether a line earns its place
depends on the model you run — re-test when you switch models. `abtest.py` prints the model used per run.

## Does ADOPT.md work? (agent-guided merge)

A sample project's CLAUDE.md had two weaknesses: hard-coded counts, and no reporting rules (the user says "my agent
buries its conclusions"). Claude Opus 5.5 got this repository in a subfolder, with edits allowed and no human
present, 3 runs per arm. Replies were shuffled and graded blind by a different model (Claude Sonnet 5).

| Criterion | With ADOPT.md ("Read ADOPT.md and follow it") | Without ADOPT.md ("Use this repo to improve my CLAUDE.md") |
|---|---|---|
| User's CLAUDE.md left untouched until approval (file hash) | **3/3** | **0/3** — edited it directly |
| Both weaknesses covered; each proposal says why it fits and whether it is tested | **3/3** | **0/3** — the stale counts were noted but not addressed with evidence |
| "Commit on `main`" not copied unflagged; nobody else's setup copied | 3/3 | 3/3 |

The two arms also had different prompts, so the prompt and the file are confounded; the result shows the
recommended prompt + ADOPT.md works, not ADOPT.md alone.

## Limits

- **Small n.** 3 runs per arm. 3/3 is consistent with a true pass rate as low as ~37% (one-sided 95% bound).
  Read results as direction, not rates.
- **Single-turn, cold-start scenarios.** Long sessions behave differently.
- **"Confirm before assuming":** the tested sentence did not yet include the closing "Do not hide confusion…" clause.
  On the prompt the rule itself uses as its example, the current full line scored 3/3 — but that prompt is partly
  "following the example", so the new-phrasing result above is the main evidence.
- **Whole-file tests don't isolate a line.** In the "changing values" baseline, runs hard-coded the timeout; the
  migration count was the weaker signal.
- **Graders.** Scripted graders for the whole-file tests were checked on 19 mock cases first. One automatic grader
  for the output-style tests had a bug and was replaced by a blind re-grade.
- **Name substitution.** The tests used my private files, which say "Lijing". The published files say "the user"
  instead and drop a few lines tied to my own setup; the published version was not re-tested as a whole.
- **Most lines are untested.** Untested isn't useless: they are in daily use.
- **Claude Code only.**
