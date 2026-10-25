# 000-111-workday-automation-learning — AI Agent Guidelines

Single source of truth for AI agents in this repository. If `CLAUDE.md` or `GEMINI.md` exists, it points to this file.

## Project status: migrated, archived pointer-only

On 2026-10-25 the owner consolidated this repository's content into the private
`000-333-workday-automation-research` repository, under its `learning/` folder.
Reason: this repository is public-tiered (`000-111-` = public "Learning" per the
manifest's classification rules), while its content scope overlapped with the
private research repo's Workday/browser-automation work. Moving the content from
this public repo into the private one creates no disclosure risk; the content here
was general learning material, not confidential operational detail.

This repository now holds no working content: no `docs/`, no `scripts/`. Do not
add new learning content here. Point any new browser-automation or Workday-learning
work to `000-333-workday-automation-research/learning/` instead. This repository
is retired and retained as a read-only GitHub archive; its public Git history
remains available.

## Security and secrets

- Never expose, print, log, commit, or include in diffs, prompts, fixtures, screenshots, or generated files any API key, token, password, credential, private key, session cookie, or other secret. Redact with `<REDACTED>`.
- Never ask the user to paste a secret into chat. Do not read or display secret-file contents. If a credential is missing, stop and explain how to provide it securely.

## Branches and pull requests

- Never push to `main` directly. Make a branch, push it, and open a pull request.

## Git identity

Commit as `Mister K <678459+kairin@users.noreply.github.com>`. This is the
public GitHub name and the GitHub noreply email. Do not commit with another
name or with a personal email address. Check with `git config user.name` and
`git config user.email` before you commit.

## Workday project group

Repository: `000-111-workday-automation-learning`. Formerly owned browser automation learning and experiments relevant to Workday; that content is now migrated to `000-333-workday-automation-research` (private), under `learning/`. This repo is retained as a pointer stub only, consistent with the manifest's public-tier naming convention for `000-111-`.
