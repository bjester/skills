# Changelog & Provenance: writing-prs

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-11-12] - Forge-Neutral Rename & Dual-Forge (gh / gt) PR Authoring

### 1. Curated Changes Applied
- **Skill Rename & Frontmatter (`1.0` -> `2.0`)**: Renamed `writing-github-prs` to `writing-prs` and generalized frontmatter (`compatibility: Git repositories hosted on GitHub (gh) or Gitea (gt)`) and CSO `description` across both GitHub (`gh`) and Gitea (`gt`).
- **Phase 1 (Forge Selection, Author Identity Gate & Template Discovery)**: Wired shared `references/forge-cli.md` for pre-flight forge selection and author identity checks (`gh api user -q .login` and `gt api user --jq .login --no-input`), added `gt issue view <num> --no-input --json number,title,body,labels` alongside `gh issue view <num>`, and expanded PR template discovery to `.gitea/pull_request_template.md` and `.gitea/PULL_REQUEST_TEMPLATE/*.md`.
- **Phase 2 & Phase 4 (Forge-Neutral Diff Framing & Dual-Forge `--body-file` Submission)**: Generalized diff framing and added Gitea `gt pr view --no-input`, `gt pr create --no-input`, and `gt pr edit --no-input` commands alongside `gh`, documenting Gitea unpushed-branch exit `2` / `--yes` confirmation safeguards and `--draft` `WIP: ` title prefix behavior.

---

## [2026-11-11] - Initial Release: Template-First, Slop-Free GitHub PR Authoring

- **Provenance**: First-party repository skill synthesized from `bjesterbot` PR review audit findings across Learning Equality repositories, `references/github-issue-guidelines.md` (DEEP AI disclosure and `--body-file` safety), and `writing-technical-docs`.

### 1. Operational Capabilities (`v1.0`)
- **Phase 1 (Pre-Flight Identity & Context)**: Verifies `gh api user -q .login` against git authorship to prevent opening/editing PRs under a bot reviewer account, grounds claims in `<base>..HEAD` commits/diffs and linked issues, and discovers `.github/pull_request_template.md` and `AGENTS.md`.
- **Phase 2 (Template-First & Intent-Driven Drafting)**: Preserves native repository PR templates (stripping `<!-- ... -->` comments and `…` placeholders), provides a 4-section fallback layout (`Summary`, `References`, `Reviewer Guidance & Verification`, `AI Usage`), bans file-by-file diff regurgitation, and enforces epistemic honesty on executed tests and follow-up `#issue` links.
- **Phase 3 & 4 (De-Slop Gate & Safe CLI Submission)**: Routes prose through `writing-technical-docs` and shared `references/word-swaps.md` with deterministic token checks, and submits safely via `gh pr create/edit --body-file`.
