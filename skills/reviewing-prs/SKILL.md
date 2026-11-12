---
name: reviewing-prs
description: "Review GitHub and Gitea Pull Requests using the gh or gt CLI. Use when auditing PR diffs across four software engineering scales, performing rebase-safe delta reviews, enforcing reviewer identity and strict approval gates, and staging or publishing diff-verified inline review comments. For author-side review thread resolution, use resolving-pr-feedback."
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
  - task
metadata:
  author: Blaine Jester
  version: "2.0"
---

# Reviewing Pull Requests

Purpose: Conduct principle-grounded Pull Request reviews across GitHub (`gh`) and Gitea (`gt`), evaluating PR diffs across four engineering scales and submitting structured review feedback with diff-verified inline comments.

## Prerequisites & Shared Guidelines

- **Consult Review Guidelines**: Always refer to the `reviewing-code` skill for the 4 scales of code review, principle checklists, finding taxonomies, Delta reviews, Dependabot workflows, and the standard review template.
- **Reference Software Engineering Invariants**: Consult the `engineering-software` skill for foundational architectural rules, modular depth, defensive error handling, and testing disciplines.
- **Organization-Specific Guidelines**: Check `git remote -v` to see if the repository belongs to a recognized organization. If the remote points to **Learning Equality** (`github.com[:/]learningequality/`), also consult the `learning-equality` skill for Django values-viewsets, KDS component reuse, declarative permissions, WCAG accessibility, and RTLCSS rules.
- **Forge Selection Gate**: Read [references/forge-cli.md](references/forge-cli.md) first to resolve the target repository (`upstream` vs. `origin`, explicit URL, or `-R OWNER/REPO`), select `gh` (GitHub) or `gt` with `--no-input` (Gitea), and verify CLI authentication.

---

## PR Review Workflow

```
1. FORGE & CONTEXT ──► 2. ANALYZE PR DIFF ──► 3. LOCAL VERIFICATION ──► 4. PARTITION FINDINGS ──► 5. SUBMIT REVIEW
         │                      │                       │                        │                        │
         ▼                      ▼                       ▼                        ▼                        ▼
   Select `gh` or `gt`    Fetch PR diff & files   Checkout PR safely       Split into summary       Stage pending (Mode A)
   Inspect identity,      Apply 4-scale review &  Run tests, linters,      body & diff-verified     or publish (Mode B)
   issues, threads & CI   verify diff hunk lines  and browser QA checks    inline comments          via active adapter
```

### Step 1: Verify Forge, Identity, PR Context, Scope & Linked Issues

1. Run the `Forge Selection Gate` in [references/forge-cli.md](references/forge-cli.md) to select the target repository and CLI binary (`gh` or `gt --no-input`).
2. Read **only** the adapter matching the active forge for exact CLI commands, JSON field names, and submission payloads:
   - **GitHub (`gh`)**: Read [references/github-gh.md](references/github-gh.md).
   - **Gitea (`gt`)**: Read [references/gitea-gt.md](references/gitea-gt.md).
3. Using the active adapter, query your active CLI login, PR metadata (author, base/head refs, head commit SHA, URL), commit list, conversation comments, prior review summaries, existing inline review threads, linked issue acceptance criteria, and CI check statuses/failed logs.

> [!IMPORTANT]
> **Reviewer Identity Gate (Hard Fail on Self-Review Submission)**: Whenever instructed to stage (`Mode A: Pending Review`) or publish (`Mode B: Autonomous / Published Submission`) a review to GitHub or Gitea, compare your active CLI login (`gh api user -q .login` or `gt api user --jq .login --no-input`) against the PR author login (`pr.author.login` on `gh`, or flat `author` string on `gt`) case-insensitively per [references/forge-cli.md](references/forge-cli.md). If they match, **abort immediately with a hard failure** before calling the review submission API or CLI:
> `Active <gh|gt> account '<active_login>' matches PR author '<pr_author_login>'. Switch to a reviewer account before posting a review.`
> Local chat-only PR analysis without posting to GitHub or Gitea remains permitted.

- **Prior Discussion & Stack Context**: Treat settled maintainer decisions and empirical measurements in prior comments/reviews as active context. Do not re-open settled architectural choices or repeat optional tactical suggestions already declined by the author on this PR or parent PRs in the same stack.
- **Dependabot / Dependency PRs**: If the author is `app/dependabot`, `dependabot[bot]`, Renovate, or a dependency bot, follow the **Dependabot & Dependency Update Reviews** workflow in the `reviewing-code` skill. Check freshness first and do not read lockfiles line-by-line.
- **Commit-by-Commit Scope & Stacked-Base Check**: Inspect commits (`git log origin/<base_ref>..<head_sha> --oneline`) and compare touched files against the linked issue:
  - Flag stacked-PR base mismatches where `<base_ref>` pulls unmerged parent-PR commits into the diff, and separate parent-stack commits from the PR's own commits.
  - Classify out-of-scope edits to unrelated modules (including mid-review workarounds added to silence unrelated flaky CI tests or unrequested core/identity mutations) as `🚨 Blocker (Must-Fix)` (`REQUEST_CHANGES`).
- **Adversarial PR-Body & Issue Contract Audit**: Treat shortcuts, simplifications, and `"later issue"` deferrals admitted in the PR description (including `"Reviewer guidance"` sections) as claims to verify against the linked issue's deliverables/testing requirements and downstream data irreversibility (analytics events, persisted records, wire schemas). Never echo unverified author claims or deferrals as `✅ Positive Highlights`.
- **Rebase-Safe Delta Reviews**: When re-reviewing after new pushes:
  1. Fetch the previously reviewed commit and base branch (`git fetch origin <prev_oid> <base_ref>`) and pick the diff command by history shape so rebasing onto an updated target branch does not flood the delta with upstream commits:
     - *Fast-forward push* (`git merge-base --is-ancestor <prev_oid> <head_sha>`): `git diff <prev_oid>..<head_sha>`
     - *Same-base amend or rebase* (`old_base == new_base`): `git diff <prev_oid> <head_sha>`
     - *Rebase onto newer `<base_ref>` commits* (`old_base != new_base`): run `git range-diff <old_base>..<prev_oid> <new_base>..<head_sha>` to isolate author changes without upstream `old_base..new_base` noise, cross-checking hunk line numbers against `gh pr diff` or `gt pr diff --no-input`
     - *Garbage-collected `<prev_oid>`*: fall back to the full PR diff via the active forge adapter while auditing prior review threads.
  2. Classify prior findings per `reviewing-code` (`RESOLVED`, `CONTESTED`, `ACKNOWLEDGED`, `UNADDRESSED`) and audit every fix for fix-induced regressions (such as weakening `toEqual` to `expect.objectContaining`).
  3. Check `CHANGELOG.md` completeness for removed/renamed public or downstream-consumed entry points and kwargs, and verify that manual verification tables or checklists (`docs/*verification*.md`) were populated after human reviews completed.

### Step 2: Fetch and Analyze the PR Diff

Retrieve changed file paths and the full unified diff using the active forge adapter ([references/github-gh.md](references/github-gh.md) or [references/gitea-gt.md](references/gitea-gt.md)).

- **Accurate Line Numbers & Diff Hunk Verification**:
  - Both GitHub and Gitea require every inline comment target line to fall inside an active diff hunk (`@@ -os,oc +ns,nc @@`): `[ns, ns + nc - 1]` for additions, modifications, or context lines (`side: "RIGHT"` on `gh`, `new_position` on `gt`) and `[os, os + oc - 1]` for deletions (`side: "LEFT"` on `gh`, `old_position` on `gt`).
  - Cross-reference `nl -ba <file>` against the single-file PR diff per the active adapter. If a finding targets code outside every diff hunk in that file, mark it for displacement into the review summary body (`### Comments on Lines Outside Diff` in Step 4).
- **Question-Driven & Evidence Bar**: Always read surrounding callers, models, and tests before asserting a bug. If an issue cannot be confirmed by reading the code, phrase it as a question (`❓ Question`) or optional suggestion.
- **Blame Deleted or Weakened Guards (`-` Lines)**: Reviewers naturally focus on `+` additions. Whenever a diff deletes or weakens a validation check, authorization guard, timeout, rate limit, lock, or error handler (`-` lines), run `git log -S` / `git blame` (or the `investigating-code-lineage` skill) on the removed code to verify whether it was added for an earlier security defect or bugfix.
- **Apply 4-Scale Review**:
  1. *Macro Resilience*: Remote timeouts, error swallowing, circuit breakers, resource leaks, race conditions.
  2. *Strategic Architecture*: Inward dependency rule, domain purity, ubiquitous language, ACLs.
  3. *Modularity & Depth*: Deep modules vs. shallow wrappers, information hiding, orthogonality, SRP.
  4. *Micro-Craftsmanship & Tests*: SLAP, CQS, parameter discipline, Primitive Obsession, Test Value lens, Comment Hygiene.
- **Blast Radius Analysis**: For sensitive changes, identify the load-bearing safety fact and look where grep stops per the `analyzing-blast-radius` skill.

### Step 3: Local Checkout & Empirical Verification

For complex PRs, risky refactors, or database/API modifications, check out the branch locally via the active forge adapter and run verification suites:

> [!WARNING]
> **Untrusted PR Checkout Safety**: Before executing `make test`, `npm test`, or build scripts on an external PR after `gh pr checkout` or `gt pr checkout --no-input`, inspect any diff changes to `Makefile`, `package.json` scripts, `conftest.py`, `.github/workflows/`, or `.gitea/workflows/` from Step 2 so PR-controlled code cannot execute malicious hooks or exfiltrate local secrets.

```bash
# After checking out via the active adapter (confirm first if local modifications exist):
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

1. **Diff-Verified Inline Comments**:
   - Restrict strictly to actionable findings and empirical questions whose target line falls within a diff hunk.
   - **Never post `✅ Positive Highlight` comments as inline diff threads** (they leave unresolved threads on the PR and dilute actionable signal).
   - Start each comment body with one of the five distinct inline badges: `🚨 **Blocker (Must-Fix)**:`, `⚠️ **Architecture & Design (Should-Fix)**:`, `💡 **Tactical Suggestion (Optional)**:`, `❓ **Question**:`, or `🧹 **Nit**:`.
   - State the violated invariant, risk, or question concisely.
   - **Prose & Tone Discipline (`writing-technical-docs`)**: Apply the `Chat Explanations, Code Reviews & PR Discussions` register from `writing-technical-docs` to all inline comments and summary prose (state the concrete fault or answer in the opening sentence, with zero em-dashes, zero negative parallelisms, and zero sycophantic filler).
   - Provide a caller- and contract-verified remediation snippet (applying `Rename-Over-Comment` and engine/spec checks from `reviewing-code`).
2. **Review Summary Body**:
   - **Lead Directly with Summary Content (No Heading)**: Omit leading `# Code Review`, `## Principle-Grounded Findings`, `# Summary`, `## Summary`, `### Summary`, or `### Executive Summary` headings when formatting for GitHub or Gitea review submission. Jump straight into the summary assessment.
   - **Do Not Repeat Inline Comments Item-by-Item**: Both GitHub and Gitea render every inline comment alongside the review summary. Mention key `🚨 Blocker` themes briefly if any exist. For all non-blocking inline categories (`⚠️`, `💡`, `❓`, `🧹`), report **only the count per non-zero category** (for example, `1 ⚠️ Architecture & Design, 2 💡 Tactical Suggestions, 1 🧹 Nit`). Do not re-list each non-blocking inline finding in the summary body.
   - **Positive Highlights in Full (Conditional)**: Include all earned `✅ Positive Highlights` in the summary body, because they are never posted inline. Omit if none stand out.
   - **Empirical Verification Status**: Report exact test/linter commands run, plus any manual/browser or integration checks that could not be executed (`### Verification Status`).
   - **Omit Empty Sections**: Never include empty sections or placeholder text (such as `*(None)*`, `(none)`, or `N/A`). If any section or finding category has no items, eliminate it completely.
   - **Comments on Lines Outside Diff (Conditional)**: Only when a finding refers to a file or line outside the PR's diff hunks, displace those findings into a dedicated section of the summary body:
     ```markdown
     ### Comments on Lines Outside Diff
     - **path/to/file.ext:L123**: 🚨 **Blocker**: [Finding explanation and remediation]
     ```
     Completely omit this section when zero findings fall outside the diff hunks.
   - **Generation Disclosure (Remote PR Submission Only)**: When submitting the review to GitHub or Gitea, end the review summary with a trailing message in italics disclosing how it was generated:
     ```markdown
     *Generated by <agent harness> using model <model>*
     ```
     Replace `<agent harness>` with the active agent harness (`Antigravity`, `Cursor`, `Claude Code`, `Codex`, `Gemini CLI`) and `<model>` with the exact active model name. Include this disclosure only when submitting the review to GitHub or Gitea (omit it from local chat-only review reports).

Determine the review verdict using the **Strict Approval Gate**:
- **`REQUEST_CHANGES`**: One or more `🚨 Blocker (Must-Fix)` findings (including out-of-scope commits or unmet acceptance criteria) must be resolved before merging.
- **`COMMENT`**: Any `⚠️ Architecture & Design` finding is present, **or** any condition below holds even when code looks clean:
  1. Requested manual/browser QA or required integration test suites were not executed.
  2. The diff modifies `.github/workflows/`, `.gitea/workflows/`, `.github/dependabot.yml`, `Dockerfile`, repository-wide dependency/supply-chain policy (`pnpm-workspace.yaml`), or security/privacy/consent gates requiring human maintainer sign-off.
- **`APPROVE`**: Zero blockers, zero `⚠️ Should-Fix` defects, zero unguarded crashes (`TypeError`, `OperationalError`) or contract gaps (never downgrade crashes or contract breaches to optional suggestions under `APPROVE`), all required verification suites executed cleanly, and no governance/workflow policy files require human sign-off.

> [!NOTE]
> Before executing Step 5, run a final check confirming `active_login != pr_author_login` (case-insensitive), zero leaked local-report headers, and zero `*(None)*` placeholders.

### Step 5: Draft and Submit Review via Active Forge Adapter

Bind every submitted review deterministically to the reviewed head commit (`commit_id` on GitHub, or re-verifying `head_sha` immediately before `gt pr review` on Gitea while omitting `--commit` so `gt` validates inline diff lines) and write review bodies and comment arrays to temporary files rather than shell-escaped command strings. Execute the exact commands and payload schemas in [references/github-gh.md](references/github-gh.md) (GitHub) or [references/gitea-gt.md](references/gitea-gt.md) (Gitea):

- **Mode A: Pending Review (Default & Recommended)**: Stages the review as **Pending** on GitHub (omitting `"event"` in `POST repos/{owner}/{repo}/pulls/<pr>/reviews`) or Gitea (`gt pr review <num> --pending ... --no-input`, checking `gt pr review list <num> --no-input --json id,state,author` and `head_sha` first). Present the drafted review summary and the pull request files URL (`.../files`) so the human reviewer can inspect inline comments, edit, and publish.
- **Mode B: Autonomous / Published Submission**: Used only when the user explicitly instructs the agent to publish directly without staging. Submits the verdict selected by the **Strict Approval Gate** (`REQUEST_CHANGES` / `--request-changes`, `COMMENT` / `--comment`, or `APPROVE` / `--approve`).
- **Outside-Diff Rejection Recovery**: If `gh` returns HTTP 422 or `gt` rejects a diff position before submitting the review, do not guess line numbers or send probe reviews. Move the rejected item into `### Comments on Lines Outside Diff` inside the summary body and re-submit.

---

## PR Review Etiquette

1. **Use Distinct Inline Badges & Avoid Summary Duplication**: Label inline items with `🚨 Blocker (Must-Fix)`, `⚠️ Architecture & Design (Should-Fix)`, `💡 Tactical Suggestion (Optional)`, `❓ Question`, or `🧹 Nit`. Do not repeat every inline comment in the summary body: note key blockers if any, report counts for non-zero inline categories, and place earned `✅ Positive Highlights` in the summary body only.
2. **Verify Every Code Snippet**: Trace all callers, check linked issue acceptance criteria, and prefer renaming ambiguous identifiers (`Rename-Over-Comment`) before suggesting code changes.
3. **Thematic Deduplication**: If multiple instances of the same issue exist, place an inline comment on the first instance and summarize the pattern in the review body rather than duplicating comments.
4. **Confirm Identity & Payload Before Submitting**: Never post a review when `active_login == pr_author_login` (case-insensitive). In interactive agent sessions, present the drafted review summary and inline comments to the user for confirmation before executing `gh api` or `gt pr review --no-input`.
5. **AI Generation Disclosure**: When submitting the review to GitHub or Gitea (whether staged as pending or published directly), include the trailing disclosure in italics: `*Generated by <agent harness> using model <model>*`. Omit this line from local chat-only reviews.
6. **Omit Empty Sections & Redundant Summary Headers**: Never include empty sections or placeholder markers like `*(None)*` or `(none)` (for example, omit `### Comments on Lines Outside Diff` when zero findings are displaced). When submitting to GitHub or Gitea, omit leading `Summary`, `Executive Summary`, or `Code Review` headers and begin directly with the summary assessment.
