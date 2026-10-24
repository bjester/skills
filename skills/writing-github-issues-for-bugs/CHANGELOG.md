# Changelog & Provenance: writing-github-issues-for-bugs

Tracks upstream sources, imported commit revisions, and curated repository modifications.

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
