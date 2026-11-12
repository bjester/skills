---
name: resolving-pr-feedback
description: "Fetch, triage, fix, verify, reply to, and resolve Pull Request review comments and inline review threads across GitHub (gh) and Gitea (gt). Use when addressing reviewer feedback on an open PR, applying surgical fixes, binding local verification to pushed commits, and marking inline threads resolved."
license: MIT - https://github.com/bjester/skills/blob/main/LICENSE
user-invocable: true
compatibility: Git repositories hosted on GitHub (gh) or Gitea (gt)
allowed-tools:
  - read_file
  - write_file
  - run_command
  - grep
  - find_by_name
  - ask_user_question
metadata:
  author: Blaine Jester
  version: "2.0"
---

# Resolving PR Feedback: Review Thread Resolution and Verification

Purpose: Address, verify, and resolve reviewer comments and inline review threads on open GitHub and Gitea pull requests, binding every reply to local verification on the pushed HEAD commit.

```
┌────────────────────────────────────────────────────────────────────────┐
│                  PR FEEDBACK RESOLUTION WORKFLOW                       │
└────────────────────────────────────────────────────────────────────────┘

  1. SELECT & ENUMERATE ──► Forge Gate, Author Identity Gate, & fetch threads
             │
             ▼
  2. TRIAGE FEEDBACK    ──► Categorize into FIX-NOW, CLARIFY, or DEFER
             │
             ▼
  3. SURGICAL FIXES     ──► Implement changes preserving surrounding invariants
             │
             ▼
  4. VERIFY ON HEAD     ──► Run local tests, linter, & bind to new commit SHA
             │
             ▼
  5. PUSH, REPLY &      ──► Push branch first, post SHA-bound replies, &
     RESOLVE                mark addressed inline threads resolved
```

---

## Prerequisites & Architecture

- **Forge Selection & Identity Rules**: Read [references/forge-cli.md](references/forge-cli.md) before executing any remote CLI command to resolve the target repository, select `gh` (GitHub) or `gt` with `--no-input` (Gitea), and run the `Author Identity Gate`.
- **Level 3 Forge Adapters (Load Only the Active Forge)**:
  - **GitHub (`gh`)**: Read [references/github-gh.md](references/github-gh.md) for GraphQL `reviewThreads` enumeration, thread replies, and thread resolution.
  - **Gitea (`gt`)**: Read [references/gitea-gt.md](references/gitea-gt.md) for `gt --no-input` inline comment enumeration, quoted-heredoc replies, and plain-text thread resolution.
  - Load only the adapter matching the active forge so inactive CLI flags and API payloads stay out of context.
- **Complementary Roles**:
  - `reviewing-prs` is the **reviewer-side** skill (audits diffs and authors structured review comments).
  - `resolving-pr-feedback` is the **author-side** skill (retrieves feedback, executes surgical repairs, pushes verified commits, and resolves review threads with empirical proof).

---

## Execution Phases

### Phase 1: Forge Selection, Author Identity Gate & Thread Enumeration

1. Run the `Forge Selection Gate` in [references/forge-cli.md](references/forge-cli.md) to resolve the target repository (`upstream` over `origin`, or `-R OWNER/REPO` when targeting a fork pull request directly) and select `gh` or `gt` (passing `--no-input` on every `gt` command). Then load only the active forge adapter ([references/github-gh.md](references/github-gh.md) or [references/gitea-gt.md](references/gitea-gt.md)).
2. Query the active CLI login (`gh api user -q .login` on GitHub, or `gt api user --jq .login --no-input` on Gitea) and inspect pull request branch metadata and author login (`pr.author.login` on GitHub, or the flat `author` string on Gitea) via the active forge adapter.

> [!IMPORTANT]
> **Author Identity Gate (Hard Fail on Mismatch)**: Compare the active CLI login (`active_login`) against the pull request author login (`pr_author_login`). If they do not match (for example, `gh` or `gt` is authenticated as a reviewer bot via `GH_TOKEN` or `GITEA_TOKEN` while resolving a human author's pull request), **stop immediately with a hard failure** before committing, pushing, replying, or resolving threads:
> `Active <gh|gt> account '<active_login>' does not match PR author '<pr_author_login>'. Authenticate <gh|gt> as '<pr_author_login>' (or unset a bot token override) before resolving feedback.`
> Proceed across mismatched logins **only** when the user explicitly instructs you in the current session to resolve feedback on another author's pull request as a co-maintainer. Never echo token values, and never run unattended credential switches (`gh auth switch`, `gh auth login`, or `gt auth login`).

3. Enumerate all unresolved inline review threads and top-level review bodies using the active forge adapter ([references/github-gh.md](references/github-gh.md) or [references/gitea-gt.md](references/gitea-gt.md)).
4. Filter out resolved threads (`isResolved == true` on GitHub, or any comment in a `[.path, .line, .old_line]` conversation group having `resolver != ""` on Gitea). Record each unresolved thread's root ID, file path, line anchor (`line`, `originalLine`, or `old_line`), reviewer login, and comment history.

---

### Phase 2: Feedback Triage & Action Planning

Categorize every unresolved comment into one of three buckets:

| Category | Description | Action |
|:---|:---|:---|
| **FIX-NOW** | Clear bugs, edge cases, missing unit tests, typos, or naming improvements within scope. | Queue for immediate local implementation. |
| **CLARIFY** | Conflicting feedback from different reviewers, ambiguous suggestions, or architectural trade-offs. | Formulate a concise question for the user or reviewer before altering code. |
| **DEFER** | Feature requests, large structural refactors, or out-of-scope suggestions beyond PR objectives. | Propose tracking in a separate follow-up issue with user consent. |

Present the triage summary to the user before touching code:
- List each thread by file and reviewer.
- State the proposed fix or question.

---

### Phase 3: Surgical Implementation

1. **Inspect Surrounding Context**:
   Read the surrounding file region around the anchored line (`file:line`). Never apply blind regex replacements without reading the function or module scope.
2. **Apply Minimal Targeted Changes**:
   Address the reviewer's concern directly without introducing opportunistic reformatting across unrelated lines. Unrelated modifications bloat the delta diff and force reviewers to re-read unchanged logic.
3. **Preserve Invariants**:
   Keep modifications aligned with project architectural invariants (inward dependency rule, defensive parameter validation, error handling).

---

### Phase 4: Local Verification & Commit Binding

1. **Execute Verification Suite**:
   Run the project's linter and automated test suite locally:
   ```bash
   make test || pytest || npm test || cargo test
   ```
   If a test fails, diagnose and fix the root cause before proceeding.

2. **Commit Changes**:
   Stage and commit only the files modified to address review feedback:
   ```bash
   git commit -m "fix: address review feedback on <component>"
   ```

3. **Bind Verification to Commit SHA**:
   Record the new commit SHA:
   ```bash
   git rev-parse --short HEAD
   ```
   Every reported fix must be explicitly bound to this commit SHA.

---

### Phase 5: Push, Evidence-Backed Reply & Thread Resolution

1. **Push to Remote First**:
   When all addressed fixes are verified locally and committed, push the commit(s) to the pull request branch before posting replies or resolving threads so reviewers can inspect `<SHA>` immediately:
   ```bash
   git push origin <branch-name>
   ```

2. **Reply to Inline Review Threads**:
   Using the exact reply command in the active forge adapter ([references/github-gh.md](references/github-gh.md) or [references/gitea-gt.md](references/gitea-gt.md)), post a reply directly on each addressed inline thread citing the pushed commit `<SHA>`, a brief explanation of the fix, and the verification command and result:
   ```text
   Addressed in commit <SHA>. <Brief explanation of fix>. Verified with `<test command>` (<result>).
   ```

3. **Resolve the Thread**:
   Once the commit is pushed and the reply is posted, mark the addressed thread resolved using the active forge adapter ([references/github-gh.md](references/github-gh.md) or [references/gitea-gt.md](references/gitea-gt.md)).

> [!IMPORTANT]
> Never resolve a review thread without:
> 1. Addressing the core concern in pushed, verified code, or
> 2. Reaching explicit mutual agreement with the reviewer to defer or reject the change.

---

## Anti-Patterns

- **Conversation Comment Dumping**: Posting a single generic top-level comment (`gh pr comment` or `gt pr comment --no-input`) saying "fixed all comments" without replying to or resolving individual inline threads.
- **Phantom Resolution**: Resolving review threads to clear the UI checklist without committing code or running verification.
- **Drive-By Scope Creep**: Using review feedback as an excuse to rewrite unrelated modules or alter project dependencies.
- **Resolving Before Pushing**: Marking threads resolved before pushing the fix to the remote repository, leaving reviewers unable to verify the commit.
- **Wrong-Account Replies**: Replying to or resolving review threads while `gh` or `gt` is authenticated as a reviewer or bot account rather than the pull request author.
