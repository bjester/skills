---
name: writing-issues-for-bugs
description: |
  Authors actionable, reproducible bug report, defect investigation, and regression
  issues on GitHub (gh) or Gitea (gt) after researching a codebase. Enforces forge
  selection, duplicate search, epistemic uncertainty markers, severity tiers, Plain
  prose, DEEP AI disclosure, and safe --body-file submission. Use for bugs and
  regressions, not feature requests (use writing-issues-for-features).
license: MIT - https://github.com/bjester/skills/blob/main/LICENSE
user-invocable: true
compatibility: Git repositories hosted on GitHub (gh) or Gitea (gt)
allowed-tools:
  - read_file
  - write_file
  - run_command
  - grep
  - ask_user_question
  - task
metadata:
  author: Blaine Jester
  version: "2.0"
---

# Writing Issues: Bugs

Purpose: Draft and submit actionable, reproducible, and well-structured bug report and regression issues on GitHub (`gh`) or Gitea (`gt`) without dictating prescriptive implementation fixes.

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. SELECT FORGE & SEARCH DUPLICATES: Resolve gh or gt and search issues │
└────────────────────────────────────┬────────────────────────────────────┘
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. DRAFT BUG CONTRACT: Capture behavior, repro steps, logs & pointers   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3. DE-SLOP SCAN: Verify Plain prose, word-swaps & epistemic markers     │
└────────────────────────────────────┬────────────────────────────────────┘
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 4. SAFE --body-file SUBMIT: Write scratch file and create issue via CLI │
└─────────────────────────────────────────────────────────────────────────┘
```

1. **Select Forge & Search Duplicates**: Run the Forge Selection Gate in [references/forge-cli.md](references/forge-cli.md) to choose `gh` or `gt` (`--no-input`), then search open and closed issues (`gh issue list --search "<keywords>" --state all --limit 20` or `gt issue list -S "<keywords>" --state all -L 20 --no-input --json number,title,state,url`) before drafting.
2. **Draft Bug Contract**: Populate the Bug Issue Template below with observed vs. expected behavior, deterministic reproduction steps, `(unconfirmed)` markers for unverified report details, sanitized logs, and regression test requirements.
3. **De-Slop Scan**: Verify every section against `writing-technical-docs` (Plain mode), [references/word-swaps.md](references/word-swaps.md), and the Self-Review Checklist below before submission.
4. **Safe `--body-file` Submit**: Write the Markdown body to `/tmp/issue-body.md`, confirm with the user when running interactively, and submit via `gh issue create --title "<Title>" --body-file /tmp/issue-body.md` or `gt issue create --no-input --title "<Title>" --body-file /tmp/issue-body.md`.

> [!IMPORTANT]
> Always pass `--no-input` on every `gt` command and submit issue bodies via `--body-file` rather than inline `--body "..."` strings so shell interpolation cannot corrupt stack traces or code fences.

---

## Prerequisites & Core Philosophy

- **Select Forge & Verify Target**: Follow [references/forge-cli.md](references/forge-cli.md) to resolve the target repository and select `gh` (GitHub) or `gt` (Gitea) before invoking any CLI command.
- **Specify What & Why, Not How**: Clearly describe the broken behavior, reproduction path, and expected outcome. Leave internal bug-fixing mechanics to the developer.
- **Reference Shared Issue Guidelines**: Consult [references/issue-guidelines.md](references/issue-guidelines.md) for writing principles, DOs/DON'Ts, duplicate search, safe `--body-file` submission, and the DEEP AI disclosure framework.
- **Apply Plain Technical Prose**: Load the `writing-technical-docs` skill (Plain mode) and consult [references/word-swaps.md](references/word-swaps.md) to write clear, active sentences with zero em-dashes, negative parallelisms, or AI filler.
- **Incorporate Foundational Software Principles**: Consult the `engineering-software` skill for characterization testing, legacy seams (`Sprout`/`Wrap`/`Override`), invariant preservation, and failure isolation.

---

## When to Use

- You have identified a regression, defect, or unexpected runtime failure.
- You have investigated the codebase to pinpoint affected modules and conditions.
- You have clear reproduction steps, logs, or failing test evidence.

**When NOT to Use:**
- New feature requests or enhancements (use `writing-issues-for-features` instead).
- Speculative bug reports without reproduction steps or verified codebase context.

---

## Issue Title Guidelines

State the **broken or missing behavior/invariant**, not the code flaw:

- ✅ **Good**: `Sync operations fail when processing self-referential foreign keys`
- ✅ **Good**: `cleanupsyncs command ignores custom sync filter arguments`
- ✅ **Good**: `Expired session tokens trigger 500 error instead of 401 Unauthorized`
- ❌ **Bad**: `Missing _self_ref_order field on AbstractStore`
- ❌ **Bad**: `[bug] SyncableModelRegistry.get_model_querysets throws exception`

---

## Bug Issue Template

````markdown
## Observed Behavior
[Clear description of what happens currently: the failure, unexpected state, or broken invariant.]

## Expected Behavior
[Clear description of what should happen according to domain contracts and expected invariants.]

## Steps to Reproduce
1. [Step 1: Setup / Precondition]
2. [Step 2: Action performed]
3. [Step 3: Triggering operation]
4. [See error / invalid state]

### Minimal Reproduction Environment / Conditions
- **Version / Branch / Commit**: [e.g. `v0.17.2` or `develop@abc1234`]
- **Configuration / Environment**: [e.g. PostgreSQL 15, Python 3.11, Docker container]
- **Preserving Epistemic Uncertainty**: Never fabricate unverified reproduction steps or environment versions when synthesizing an issue from partial logs or user reports; mark unverified details explicitly as `(unconfirmed)`.

## Errors, Logs & Telemetry
```
[Paste relevant sanitized traceback, error logs, or terminal output here]
```

## Deliverables & Testing Requirements
- [Expected invariant restoration or behavior contract]
- **Regression Safety**: Require a characterization or regression unit/integration test that reproduces the failure and prevents future regressions.
- **Legacy Seam Note** (if applicable): If modifying untested legacy code, suggest isolating a test seam (`Sprout`/`Wrap`/`Override`).

## Technical Pointers & Root Cause Clues
- **Suspected Components**: [Relevant files/modules, e.g. `src/sync/engine.py:120-150`, `AbstractStore`]
- **Related Issues / PRs**: [Links to recent commits or related issues that may have introduced the regression]

## Notes & Edge Cases
- **Data Integrity / Migration Impact**: [Does this bug leave corrupted data in DB? Is a data cleanup or migration needed?]
- **Backward Compatibility**: [Compatibility considerations with older clients or serialized models]

## Metadata
**Severity / Priority**: [P0 (Blocker: data corruption, security exposure, or crash with no workaround) | P1 (High: core workflow broken with no workaround) | P2 (Medium: impaired behavior with a viable workaround)]  
**Area**: `bug`, `area:sync` (optional)

## AI Usage
[Disclose AI assistance following the DEEP framework: Disclose, Engage critically, Edit, Process sharing.]
````

---

## Self-Review Checklist Before Submitting

- [ ] **Symptom-Oriented Title**: Does the title describe the broken behavior or failed contract?
- [ ] **Deterministic Reproduction Steps**: Can another engineer replicate the issue from the steps provided?
- [ ] **Sanitized Logs & Error Outputs**: Are relevant stack traces included and sensitive tokens/secrets scrubbed?
- [ ] **Regression Test Mandated**: Is a regression test explicitly required in deliverables?
- [ ] **No Prescriptive Code Rewrites**: Are technical pointers provided without dictating specific inline code changes?
- [ ] **Zero AI Slop (`writing-technical-docs`)**: Verified against `writing-technical-docs` and [references/word-swaps.md](references/word-swaps.md) (zero em-dashes, negative parallelisms, or trailing `, -ing` fluff)?
- [ ] **AI Disclosure Included**: Is AI involvement stated transparently?
- [ ] **Duplicate Search & Safe CLI Creation**: Did you select the target forge per [references/forge-cli.md](references/forge-cli.md), search existing issues (`gh issue list --search "<keywords>"` or `gt issue list -S "<keywords>" --no-input`), and submit via `--body-file` (`gh issue create --body-file` or `gt issue create --no-input --body-file`) per [references/issue-guidelines.md](references/issue-guidelines.md)?
