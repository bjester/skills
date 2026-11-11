---
name: writing-github-prs
description: |
  Authors, updates, and submits clear, slop-free GitHub Pull Request (PR) titles
  and descriptions grounded in git diffs, commit history, repository PR templates,
  and linked issues. Enforces pre-flight GitHub CLI author identity checks,
  intent-over-diff-narration, epistemic verification honesty, DEEP AI disclosure,
  writing-technical-docs Plain prose, and safe --body-file submission. Use when
  drafting PR descriptions, opening PRs (gh pr create), or updating PR bodies
  (gh pr edit).
license: MIT - https://github.com/bjester/skills/blob/main/LICENSE
user-invocable: true
compatibility: GitHub repositories using the GitHub CLI (gh) and git
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

# Writing GitHub Pull Requests

Purpose: Author accurate, concise, and slop-free GitHub Pull Request titles and descriptions grounded in repository templates, verified diffs, and linked issues.

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. PRE-FLIGHT: Verify gh author identity, <base>, diff & PR template   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. DRAFT: Populate repo template (or default), focusing on WHY > WHAT   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3. DE-SLOP GATE: Apply writing-technical-docs + word-swaps self-check   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 4. SUBMIT: Write scratch file and run gh pr create/edit --body-file     │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Pre-Flight Identity, Diff Grounding & Template Discovery

1. **Author Identity Gate (Before Any `gh pr create` or `gh pr edit`)**:
   - When submitting or editing a PR via `gh`, verify the active GitHub CLI account against git authorship:
     ```bash
     gh api user -q .login
     git config user.name
     git config user.email
     ```
   - > [!WARNING]
     > **Account Mismatch Halt**: If `gh` is authenticated as a dedicated bot or reviewer account (for example, `*-bot` or `*bot`) while local commits belong to a human author (or vice versa without explicit user direction), **HALT immediately**. Do not open or edit the PR under the wrong GitHub identity; save the drafted Markdown file locally and ask the user whether to switch `gh auth` first.

2. **Ground Context in Target `<base>`, Commits, Diff & Linked Issues**:
   - Confirm the intended target `<base>` branch (`main`, `develop`, release branch, or parent branch in a stacked PR series):
     ```bash
     git status --short
     git log --oneline <base>..HEAD
     git diff --stat <base>...HEAD
     git diff <base>...HEAD
     ```
   - When commits or branch names reference an issue (`#123`), inspect the issue requirements (`gh issue view 123`) so `References` and `Summary` align with the actual acceptance criteria.

3. **Discover Repository PR Templates & Conventions**:
   - Search for `.github/pull_request_template.md`, `.github/PULL_REQUEST_TEMPLATE/*.md`, `docs/pull_request_template.md`, `AGENTS.md`, and `CONTRIBUTING.md`.

---

## Phase 2: Structure & Author PR Title and Body

1. **Outcome-Oriented PR Title**:
   - Write an imperative subject line (`<= 72` chars) naming the capability added or broken behavior fixed rather than internal variable/helper names.
   - Follow conventional commit prefixes (`feat:`, `fix:`) **only** when `git log` or `CONTRIBUTING.md` shows the repository uses them.
   - Good: `Gate router pageview tracking on authenticated session`
   - Bad: `Add if check in setupRouter afterEach hook`

2. **Template-First Body Rule**:
   - **When a repository PR template exists**: Keep its required headings and section order intact. Replace every placeholder (`…`), check off `[x]` **only** checklist items genuinely verified, omit or mark N/A optional items per template instructions, and delete instructional HTML comment blocks (`<!-- ... -->`).
   - **When no repository PR template exists**, use this concise four-section layout:
     ````markdown
     ## Summary
     [1-3 short paragraphs or bullets stating what changes, why it is needed now, and why this design was chosen over alternatives.]

     ## References
     - Closes #<issue> (or Part of #<epic> / Depends on #<parent-pr>)

     ## Reviewer Guidance & Verification
     - Automated checks run: `<exact commands executed>`
     - Manual verification: [Steps actually tested, or note screenshots/recordings for UI changes]
     - Focus areas / open questions: [Subtle trade-offs or areas warranting extra scrutiny, if any]

     ## AI Usage
     [Transparent DEEP disclosure if AI assisted: Disclose, Engage critically, Edit, Process sharing.]
     ````

3. **Intent Over Diff Regurgitation**:
   - Explain *why* the problem occurs, *what* invariants or contracts changed, and *why* this approach was selected.
   - Do **not** write a mechanical file-by-file inventory repeating `git diff --stat`; reviewers already see changed files in GitHub's diff view.

4. **Epistemic Verification Honesty & Deferral Discipline**:
   - > [!IMPORTANT]
     > Never claim unit tests, integration suites, linters, or manual browser flows were executed unless verified in the current session or explicitly confirmed by the user. State unexecuted manual checks transparently under `Reviewer Guidance`.
   - Never hand-wave known gaps or shortcuts as *"will handle in a later issue"* without linking a real tracking `#issue` number.
   - For stacked PRs, state the parent PR (`Depends on #...`) and target base branch explicitly so reviewers evaluate only this slice's commits.

---

## Phase 3: Prose De-Slopping & Verifiable Self-Check

Load the **`writing-technical-docs`** skill (`Chat Explanations, Code Reviews & PR Discussions` register) and consult `references/word-swaps.md` before finalizing the PR body:

- [ ] **Direct First Sentence**: Does `Summary` open directly with what changes and why (never `"This PR aims to..."`, `"This PR introduces a comprehensive..."`, or `"In this pull request, we..."`)?
- [ ] **Deterministic Slop Scan**: Search the draft for `—` (em-dashes), ` - ` (spaced hyphen clause-splices), `;`, `aims to`, `not just`, `ensure`, `, ensuring`, `, making`, `, highlighting`, and abstract AI nouns (`substrate`, `bedrock`, `locus`, `primitive`, `flywheel`). Fix every hit.
- [ ] **Template Cleanliness**: Are all `<!-- ... -->` instruction blocks and `…` placeholders removed?
- [ ] **Durable Claims**: Are volatile version pins or line counts avoided when code manifests own them?
- [ ] **AI Disclosure Included**: Is AI involvement disclosed candidly (following the DEEP framework: *Disclose, Engage critically, Edit, Process sharing*)?

---

## Phase 4: Safe CLI Submission via `--body-file`

> [!TIP]
> Never pass multi-line Markdown inline via `gh pr create --body "..."` because backticks and `$` expansions corrupt shell strings. Always write to a scratch file and pass `--body-file`.

1. Write the verified PR description to a scratch file (for example, `/tmp/pr-body.md`).
2. Confirm with the user if creating a new PR (`--draft` vs. ready for review) or overwriting an existing human-edited PR description (`gh pr view <num> --json body -q .body`).
3. Submit using `--body-file`:
   ```bash
   # Create a new PR targeting <base>
   gh pr create --base <base> --title "<Title>" --body-file /tmp/pr-body.md

   # Update an existing PR description
   gh pr edit <pr-number> --body-file /tmp/pr-body.md
   ```
