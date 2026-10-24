# Changelog & Provenance: composing-commit-history

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-10-24] - Pre-Flight Branch & Untracked Hygiene and Anti-Slop Commit Guidelines

- **Upstream Repository**: `https://github.com/sickn33/agentic-awesome-skills`
- **Upstream Revision**: `6d4ea18320984083107f07ff69587fa355ee94c0` (Tag: `v20.0.0`), committed on 2026-04-20
- **Integrated Sources**:
  - `sources/agentic-awesome-skills/skills/unslop-commit/`
  - `sources/agentic-awesome-skills/skills/commit/`
  - `sources/agentic-awesome-skills/skills/git-workflow-and-versioning/`

### 1. Base State (A)
- Provided the 5-step soft-reset and selective re-commit workflow (`git reset --soft <base>`, baseline patch capture via `git add -A`, unstage, atomic re-commit, and `diff -u` verification).
- Lacked a pre-flight hygiene check before Step 2's `git add -A`, meaning untracked scratch files or secrets left in the working tree would be locked into `/tmp/before-history.patch`.

### 2. Curated Changes Applied (A -> B)
- **Step 0 (`Pre-Flight Branch & Untracked File Hygiene`)**:
  - Added protected branch check (`git branch --show-current`) to prevent rewriting `main`/`master`.
  - Added untracked file and secret cleanup before `git add -A` locks working-tree artifacts into `/tmp/before-history.patch`.
- **Commit Message Guidelines**:
  - Added anti-slop rules banning filler openings (*"This commit..."*, *"This change..."*) and corporate buzzwords.
  - Added subject line length precision (`<= 50` chars, hard cap `72`, no trailing period, no redundant scope repetition).
  - Clarified when to omit vs. include a commit body (mandatory for breaking changes, security fixes, migrations, and reverts).
- Bumped `metadata.version` to `1.1`.

### 3. Resulting State (B)
- Hardened commit curation workflow that prevents accidental inclusion of untracked scratch files/secrets in the baseline patch and enforces crisp, slop-free commit messages.

### 4. Re-sync / Update Recipe
```bash
git -C sources/agentic-awesome-skills fetch origin
git -C sources/agentic-awesome-skills log -p 6d4ea18320984083107f07ff69587fa355ee94c0..origin/main -- \
  skills/unslop-commit/ skills/commit/ skills/git-workflow-and-versioning/
```
