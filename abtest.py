#!/usr/bin/env python3
"""Before/after test for one instruction: does adding it change what your agent does?

Runs the same scenario N times WITHOUT and N times WITH your instruction file, each run in a
fresh throwaway folder, and prints a pass count per arm. Standard library only.

  python3 abtest.py examples/changing_values.py --with CLAUDE.md --runs 3
  python3 abtest.py my_scenario.py --with my-line.md --as output-style --runs 3

A scenario is a small Python file defining:
  PROMPT              the message sent to the agent
  setup(folder)       write the starting files into `folder`
  grade(folder, reply) -> ("PASS" | "FAIL" | "INVALID", reason)
                      INVALID = the run did not do the task at all, so it counts in neither direction

--as claude-md      (default) the file is copied to the folder's CLAUDE.md in the WITH arm
--as output-style   the file is copied to .claude/output-styles/ and switched on in the WITH arm

Safety: the agent runs with your own OS user's privileges. The temp folder is its working directory,
not a sandbox, and it has the Bash tool. Only run scenarios (and their PROMPT) you trust as much as any
script you would execute yourself. Needs the `claude` CLI, logged in. Runs cost real model usage.
"""
import argparse
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def load_scenario(path):
    spec = importlib.util.spec_from_file_location("scenario", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for name in ("PROMPT", "setup", "grade"):
        if not hasattr(mod, name):
            sys.exit(f"{path} must define {name}")
    return mod


def install(folder, instruction, kind):
    if kind == "claude-md":
        shutil.copy(instruction, folder / "CLAUDE.md")
        return
    text = Path(instruction).read_text()
    m = re.search(r"^name:\s*(.+)$", text, re.M)
    name = m.group(1).strip() if m else Path(instruction).stem
    styles = folder / ".claude" / "output-styles"
    styles.mkdir(parents=True, exist_ok=True)
    shutil.copy(instruction, styles / Path(instruction).name)
    (folder / ".claude" / "settings.local.json").write_text(json.dumps({"outputStyle": name}))


def run_once(scenario, instruction, kind, arm, timeout, model):
    folder = Path(tempfile.mkdtemp(prefix=f"abtest-{arm}-"))
    try:
        scenario.setup(folder)
        if arm == "with":
            install(folder, instruction, kind)
        cmd = ["claude", "-p", scenario.PROMPT, "--output-format", "json",
               "--permission-mode", "acceptEdits",
               "--setting-sources", "project,local",   # ignore your personal ~/.claude settings
               "--strict-mcp-config",                  # no MCP servers
               "--tools", "Read,Write,Edit,Bash,Glob,Grep"]  # enough to do a task; keeps each run cheap
        if model:
            cmd += ["--model", model]
        try:
            out = subprocess.run(cmd, cwd=folder, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return "INVALID", f"timed out after {timeout}s", folder
        try:
            data = json.loads(out.stdout)
        except json.JSONDecodeError:
            return "INVALID", f"no JSON from claude: {(out.stderr or out.stdout)[:200]}", folder
        verdict, reason = scenario.grade(folder, data.get("result", ""))
        if verdict not in ("PASS", "FAIL", "INVALID"):
            return "INVALID", f"grade() returned unexpected verdict {verdict!r}", folder
        models = ",".join(data.get("modelUsage", {})) or "?"
        return verdict, f"{reason}  (model: {models})", folder
    except Exception as e:  # a broken scenario should not stop the other runs
        return "INVALID", f"{type(e).__name__}: {e}", folder


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("scenario")
    ap.add_argument("--with", dest="instruction", required=True, help="instruction file for the WITH arm")
    ap.add_argument("--as", dest="kind", choices=["claude-md", "output-style"], default="claude-md")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--model", help="pin the model; results can differ between models, so say which one you tested")
    ap.add_argument("--keep", action="store_true", help="keep the temp folders for inspection")
    a = ap.parse_args()

    if not Path(a.instruction).is_file():
        sys.exit(f"--with file not found: {a.instruction}")
    if a.runs < 1:
        sys.exit("--runs must be at least 1")
    scenario = load_scenario(a.scenario)
    results = {"without": [], "with": []}
    for arm in results:
        for i in range(a.runs):
            verdict, reason, folder = run_once(scenario, a.instruction, a.kind, arm, a.timeout, a.model)
            results[arm].append(verdict)
            print(f"{arm:>7} run {i + 1}: {verdict:<7} {reason}" + (f"  [{folder}]" if a.keep else ""))
            if not a.keep:
                shutil.rmtree(folder, ignore_errors=True)

    print("\narm      pass/valid  (invalid)")
    for arm, vs in results.items():
        valid = [v for v in vs if v != "INVALID"]
        print(f"{arm:<8} {valid.count('PASS')}/{len(valid):<9} ({len(vs) - len(valid)})")
    print("\nSmall n: 3/3 is consistent with a true pass rate as low as ~37% (one-sided 95% bound). "
          "Same score in both arms = the instruction made no measurable difference here.")


if __name__ == "__main__":
    main()
