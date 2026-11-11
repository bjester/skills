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
  version: "1.6"
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

### Step 1: Verify Identity, PR Context, Scope & Linked Issues

Query your active GitHub login, PR metadata, prior discussions, and linked issues:
```bash
# Query active GitHub account login (never echo token values)
gh api user -q .login

# Get PR metadata including author, commits, head OID, and linked issues
gh pr view <pr-number-or-url> --json number,title,body,baseRefName,headRefName,headRefOid,url,closingIssuesReferences,author,commits

# View general conversation comments (does NOT include inline code review threads)
gh pr view <pr-number-or-url> --comments

# Fetch prior review summary bodies and verdicts
gh api repos/{owner}/{repo}/pulls/<pr-number>/reviews --jq '.[] | {user: .user.login, state, commit_id, body}'

# Fetch existing inline code review comments and discussion threads (critical for Delta Reviews)
gh api repos/{owner}/{repo}/pulls/<pr-number>/comments --jq '.[] | {id, path, line: (.line // .original_line), user: .user.login, body}'

# For linked issues, inspect requirements and acceptance criteria
gh issue view <issue-number> --json title,body,labels

# Inspect CI check status and view failure logs
gh pr checks <pr-number-or-url>
gh run view <run-id> --log-failed
```

> [!IMPORTANT]
> **Reviewer Identity Gate (Hard Fail on Self-Review Submission)**: Whenever instructed to stage (`Mode A: Pending Review`) or publish (`Mode B: Autonomous / Published Submission`) a review to GitHub, compare `gh api user -q .login` against `pr.author.login`. If they match, **abort immediately with a hard failure** before calling `POST repos/{owner}/{repo}/pulls/<pr-number>/reviews`:
> `Active gh account '<gh_user>' matches PR author '<pr.author.login>'. Switch to a reviewer account before posting a review to GitHub.`
> Local chat-only PR analysis without posting to GitHub remains permitted.

- **Prior Discussion & Stack Context**: Treat settled maintainer decisions and empirical measurements in prior comments/reviews as active context. Do not re-open settled architectural choices or repeat optional tactical suggestions already declined by the author on this PR or parent PRs in the same stack.
- **Dependabot / Dependency PRs**: If the author is `app/dependabot` or a bot, follow the **Dependabot & Dependency Update Reviews** workflow in the `reviewing-code` skill. Check freshness first; do not read lockfiles line-by-line.
- **Commit-by-Commit Scope & Stacked-Base Check**: Inspect commits (`git log origin/<baseRefName>..<headRefOid> --oneline`) and compare touched files against the linked issue:
  - Flag stacked-PR base mismatches where `baseRefName` pulls unmerged parent-PR commits into the diff, and separate parent-stack commits from the PR's own commits.
  - Classify out-of-scope edits to unrelated modules (including mid-review workarounds added to silence unrelated flaky CI tests or unrequested core/identity mutations) as `🚨 Blocker (Must-Fix)` (`REQUEST_CHANGES`).
- **Adversarial PR-Body & Issue Contract Audit**: Treat shortcuts, simplifications, and `"later issue"` deferrals admitted in the PR description (including `"Reviewer guidance"` sections) as claims to verify against the linked issue's deliverables/testing requirements and downstream data irreversibility (analytics events, persisted records, wire schemas). Never echo unverified author claims or deferrals as `✅ Positive Highlights`.
- **Rebase-Safe Delta Reviews**: When re-reviewing after new pushes:
  1. Fetch the previously reviewed commit and base branch (`git fetch origin <prev_oid> <baseRefName>`) and pick the diff command by history shape so rebasing onto an updated target branch does not flood the delta with upstream commits:
     - *Fast-forward push* (`git merge-base --is-ancestor <prev_oid> <headRefOid>`): `git diff <prev_oid>..<headRefOid>`
     - *Same-base amend or rebase* (`old_base == new_base`): `git diff <prev_oid> <headRefOid>`
     - *Rebase onto newer `baseRefName` commits* (`old_base != new_base`): run `git range-diff <old_base>..<prev_oid> <new_base>..<headRefOid>` to isolate author changes without upstream `old_base..new_base` noise, cross-checking hunk line numbers against `gh pr diff`
     - *Garbage-collected `<prev_oid>`*: fall back to `gh pr diff` while auditing prior review threads.
  2. Classify prior findings per `reviewing-code` (`RESOLVED`, `CONTESTED`, `ACKNOWLEDGED`, `UNADDRESSED`) and audit every fix for fix-induced regressions (such as weakening `toEqual` to `expect.objectContaining`).
  3. Check `CHANGELOG.md` completeness for removed/renamed public or downstream-consumed entry points and kwargs, and verify that manual verification tables or checklists (`docs/*verification*.md`) were populated after human reviews completed.

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

- **Conditional Manual & Browser QA Gate**: When a PR touches frontend routing, session/auth redirects, consent/analytics flows, DOM lifecycles, or lists manual browser QA steps in the PR description:
  - Execute live runtime checks when browser/devserver tooling (such as the `verifying-prs-in-browser` skill, when installed) is available.
  - Skip runtime browser verification when unnecessary (pure backend or CLI changes with no UI/manual QA surface).
  - If live browser checks or integration suites (`pytest -m integration`, devserver checks) are warranted yet cannot run in the current environment, **complete the rest of the review normally**, record the unexecuted checks under `### Verification Status`, and **withhold `APPROVE`**.
- **Multi-Model Adversarial Check (`interrogate`)**: For high-stakes or contested PRs, or when `Co-Authored-By` / `AI usage` notes show the same model family generated the PR, dispatch the diff to a distinct LLM family per `reviewing-code`.

### Step 4: Partition Findings into Inline Comments & Summary Body

Classify actionable findings, questions, and summary highlights clearly:
- `🚨 Blocker (Must-Fix)`: Invariant bugs, crashes, data corruption, security flaws, missing timeouts on remote I/O, error swallowing, out-of-scope commits, unmet acceptance criteria.
- `⚠️ Architecture & Design (Should-Fix)`: Shallow wrappers, leaky abstractions, Primitive Obsession, violating SLAP/CQS, tautological or over-mocked tests.
- `💡 Tactical Suggestion (Optional)`: Non-blocking structural, idiomatic, or readability improvements.
- `❓ Question`: Empirical, architectural, or benchmark inquiries where a defect is not yet confirmed.
- `🧹 Nit`: Minor 1-line polish, naming, or typo fixes.
- `✅ Positive Highlights` *(Summary Body Only)*: Genuinely non-obvious deep interfaces, domain modeling, or invariant coverage.

Partition output into two destinations:

1. **Diff-Verified Inline Comments** (`comments` array in API payload):
   - Restrict strictly to actionable findings and empirical questions whose target line falls within a diff hunk.
   - **Never post `✅ Positive Highlight` comments as inline diff threads** (they leave unresolved threads on the PR and dilute actionable signal).
   - Format:
     - Start comment body with one of the five distinct inline badges: `🚨 **Blocker (Must-Fix)**:`, `⚠️ **Architecture & Design (Should-Fix)**:`, `💡 **Tactical Suggestion (Optional)**:`, `❓ **Question**:`, or `🧹 **Nit**:`.
     - State the violated invariant, risk, or question concisely.
     - **Prose & Tone Discipline (`writing-technical-docs`)**: Apply the `Chat Explanations, Code Reviews & PR Discussions` register from `writing-technical-docs` to all inline comments and summary prose (state the concrete fault or answer in the opening sentence; zero em-dashes, zero negative parallelisms, zero sycophantic filler).
     - Provide a caller- and contract-verified remediation snippet (applying `Rename-Over-Comment` and engine/spec checks from `reviewing-code`).
2. **Review Summary Body** (`body` string in API payload):
   - **Lead Directly with Summary Content (No Heading)**: Omit leading `# Code Review`, `## Principle-Grounded Findings`, `# Summary`, `## Summary`, `### Summary`, or `### Executive Summary` headings when formatting for GitHub review submission. Jump straight into the summary assessment.
   - **Do Not Repeat Inline Comments Item-by-Item**: GitHub already renders every inline comment directly beneath the review summary. Mention key `🚨 Blocker` themes briefly if any exist; for all non-blocking inline categories (`⚠️`, `💡`, `❓`, `🧹`), report **only the count per non-zero category** (for example, `1 ⚠️ Architecture & Design, 2 💡 Tactical Suggestions, 1 🧹 Nit` or a compact count list). Do not re-list each non-blocking inline finding in `body`.
   - **Positive Highlights in Full (Conditional)**: Include all earned `✅ Positive Highlights` here in the summary body, since they are never posted inline. Omit if none stand out.
   - Empirical verification status (exact test/linter commands run, plus any manual/browser or integration checks that could not be executed).
   - **Omit Empty Sections**: Never include empty sections or placeholder text (such as `*(None)*`, `(none)`, or `N/A`). If any section or finding category has no items, eliminate it entirely.
   - **Comments on Lines Outside Diff (Conditional)**: If and only if a finding refers to a file or line outside the PR's diff hunks (which GitHub API rejects as an inline comment with HTTP 422), displace those findings into a dedicated section of the summary body:
     ```markdown
     ### Comments on Lines Outside Diff
     - **path/to/file.ext:L123**: 🚨 **Blocker**: [Finding explanation and remediation]
     ```
     If there are no displaced findings on lines outside the diff hunks, completely omit this section.
   - **Generation Disclosure (GitHub Submission Only)**: When submitting the review to GitHub, the review summary must include a trailing message in italics disclosing how it was generated:
     ```markdown
     *Generated by <agent harness> using model <model>*
     ```
     Replace `<agent harness>` with the active agent harness or runtime environment (e.g., `Antigravity`, `Cursor`, `Claude Code`, `Codex`, `Gemini CLI`) and `<model>` with the exact active model name. This disclosure must only appear when an agent submits the review for a PR to GitHub (do not include it in local review reports or non-GitHub reviews).

Determine review action (`event`) using the **Strict Approval Gate**:
- **`REQUEST_CHANGES`**: One or more `🚨 Blocker (Must-Fix)` findings (including out-of-scope commits or unmet acceptance criteria) must be resolved before merging.
- **`COMMENT`**: Any `⚠️ Architecture & Design` finding is present, **or** any condition below holds even when code looks clean:
  1. Requested manual/browser QA or required integration test suites were not executed.
  2. The diff modifies `.github/workflows/`, `.github/dependabot.yml`, `Dockerfile`, repository-wide dependency/supply-chain policy (`pnpm-workspace.yaml`), or security/privacy/consent gates requiring human maintainer sign-off.
- **`APPROVE`**: Zero blockers, zero `⚠️ Should-Fix` defects, zero unguarded crashes (`TypeError`, `OperationalError`) or contract gaps (never downgrade crashes or contract breaches to optional suggestions under `APPROVE`), all required verification suites executed cleanly, and no governance/workflow policy files require human sign-off.

> [!NOTE]
> Before executing `POST .../reviews` in Step 5, run a final check confirming `gh api user -q .login != pr.author.login`, zero leaked local-report headers, and zero `*(None)*` placeholders.

### Step 5: Draft and Submit Review via GitHub API

Draft the review JSON payload to a file (avoiding shell quoting and escaping errors with Markdown blocks):

```json
{
  "commit_id": "<headRefOid>",
  "body": "Overall architecture is clean, but outbound RPC calls need bounded timeouts before merge.\n\n- 🚨 **Key Blocker**: Missing timeout on payment client (`src/clients/payment.py`)\n- **Inline Comments**: 1 🚨 Blocker, 2 💡 Tactical Suggestions, 1 🧹 Nit\n- ✅ **Positive Highlight**: `OrderAggregate` keeps retry idempotency isolated from transport concerns.\n\n### Verification Status\n- Tests: Passing (`pytest`)\n- Lint: Clean (`ruff check .`)\n\n*Generated by <agent harness> using model <model>*",
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

1. **Use Distinct Inline Badges & Avoid Summary Duplication**: Label inline items with `🚨 Blocker (Must-Fix)`, `⚠️ Architecture & Design (Should-Fix)`, `💡 Tactical Suggestion (Optional)`, `❓ Question`, or `🧹 Nit`. Do not repeat every inline comment in the summary body: note key blockers if any, report counts for non-zero inline categories, and place earned `✅ Positive Highlights` in the summary body only.
2. **Verify Every Code Snippet**: Trace all callers, check linked issue acceptance criteria, and prefer renaming ambiguous identifiers (`Rename-Over-Comment`) before suggesting code changes.
3. **Thematic Deduplication**: If multiple instances of the same issue exist, place an inline comment on the first instance and summarize the pattern in the review body rather than duplicating comments.
4. **Confirm Identity & Payload Before Submitting**: Never post a review when `gh api user -q .login == pr.author.login`. In interactive agent sessions, present the drafted review summary and inline comments to the user for confirmation before executing `gh api`.
5. **AI Generation Disclosure**: When submitting the review to GitHub (whether staged as pending or published directly), ensure the review summary includes the trailing message in italics: `*Generated by <agent harness> using model <model>*`. This disclosure must only appear when submitting the review to GitHub.
6. **Omit Empty Sections & Redundant Summary Headers**: Never include empty sections or placeholder markers like `*(None)*` or `(none)` (e.g., omit `### Comments on Lines Outside Diff` when there are no such comments). When submitting to GitHub, omit leading `Summary`, `Executive Summary`, or `Code Review` headers and begin directly with the summary assessment.
