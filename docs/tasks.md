# Task list

Status: P0 done; P1 not started. This list is the dispatch plan for the proof stages in [current recommendations](recommendations.md). Specifications live elsewhere and are linked, not repeated: the [baseline specification](baseline/README.md), [segment 01](segments/01-llm-web-operation/README.md) (tasks T1–T3), [segment 07](segments/07-rust-chrome-controller/README.md) (registry design, mock tests) and [segment 08](segments/08-workday-data-access/README.md) (sandbox conditions).

## Orchestrator notes

- A task is ready when every ID in `Depends` is done. Dispatch all ready tasks with `Par = y` concurrently; run `Par = n` tasks one at a time.
- Stop and wait at every task with a non-empty `Human` column and at every gate (`G1-01`, `G2-01`). Do not start the next phase before the gate file names `proceed`.
- Never commit secrets, personal data, cookies, Chrome profiles, downloaded files, snapshot text or screenshots of non-fixture pages ([AGENTS.md](../AGENTS.md)). Record hashes and counts instead.
- Every task ends with evidence: command output, a log line or a screenshot, as [AGENTS.md](../AGENTS.md) requires. The acceptance column names the evidence.
- Phases that change `AGENTS.md`: P0 (check commands), P2 (record scripts), P3 (crate path, build and test commands), P5 (MCP binary). The task that adds a command also adds its `AGENTS.md` line.

Conventions: paths are relative to the repository root. `<date>` is the run date as `YYYYMMDD`. The crate lives at `crates/registry/`. Fixture pages are served with `python3 -m http.server 8000 --directory docs/baseline/fixtures/pages`. Tier: `haiku` = mechanical, `sonnet` = code or research, `opus` = judgement or gate decision. `Human`: `approval`, `network`, `launch` (start a browser), `login` (SSO/MFA), or empty.

## P0 Repo prerequisites

| ID | Title | Depends | Par | Tier | Inputs | Deliverable | Acceptance | Human |
|---|---|---|---|---|---|---|---|---|
| P0-01 | Relative-link checker | — | y | sonnet | `README.md`, `docs/**/*.md` | `scripts/check-links.py`; one `AGENTS.md` line with the command | `python3 scripts/check-links.py` exits 0 and prints the count of links checked; a deliberately broken link in a scratch copy exits 1 | |
| P0-02 | Ignore rules for build and run output | — | y | haiku | `AGENTS.md` | `.gitignore` with `target/`, `chrome-profile/`, `downloads/`, `config/local.toml` | `git check-ignore -v target/x chrome-profile/x downloads/x config/local.toml` lists all four | |
| P0-03 | Fixture and record validators | — | y | sonnet | `docs/baseline/README.md` (record schema) | `scripts/check-records.py` validates every `docs/baseline/runs/*.jsonl` against the step and summary keys; `AGENTS.md` line | Exits 0 on an empty `runs/`; exits 1 on a sample line with a missing key (show both outputs) | |

## P1 Test-site selection and fixtures

| ID | Title | Depends | Par | Tier | Inputs | Deliverable | Acceptance | Human |
|---|---|---|---|---|---|---|---|---|
| P1-01 | Shortlist public test sites | — | y | sonnet | Site criteria in `docs/baseline/README.md` | `docs/baseline/site-selection.md`: table of at least 3 candidates with criteria (a)–(d), terms-of-service link and check date | File exists; every row fills every column; each terms link is quoted with the clause that permits or does not forbid automation | network |
| P1-02 | Choose the site | P1-01 | n | opus | `docs/baseline/site-selection.md` | "Decision" section in `docs/baseline/site-selection.md`: URL, date, `sha256sum` of the fetched landing page | Hash command and output are shown; owner approval line present | approval, network |
| P1-03 | Fixture schema | — | y | sonnet | Task fields in `docs/baseline/README.md` | `docs/baseline/fixtures/schema.json`; `scripts/check-fixtures.py`; "Fixture file" paragraph in `docs/baseline/README.md` naming the keys | Required keys: `task`, `site_url`, `site_hash`, `date`, `preconditions`, `params`, `expected`, `forbidden_actions`; `expected` is either `values` or `file.sha256` + `file.row_count`; checker exits 1 on a sample missing `forbidden_actions` | |
| P1-04 | Fixture T1 | P1-02, P1-03 | y | sonnet | Chosen site, T1 goal in segment 01 | `docs/baseline/fixtures/T1.json` | `python3 scripts/check-fixtures.py` exits 0; expected values were read from the site on the recorded date | network |
| P1-05 | Fixture T2 | P1-02, P1-03 | y | sonnet | Chosen site, T2 goal | `docs/baseline/fixtures/T2.json` with N ≥ 5 expected values | Checker exits 0; values shown with their source filter | network |
| P1-06 | Fixture T3 | P1-02, P1-03 | y | sonnet | Chosen site, T3 goal | `docs/baseline/fixtures/T3.json` with `file.sha256` and `file.row_count`; the file itself is not committed | Checker exits 0; `git status` shows no downloaded file | network |
| P1-07 | Negative page N1: delayed control | — | y | sonnet | Segment 01 step 7 | `docs/baseline/fixtures/pages/n1-delayed-control.html` | Served page shows the target button only after 3 s; `curl` of the page contains no external URL | |
| P1-08 | Negative page N2: DOM replacement | — | y | sonnet | Segment 01 step 7; segment 07 mock test 3 | `docs/baseline/fixtures/pages/n2-dom-replacement.html` | A first click replaces the results list node with new ids and a new `data-revision`; documented in a comment at the top of the file | |
| P1-09 | Negative page N3: continuous network activity | — | y | sonnet | Segment 01 step 7 | `docs/baseline/fixtures/pages/n3-network-active.html` | Page polls a same-origin `fetch` every 500 ms after the visible result is ready; the result text is stable | |
| P1-10 | Negative fixtures N1–N3 | P1-03, P1-07, P1-08, P1-09 | y | haiku | The three pages | `docs/baseline/fixtures/N1.json`, `N2.json`, `N3.json` with `site_url` on `localhost:8000` | Checker exits 0 for all three | |

## P2 Playwright MCP baseline runs and records

| ID | Title | Depends | Par | Tier | Inputs | Deliverable | Acceptance | Human |
|---|---|---|---|---|---|---|---|---|
| P2-01 | Install Playwright MCP and record versions | P0-02 | n | sonnet | `docs/baseline/README.md` (Runs) | `docs/baseline/environment.md`: Playwright MCP version, browser version, OS, model id | `npx @playwright/mcp@<version> --version` output pasted; no home path or username in the file | network |
| P2-02 | Run protocol | P0-03, P1-03 | y | sonnet | `docs/baseline/README.md` (Metrics, Runs) | "Run protocol" section in `docs/baseline/README.md`: warm and cold definitions, how a step line is written, counting rules for recoveries and wrong actions, token estimate rule | Section exists; each deciding metric has one counting rule; `scripts/check-links.py` exits 0 | |
| P2-03 | Pilot run T1 | P2-01, P2-02, P1-04 | n | sonnet | `fixtures/T1.json`, protocol | `docs/baseline/runs/<date>-T1-0.jsonl`; protocol corrections in the same section | `scripts/check-records.py` exits 0; the summary line is complete | network |
| P2-04 | Runs T1 | P2-03 | n | sonnet | `fixtures/T1.json` | `runs/<date>-T1-1..5.jsonl` warm and cold (condition in the step lines) | 10 files (minimum 6); checker exits 0; every run reported, including failures | network |
| P2-05 | Runs T2 | P2-03, P1-05 | n | sonnet | `fixtures/T2.json` | `runs/<date>-T2-1..5.jsonl` warm and cold | Same as P2-04 | network |
| P2-06 | Runs T3 | P2-03, P1-06 | n | sonnet | `fixtures/T3.json` | `runs/<date>-T3-1..5.jsonl` warm and cold | Same as P2-04; `data_matches` compares SHA-256 and row count only | network |
| P2-07 | Runs N1–N3 | P2-03, P1-10 | n | sonnet | `fixtures/N1..N3.json`, served pages | `runs/<date>-N1..N3-1..3.jsonl` | 9 files; checker exits 0; each stale-target re-observation counted as a recovery | launch |
| P2-08 | Summary script | P0-03 | y | sonnet | Record schema | `scripts/baseline-summary.py`: per task, condition and controller prints success rate, correct-data ratio, recoveries, wrong actions, mean steps, bytes and ms; `AGENTS.md` line | Runs on a synthetic two-run sample and on `runs/`; output is a Markdown table | |
| P2-09 | Baseline results | P2-04, P2-05, P2-06, P2-07, P2-08 | n | sonnet | `runs/`, summary script | `docs/baseline/results-<date>.md`: generated table plus observation gaps, screenshot cases and maintenance notes | Table matches `python3 scripts/baseline-summary.py` output byte for byte; no snapshot text quoted | |
| P2-10 | Status updates after the baseline | P2-09 | y | haiku | Results file | Status lines in segment 01, `docs/baseline/README.md` and this file set to "baseline run <date>" | `grep -n "Status:"` on the three files shows the new text; link checker exits 0 | |

## Gate 1

| ID | Title | Depends | Par | Tier | Inputs | Deliverable | Acceptance | Human |
|---|---|---|---|---|---|---|---|---|
| G1-01 | Gate 1 decision | P2-09 | n | opus | `docs/baseline/results-<date>.md`; Gate 1 rule in [current recommendations](recommendations.md) (Selection conditions 3) | `docs/baseline/gates/<date>-gate-1.md`: outcome `proceed`, `stop` or `revise`; the evidence rows cited by file name; the owner's approval line | File exists and names one outcome; `stop` ends the plan at P2; `revise` names the P1 or P2 tasks to redo | approval |

## P3 Rust registry crate with mock browser

| ID | Title | Depends | Par | Tier | Inputs | Deliverable | Acceptance | Human |
|---|---|---|---|---|---|---|---|---|
| P3-01 | Scaffold the crate | G1-01, P0-02 | n | sonnet | Segment 07 registry design | `crates/registry/` library crate, edition 2021, dependencies `serde`, `serde_json`, `schemars` 1, `sha2`, `thiserror`; the two protected blueprint `Cargo.toml` files untouched | `cargo build` and `cargo test` exit 0 in `crates/registry`; `git diff --stat` shows no change under `docs/segments/02-*` or `03-*` | |
| P3-02 | AGENTS.md crate entry | P3-01 | y | haiku | `AGENTS.md` | Crate path and `cargo build`, `cargo test` commands in `AGENTS.md`; "Technologies" and "Project overview" no longer say there is no implementation | `grep -n "crates/registry" AGENTS.md` shows the lines | |
| P3-03 | Layer 0 browser trait | P3-01 | y | sonnet | Segment 07 (Layer 0 and Layer 1) | `crates/registry/src/browser.rs`: trait with `snapshot`, `click`, `type_text`, `wait_for`, `navigate`; `Snapshot { revision, nodes: [{ref_id, role, name}] }`; refs carry the revision | `cargo build` exits 0; the trait is `pub(crate)` | |
| P3-04 | Mock browser | P3-03 | y | sonnet | Fixture files, `n2-dom-replacement.html` behaviour | `crates/registry/src/mock.rs`: scripted pages loaded from `docs/baseline/fixtures/*.json`; `replace_node()` increments the revision | `cargo test mock` exits 0 with at least 3 tests | |
| P3-05 | Command spec and registry | P3-01 | y | sonnet | Segment 07 (one choke point) | `crates/registry/src/registry.rs`: `CommandSpec { id, params_schema, url_allowlist, enabled, run }`, lookup by id | `cargo test registry` exits 0; a test shows the unknown id error | |
| P3-06 | `execute()` choke point | P3-03, P3-05 | n | sonnet | Segment 07 (one choke point) | `crates/registry/src/execute.rs`: lookup, params object and schema check, URL allowlist, enabled check, `catch_unwind`, verification, audit; error codes `UNKNOWN_COMMAND`, `INVALID_PARAMS`, `URL_NOT_ALLOWED`, `STALE_PAGE_REVISION`, `COMMAND_DISABLED`, `PANIC` | `cargo test execute` exits 0; a panicking command returns `PANIC` and the process continues | |
| P3-07 | Audit log | P3-01 | y | sonnet | Segment 07 (Audit fields) | `crates/registry/src/audit.rs`: append-only JSONL with `ts`, `command_id`, `params_schema_hash`, `snapshot_hash`, `verification_hash`, `decision`, `outcome`, `dropped_count` | A test writes a snapshot containing the sentinel `SENTINEL-7f3a` and asserts the sentinel is absent from the log file | |
| P3-08 | Deny-by-default field projection | P3-01 | y | sonnet | Segment 07 (Deny by default) | `crates/registry/src/redact.rs`: allowlisted fields, size cap, row cap, dropped count | Tests: unmapped field dropped and counted; row cap truncates; size cap truncates | |
| P3-09 | Mock-browser acceptance tests | P3-04, P3-06, P3-07, P3-08 | n | sonnet | Segment 07 (Mock-browser acceptance tests) | `crates/registry/tests/acceptance.rs` with the four listed tests, including rejected calls appearing in the audit | `cargo test --test acceptance` exits 0 with 4 passing tests | |
| P3-10 | Layer 1 commands for T1–T3 | P3-09 | n | sonnet | Fixtures T1–T3; segment 07 (`choice` param) | `crates/registry/src/commands/{search_open_item,filter_read_values,download_verify}.rs`; each returns a redacted snapshot and accepts `choice` from enumerated targets | A test completes each task against the mock and matches the fixture's `expected`; a `choice` outside the enumerated targets returns `INVALID_PARAMS` | |
| P3-11 | Segment 07 and README status | P3-10 | y | haiku | Crate | Segment 07 status "registry crate built against mock, <date>"; `README.md` layout row for `crates/` | `grep -n "crates/" README.md`; link checker exits 0 | |

## P4 Rust CDP candidate

| ID | Title | Depends | Par | Tier | Inputs | Deliverable | Acceptance | Human |
|---|---|---|---|---|---|---|---|---|
| P4-01 | Candidate choice | G1-01 | y | opus | Recommendations (Selection condition 2); repositories for `chromiumoxide`, `cdp-rs`, `playwright-rs` | "Candidate choice" section in segment 07: attach to a running Chrome, accessibility tree access, last release date, licence, reason for the choice, owner approval line | Section exists with one chosen candidate; all three rows filled | approval, network |
| P4-02 | `CdpBrowser` behind a feature | P3-09, P4-01 | n | sonnet | Browser trait; chosen candidate | `crates/registry/src/cdp.rs` under feature `cdp`; connects to `http://127.0.0.1:9222` | `cargo build --features cdp` exits 0; `cargo test` without the feature still exits 0 | |
| P4-03 | Minimal CLI | P3-10 | y | sonnet | Registry | `crates/registry/src/bin/registry-cli.rs`: `list --json`, `run <id> --params <json>`; non-zero exit on any error code | `registry-cli list --json` prints exactly the Layer 1 ids; `run` with an unknown id exits 1 with `UNKNOWN_COMMAND` | |
| P4-04 | Chrome launch procedure | P0-02 | y | haiku | `AGENTS.md` (never commit profiles) | "Chrome for the comparison" paragraph in `docs/baseline/README.md`: launch with `--remote-debugging-port=9222 --user-data-dir=./chrome-profile` | `curl -s http://127.0.0.1:9222/json/version` returns JSON after the owner launches Chrome; `git check-ignore chrome-profile/x` succeeds | launch |
| P4-05 | Smoke test on a fixture page | P4-02, P4-04 | n | sonnet | Served `n2-dom-replacement.html` | `crates/registry/examples/smoke.rs`: snapshot, print revision and node count | `cargo run --features cdp --example smoke -- http://localhost:8000/n2-dom-replacement.html` prints both numbers | launch |
| P4-06 | Live stale-ref test | P4-05 | n | sonnet | Segment 07 mock test 3 | `#[ignore]` integration test in `crates/registry/tests/live.rs`: click through an old ref after replacement returns `STALE_PAGE_REVISION` | `cargo test --features cdp --test live -- --ignored` exits 0 | launch |
| P4-07 | Rust runs T1 | P4-03, P4-05 | n | sonnet | `fixtures/T1.json`; run protocol | `runs/<date>-T1-1..5-rust.jsonl` warm and cold, `versions.controller` set; the operator calls only `registry-cli` | 10 files (minimum 6); `scripts/check-records.py` exits 0 | launch, network |
| P4-08 | Rust runs T2 | P4-07 | n | sonnet | `fixtures/T2.json` | `runs/<date>-T2-1..5-rust.jsonl` | Same as P4-07 | launch, network |
| P4-09 | Rust runs T3 | P4-07 | n | sonnet | `fixtures/T3.json` | `runs/<date>-T3-1..5-rust.jsonl` | Same as P4-07; download verified by SHA-256 and row count | launch, network |
| P4-10 | Rust runs N1–N3 | P4-06 | n | sonnet | `fixtures/N1..N3.json` | `runs/<date>-N1..N3-1..3-rust.jsonl` | 9 files; checker exits 0 | launch |
| P4-11 | Comparison table | P4-08, P4-09, P4-10 | n | sonnet | `runs/`, `scripts/baseline-summary.py` | `docs/baseline/comparison-<date>.md`: baseline and Rust rows side by side for every deciding and supporting metric | Table matches the summary script output byte for byte | |
| P4-12 | Maintenance cost record | P4-11 | y | sonnet | Crate, git log | "Maintenance cost" section in `docs/baseline/comparison-<date>.md`: lines of code (`tokei` or `wc -l`), dependency count from `cargo tree --depth 1`, breakages met, time spent per phase from the task evidence | Every number has its command shown | |

## Gate 2

| ID | Title | Depends | Par | Tier | Inputs | Deliverable | Acceptance | Human |
|---|---|---|---|---|---|---|---|---|
| G2-01 | Gate 2 decision | P4-12 | n | opus | `docs/baseline/comparison-<date>.md`; Gate 2 rule in [current recommendations](recommendations.md) (Selection condition 4) | `docs/baseline/gates/<date>-gate-2.md`: outcome `proceed`, `stop` or `revise`; the metric rows cited; the owner's approval line | File names one outcome; `stop` records "continue with the baseline" and whether the Playwright MCP fallback in segment 07 is taken; `revise` names the P3 or P4 tasks to redo | approval |

## P5 MCP stdio and CLI

| ID | Title | Depends | Par | Tier | Inputs | Deliverable | Acceptance | Human |
|---|---|---|---|---|---|---|---|---|
| P5-01 | MCP server over stdio | G2-01 | n | sonnet | Segment 07 (Layer 1 tools); `rmcp` | `crates/registry/src/bin/registry-mcp.rs` exposing only `command_list` and `command_run` | Piping an `initialize` then `tools/list` JSON-RPC request into the binary returns exactly two tools | |
| P5-02 | Tool-visibility test | P5-01 | y | sonnet | MCP server | Test in `crates/registry/tests/mcp.rs` | Test asserts the tools list contains no name among `click`, `type`, `navigate`, `snapshot`, `screenshot`; `cargo test --test mcp` exits 0 | |
| P5-03 | Crate README and client configuration | P5-01 | y | haiku | Both binaries | `crates/registry/README.md`: build, CLI usage, an `.mcp.json` example with placeholder paths; `AGENTS.md` lines for both binaries | Link checker exits 0; `grep -n registry-mcp AGENTS.md` shows the line | |
| P5-04 | End-to-end runs through MCP | P5-02, P4-04 | n | sonnet | Fixtures T1–T3; run protocol | `runs/<date>-T1..T3-1..3-rust.jsonl` with `versions.controller` = `registry-mcp <version>`; the operator sees only the two MCP tools | 9 files; checker exits 0; the audit log line count equals the `command_run` count | launch, network |
| P5-05 | Results after MCP | P5-04 | n | sonnet | Runs, summary script | "MCP runs" section appended to `docs/baseline/comparison-<date>.md`; status lines in segment 07 and this file | Table matches the summary script output; link checker exits 0 | |

## P6 Workday sandbox (blocked)

Blocked until every condition in [segment 08](segments/08-workday-data-access/README.md) (Conditions for the sandbox step) has evidence. The repository cannot grant them.

| ID | Title | Depends | Par | Tier | Inputs | Deliverable | Acceptance | Human |
|---|---|---|---|---|---|---|---|---|
| P6-01 | Condition evidence | G2-01 | n | opus | Segment 08 conditions table | "Condition evidence" section in segment 08: one row per condition with the evidence reference; tenant alias only, no address | All five rows filled; owner approval line; no URL containing a tenant name | approval |
| P6-02 | Workday fixture | P6-01 | n | sonnet | Approved report name; fixture schema | `docs/baseline/fixtures/WD1.json`: alias, report name, expected `file.sha256` and `file.row_count` from the reference result | `scripts/check-fixtures.py` exits 0; `grep -i` for the tenant address finds nothing | approval |
| P6-03 | Runtime allowlist configuration | P6-01 | y | sonnet | Segment 08 redaction rules; `redact.rs` | `crates/registry/config/example.toml` with placeholders; loader reads `config/local.toml` (ignored by git) for the URL allowlist and field allowlist | `cargo test config` exits 0; `git check-ignore config/local.toml` succeeds | |
| P6-04 | One approved sandbox read | P6-02, P6-03, P5-04 | n | sonnet | `WD1.json`; MCP server | `runs/<date>-WD1-1.jsonl`; the export verified by hash and row count; audit log kept locally | Checker exits 0; `data_matches` equals 1; the owner logged in before the run and the agent never saw a credential | login, approval |
| P6-05 | Sandbox record review | P6-04 | n | opus | Run record, audit log, segment 08 redaction rules | `docs/baseline/gates/<date>-sandbox-review.md`: leakage check of the record and audit (names, addresses, tokens, snapshot text), outcome, approval line | Review names each check and its result; nothing from the audit log is committed | approval |
