# ADOPT.md — instructions for an AI agent

You are helping your user adopt parts of this repository into their own setup. The repository holds a
work agreement (`CLAUDE.md`) and communication requirements (`output-styles/colleague-voice.md`) that make an
AI agent behave like a reliable colleague. Follow these steps in order.

## 1. Read before proposing

1. Read the user's current `CLAUDE.md` (project root, and `~/.claude/CLAUDE.md` if it exists) and any
   active output style (`.claude/output-styles/`, `outputStyle` in settings).
2. Read this repository's `CLAUDE.md`, `output-styles/colleague-voice.md` and `EVIDENCE.md`.
3. Ask the user, in one question, what goes wrong with their agent today, unless they already told you.

## 2. Compare section by section

For each section of this repository's files, decide whether the user's setup already covers it, covers it
partly, or lacks it. Do not propose a line the user's files already cover in other words.

## 3. Propose, do not write

Present a short table of proposals. For each one give:

- the line or section to add, adapted to the user's context;
- **why it fits**: a failure the user described, or a gap in their coverage (for example, no reporting rules);
- **evidence**: "tested" with the result from `EVIDENCE.md`, or "untested — adopted from daily use".

Then show the exact diff and **wait for the user's approval before editing any file**. Never overwrite a file
wholesale; merge into what exists.

## 4. Flag personal preferences

Some lines are one person's working preferences, not general rules. Flag them and let the user decide:

- **"Commit finished changes … directly on `main`, then push"** — suits a solo repository; teams usually need
  branches and reviews.
- **"Write system files in English"** — only matters in multilingual setups.
- The example 「剩下的task？」 in "Confirm before assuming" is a real terse message in Chinese; replace it with a
  terse message typical for the user.

## 5. Adapt names and links

- The files say "the user". Keep that, or use the user's name if they prefer.
- `CLAUDE.md` links to `.claude/output-styles/colleague-voice.md`. If the user installs the output style as a
  plugin, it is active as `ideal-ai-colleague:colleague-voice` and the links are references only.

## 6. Offer one check

After the user approves and you apply the changes, offer one cheap before/after check with `abtest.py`
(see `TESTING.md`) on the behaviour the user cares about most. Report the result honestly, including
"no measurable difference".
