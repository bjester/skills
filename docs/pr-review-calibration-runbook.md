# Calibrating Skills from GitHub PR Reviews

Purpose: Audit a reviewer account's multi-reviewer GitHub Pull Request history against subsequent and prior peer reviews, extract recurring reasoning blind spots, and translate verified lessons into atomic skill updates.

## When to Run

Run this playbook from the root of this repository's working copy (`git rev-parse --show-toplevel`) when you want to evaluate how an AI reviewer account (such as `bjesterbot`) performed on real pull requests and harden the skills in this repository from empirical peer-review outcomes.

> [!NOTE]
> This runbook is a repository-local maintenance guide. Keep it in `docs/` rather than `skills/` so `make build` does not package it into `output/skills/` or load discovery metadata into unrelated coding sessions.

## Inputs & Incremental Window

1. **Target Reviewer (`<login>`)**: GitHub username to audit (default: `bjesterbot`).
2. **Audit Window (`<since-date>`)**:
   - If the user provides an explicit date range, repository filter, or PR list, use that scope.
   - Otherwise, look up `<login>`'s most recent row in the [Calibration Watermark Log](#calibration-watermark-log) at the bottom of this file and set `<since-date>` to that `Run Date`.
   - Query `updated:>=<since-date>` (rather than `created:>=<since-date>`) so PRs opened before the last audit that received *new* peer reviews after the watermark are captured.

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. DISCOVER & BUCKET: Query gh (reviewed-by / commenter / involves)     │
│    Apply watermark; split Primary (after) / Secondary (before) / Skip   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. COMMIT-ANCHORED FORENSICS: Shard repos across research subagents     │
│    Score Fixed vs. Regression vs. Refuted vs. Missed at commit_id       │
└────────────────────────────────────┬────────────────────────────────────┘
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3. SYNTHESIZE & ROUTE: Generalize into missing verification pathways    │
│    Route across repo boundaries -> HARD GATE: User Roadmap Approval     │
└────────────────────────────────────┬────────────────────────────────────┘
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 4. HARDEN & RECORD: writing-specs -> plans -> executing-plans           │
│    Run make validate, compose atomic commits, append Watermark Log      │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Incremental Discovery & Signal-Weighted Bucketing

1. **Query All Three Participation Axes**:
   `COMMENT`-only reviews and inline thread replies do not all appear under `--reviewed-by` alone. Run all three `gh` queries and deduplicate by `owner/repo#number`:
   ```bash
   gh search prs --reviewed-by "<login>" --updated ">=<since-date>" --limit 200 --json number,repository,title,state,updatedAt,url
   gh search prs --commenter "<login>" --updated ">=<since-date>" --limit 200 --json number,repository,title,state,updatedAt,url
   gh search prs --involves "<login>" --updated ">=<since-date>" --limit 200 --json number,repository,title,state,updatedAt,url
   ```
   Exclude PRs where `<login>` only has a pending review request and never submitted a review or comment. If a PR was already covered in an earlier audit and has zero new review or commit activity after `<since-date>`, skip re-auditing it.

2. **Fetch Timeline Metadata & Partition into Three Buckets**:
   For each candidate PR, inspect review submissions and inline review comments (`gh api repos/{owner}/{repo}/pulls/{num}/reviews` and `gh api repos/{owner}/{repo}/pulls/{num}/comments`). Exclude the PR author's own replies when counting peer reviewers.

   Classify every PR into one of three buckets:
   - **Bucket 1 (`Primary Focus`: Reviewed by others *after* `<login>`)**: Highest ground-truth signal. Subsequent human or bot reviewers (and post-review integration fixes) expose missed defects, premature `APPROVE` verdicts, rejected nits, and regressions introduced when fixing `<login>`'s comments.
   - **Bucket 2 (`Secondary Focus`: Reviewed by others *before* `<login>` only)**: Evaluates prior-thread synthesis, duplicate-comment avoidance, author refutations, and `gh` token or account hygiene.
   - **Bucket 3 (`Skipped`: Solo-reviewed by `<login>` only)**: Record the count and repository breakdown in the audit inventory table for completeness, then skip deep forensics. Absence of peer review is not evidence of a zero-miss review.

---

## Phase 2: Parallel Commit-Anchored Forensics

1. **Shard by Repository Across `research` Subagents**:
   Group `Primary Focus` and `Secondary Focus` PRs by repository (`2` to `5` PRs per read-only `research` subagent) so raw diffs, commit histories, and GraphQL thread payloads stay out of the coordinator's context window.

2. **Enforce Commit-Anchored Evaluation**:
   > [!IMPORTANT]
   > Never judge `<login>`'s review against final `HEAD` blindly. Always anchor evaluation to the exact `commit_id` `<login>` inspected at review time, plus any delta reviews `<login>` posted on subsequent pushes.

   For each audited PR, collect:
   - **PR & Harness Metadata**: PR author, `<login>` review `state` (`APPROVED`, `CHANGES_REQUESTED`, `COMMENTED`), review turnaround time, harness/model signature if recorded in the review body or session logs, and whether delta re-reviews ran on later commits.
   - **Linked Issue Contract**: Read linked issues (`gh issue view <num>`) so PR description shortcuts or deferrals are checked against original acceptance and testing requirements rather than accepted at face value.
   - **Thread Resolution & Commit Forensics**: Fetch review threads (including `isResolved`, `isOutdated`, and author replies via `gh api graphql`) alongside subsequent commits (`git log` / `pulls/{num}/commits`).

3. **Score Every Finding by Empirical Outcome**:
   Classify each `<login>` finding and each peer/subsequent finding using concrete outcomes:
   - **`<login>` Finding Outcomes**:
     - `Fixed`: Author accepted the finding and landed a code or doc change.
     - `Fixed -> Caused Regression`: Author applied `<login>`'s suggested fix or snippet, which introduced a new bug or broke an existing contract/test.
     - `Refuted / Rejected`: Author or maintainer pushed back with a valid architectural, spec, or domain reason.
     - `Hallucinated Praise / Redundant Nit`: `<login>` praised a vacuous test or repeated a previously rejected style nit.
   - **Peer / Subsequent Reviewer Outcomes**:
     - `Missed Defect on Reviewed Commit (Fixed)`: A real bug, test tautology, runtime floor crash, or config gap was present in `<login>`'s reviewed `commit_id` and caught later by another reviewer or integration test.
     - `Post-Review Push Defect (Delta Trigger Gap)`: Defect was introduced in a commit pushed *after* `<login>`'s review where `<login>` was never re-run.
     - `Rejected Peer Nit`: A peer reviewer's suggestion was rejected by maintainers. Do **not** import rejected peer nits into repository skills.

4. **Stratify by Model Tier & Verdict Posture**:
   Separate historical misses caused by fast/smaller models or permissive `APPROVE` defaults from structural blind spots that still occur on frontier models using `COMMENT`. Prioritize blind spots that persist on current frontier models.

---

## Phase 3: Pathway Synthesis, Routing & User Alignment Gate

1. **Extract Missing Verification Pathways**:
   Cluster misses and false positives by the **missing reasoning pathway** rather than narrow bug trivia. Ask: *What concrete verification step would have forced the reviewer to catch this defect or suppress this bad suggestion?* (Examples: counterfactual two-edit test mutation, checking all callers before proposing a helper snippet, opening imported root wrapper components, checking `pyproject.toml` / CI matrix floors.)

2. **Route Each Improvement to the Right Architectural Home**:
   Follow the boundaries defined in `AGENTS.md`:

   | Destination | What Belongs Here |
   | :--- | :--- |
   | `skills/engineering-software/` | Timeless computer science, architecture, concurrency, data-integrity, and refactoring invariants that apply equally to human and AI engineers. |
   | `skills/engineering-with-agents/` | LLM-specific behavioral guardrails countering autoregressive pathologies (anchoring on PR prose, same-model blind spots, hallucinated praise, proxy checks). |
   | Workflow & capability skills (`reviewing-code`, `reviewing-github-prs`, `verifying-prs-in-browser`, `resolving-github-pr-feedback`, `analyzing-blast-radius`, `writing-github-prs`, `writing-technical-docs`) | Phased procedural gates, pre-flight CLI identity checks, rebase-safe delta diffing, prose hygiene, and isolated browser verification steps. |
   | Organization / ecosystem skills (`skills/learning-equality/`, etc.) | Organization-specific framework conventions, database floors, KDS rules, and workspace packaging globs (split into on-demand `references/*.md` files when detailed). |
   | Out-of-repo harness / bot config | Bot-specific GitHub webhooks, `GH_TOKEN` credential wrappers, cron triggers, and account personas. Keep these out of `skills/`. |

3. **Present Audit Report & Pause at the Hard Alignment Gate**:
   Write a structured Audit Report artifact containing:
   - `1. Inventory & Executive Summary` (bucket counts + model/era stratification)
   - `2. Master Comparative Matrix` (one row per audited PR with `<login>` signal, peer signal, and key takeaway)
   - `3. Root-Cause Blind Spots & Reasoning Pathways` (evidence-backed clusters citing exact PRs)
   - `4. Prioritized Skill Improvement Roadmap` (mapped to target files)

   > [!WARNING]
   > **Hard Gate**: Stop and get explicit user feedback on the Audit Report and roadmap priorities before drafting specifications or editing any files under `skills/`.

---

## Phase 4: Multi-Spec Hardening & Watermark Update

1. **Decompose into Cohesive Specs (`writing-specs`)**:
   Split approved roadmap items into small, independent specs by bounded context (typically `2` to `4` specs, such as core review/blast-radius gates, org-specific references, prose/PR-authoring rules, and standalone verification tooling).

2. **Execute Each Spec Sequentially**:
   Run each spec through the full repository lifecycle before starting the next spec:
   1. `writing-specs`: Draft spec, self-review in Plain English (`writing-technical-docs`, zero em-dashes), and obtain user approval.
   2. `writing-plans`: Propose task breakdown, confirm with the user, assemble plan, and obtain user approval.
   3. `executing-plans`: Apply skill edits, update each modified skill's `CHANGELOG.md` and version, update `README.md` (`Skills Catalog` and `Repository Structure`) and `Makefile` shared references when needed, and run `make validate` (`shinyskills` must exit `0`).
   4. `composing-commit-history`: After user diff review, create clean atomic commits per logical change unit.

3. **Record the New Calibration Watermark**:
   In the final commit of the calibration session, append a row to the **Calibration Watermark Log** below so the next calibration run resumes cleanly from today's date.

---

## Calibration Watermark Log

| Run Date | Reviewer | Window Audited | PRs Scanned (Primary / Secondary / Skipped) | Key Outcomes & Landed Commits |
| :--- | :--- | :--- | :--- | :--- |
| `2026-11-11` | `bjesterbot` | Through `2026-11-11` | `36` reviewed (`9` Primary / `2` Secondary / `25` Skipped; `1` pending request) | Specs 1-4 (`14d7c98..7c4d1e4`): hardened PR review, feedback resolution, and blast-radius gates; added `learning-equality` sync/DB and frontend/packaging references; calibrated Plain prose and added `writing-github-prs`; added profile-isolated `verifying-prs-in-browser`. |
