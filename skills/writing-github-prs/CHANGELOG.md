# Changelog & Provenance: writing-github-prs

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-11-11] - Initial Release: Template-First, Slop-Free GitHub PR Authoring

- **Provenance**: First-party repository skill synthesized from `bjesterbot` PR review audit findings across Learning Equality repositories, `references/github-issue-guidelines.md` (DEEP AI disclosure and `--body-file` safety), and `writing-technical-docs`.

### 1. Operational Capabilities (`v1.0`)
- **Phase 1 (Pre-Flight Identity & Context)**: Verifies `gh api user -q .login` against git authorship to prevent opening/editing PRs under a bot reviewer account, grounds claims in `<base>..HEAD` commits/diffs and linked issues, and discovers `.github/pull_request_template.md` and `AGENTS.md`.
- **Phase 2 (Template-First & Intent-Driven Drafting)**: Preserves native repository PR templates (stripping `<!-- ... -->` comments and `…` placeholders), provides a 4-section fallback layout (`Summary`, `References`, `Reviewer Guidance & Verification`, `AI Usage`), bans file-by-file diff regurgitation, and enforces epistemic honesty on executed tests and follow-up `#issue` links.
- **Phase 3 & 4 (De-Slop Gate & Safe CLI Submission)**: Routes prose through `writing-technical-docs` and shared `references/word-swaps.md` with deterministic token checks, and submits safely via `gh pr create/edit --body-file`.
