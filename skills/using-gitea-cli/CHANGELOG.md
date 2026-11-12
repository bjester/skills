# Changelog & Provenance: using-gitea-cli

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-11-12] - Import and Curation from Official Gitea CLI (gt)

- **Upstream Repository**: `https://gitea.com/gitea/cli.git`
- **Upstream Revision**: `2fb208e88ed4c8f64478f585dec868d0b08fc90d07c3bb42e6737420f4f5d8bf` (Release tag: untagged `main` snapshot targeting Gitea 28+), committed on `2026-11-11`
- **Upstream Source Path**: `sources/gt-cli/skills/gt/`

### 1. Base State (A)

- Upstream `gt` skill (`sources/gt-cli/skills/gt/SKILL.md`, 177 lines) documents non-interactive `gt` CLI rules (`--no-input`, `--json` and `--jq`, `--yes` confirmation gating, `-L 30` list limit, integer `comments` count), quick-start recipes, a task reference table, authentication and remote targeting notes, exit codes, a validation checklist, and scope exclusions.
- Bundles six Level 3 reference guides under `references/`: `api.md`, `automation.md`, `monitoring.md`, `resources.md`, `search.md`, and `workflow-authoring.md`.
- Uses minimal upstream frontmatter (`name: gt`, folded `description: >-`, `license: MIT`) without repository provenance metadata, `user-invocable`, `compatibility`, `allowed-tools`, an ASCII workflow diagram, or numbered execution phases.

### 2. Curated Changes Applied (A -> B)

- **Renamed**: Converted upstream `gt` to `using-gitea-cli` to match the repository gerund phrase naming convention (`<verb-ing>-<noun>`) and mark local curation.
- **Standardized Frontmatter**:
  - Replaced upstream frontmatter with the repository YAML schema (`license: MIT - https://github.com/bjester/skills/blob/main/LICENSE`, `user-invocable: true`, `compatibility`, `allowed-tools`, and `metadata`).
  - Authored a double-quoted Context-Search-Optimized `description` free of `<` and `>` characters covering `gt` operations, Gitea Actions, `.gitea/workflows`, `tea` migration, and pairing with `reviewing-prs`, `writing-prs`, `resolving-pr-feedback`, `writing-issues-for-bugs`, and `writing-issues-for-features`.
- **Structured Repository Document Anatomy**:
  - Added `# Using Gitea CLI`, executive `Purpose:` statement, and 4-stage ASCII workflow diagram.
  - Organized instructions into four sequential phases (`Phase 1: Pre-Flight Forge, Target & Identity Verification`, `Phase 2: Non-Interactive Rules & Quick-Start Workflows`, `Phase 3: Confirmation, Push & Mutation Safety`, and `Phase 4: Verification Checklist`) with GitHub-style alerts (`[!IMPORTANT]`, `[!WARNING]`).
  - Added active-account verification via `gt api user --jq .login --no-input`, documenting that `GITEA_TOKEN` omits `user` in `gt auth status --no-input --json` unless `--verify` is passed.
  - Added `--no-input` to every `gt` example command in `SKILL.md`, including the `Task Reference` table.
  - Preserved the `## Exit Codes` (`#exit-codes`) heading anchor so `[SKILL.md](../SKILL.md#exit-codes)` in `references/automation.md` resolves cleanly.
  - Expanded `When Not to Use` to route GitHub repositories to `gh` and route full issue, pull request, review, and feedback workflows to their dedicated dual-forge skills.
- **Encapsulated Skill-Specific References & Attribution**:
  - Retained all six upstream reference files under `skills/using-gitea-cli/references/` (`api.md`, `automation.md`, `monitoring.md`, `resources.md`, `search.md`, and `workflow-authoring.md`), normalizing sibling cross-references in `resources.md`, `search.md`, and `workflow-authoring.md` to skill-root-relative `references/<file>.md` paths required by `shinyskills` validation.
  - Added `skills/using-gitea-cli/NOTICE.md` (linked from `SKILL.md`) preserving `Copyright (c) 2016 The Gitea Authors` and the upstream MIT permission notice in packaged skill distributions (`Makefile` excludes `CHANGELOG.md` and `LICENSE*` from `output/skills/`).

### 3. Resulting State (B)

- A self-contained capability-primitive skill for driving Gitea instances safely and non-interactively with `gt` across CI checks, Actions logs, workflow dispatch, issues, pull requests, inline reviews, merges, releases, wikis, search, and `gt api`, integrated with the repository dual-forge workflow skills.

### 4. Re-sync / Update Recipe

When upstream `sources/gt-cli` updates:

1. Fetch and fast-forward the upstream clone:
   ```bash
   git -C sources/gt-cli fetch origin
   git -C sources/gt-cli pull --ff-only
   ```
2. Inspect commit history and diffs since base commit `2fb208e88ed4c8f64478f585dec868d0b08fc90d07c3bb42e6737420f4f5d8bf`:
   ```bash
   git -C sources/gt-cli log --oneline 2fb208e88ed4c8f64478f585dec868d0b08fc90d07c3bb42e6737420f4f5d8bf..HEAD -- skills/gt/
   git -C sources/gt-cli diff 2fb208e88ed4c8f64478f585dec868d0b08fc90d07c3bb42e6737420f4f5d8bf..HEAD -- skills/gt/
   ```
3. Port new `gt` subcommands, flags, JSON fields, exit codes, and `references/*.md` updates into `skills/using-gitea-cli/` while preserving:
   - Repository YAML frontmatter (`name: using-gitea-cli`, `license`, `user-invocable`, `compatibility`, `allowed-tools`, `metadata`).
   - Document anatomy (`# Using Gitea CLI`, `Purpose:`, workflow diagram, phased execution, and `--no-input` on every `gt` example).
   - The `## Exit Codes` (`#exit-codes`) heading anchor referenced by `references/automation.md`, upstream MIT attribution in `NOTICE.md`, and dual-forge skill routing in `When Not to Use`.
4. Run `make build` and `make validate` from the repository root and confirm both exit `0`.
5. Record the new upstream commit hash, commit date, and curated delta in this changelog.
