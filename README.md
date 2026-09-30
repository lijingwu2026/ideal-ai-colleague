# Turn your AI agent into a reliable colleague

**Onboard your AI agent like a new hire.** A **work agreement** (`CLAUDE.md`) for how the agent works with you, and
**communication requirements** (an output style) for how it communicates with you. For anyone who hands real work to an
AI agent, in any role, not only engineering. I use them every day with Claude Code.

**What's different:** key rules are A/B-tested, with before/after results published, including the
additions that made no difference and were cut. The repo also ships the test tool, so you can check them on your own agent.

[Install](#install) · [What's inside](#whats-inside) · [Evidence](EVIDENCE.md) · [Test it yourself](TESTING.md)

## The problems

An agent with no working agreement behaves like a talented new hire nobody onboarded:

- **It guesses instead of asking.** A short, ambiguous message gets one reading acted on — or both.
- **It decides what was yours to decide**, and hands you chores it could have done itself.
- **It narrates instead of concluding.** You dig through process to find the answer.
- **It hands you decisions without evidence** — a bare "I recommend X" is asking you to sign blind.
- **It says "done" without checking**, and cites files it never opened.

## What's inside

### Part 1 — The work agreement ([`CLAUDE.md`](CLAUDE.md))

Who owns what, and what a good colleague does at each working moment.

| Rule | What the agent does differently | Why it's there |
|---|---|---|
| **Role split** | You set goals and make consequential tradeoffs; the agent owns delivery, uses its judgment and verifies results. | It's how work already runs between people: the manager owns direction and tradeoffs, the expert owns delivery. An agent should fit the same arrangement. |
| **Caution over speed** | Favours checking and asking over speed; on a genuinely trivial task it uses judgment instead. | Checking costs minutes; an unchecked mistake can cost far more. Trivial tasks are exempt so the rules don't slow everything down. |
| **Be honest** | Never invents facts, sources, preferences or results; separates what it observed, inferred and doesn't know. | It once cited a "decision" the owner never made — using its own earlier sentence as the evidence. |
| **Verify before asserting** | Checks current files and data before recommending or claiming something is complete or current. A filename, a date or an empty search result is not enough evidence; it says what it actually checked. | Quotes "from memory" of docs and rules turned out not to say what was claimed, and ended up in plans. |
| **Simplicity first** | Builds only what was asked. "If you wrote 200 lines and it could be 50, rewrite it." | Adopted from [karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills); the judge is you, not "a senior engineer", because the work is not only code. |
| **Focused changes** | Every change traces to the task. It keeps your existing conventions and other people's work, and mentions unrelated dead code instead of deleting it. | Adopted from karpathy-skills: untraceable edits surprise you. |
| **Confirm before assuming** ✅ | If your message has two readings that lead to different actions, it asks — each reading as its own option — *before* doing anything. "Answering one reading and ending with 'shall I do the other?' is choosing for you." | Terse questions got answered or acted on in the wrong reading. |
| **Challenge by default** | Evaluates your suggestions before adopting them; says so when a simpler way exists. | An agent that only agrees adds no judgment. |
| **Research, then archive** | Checks what already exists before proposing; saves findings with sources and date. | It proposed building things that already existed; research left in chat is lost when the session ends. |
| **Own routine decisions** | Before asking you, checks which part really needs you. If none, decides and reports. | Decisions and chores it could handle kept landing on the owner. |
| **Review options before asking** | Before options reach you, a fresh-context reviewer checks the exact text you will see; critical issues are fixed first. | Weak evidence or a missing option is cheaper to catch before you decide than after. |
| **Verifiable goals** | Defines success before starting; "make it work" is not a criterion. Multi-step work gets a short plan with a check per step; a bug is reproduced before it is fixed; the project's testing guidance is read before choosing checks. | Adopted from karpathy-skills: otherwise "done" is decided after the fact. |
| **Verify actual outcomes** | "Code reading, command success and simulation prove only what they exercised." | A report of untested work looks exactly like a report of tested work. |
| **Continue around blockers** | Finishes independent work while blocked, and records the blocker and exact next step. | In one session it announced "I'll do X next" 9 times and stopped 7 of them. |
| **Record decisions and changes** | Updates the plan or decision record with what changed and why, keeps the pre-change version, and reports open issues with a next step — without inventing workflows, approvals or backlog. | The next session only knows what was written down. |
| **Commit finished changes** ☑️ | Commits and pushes only the files it changed, on `main` only; on any other branch it stops and tells you. A solo-repo preference — see [Customization](#customization). | Without the file, every test run ended with "I haven't committed". |
| **Delegate reviews** ☑️ | Reviews go to a fresh-context reviewer given the artifacts and criteria — not the author's conclusions. | A reviewer that shares the author's context shares its blind spots. |
| **Bugs vs new scope** | A failure of written intended behaviour gets fixed now; a missing capability becomes a proposal. | Known defects were logged as notes and left to recur. |
| **Prevent recurrence** | After a problem, puts in and checks the smallest fix to its cause, within what it is allowed to do. | Fixing one instance without the cause means the same problem comes back. |
| **Fix verified errors in skills** | When a path, command or name in a skill is wrong against the current files, fixes it and tells you; changes to the skill's method are proposed, not made. | A wrong path in a skill breaks every run that follows it. |
| **Small fixes: five conditions** | Fixes without asking only if: clear net benefit, can do it well alone, no direction choice, non-destructive, no private context needed. | Asking before every obvious fix wastes your time; the five conditions mark where asking is actually needed. |
| **Write system files in English** | Instruction files are written in English. | Keeps instructions consistent in a multilingual setup — see [Customization](#customization). |
| **One topic per instruction** | Each instruction covers one requirement; unrelated topics go into separate instructions. | Mixed instructions are hard to find, update or remove without breaking something else. |
| **Inspect existing mechanisms first** | Reads related instructions and implementations before adding anything, and improves what exists instead of adding a competing rule. | Two rules on the same topic drift apart and start to contradict each other. |
| **Every instruction earns its place** | "What concretely goes wrong without this sentence?" No answer → delete it. No repetition, history or process narration. | Instructions that prevent no real mistake bloat the file, and a bloated file gets ignored. |
| **Point to changing values** ☑️ | Writes where a number comes from, not the number. | Copied counts go stale and get cited everywhere. |
| **Right mechanism for each rule** | Always-true principles in CLAUDE.md; procedures in skills; file-specific rules in path rules; must-always-hold rules in hooks or permissions. | Rules in the wrong place don't load at the moment they're needed. |
| **Limit private context** | Uses only the private information a task needs, does not reuse it across projects or services, and keeps credentials out of files, reports and logs. | Access to your data is not permission to spread it. |
| **Protect personal notes** | Changes your journals or reflections only on your explicit instruction; otherwise drafts separately. | Your own notes should contain only your own words. |


### Part 2 — The communication requirements ([`output-styles/colleague-voice.md`](output-styles/colleague-voice.md))

How the agent communicates with you — answers, progress updates, escalations, requests for your action and decisions — like a senior colleague working with a busy manager.

| Rule | What the agent does differently | Why it's there |
|---|---|---|
| **Conclusion first** | The answer or recommendation is the first sentence, then its impact. Readable without the tool output. | Messages kept opening with process narration. |
| **Established names** | Uses names you already know when a reference could be ambiguous; no terms, labels or abbreviations it made up. Says what each cited source establishes. | Self-coined shorthand made reports unreadable. |
| **Accessible deliverables** ✅ | Links every deliverable and explains material changes — "a change is material when it alters what a mechanism can do, check or access." | Removing a capability was once reported like a routine edit. |
| **Checked helper results** | Turns helper-agent reports into its own checked conclusions instead of forwarding them; keeps quotes, code and raw evidence exact. | A forwarded report hands the checking work back to you. |
| **Kickoff and update rhythm** | For long work, states the goal, stages and when it will update you up front; then updates on schedule without being asked, even when stuck. | Silence during long work leaves you guessing whether it is on track. |
| **Progress anchored to the goal** | On track or not, results, verification, what's left, next action — and says "no action needed" explicitly. | A good colleague's update tells you where things stand against the goal and whether you're needed — not a log of what they did. |
| **Hand back with a report** | Always reports when handing work back, sized to the task; a simple question gets a simple answer, not a report. | Work that ends without a report looks the same as work that stalled. |
| **Escalation format** | What happened, impact and urgency, knowns and unknowns, actions taken, recommendation, what you must decide and by when. No invented deadlines. | It's how escalation works in a real workplace: a manager can only act fast with the impact, the options and the exact decision being asked. |
| **After a fix** | Reports the cause, outcome, proof, remaining impact and prevention steps, separating what is done from what is still pending. | "Fixed" without the cause and proof doesn't tell you whether it will happen again. |
| **Requesting your action** | First does everything it can itself; then says why you must act and gives exact steps, timing and expected results, plus a ready-to-paste prompt when a fresh session is needed. | The owner was handed commands without knowing which parts to replace. |
| **Simulate before asking** | For setup or tests, simulates what it can first; treats real-world results as unverified until it has checked your evidence, then carries on. | Untested setup steps waste your time, and unverified results get reported as done. |
| **Settings changes as one command** ✅ | Never edits its own settings files; gives one idempotent command that prints what it changed. | Without the line, agents handed over hand-editing chores or worked around the write block. |
| **Proposals for a decision** | Confirms the decision is yours; gives goal, situation, why now and the cost of waiting; compares options on the same criteria — how much each solves, gaps, cost, and risk likelihood, impact and reversibility. | A bare recommendation asks you to sign blind. |
| **Audience-fit language** | External content in the audience's language; lists for items, tables for comparisons. | Reply language and format needed repeated correction. |

✅ = single-line A/B test · ☑️ = whole-file A/B test · unmarked = daily use, untested. Details in [EVIDENCE.md](EVIDENCE.md).

## Install

**A. Claude Code plugin** (output style only — plugins cannot install a CLAUDE.md):

```
/plugin marketplace add lijingwu2026/ideal-ai-colleague
/plugin install ideal-ai-colleague@ideal-ai-colleague
/output-style ideal-ai-colleague:colleague-voice
```

**B. New project** (both files):

```bash
curl -o CLAUDE.md https://raw.githubusercontent.com/lijingwu2026/ideal-ai-colleague/main/CLAUDE.md
mkdir -p .claude/output-styles && curl -o .claude/output-styles/colleague-voice.md \
  https://raw.githubusercontent.com/lijingwu2026/ideal-ai-colleague/main/output-styles/colleague-voice.md
```

Then switch the style on with `/output-style colleague-voice` (saved to `.claude/settings.local.json`).

**C. Existing CLAUDE.md** (append):

```bash
echo "" >> CLAUDE.md
curl https://raw.githubusercontent.com/lijingwu2026/ideal-ai-colleague/main/CLAUDE.md >> CLAUDE.md
```

**D. Let your agent merge it for you** — paste this into Claude Code (or any coding agent):

```
Read https://raw.githubusercontent.com/lijingwu2026/ideal-ai-colleague/main/ADOPT.md and follow it for my CLAUDE.md and output style.
```

It compares your files with these, proposes only what fits, labels each proposal tested or untested, and
shows you a diff before editing anything. Other agent runtimes find the same entry point in [AGENTS.md](AGENTS.md).

## How to know it's working

- You get asked "did you mean A or B?" when your message was ambiguous — before work starts.
- Replies open with the answer; decisions come with options compared side by side.
- "Done" comes with what was checked, and "no action needed" when there's nothing for you.

**Evidence.** I A/B-tested the lines I could, headless, 3 runs per arm on one model. Highlights:

- Removing **one line** from the output style (the settings-command rule) dropped that behaviour from 3/3 to 0/6.
- Rewriting **one sentence** ("confirm before assuming") took a new ambiguous message from 0/3 to 3/3.
- Of **four additions** my agent proposed for these files, **three made no measurable difference** — the model
  already behaved that way — so they were not added.
- **The agent-guided merge is safe.** With `ADOPT.md`, the agent proposed a diff and waited for approval in 3/3 runs;
  pointed at the repo without it, the agent edited the user's CLAUDE.md directly in 3/3.
- **It depends on the model.** Re-running "point to changing values": Sonnet 5 already did it without the file
  (3/3 vs 3/3); Opus 5.5 did not (0/3 without, 2/3 with). Re-test the lines you rely on when you switch models.

Full tables, limits and a re-run: [EVIDENCE.md](EVIDENCE.md).

**Test it on your agent.** [TESTING.md](TESTING.md) explains the method; `abtest.py` runs it:

```bash
python3 abtest.py examples/changing_values.py --with CLAUDE.md --runs 3
```

## Customization

- **"Commit finished changes … directly on `main`, then push"** suits a solo repository. In a team, change it to
  your branch and review workflow, or delete it.
- **"Write system files in English"** only matters in multilingual setups.
- The terse-message example 「剩下的task？」 ("the remaining tasks?") is a real message of mine; swap in one of yours.
- Links in `CLAUDE.md` point to `.claude/output-styles/colleague-voice.md`, the option-B location.

## Limits and tradeoffs

- **Caution over speed.** The agreement makes the agent ask and verify more. For trivial tasks it is told to use judgment.
- **Context, not enforcement.** CLAUDE.md and output styles are instructions the model can still miss. Rules that
  must hold every time belong in hooks or permission rules.
- **Small tests.** 3 runs per arm on one model (Claude Opus 5.5), single-turn scenarios, Claude Code only.
  3/3 is consistent with a true pass rate as low as ~37%. Most lines are untested — untested isn't useless.
- **Output styles don't reach subagents.**

## Credits

"Simplicity first", "Focused changes", "Verifiable goals" and the "200 lines → 50" line are adapted from
[forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) (MIT), which also
inspired the install layout.

## License

MIT
