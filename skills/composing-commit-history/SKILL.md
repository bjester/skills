---
name: composing-commit-history
description: "Compose or clean up commit history before review or opening a PR—creating logical review units from uncommitted/staged working changes or reorganizing messy commit history into clean, cohesive commits."
license: MIT - https://github.com/bjester/skills/blob/main/LICENSE
user-invocable: true
compatibility: a software project with git version control
allowed-tools:
  - read_file
  - write_file
  - run_command
  - grep
  - find_by_name
  - ask_user_question
  - task
metadata:
  author: Blaine Jester
  version: "1.0"
---

# Composing & Cleaning Up Commit History

Purpose: Compose clean, review-ready commit history using `git reset --soft` and selective re-committing—transforming uncommitted changes or messy development commits into atomic, logical review units.

## Prerequisites & Core Philosophy

- **Reviewer-Centric History**: Commits should reflect logical units of change that a reviewer can inspect and understand independently, not the chronological trial-and-error process that produced them.
- **Explicit User Go-Ahead**: This skill is the user-gated commit step. Execution skills (`writing-plans`, `executing-plans`) stage work without auto-committing; invoking this skill provides the explicit instruction to form commits.
- **Preserve Net Diffs**: The combined net diff against the base branch must remain 100% identical before and after reorganizing commits.
- **Two Hats Discipline**: Keep refactoring commits separate from functional feature additions.

---

## When to Use

- **No Commits Yet**: Changes are staged or untracked in the working tree (e.g., after plan execution). Create clean commits from scratch.
- **Messy Intermediate Commits**: The branch contains noisy commits (`git log --oneline <base>..HEAD` shows red/green TDD cycles, typo fixes, lint cleanups, or mixed concerns). Reorganize into cohesive review units.
- **Mixed State**: A mixture of existing commits and uncommitted working tree changes.

**Skip When**: The history is already clean and logical, and there are no uncommitted changes.

---

## The Soft-Reset & Re-Commit Technique

```
1. SOFT RESET ──► 2. CAPTURE BASELINE ──► 3. UNSTAGE ALL ──► 4. RE-COMMIT GROUPS ──► 5. VERIFY EQUALITY
        │                     │                    │                    │                     │
        ▼                     ▼                    ▼                    ▼                     ▼
   Collapse to           Save complete         `git reset           Stage & commit       Compare before &
   single pile:          target patch to       HEAD .`              atomic logical       after diffs
   `git reset            /tmp/before.patch                          units                (`diff -u`)
   --soft <base>`
```

### 1. Collapse Existing Commits into Working State

If there are existing commits on the branch (`git log --oneline <base>..HEAD` is non-empty):

```bash
git reset --soft <base>
```

*(If all changes are already uncommitted in the working tree, skip this step.)*

### 2. Capture Baseline Diff (Safety Net)

Capture the exact end-state diff including untracked files:

```bash
git add -A
git diff --staged <base> > /tmp/before-history.patch
```

### 3. Unstage Everything

```bash
git reset HEAD .
```

*Note: Modified files will appear as unstaged; newly created files will appear as untracked.*

### 4. Re-Commit in Atomic Logical Groups

Stage related files and author clear, descriptive commits:

```bash
# Example: Data model, migrations, and unit tests
git add path/to/model.py path/to/migration.py tests/test_model.py
git commit -m "Add Widget model with migrations and validation tests"

# Example: Service workflow logic
git add path/to/service.py tests/test_service.py
git commit -m "Implement Widget registration service and domain invariants"

# Example: API endpoint and integration routes
git add path/to/routes.py tests/test_routes.py
git commit -m "Expose Widget REST API endpoints"
```

- For modifications within the same tracked file that belong to different logical commits, use `git add -p` to stage hunks interactively.

### 5. Verify Diff Equality (CRITICAL)

Verify that the reorganized history produces the exact same final state as the baseline:

```bash
git diff <base>..HEAD > /tmp/after-history.patch
diff -u /tmp/before-history.patch /tmp/after-history.patch
```

**The diffs must be identical.** If there are discrepancies:
- Check `git status` for unstaged or forgotten files.
- If necessary to recover, use `git reflog` and `git reset --hard <sha-before-soft-reset>` to restore the pre-reset state.

---

## Grouping Heuristics

| Pattern | Action |
| :--- | :--- |
| **TDD Red/Green Cycles** ("Add failing test" + "Fix implementation") | Consolidate into a single cohesive commit. |
| **Fixups & Cleanups** (lint fixes, typo corrections, import cleanups) | Fold into the original commit they modify. |
| **Feature Addition vs. Refactor** | Keep as separate commits (Two Hats discipline). |
| **Model + Migration + Isolated Model Tests** | Group as a single foundational commit. |
| **Granular Slices** that only make sense together | Consolidate—avoid fragmented micro-commits that lack context in isolation. |
| **Single Cohesive Feature** | A single clean commit is preferred over arbitrary slicing. |

---

## Commit Message Guidelines

- **Imperative Mood**: Use concise, imperative verbs in the subject line (*"Add feature"*, *"Fix edge case"*, *"Refactor parser"*, not *"Added"* or *"Fixing"*).
- **Match Repository Style**: Inspect `git log --oneline -10 <base>` to match project casing, prefixes, or conventional commit tags (e.g. `feat:`, `fix:`).
- **Explain What & Why**: Focus the commit message on the technical intent and domain rationale, not the trial-and-error development steps.
- **Do Not Reference Cleanup**: Do not mention staging artifacts, soft resets, or commit reordering in the message.

---

## Recovery Procedure

If anything goes wrong during re-committing:

```bash
# Inspect reflog to locate pre-reset state
git reflog

# Restore pre-reset HEAD
git reset --hard <sha-before-soft-reset>
```

---

## Operational Directives for the Agent

1. **Always Capture Baseline First**: Never execute `git reset HEAD .` without first capturing `/tmp/before-history.patch`.
2. **Mandatory Diff Equality Check**: Always execute Step 5 and verify zero differences between baseline and post-rewrite patches.
3. **Never Commit Without Invocational Context**: Only create git commits when explicitly invoked or approved by the user.
