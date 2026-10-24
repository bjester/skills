---
name: resolving-github-pr-feedback
description: "Systematically fetch, categorize, and address review comments and inline review threads on an open GitHub Pull Request using the gh CLI. Classifies feedback, applies targeted fixes, binds verification to updated HEAD, and posts evidence-backed replies."
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
metadata:
  author: Blaine Jester
  version: "1.0"
---

# Resolving GitHub PR Feedback: Review Thread Resolution and Verification

Purpose: Systematically address, verify, and resolve reviewer comments and inline review threads on open GitHub Pull Requests using the gh CLI, ensuring every change is backed by local verification bound to the new HEAD commit.

```
┌────────────────────────────────────────────────────────────────────────┐
│               GITHUB PR FEEDBACK RESOLUTION WORKFLOW                   │
└────────────────────────────────────────────────────────────────────────┘

  1. FETCH & ENUMERATE  ──► Inspect PR review threads via GraphQL / `gh api`
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
  5. REPLY & RESOLVE    ──► Reply with commit & verification evidence; resolve threads
```

---

## Prerequisites & Architecture

- **Tooling**: Ensure GitHub CLI (`gh`) is installed and authenticated (`gh auth status`).
- **Complementary Roles**:
  - `reviewing-github-prs` is the **reviewer-side** skill (audits diffs and authors structured review comments).
  - `resolving-github-pr-feedback` is the **author-side** skill (retrieves feedback, executes surgical repairs, and resolves review threads with empirical proof).

---

## Execution Phases

### Phase 1: Authentication & Thread Enumeration

1. Verify GitHub CLI authentication:
   ```bash
   gh auth status
   ```
2. Inspect PR branch metadata:
   ```bash
   gh pr view --json number,title,baseRefName,headRefName,headRefOid
   ```

> [!WARNING]
> `gh pr view --comments` only outputs top-level issue conversation comments. It completely omits inline diff review threads. You must query inline review threads explicitly.

3. Enumerate all active review threads using the GitHub GraphQL API:
   ```bash
   gh api graphql -f query='
     query($owner: String!, $repo: String!, $pr: Int!) {
       repository(owner: $owner, name: $repo) {
         pullRequest(number: $pr) {
           headRefOid
           reviewThreads(first: 100) {
             nodes {
               id
               isResolved
               path
               line
               originalLine
               comments(first: 10) {
                 nodes {
                   id
                   author { login }
                   body
                   createdAt
                 }
               }
             }
           }
         }
       }
     }' -F owner=':owner' -F repo=':repo' -F pr=<pr_number>
   ```
4. Filter out threads where `isResolved == true`. Record each unresolved thread's ID, file path, line anchor, reviewer login, and comment body.

---

### Phase 2: Feedback Triage & Action Planning

Categorize every unresolved comment into one of three buckets:

| Category | Description | Action |
|:---|:---|:---|
| **FIX-NOW** | Clear bugs, edge cases, missing unit tests, typos, or naming improvements within scope. | Queue for immediate local implementation. |
| **CLARIFY** | Conflicting feedback from different reviewers, ambiguous suggestions, or architectural trade-offs. | Formulate concise question for the user or reviewer before altering code. |
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
   Ensure modifications adhere to project architectural invariants (inward dependency rule, defensive parameter validation, error handling).

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

### Phase 5: Evidence-Backed Reply & Thread Resolution

1. **Reply to Inline Review Threads**:
   Post a reply directly to the specific review thread using the GraphQL API or REST endpoint:
   ```bash
   gh api graphql -f query='
     mutation($threadId: ID!, $body: String!) {
       addPullRequestReviewThreadReply(input: {pullRequestReviewThreadId: $threadId, body: $body}) {
         comment { id url }
       }
     }' -f threadId="<THREAD_ID>" -f body="Addressed in commit <SHA>. <Brief explanation of fix>. Verified with \`<test command>\` (<result>)."
   ```

2. **Resolve the Thread**:
   Once the fix is committed, verified, and replied to, mark the thread resolved:
   ```bash
   gh api graphql -f query='
     mutation($threadId: ID!) {
       resolveReviewThread(input: {threadId: $threadId}) {
         thread { id isResolved }
       }
     }' -f threadId="<THREAD_ID>"
   ```

> [!IMPORTANT]
> Never resolve a review thread without:
> 1. Actually addressing the core concern in code, or
> 2. Reaching explicit mutual agreement with the reviewer to defer or reject the change.

3. **Push to Remote**:
   When all threads are addressed and verified, push the commit(s) to the PR branch:
   ```bash
   git push origin <branch-name>
   ```

---

## Anti-Patterns

- **Conversation Comment Dumping**: Posting a single generic top-level comment (`gh pr comment`) saying "fixed all comments" without replying to or resolving individual inline threads.
- **Phantom Resolution**: Resolving review threads to clear the UI checklist without actually committing code or running verification.
- **Drive-By Scope Creep**: Using review feedback as an excuse to rewrite unrelated modules or alter project dependencies.
- **Resolving Before Pushing**: Marking threads resolved before the fix is pushed to the remote repository, leaving reviewers unable to verify the commit.
