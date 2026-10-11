# Baseline specification

Status: specification written, not run. No record exists yet.

This folder holds the Playwright MCP baseline for the comparison in [current recommendations](../recommendations.md). The summary and the experiment are in [segment 01](../segments/01-llm-web-operation/README.md). Registry design and mock tests are in [segment 07](../segments/07-rust-chrome-controller/README.md).

## Test site and fixtures

- The site is public and stable. It needs no login and has no terms-of-service bar on automation.
- It has (a) a search with a results list, (b) a sortable or filterable table or virtual list, (c) a file download and (d) an SPA route change.
- Record the URL, the date and a page hash.
- Self-hosted fixture copies cover three negative scenarios: a delayed control, a DOM replacement and continuous network activity.

## Tasks

| Task | Goal |
|---|---|
| T1 | Search and open an item |
| T2 | Filter a table and read N values |
| T3 | Trigger a download and verify the file |

Each task has preconditions, params, an exact expected result and forbidden actions. The expected result is a set of values, or a file SHA-256 and a row count.

`fixtures/<task>.json` holds the params and the expected result. Never commit downloaded files. Commit only their SHA-256 and row count.

## Metrics

| Kind | Metric |
|---|---|
| Deciding | Complete-task success |
| Deciding | Correct data (exact matches divided by total) |
| Deciding | Recoveries (human interventions plus re-observations after a stale target) |
| Deciding | Wrong-action count |
| Supporting | Step count |
| Supporting | Snapshot bytes and estimated tokens |
| Supporting | Wall time from action to verified result (warm and cold reported separately) |
| Supporting | Screenshot count |
| Supporting | Maintenance notes |

## Runs

Do 5 runs per task per condition (warm and cold), and at least 3. Report all runs. Use the same model and the same Playwright MCP version for every run.

## Record schema

Records go in `runs/YYYYMMDD-<task>-<n>.jsonl`. `<task>` is `T1`, `T2` or `T3`, or `N1` (delayed control), `N2` (DOM replacement) or `N3` (continuous network activity) for the self-hosted negative fixtures. Each file has step lines and one summary line. Comparison runs made with the Rust controller use the same lines, add `controller` (crate name and version) to `versions`, and end the file name with `-rust.jsonl`.

Step line:

```json
{"run_id": "", "task": "", "step": 0, "tool": "", "target_role": "", "target_name": "", "snapshot_bytes": 0, "snapshot_tokens_est": 0, "elapsed_ms": 0, "outcome": "", "error_kind": ""}
```

Summary line:

```json
{"run_id": "", "success": false, "data_matches": 0, "recoveries": 0, "wrong_actions": 0, "steps": 0, "total_ms": 0, "versions": {"playwright_mcp": "", "browser": "", "model": ""}, "site_hash": ""}
```

Never record cookies, tokens, profile paths, full snapshot text, screenshots of non-fixture pages, personal names from live sites, local usernames or home paths.

## Gate

Both gate rules live in [current recommendations](../recommendations.md). Gate 1 reads the records in `runs/` and decides whether Rust work starts. Gate 2 compares a Rust run, in the same record format and on identical fixtures, with the baseline. Gate decisions are recorded in `docs/baseline/gates/`.
