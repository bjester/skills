---
name: writing-github-issues-for-bugs
description: "Use when creating GitHub issues to track bug reports, defect investigations, or system failures after researching a codebase."
license: MIT - https://github.com/bjester/skills/blob/main/LICENSE
user-invocable: true
compatibility: a software project hosted on GitHub
allowed-tools:
  - read_file
  - run_command
  - grep
  - ask_user_question
  - task
metadata:
  author: Blaine Jester
  version: "1.0"
---

# Writing GitHub Issues: Bugs

Purpose: Facilitate the creation of actionable, reproducible, and well-structured GitHub issues for bug reports and regressions without dictating prescriptive implementation fixes.

## Prerequisites & Core Philosophy

- **Specify What & Why, Not How**: Clearly describe the broken behavior, reproduction path, and expected outcome. Leave internal bug-fixing mechanics to the developer.
- **Reference Shared Issue Guidelines**: Consult `references/github-issue-guidelines.md` for writing principles, DOs/DON'Ts, and the DEEP AI disclosure framework.
- **Incorporate Foundational Software Principles**: Consult `references/software-engineering.md` for characterization testing, legacy seams (`Sprout`/`Wrap`/`Override`), invariant preservation, and failure isolation.

---

## When to Use

- You have identified a regression, defect, or unexpected runtime failure.
- You've investigated the codebase to pinpoint affected modules and conditions.
- You have clear reproduction steps, logs, or failing test evidence.

**When NOT to Use:**
- New feature requests or enhancements (use `writing-github-issues-for-features` instead).
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
**Severity / Priority**: [P0 (Blocker) | P1 (High) | P2 (Medium)]  
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
- [ ] **AI Disclosure Included**: Is AI involvement stated transparently?

