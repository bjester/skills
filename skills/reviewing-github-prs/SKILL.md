---
name: reviewing-github-prs
description: "Review GitHub Pull Requests using the GitHub CLI (`gh`). Evaluates PR diffs against foundational software engineering invariants, modular depth, resilience, and test quality, and drafts/submits structured reviews with inline diff comments via the GitHub API."
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
  version: "1.4"
---

# Reviewing GitHub Pull Requests

Purpose: Conduct thorough, constructive, and principle-grounded GitHub Pull Request reviews using the GitHub CLI (`gh`). Evaluate PR diffs across all engineering scales and submit clear, structured review feedback with inline diff comments.

## Prerequisites & Shared Guidelines

- **Consult Review Guidelines**: Always refer to the `reviewing-code` skill for the 4 scales of code review, principle checklists, finding taxonomies, Delta reviews, Dependabot workflows, and the standard review template.
- **Reference Software Engineering Invariants**: Consult the `engineering-software` skill for foundational architectural rules, modular depth, defensive error handling, and testing disciplines.
- **Organization-Specific Guidelines**: Check if the repository belongs to a recognized organization:
  ```bash
  git remote -v
  ```
  - If the remote points to **Learning Equality** (`github.com[:/]learningequality/`), also consult the `learning-equality` skill for Django values-viewsets, KDS component reuse, declarative permissions, WCAG accessibility, and RTLCSS rules.
- **Tooling Prerequisites**: Ensure the GitHub CLI (`gh`) is authenticated (`gh auth status`).

---

## PR Review Workflow

```
1. CONTEXT & SCOPE ──► 2. ANALYZE PR DIFF ──► 3. LOCAL VERIFICATION ──► 4. PARTITION FINDINGS ──► 5. SUBMIT VIA GH API
        │                        │                       │                      │                       │
        ▼                        ▼                       ▼                      ▼                       ▼
   `gh pr view <id>`        `gh pr diff <id>`       `gh pr checkout <id>`   Split into summary      `gh api .../reviews`
   Check issue context,     Apply 4-scale review;   Run tests, linters,     body & diff-verified    Submit pending or
   scope & constraints      verify diff hunk lines  and build suite         inline comments         published review
```

### Step 1: Inspect PR Context, Scope & Linked Issues

Fetch PR metadata and linked issues:
```bash
# Get PR metadata including linked issues and base/head branches
gh pr view <pr-number-or-url> --json number,title,body,baseRefName,headRefName,url,closingIssuesReferences,author

# View general conversation comments (does NOT include inline code review threads)
gh pr view <pr-number-or-url> --comments

# Fetch existing inline code review comments and discussion threads (critical for Delta Reviews)
gh api repos/{owner}/{repo}/pulls/<pr-number>/comments --jq '.[] | {id, path, line: (.line // .original_line), user: .user.login, body}'

# For linked issues, inspect requirements and acceptance criteria
gh issue view <issue-number> --json title,body,labels

# Inspect CI check status and view failure logs
gh pr checks <pr-number-or-url>
gh run view <run-id> --log-failed
```

- **Dependabot / Dependency PRs**: If the author is `app/dependabot` or a bot, follow the **Dependabot & Dependency Update Reviews** workflow in the `reviewing-code` skill. Check freshness first; do not read lockfiles line-by-line.
- **Re-reviews (Delta Reviews)**: If you have already reviewed this PR and new commits were pushed, apply the **Delta Review** procedure in the `reviewing-code` skill to classify prior findings (`RESOLVED`, `CONTESTED`, `ACKNOWLEDGED`, `UNADDRESSED`).
- **Scope Check**: Compare the changed file list against the linked issue's requirements. Changes touching files or introducing features outside the stated scope should be flagged.

### Step 2: Fetch and Analyze the PR Diff

Retrieve the complete diff and changed files:
```bash
# List changed files
gh pr diff <pr-number-or-url> --name-only

# Fetch full diff
gh pr diff <pr-number-or-url>
```

- **Accurate Line Numbers & Diff Hunk Verification**:
  - For inline comments, GitHub requires the target line to exist within an active diff hunk on the chosen side.
  - When inspecting code with `nl -ba <file>`, cross-reference against `gh pr diff <pr-number-or-url> -- <file>`:
    - Check the hunk header: `@@ -os,oc +ns,nc @@`
    - For additions, modifications, or unchanged context (`side: "RIGHT"`): target line must fall within `[ns, ns + nc - 1]`.
    - For deletions (`side: "LEFT"`): target line must fall within `[os, os + oc - 1]`.
  - If a finding references code outside of any diff hunk in that file, mark it for displacement into the review summary body (see Step 4).
- **Question-Driven & Evidence Bar**: Always read the surrounding callers, models, and tests before asserting a bug. If an issue cannot be confirmed by reading the code, phrase it as a question or `suggestion`.
- **Blame Deleted or Weakened Guards (`-` Lines)**: Reviewers naturally focus on `+` additions. Whenever a diff deletes or weakens a validation check, authorization guard, timeout, rate limit, lock, or error handler (`-` lines), run `git log -S` / `git blame` (or the `investigating-code-lineage` skill) on the removed code to verify whether it was originally added for an earlier security defect or bugfix.
- **Apply 4-Scale Review**:
  1. *Macro Resilience*: Remote timeouts, error swallowing, circuit breakers, resource leaks, race conditions.
  2. *Strategic Architecture*: Inward dependency rule, domain purity, ubiquitous language, ACLs.
  3. *Modularity & Depth*: Deep modules vs. shallow wrappers, information hiding, orthogonality, SRP.
  4. *Micro-Craftsmanship & Tests*: SLAP, CQS, parameter discipline, Primitive Obsession, Test Value lens, Comment Hygiene.
- **Blast Radius Analysis**: For sensitive changes, identify the load-bearing safety fact and look where grep stops per the `analyzing-blast-radius` skill.

### Step 3: Local Checkout & Empirical Verification

For complex PRs, risky refactors, or database/API modifications, checkout the branch locally and run verification tools:

> [!WARNING]
> **Untrusted PR Checkout Safety**: Before executing `make test`, `npm test`, or build scripts on an external PR after `gh pr checkout`, inspect any diff changes to `Makefile`, `package.json` scripts, `conftest.py`, or `.github/workflows/` from Step 2 so PR-controlled code cannot execute malicious hooks or exfiltrate local secrets.

```bash
# Checkout the PR branch locally
gh pr checkout <pr-number-or-url>

# Run verification suite
make test || pytest || npm test || cargo test
make lint || ruff check . || npm run lint
```

- **Multi-Model Adversarial Check (`interrogate`)**: For high-stakes or contested PRs, dispatch the PR diff to 2+ distinct LLM families. High-agreement findings across diverse models serve as high-confidence blockers in Step 4.

### Step 4: Partition Findings into Inline Comments & Summary Body

Classify all findings into the standard 4-tier taxonomy:
- `🚨 Blocker (Must-Fix)`: Invariant bugs, data corruption, security flaws, missing timeouts on remote I/O, error swallowing, scope violations, unmet acceptance criteria.
- `⚠️ Architecture & Design (Should-Fix)`: Shallow wrappers, leaky abstractions, Primitive Obsession, violating SLAP/CQS, over-mocked brittle tests.
- `💡 Tactical Suggestion (Optional)`: Minor polish, non-blocking cleanup, readability notes.
- `✅ Positive Highlights`: Well-designed deep interfaces, excellent domain modeling, solid test invariants.

Partition findings into two destinations:

1. **Diff-Verified Inline Comments** (`comments` array in API payload):
   - Findings whose target line falls within a diff hunk.
   - Format:
     - Start comment body with bold severity badge: e.g. `🚨 **Blocker (Must-Fix)**`, `⚠️ **Architecture & Design (Should-Fix)**`, `💡 **Tactical Suggestion (Optional)**`, `✅ **Positive Highlight**`.
     - State the violated invariant or risk concisely.
     - Provide a concrete code diff or remediation snippet.
2. **Review Summary Body** (`body` string in API payload):
   - **Lead Directly with Summary Content (No Heading)**: Omit leading `# Summary`, `## Summary`, `### Summary`, or `### Executive Summary` headings when formatting for GitHub review submission. The PR review container in GitHub already establishes review context, so jump straight into the summary text and overall assessment.
   - Bulleted list of findings by severity, referencing the inline comments rather than duplicating entire diffs.
   - Empirical verification status (test runner and linter output).
   - **Omit Empty Sections**: Never include empty sections or placeholder text (such as `*(None)*`, `(none)`, or `N/A`). If any section or finding category has no items, eliminate it entirely.
   - **Comments on Lines Outside Diff (Conditional)**: If and only if a finding refers to a file or line outside the PR's diff hunks (which GitHub API rejects as an inline comment with HTTP 422), displace those findings into a dedicated section of the summary body:
     ```markdown
     ### Comments on Lines Outside Diff
     - **path/to/file.ext:L123** — 🚨 **Blocker**: [Finding explanation and remediation]
     ```
     If there are no displaced findings on lines outside the diff hunks, completely omit this section.
   - **Generation Disclosure (GitHub Submission Only)**: When submitting the review to GitHub, the review summary must include a trailing message in italics disclosing how it was generated:
     ```markdown
     *Generated by <agent harness> using model <model>*
     ```
     Replace `<agent harness>` with the active agent harness or runtime environment (e.g., `Antigravity`, `Cursor`, `Claude Code`, `Codex`, `Gemini CLI`) and `<model>` with the active model name (e.g., `Gemini 3.8 Flash`, `Claude 3.5 Sonnet`, `GPT-4o`). This disclosure must only appear when an agent submits the review for a PR to GitHub (do not include it in local review reports or non-GitHub reviews).

Determine review action (`event`):
- **`REQUEST_CHANGES`**: One or more `🚨 Blocker (Must-Fix)` findings must be resolved before merging.
- **`COMMENT`**: Only `⚠️ Architecture & Design`, `💡 Tactical Suggestion`, or `✅ Positive Highlights` are present (no blockers).
- **`APPROVE`**: Zero blockers, zero required changes, clean verification suite (praise-only is fine).

> [!NOTE]
> Do not approve a PR that has unresolved blockers or outstanding change requests.

### Step 5: Draft and Submit Review via GitHub API

Draft the review JSON payload to a file (avoiding shell quoting and escaping errors with Markdown blocks):

```json
{
  "commit_id": "<headRefOid>",
  "body": "Overall architecture is clean and well-structured, but requires timeout protections on outbound RPC calls.\n\n### Findings Summary\n- 🚨 **Blocker**: Missing timeout on payment client (`src/clients/payment.py`)\n- 💡 **Suggestion**: Prefer domain enum over raw string flag (`src/models/order.py`)\n\n### Verification Status\n- Tests: Passing (`pytest`)\n- Lint: Clean (`ruff check .`)\n\n*Generated by <agent harness> using model <model>*",
  "comments": [
    {
      "path": "src/clients/payment.py",
      "line": 42,
      "side": "RIGHT",
      "body": "🚨 **Blocker (Must-Fix)**: Remote network calls must specify an explicit, bounded deadline.\n\n**Principle**: Scale 1: Macro Resilience / Explicit Timeouts\n\n```python\n# Suggested fix:\nresponse = self.http_client.post(url, json=payload, timeout=5.0)\n```"
    }
  ]
}
```

- **Deterministic Commit Binding**: Include `"commit_id": "<headRefOid>"` (obtain via `gh pr view --json headRefOid -q .headRefOid`) at the top level of the review JSON payload to bind comments deterministically to the reviewed commit.
- **Multi-Line Comment Spans**: For findings spanning multiple lines within the same diff hunk, add `"start_line"` and `"start_side"` to the comment object (e.g. `"start_line": 40, "start_side": "RIGHT", "line": 45, "side": "RIGHT"`).

#### Submission Modes

- **Mode A: Pending Review (Default & Recommended)**:
  Omit the `"event"` field in the JSON payload:
  ```bash
  gh api repos/{owner}/{repo}/pulls/<pr-number>/reviews \
    --method POST \
    --input /path/to/review_payload.json
  ```
  *(Note: GitHub CLI automatically substitutes `{owner}` and `{repo}` with the active repository).*
  This stages the review as **Pending** in GitHub. The agent presents the review summary to the user with a link:
  `https://github.com/{owner}/{repo}/pull/<pr-number>/files` -> click **Finish your review** to inspect inline comments, edit, and publish.

- **Mode B: Autonomous / Published Submission**:
  When the user explicitly instructs the agent to publish directly without a staging step, include the `"event"` field in the JSON payload (`"REQUEST_CHANGES"`, `"COMMENT"`, or `"APPROVE"`):
  ```bash
  gh api repos/{owner}/{repo}/pulls/<pr-number>/reviews \
    --method POST \
    --input /path/to/review_payload.json
  ```

#### Handling HTTP 422 Errors

- If GitHub returns HTTP 422 (`Line could not be resolved` or `pull request review thread position is invalid`), an inline comment line was outside the diff hunk.
- Do NOT guess line numbers or submit probe reviews to GitHub.
- Remove the rejected comment from `comments[]`, append it to the `### Comments on Lines Outside Diff` section in `body` (creating the section if it does not yet exist), and re-run.

---

## PR Review Etiquette

1. **Distinguish Must-Fix from Nits**: Clearly label non-blocking suggestions with `💡 Suggestion (Optional)` or `Nit:`.
2. **Provide Concrete Code Snippets**: Include markdown diffs or code suggestions showing the remediation in inline comments.
3. **Thematic Deduplication**: If multiple instances of the same issue exist, place an inline comment on the first instance and summarize the pattern in the review body rather than duplicating comments.
4. **Confirm Before Submitting**: In interactive agent sessions, present the drafted review summary and inline comments to the user for confirmation before executing `gh api`.
5. **AI Generation Disclosure**: When submitting the review to GitHub (whether staged as pending or published directly), ensure the review summary includes the trailing message in italics: `*Generated by <agent harness> using model <model>*`. This disclosure must only appear when submitting the review to GitHub.
6. **Omit Empty Sections & Redundant Summary Headers**: Never include empty sections or placeholder markers like `*(None)*` or `(none)` (e.g., omit `### Comments on Lines Outside Diff` when there are no such comments). When submitting to GitHub, omit leading `Summary` or `Executive Summary` headers and begin directly with the summary assessment.
