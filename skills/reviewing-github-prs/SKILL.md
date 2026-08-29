---
name: reviewing-github-prs
description: "Review GitHub Pull Requests using the GitHub CLI (`gh`). Evaluates PR diffs against foundational software engineering invariants, modular depth, resilience, and test quality, and submits structured reviews via `gh pr review`."
license: MIT - https://github.com/bjester/skills/blob/main/LICENSE
user-invocable: true
compatibility: a software project with git version control and the gh CLI
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

# Reviewing GitHub Pull Requests

Purpose: Conduct thorough, constructive, and principle-grounded GitHub Pull Request reviews using the GitHub CLI (`gh`). Evaluate PR diffs across all engineering scales and submit clear, structured review feedback.

## Prerequisites & Shared Guidelines

- **Consult Shared Guidelines**: Always refer to `references/code-review-guidelines.md` for the 4 scales of code review, principle checklists, finding taxonomies, Delta reviews, Dependabot workflows, and the standard review template.
- **Reference Software Engineering Invariants**: Consult `references/software-engineering.md` for foundational architectural rules, modular depth, defensive error handling, and testing disciplines.
- **Organization-Specific Guidelines**: Check if the repository belongs to a recognized organization:
  ```bash
  git remote -v
  ```
  - If the remote points to **Learning Equality** (`github.com[:/]learningequality/`), also consult `references/learning-equality-guidelines.md` for Django values-viewsets, KDS component reuse, declarative permissions, WCAG accessibility, and RTLCSS rules.
- **Tooling Prerequisites**: Ensure the GitHub CLI (`gh`) is authenticated (`gh auth status`).

---

## PR Review Workflow

```
1. CONTEXT & SCOPE ──► 2. ANALYZE PR DIFF ──► 3. LOCAL VERIFICATION ──► 4. SUBMIT REVIEW
        │                        │                       │                      │
        ▼                        ▼                       ▼                      ▼
   `gh pr view <id>`        `gh pr diff <id>`       `gh pr checkout <id>`  `gh pr review <id>`
   Check issue context,     Apply 4-scale review;   Run tests, linters,    Submit approved/changes
   scope & constraints      classify findings       and build commands     with markdown report
```

### Step 1: Inspect PR Context, Scope & Linked Issues

Fetch PR metadata and linked issues:
```bash
# Get PR metadata including linked issues and base/head branches
gh pr view <pr-number-or-url> --json number,title,body,baseRefName,headRefName,url,closingIssuesReferences,author

# View comments and discussion history
gh pr view <pr-number-or-url> --comments

# For linked issues, inspect requirements and acceptance criteria
gh issue view <issue-number> --json title,body,labels
```

- **Dependabot / Dependency PRs**: If the author is `app/dependabot` or a bot, follow the **Dependabot & Dependency Update Reviews** workflow in `references/code-review-guidelines.md`. Check freshness first; do not read lockfiles line-by-line.
- **Re-reviews (Delta Reviews)**: If you have already reviewed this PR and new commits were pushed, apply the **Delta Review** procedure in `references/code-review-guidelines.md` to classify prior findings (`RESOLVED`, `CONTESTED`, `ACKNOWLEDGED`, `UNADDRESSED`).
- **Scope Check**: Compare the changed file list against the linked issue's requirements. Changes touching files or introducing features outside the stated scope should be flagged.

### Step 2: Fetch and Analyze the PR Diff

Retrieve the complete diff and changed files:
```bash
# List changed files
gh pr diff <pr-number-or-url> --name-only

# Fetch full diff
gh pr diff <pr-number-or-url>
```

- **Accurate Line Numbers**: When citing line numbers in review findings, read the actual source files or use `nl -ba <file>` to verify exact lines rather than guessing from diff hunks.
- **Question-Driven & Evidence Bar**: Always read the surrounding callers, models, and tests before asserting a bug. If an issue cannot be confirmed by reading the code, phrase it as a question or `suggestion`.
- **Apply 4-Scale Review**:
  1. *Macro Resilience*: Remote timeouts, error swallowing, circuit breakers, resource leaks, race conditions.
  2. *Strategic Architecture*: Inward dependency rule, domain purity, ubiquitous language, ACLs.
  3. *Modularity & Depth*: Deep modules vs. shallow wrappers, information hiding, orthogonality, SRP.
  4. *Micro-Craftsmanship & Tests*: SLAP, CQS, parameter discipline, Primitive Obsession, Test Value lens.

### Step 3: Local Checkout & Empirical Verification

For complex PRs, risky refactors, or database/API modifications, checkout the branch locally and run verification tools:
```bash
# Checkout the PR branch locally
gh pr checkout <pr-number-or-url>

# Run verification suite
make test || pytest || npm test || cargo test
make lint || ruff check . || npm run lint
```

### Step 4: Synthesize Findings and Select Verdict

Classify all findings into the standard 4-tier taxonomy:
- `🚨 Blocker (Must-Fix)`: Invariant bugs, data corruption, security flaws, missing timeouts on remote I/O, error swallowing, scope violations, unmet acceptance criteria.
- `⚠️ Architecture & Design (Should-Fix)`: Shallow wrappers, leaky abstractions, Primitive Obsession, violating SLAP/CQS, over-mocked brittle tests.
- `💡 Tactical Suggestion (Optional)`: Minor polish, non-blocking cleanup, readability notes.
- `✅ Positive Highlights`: Well-designed deep interfaces, excellent domain modeling, solid test invariants.

Determine review action:
- **`--approve`**: No blockers, architecture is sound, minor suggestions are optional.
- **`--request-changes`**: One or more blockers or critical design flaws must be resolved before merging.
- **`--comment`**: Informational feedback, clarification questions, or preliminary assessment.

### Step 5: Submit the Review via GitHub CLI

Format the review using the standard report template in `references/code-review-guidelines.md` and submit:

```bash
# Option A: Submit review from a markdown file (Recommended)
gh pr review <pr-number-or-url> --request-changes --body-file /path/to/review_summary.md

# Option B: Submit review directly
gh pr review <pr-number-or-url> --approve --body "### Summary
Overall architecture is clean and well-tested. Approved with minor optional suggestions noted below.
..."
```

---

## PR Review Etiquette

1. **Distinguish Must-Fix from Nits**: Clearly label non-blocking suggestions with `💡 Suggestion (Optional)` or `Nit:`.
2. **Provide Concrete Code Snippets**: Include markdown diffs or code suggestions showing the remediation.
3. **Thematic Deduplication**: If multiple instances of the same issue exist, reference the primary finding rather than duplicating comments.
4. **Confirm Before Submitting**: In interactive agent sessions, present the drafted review report to the user for confirmation before executing `gh pr review`.
