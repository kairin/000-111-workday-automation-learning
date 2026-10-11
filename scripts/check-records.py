#!/usr/bin/env python3
"""Validate baseline run records against the schema in docs/baseline/README.md.

Usage: python3 scripts/check-records.py [runs_dir]

Checks every *.jsonl file in runs_dir (default docs/baseline/runs):
file name, JSON syntax, exact keys per line type, value types, and the
file layout (one or more step lines, then exactly one summary line).
Prints problems as `file:line: message`, then `checked N files, M problems`.
Exit code 0 if no problems, 1 otherwise.
"""
import json
import re
import sys
from pathlib import Path

NAME = re.compile(r"^\d{8}-(T[123]|N[123])-\d+(-rust)?\.jsonl$")

STEP = {"run_id": str, "task": str, "step": int, "tool": str, "target_role": str,
        "target_name": str, "snapshot_bytes": int, "snapshot_tokens_est": int,
        "elapsed_ms": int, "outcome": str, "error_kind": str}
SUMMARY = {"run_id": str, "success": bool, "data_matches": int, "recoveries": int,
           "wrong_actions": int, "steps": int, "total_ms": int, "versions": dict,
           "site_hash": str}
VERSIONS = ("playwright_mcp", "browser", "model")


def type_ok(value, want):
    # bool is a subclass of int in Python; do not accept it as a count.
    if want is int:
        return isinstance(value, int) and not isinstance(value, bool)
    return isinstance(value, want)


def check_line(obj, schema, rust, report):
    keys = set(obj)
    for k in sorted(set(schema) - keys):
        report(f"missing key '{k}'")
    for k in sorted(keys - set(schema)):
        report(f"unknown key '{k}'")
    for k, want in schema.items():
        if k in obj and not type_ok(obj[k], want):
            report(f"'{k}' should be {want.__name__}, got {type(obj[k]).__name__}")
    if schema is SUMMARY and isinstance(obj.get("versions"), dict):
        need = VERSIONS + (("controller",) if rust else ())
        for k in need:
            v = obj["versions"].get(k)
            if not isinstance(v, str):
                report(f"versions.{k} missing or not a string")


def check_file(path):
    problems = []
    name = path.name
    if not NAME.match(name):
        problems.append(f"{name}:0: bad file name (want YYYYMMDD-<T1|T2|T3|N1|N2|N3>-<n>[-rust].jsonl)")
    rust = name.endswith("-rust.jsonl")
    kinds = []  # "step" or "summary" per classified line
    for no, line in enumerate(path.read_text().splitlines(), 1):
        def report(msg, no=no):
            problems.append(f"{name}:{no}: {msg}")
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            report(f"invalid JSON ({e.msg})")
            continue
        if not isinstance(obj, dict):
            report("line is not a JSON object")
        elif "success" in obj:
            kinds.append("summary")
            check_line(obj, SUMMARY, rust, report)
        elif "step" in obj:
            kinds.append("step")
            check_line(obj, STEP, rust, report)
        else:
            report("neither a step line (has 'step') nor a summary line (has 'success')")
    if kinds.count("summary") != 1:
        problems.append(f"{name}:0: expected exactly one summary line, found {kinds.count('summary')}")
    elif kinds[-1] != "summary":
        problems.append(f"{name}:0: summary line must come last")
    if "step" not in kinds:
        problems.append(f"{name}:0: no step lines")
    return problems


def main():
    default = Path(__file__).resolve().parent.parent / "docs/baseline/runs"
    runs = Path(sys.argv[1]) if len(sys.argv) > 1 else default
    files = sorted(runs.glob("*.jsonl"))
    problems = [p for f in files for p in check_file(f)]
    if problems:
        print("\n".join(problems))
    print(f"checked {len(files)} files, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
