---
name: replaying-file-revisions
description: "Reconstruct and replay the iterative revision sequence of specific files (e.g. prompts, tuning constants, algorithmic iterations, schema evolutions) into rewritten commit history while preserving surrounding code coherence."
license: MIT - https://github.com/bjester/skills/blob/main/LICENSE
user-invocable: true
compatibility: a software project with git version control
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
  version: "1.1"
---

# Replaying File Revisions Into Rewritten History

Purpose: Reconstruct and replay historical file revisions into clean, successive commits when the iteration sequence itself carries architectural or reasoning value (e.g., prompt iterations, algorithm tuning, heuristic thresholds, schema migrations).

## Prerequisites & Core Philosophy

- **Extends `composing-commit-history`**: Builds on the soft-reset and baseline verification principles from `composing-commit-history` by adding precise reverse-patching and historical reconstruction.
- **Preserve Deliberate Iteration**: When a file's edit history documents the rationale behind subtle tuning or prompt wording, collapsing to a single commit erases that context. Replaying reconstructs each step with surrounding code kept intact and compilable.
- **Net Diff Equality**: The final commit in the replay chain must converge exactly on the final tree state.

---

## When to Use

- **Prompt & Constant Tuning**: A prompt, heuristic weight, or threshold was tuned over multiple steps, and understanding the final result requires seeing the progression.
- **Explicit User Request**: The user requested preserving incremental iterations for specific files.
- **Large Branches (20+ Commits / 100+ Files)**: Disentangling changes requires mapping individual file histories rather than reading commit subjects alone.

**Skip When**: Iterations are routine noise (TDD red/green cycles, typo fixes, lint fixups). Squash those using `composing-commit-history`.

---

## Step-by-Step Replay Workflow

```
1. RECONNAISSANCE ──► 2. TAG HEAD ──► 3. REVERSE-PATCH ──► 4. VERIFY REVISIONS ──► 5. STAGE & CONVERGE
        │                     │                 │                    │                     │
        ▼                     ▼                 ▼                    ▼                     ▼
   Map file-to-commit    Tag safety net    Rebuild versions     Check intermediate   Commit successive
   matrix to find        `git tag          newest-first using   content against      versions & verify
   split candidates      pre-rewrite`      `patch -R --fuzz=3`  original commits     net diff
```

### 1. Reconnaissance: Build the File-to-Commit Matrix

Examine the actual file modification history rather than relying on commit titles:

```bash
# View chronological commit-to-file mapping
git log --reverse --format='%n### %h %s' --name-only <base>..HEAD

# Inspect commits modifying a specific candidate path
git log --format='%h %s' <base>..HEAD -- <path>
```

- **Whole Files by Default**: Assign whole files to commits unless a path genuinely contains distinct, separable ideas.

### 2. Tag the Safety Net

Tag the tip before altering history:

- **Verify Clean Working Tree & No Active Rebase/Merge**: Run `git status` before tagging `pre-rewrite`. Because `git tag -f pre-rewrite HEAD` only snapshots committed state, any uncommitted or untracked working tree modifications will be lost when checking out or reverse-patching files. Commit or stash dirty changes first, and confirm no `MERGE_HEAD` or `REBASE_HEAD` is active.

```bash
git tag -f pre-rewrite HEAD
```

### 3. Reconstruct Historical Versions by Reverse-Patching

Start from the final file state (`HEAD`) and reverse-apply subsequent patches **newest-first**:

- Use an isolated scratch directory (`REV_DIR=$(mktemp -d)`) or clean `/tmp/rev` before starting.
- Inspect `git show <sha> -- <path>` when a commit mixed an intentional iteration of `<path>` with unrelated formatting/renames.

```bash
mkdir -p /tmp/rev

# Save final state as baseline
git show HEAD:<path> > /tmp/rev/v3

# Extract patch for the latest revision and reverse-apply
git show <sha-newest> -- <path> > /tmp/p_newest
patch -R -p1 --fuzz=3 /tmp/rev/v3 < /tmp/p_newest
```

*Note: Use `patch -R --fuzz=3` rather than `git apply -R` to tolerate line-offset drift caused by other commits.*

### 4. Verify Each Reconstructed Revision (CRITICAL)

Verify that the intermediate reconstructed file accurately matches historical state:

```bash
diff -u <(git show <sha>:<path>) /tmp/rev/<version>
```

- If no other commit touched the path between `<sha>` and `HEAD`, the diff will be empty. If other commits did touch it, ensure the delta contains *only* those expected changes.
- **Do not skip this check**: Intermediate corruption is invisible to the end-to-end net diff check.

### 5. Stage Versions as Successive Commits

Stage each version in chronological order and commit to the index:

```bash
cp /tmp/rev/v1 <path> && git add <path> && git commit -m "Tune prompt for edge-case reasoning (v1)"
cp /tmp/rev/v2 <path> && git add <path> && git commit -m "Refine prompt system constraints (v2)"
git checkout pre-rewrite -- <path> && git commit -m "Finalize prompt format (v3)"
```

### 6. Verify Intermediate Commits and Net Diff

Test intermediate states in the primary working tree:

```bash
# Check out intermediate commit files and run test suite
git checkout <sha> -- <paths>
<test-command>
git checkout HEAD -- <paths>

# Verify final net diff matches baseline
git diff <base>..HEAD > /tmp/after-rewrite.patch
diff -u /tmp/before-history.patch /tmp/after-rewrite.patch
```

*Caution: Do not use `git worktree` for intermediate testing if the project uses editable/linked installs (`pip install -e`, `npm link`), as tests may resolve dependencies against the primary tree.*

---

## Quick Reference Commands

| Operation | Command |
| :--- | :--- |
| **File-to-commit matrix** | `git log --reverse --format='%n### %h %s' --name-only <base>..HEAD` |
| **Commits touching path** | `git log --format='%h %s' <base>..HEAD -- <path>` |
| **Reverse-apply with fuzz** | `patch -R -p1 --fuzz=3 <file> < <patch>` |
| **Restore final state** | `git checkout pre-rewrite -- <path>` |
| **Check revision match** | `diff -u <(git show <sha>:<path>) <reconstructed-file>` |
| **Verify final net diff** | `diff -u <before>.patch <(git diff <base>..HEAD)` |

---

## Common Pitfalls to Avoid

- **Reverse-Applying Oldest-First**: Applying oldest patches first will fail due to shifted line context. Always reverse-apply newest-first.
- **Skipping Intermediate Diff Checks**: The net diff check only verifies start and end states; always check intermediate revisions against `git show <sha>:<path>`.
- **Testing Intermediates in Worktrees with Editable Installs**: Can produce false-positive green test runs due to package resolution shadowing.
