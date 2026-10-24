# Changelog & Provenance: replaying-file-revisions

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-10-24] - Clean Working-Tree Pre-Flight Check & Scratch Directory Isolation

- **Upstream Repository**: `https://github.com/sickn33/agentic-awesome-skills`
- **Upstream Revision**: `6d4ea18320984083107f07ff69587fa355ee94c0` (Tag: `v20.0.0`), committed on 2026-04-20
- **Integrated Sources**:
  - `sources/agentic-awesome-skills/skills/conductor-revert/`
  - `sources/agentic-awesome-skills/skills/git-advanced-workflows/`

### 1. Base State (A)
- Reconstructed chronological iterations of target files via reverse-patching (`git show <sha> -- <path> | git apply -R`) and replayed them into rewritten commit history after tagging `pre-rewrite`.
- Did not verify whether the working tree was clean or whether an active rebase/merge was in progress before tagging `pre-rewrite`.

### 2. Curated Changes Applied (A -> B)
- **Step 2 (`Tag the Safety Net`)**:
  - Added mandatory pre-flight check (`git status`) verifying a clean working tree and absence of `MERGE_HEAD` / `REBASE_HEAD` before creating the `pre-rewrite` tag so uncommitted modifications cannot be lost during reverse-patching.
- **Step 3 (`Reconstruct Historical Versions by Reverse-Patching`)**:
  - Added guidance to use an isolated scratch directory (`REV_DIR=$(mktemp -d)` or cleaned `/tmp/rev`) and to inspect `git show <sha> -- <path>` when commits mix intentional revisions with unrelated formatting or renames.
- Bumped `metadata.version` to `1.1`.

### 3. Resulting State (B)
- Safer revision-replay workflow with working-tree state protection and isolated snapshot storage.

### 4. Re-sync / Update Recipe
```bash
git -C sources/agentic-awesome-skills fetch origin
git -C sources/agentic-awesome-skills log -p 6d4ea18320984083107f07ff69587fa355ee94c0..origin/main -- \
  skills/conductor-revert/ skills/git-advanced-workflows/
```
