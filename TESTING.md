# Testing an instruction on your own agent

An instruction file only helps if it changes what your agent does. You can check that cheaply: run the
same task **without** and **with** the instruction, a few times each, and compare.

## The method

1. **Pick one behaviour** you want to change, e.g. "writes hard-coded numbers into docs".
2. **Write a scenario** where an agent could plausibly get it wrong: a small set of starting files and one
   prompt. Make the task ordinary; do not hint at the rule in the prompt.
3. **Write a mechanical pass rule**: something a script can check (a file exists, a number is absent, a
   command was not run). Decide what counts as INVALID (the agent did not do the task at all) so it does
   not count for either side.
4. **Run both arms**, 3 runs each, in fresh throwaway folders.
5. **Read the result honestly**:
   - WITHOUT fails and WITH passes → the instruction changes behaviour here.
   - Both pass → your agent already does this; the line may not be earning its place.
   - Both fail → the instruction is not working; reword it or move it to a stronger mechanism (a hook,
     a permission rule).
   - 3/3 is not a rate: it is consistent with a true pass rate as low as ~37% (one-sided 95% bound). Treat results as direction,
     not proof.

## The starter tool

`abtest.py` runs the method above with the `claude` CLI. Standard library only.

```bash
# the bundled example: does CLAUDE.md stop the agent hard-coding values in docs?
python3 abtest.py examples/changing_values.py --with CLAUDE.md --runs 3

# test an output style instead
python3 abtest.py my_scenario.py --with output-styles/colleague-voice.md --as output-style
```

A scenario is a Python file with `PROMPT`, `setup(folder)` and `grade(folder, reply)`; copy
`examples/changing_values.py` to start. Each run happens in its own temp folder with
`--permission-mode acceptEdits`, your personal `~/.claude` settings ignored (`--setting-sources project,local`),
no MCP servers, and only the tools `Read, Write, Edit, Bash, Glob, Grep`. Runs cost real model usage.

**Safety:** the agent runs with your own OS user's privileges. The temp folder is its working directory, not a sandbox, and it has the Bash tool. Only run scenarios you trust as much as any script you would run yourself.

## Worked example: re-running my own test

On 2026-09-24 my agent without any CLAUDE.md wrote the timeout value into the guide in 3 of 3 runs, and
with my CLAUDE.md it pointed to `app/settings.py` instead in 3 of 3. Re-running the same scenario with
`abtest.py` on 2026-09-28 gave the result in [EVIDENCE.md](EVIDENCE.md#re-run-with-abtestpy) — which is
the point of the tool: models change, so re-test the lines you rely on.

## Limits

- It tests one scenario, one turn, cold start. Long sessions behave differently.
- Your scenario, your model, your results. Mine are in [EVIDENCE.md](EVIDENCE.md).
- Output styles do not reach subagents; test them on the main agent.
