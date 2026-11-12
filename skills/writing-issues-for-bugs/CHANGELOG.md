# Changelog & Provenance: writing-issues-for-bugs

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-11-12] - Forge-Neutral Rename & Dual-Forge (gh / gt) Support

### 1. Curated Changes Applied
- **Skill Rename (`1.2` -> `2.0`)**: Moved `skills/writing-github-issues-for-bugs/` to `skills/writing-issues-for-bugs/` and updated `# Writing Issues: Bugs`, CSO `description`, `compatibility`, and `Purpose:` to cover both GitHub (`gh`) and Gitea (`gt`).
- **Workflow & Shared Reference Wiring**: Added the 4-step ASCII workflow diagram (`SELECT FORGE & SEARCH DUPLICATES -> DRAFT BUG CONTRACT -> DE-SLOP SCAN -> SAFE --body-file SUBMIT`) and linked `references/forge-cli.md`, `references/issue-guidelines.md` (replacing `references/github-issue-guidelines.md`), and `references/word-swaps.md`.
- **Dual-Forge CLI & Cross-Reference Updates**: Updated feature cross-reference to `writing-issues-for-features` and expanded duplicate search and `--body-file` submission gates to cover `gh issue list --search` / `gh issue create --body-file` and `gt issue list -S --no-input` / `gt issue create --no-input --body-file`.

---

## [2026-11-11] - Plain Technical Prose & De-Slop Routing (`writing-technical-docs`)

### 1. Curated Changes Applied
- **`SKILL.md` (`1.1` -> `1.2`)**: Added `writing-technical-docs` (Plain mode) and shared `references/word-swaps.md` routing to `Prerequisites & Core Philosophy` and `Self-Review Checklist Before Submitting`.
- **`references/github-issue-guidelines.md` & `Makefile`**: Added Plain Technical Prose & De-Slopping standards and wired `references/word-swaps.md` into the packaged skill.

---

## [2026-10-24] - Epistemic Uncertainty Markers, Severity Tiers & Safe CLI Submission

- **Upstream Repository**: `https://github.com/sickn33/agentic-awesome-skills`
- **Upstream Revision**: `6d4ea18320984083107f07ff69587fa355ee94c0` (Tag: `v20.0.0`), committed on 2026-04-20
- **Integrated Sources**:
  - `sources/agentic-awesome-skills/skills/github-issue-creator/`
  - `sources/agentic-awesome-skills/skills/issues/`

### 1. Base State (A)
- Structured bug report authoring around observed vs. expected behavior, reproduction steps, root-cause orientation pointers, and shared `references/github-issue-guidelines.md`.
- Lacked explicit guardrails against fabricating unverified reproduction steps from partial logs and operational definitions for `P0` / `P1` / `P2` severity tiers.

### 2. Curated Changes Applied (A -> B)
- **`SKILL.md`**:
  - Added epistemic uncertainty preservation under `### Minimal Reproduction Environment / Conditions`: never fabricate reproduction steps or environment details; mark unverified details as `(unconfirmed)`.
  - Defined operational criteria for `P0 (Blocker)`, `P1 (High)`, and `P2 (Medium)` under `## Metadata`.
  - Added pre-submission duplicate check (`gh issue list --search`) and `--body-file` submission check to `## Self-Review Checklist Before Submitting`.
  - Bumped `metadata.version` to `1.1`.
- **`references/github-issue-guidelines.md` (Shared Reference)**:
  - Added `## Pre-Submission Duplicate Check & Safe CLI Creation`.

### 3. Resulting State (B)
- Bug issue authoring workflow that preserves epistemic honesty on partial reports, standardizes severity triage, and prevents shell-escaped Markdown corruption during `gh issue create`.

### 4. Re-sync / Update Recipe
```bash
git -C sources/agentic-awesome-skills fetch origin
git -C sources/agentic-awesome-skills log -p 6d4ea18320984083107f07ff69587fa355ee94c0..origin/main -- \
  skills/github-issue-creator/ skills/issues/
```
