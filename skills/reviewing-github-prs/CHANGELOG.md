# Changelog & Provenance: reviewing-github-prs

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-10-18] - Blast Radius Analysis & Multi-Model Adversarial Review from pstack (v0.15.26)

- **Upstream Repository**: `git@github.com:cursor/plugins.git`
- **Upstream Revision**: `0b8e952052d482ee6de06deebf14d590d77b1b34` (Release: `chore(pstack): bump to 0.15.26`), committed on 2026-10-18
- **Upstream Source Paths**:
  - `sources/cursor-plugins/pstack/skills/blast-radius/`
  - `sources/cursor-plugins/pstack/skills/interrogate/`

### 1. Curated Changes Applied
- **Step 2 (Fetch and Analyze Diff)**:
  - Added Blast Radius analysis check referencing `analyzing-blast-radius` to detect lifecycle issues, serialization shifts, and database column dependencies.
  - Injected Comment Hygiene check under Micro-Craftsmanship.
- **Step 3 (Local Checkout & Verification)**:
  - Injected Multi-Model Adversarial PR Review (`interrogate`) option: dispatching PR diff to 2+ distinct LLM families to discover high-confidence consensus blockers.

---

## [2026-10-14] - Inline Comments via GitHub API & Curation from le-skills

- **Upstream Repository**: `https://github.com/learningequality/le-skills.git`
- **Upstream Revision**: `9dc3e40713b25f74509e01847cf80e6582421d70`, committed on 2026-08-01 (tag: `v26.08.01.1`)
- **Upstream Source Path**: `sources/le-skills/skills/github-pr-review/`

### 1. Base State (A)
- Upstream `github-pr-review` in `le-skills` provided a 5-phase PR review protocol with visual inspection, manual QA, terse writing gates, delta reviews, and submission of reviews with inline comments using `gh api repos/{owner}/{repo}/pulls/{pr_number}/reviews`.
- Handled diff line verification against hunk headers (`[ns, ns+nc-1]` for `RIGHT`, `[os, os+oc-1]` for `LEFT`) and displaced out-of-hunk findings to review body to avoid HTTP 422 errors.
- Handled pending review creation (omitting `event`) vs. autonomous publishing (`REQUEST_CHANGES`, `COMMENT`, `APPROVE`).

### 2. Curated Changes Applied (A -> B)
- **Renamed**: `github-pr-review` → `reviewing-github-prs` to adhere to repository gerund authoring conventions (`reviewing-code`, `executing-plans`, `writing-specs`).
- **Standardized Metadata**:
  - Configured repository-standard YAML frontmatter in `SKILL.md`: `license: MIT`, `user-invocable: true`, `compatibility`, `allowed-tools`, and `metadata`.
- **Integrated Multi-Scale Engineering Taxonomy**:
  - Replaced upstream terse-writing gate and bespoke severity labels with this repository's 4-scale software engineering review philosophy (`software-engineering` and `reviewing-code`) and standard 4-tier finding taxonomy (`🚨 Blocker (Must-Fix)`, `⚠️ Architecture & Design (Should-Fix)`, `💡 Tactical Suggestion (Optional)`, `✅ Positive Highlights`).
- **Inline Comment Drafting & Diff Hunk Verification**:
  - Replaced single-comment `gh pr review --body-file` submission with structured inline comment drafting via `gh api repos/{owner}/{repo}/pulls/<pr-number>/reviews`.
  - Added strict diff hunk verification using `gh pr diff <pr-number> -- <file>` to ensure comment lines fall within hunk bounds (`side: "RIGHT"` / `side: "LEFT"`).
  - Adopted out-of-hunk displacement pattern: automatically shift findings on unmodified lines into a dedicated `### Comments on Lines Outside Diff` section in the review summary body, preventing HTTP 422 API errors.
  - Standardized JSON input drafting via `--input <payload.json>` to eliminate shell escaping issues with complex multi-line Markdown and code diffs.
  - Maintained default pending review workflow (omitting `event` for human inspection via "Finish your review") while documenting autonomous submission (`REQUEST_CHANGES`, `COMMENT`, `APPROVE`).

### 3. Resulting State (B)
- A comprehensive GitHub Pull Request review skill combining multi-scale architectural analysis with battle-tested GitHub API inline diff comment submission, hunk verification, pending review staging, and HTTP 422 resilience.

### 4. Re-sync / Update Recipe
When upstream `sources/le-skills` is updated:
1. Fetch latest changes in upstream:
   ```bash
   git -C sources/le-skills pull
   ```
2. Diff upstream `skills/github-pr-review/` against base commit `9dc3e40713b25f74509e01847cf80e6582421d70`:
   ```bash
   git -C sources/le-skills diff 9dc3e40713b25f74509e01847cf80e6582421d70..HEAD -- skills/github-pr-review/
   ```
3. Evaluate updates to GitHub API review payloads, delta review logic, or diff handling.
4. Port improvements into `skills/reviewing-github-prs/` while preserving:
   - The skill name `reviewing-github-prs` and repository frontmatter.
   - The 4-scale software engineering review integration and 4-tier finding taxonomy.
   - Cross-skill wiring with `reviewing-code`, `software-engineering`, and `learning-equality`.
5. Run `make build` to verify output packaging.
6. Record the new upstream commit hash, date, and changes in this changelog.
