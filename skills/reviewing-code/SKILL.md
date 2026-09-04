---
name: reviewing-code
description: "Perform local code reviews across git working tree diffs, staged changes, branches, or targeted modules. Uses shared software engineering and code review guidelines to identify architectural flaws, resilience gaps, code smells, and test regressions."
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

# Reviewing Code (Local Review)

Purpose: Perform rigorous, local code reviews across uncommitted changes, branches, or specific modules before committing, opening pull requests, or merging.

## Prerequisites & Shared Guidelines

- **Consult Shared Guidelines**: Always refer to `references/code-review-guidelines.md` for the 4 scales of code review, principle checklists, finding taxonomies, Test Value lens, and output report format.
- **Reference Software Engineering Invariants**: Consult the `software-engineering` skill for in-depth definitions of architectural rules (Clean/Hexagonal), modular depth, defensive programming, refactoring recipes, resilience patterns, and testing invariants.
- **Organization-Specific Guidelines**: Check if the repository belongs to a recognized organization:
  ```bash
  git remote -v
  ```
  - If the remote points to **Learning Equality** (`github.com[:/]learningequality/`), also consult `references/learning-equality-guidelines.md` for Django values-viewsets, KDS component reuse, declarative permissions, WCAG accessibility, and RTLCSS rules.
- **Manage Cognitive Load**: Focus on complexity reduction, inward dependency flows, error semantics, and test quality rather than cosmetic styling.

---

## Local Review Workflow

```
1. SCOPE TARGETS ──► 2. EXECUTE 4-SCALE REVIEW ──► 3. VERIFY WITH TOOLS ──► 4. DELIVER REPORT & REMEDIATION
        │                         │                          │                          │
        ▼                         ▼                          ▼                          ▼
   Working tree,             Check against              Run tests, linter,         Present findings,
   staged diff, branch,      code-review-guidelines     and build suite for        offer interactive
   or target files           checklists                 empirical evidence         remediations
```

### Step 1: Determine the Review Scope

Identify the target of the review:
- **Working Tree / Uncommitted Changes**:
  ```bash
  git status
  git diff
  ```
- **Staged Changes Only**:
  ```bash
  git diff --cached
  ```
- **Branch vs. Base**:
  ```bash
  git diff main...HEAD
  ```
- **Specific Module / Files**:
  Inspect the specified files and their immediate callers, dependencies, and corresponding test files.

### Step 2: Conduct Multi-Scale Analysis

Evaluate the diff against the checklists in `references/code-review-guidelines.md`:
1. **Macro-Scale & Resilience**: Timeouts, circuit breakers, bounded retries, resource cleanup (RAII/defer), concurrency safety, no silent error suppression.
2. **Strategic Architecture**: Inward dependency flow, bounded contexts, ubiquitous language, ACLs for external dependencies.
3. **Modularity & Depth Design**: Deep modules vs. shallow wrappers, information hiding, orthogonality, SRP.
4. **Micro-Craftsmanship & Smells**: Single Level of Abstraction (SLAP), Command-Query Separation (CQS), parameter limits (<3), Primitive Obsession, code smells.
5. **Verification & Test Value**: F.I.R.S.T. properties, asserting observable behavior vs. over-mocking, legacy characterization safety nets.

### Step 3: Run Empirical Verification Commands

Run the repository's verification tools to gather hard evidence before finalizing the review:
- Unit & integration tests (`pytest`, `npm test`, `cargo test`, `go test ./...`, etc.)
- Type checkers (`mypy`, `tsc`, `pyright`, etc.)
- Linters & static analysis (`ruff`, `eslint`, `golangci-lint`, etc.)
- Build commands (`make build`, `cargo build`, `npm run build`, etc.)

### Step 4: Format and Present Findings

1. Structure the review report using the standard template in `references/code-review-guidelines.md`.
2. Categorize all findings by severity:
   - `🚨 Blocker (Must-Fix)`
   - `⚠️ Architecture & Design (Should-Fix)`
   - `💡 Tactical Suggestion (Optional)`
   - `✅ Positive Highlights`
3. Clearly cite exact file paths and line ranges (`path/to/file#L10-L25`).
4. Provide concrete code diffs or refactoring recipes for all blockers and design issues.
5. Offer to assist the developer in interactively applying the recommended fixes.

---

## Operational Directives for the Agent

1. **Evidence-Based Findings**: Base feedback on observable code paths and empirical test/linter runs.
2. **Actionable Suggestions**: Never point out an issue without explaining *why* it matters and demonstrating a concrete alternative.
3. **Check Compilability First**: Always run tests before reviewing to verify whether the baseline is working or already broken.
