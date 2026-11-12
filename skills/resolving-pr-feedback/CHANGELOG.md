# Changelog & Provenance: resolving-pr-feedback

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-11-12] - Forge-Neutral Rename, Level 3 Forge Adapters & Gitea (gt) Support

### 1. Base State (A)
- `resolving-github-pr-feedback` (`v1.1`) hardcoded GitHub-specific naming, `gh` CLI commands, and inline GraphQL thread queries and mutations directly inside `SKILL.md`.
- Phase 5 placed `git push` after replying and marking threads resolved, conflicting with the skill's own `Resolving Before Pushing` anti-pattern.

### 2. Curated Changes Applied (A -> B)
- **Renamed**: `resolving-github-pr-feedback` -> `resolving-pr-feedback`, updating complementary reviewer pairing from `reviewing-github-prs` to `reviewing-prs`.
- **Shared Forge & Identity Contract**:
  - Wired shared `references/forge-cli.md` into Phase 1 for deterministic `Forge Selection Gate` routing (`gh` vs. `gt --no-input`) and unified `Author Identity Gate` enforcement across GitHub (`pr.author.login`) and Gitea (flat string `author` via `gt api user --jq .login --no-input`).
- **Level 3 Forge Adapters**:
  - Extracted GitHub CLI and GraphQL thread operations (`reviewThreads(first: 100)`, `addPullRequestReviewThreadReply`, `resolveReviewThread`) into `references/github-gh.md`.
  - Authored `references/gitea-gt.md` for Gitea `gt` (`--no-input` on all commands, `gt pr review comments <pr-number> -L 1000` grouping conversations by `[.path, .line, .old_line]` with `all(.resolver == "")` and handling `old_line`, `gt pr review list -L 100`, quoted-heredoc `gt pr review reply <pr-number> <root-id> --no-input --body-file -`, and plain-text `gt pr review resolve <pr-number> <root-id> --no-input` noting rejection of `--json` and `--jq`).
- **Phase 5 Push-Before-Resolve Ordering**:
  - Reordered Phase 5 so `git push` runs before posting thread replies and marking threads resolved, matching the `Resolving Before Pushing` anti-pattern.
- **Anti-Patterns & Metadata**:
  - Generalized Anti-Patterns (`gh pr comment` / `gt pr comment --no-input`, `Wrong-Account Replies`) across `gh` and `gt`.
  - Bumped `metadata.version` from `1.1` to `2.0` and updated `compatibility` to `Git repositories hosted on GitHub (gh) or Gitea (gt)`.

### 3. Resulting State (B)
- A forge-neutral author-side review thread resolution skill supporting both GitHub (`gh`) and Gitea (`gt`) while loading only the active forge's CLI/API adapter into context.

---

## [2026-11-11] - Pre-Flight Author Identity Gate

### 1. Base State (A)
- Phase 1 checked `gh auth status` without verifying that the active GitHub user matched `pr.author.login`, allowing an active reviewer bot token (`GH_TOKEN`) to post author replies and resolve threads on a human author's PR.

### 2. Curated Changes Applied (A -> B)
- **Phase 1 (Authentication, Author Identity Gate & Thread Enumeration)**:
  - Added `gh api user -q .login` and `author` to `gh pr view --json`.
  - Added a hard-fail **Author Identity Gate** aborting execution whenever `gh_user != pr.author.login` (unless the user explicitly authorizes cross-author maintainer resolution in the session).
- **Anti-Patterns**:
  - Added *Wrong-Account Replies*.
- Bumped version metadata to `1.1`.

### 3. Resulting State (B)
- Prevents cross-account identity collisions before any local commits, pushes, replies, or thread resolutions occur.

---

## [2026-10-24] - Synthesis & Curation from agentic-awesome-skills (v20.0.0)

- **Upstream Repository**: `https://github.com/sickn33/agentic-awesome-skills`
- **Upstream Revision**: `6d4ea18320984083107f07ff69587fa355ee94c0` (Release: `v20.0.0`), committed on 2026-04-20
- **Upstream Source Path**: `sources/agentic-awesome-skills/skills/address-github-comments/`

### 1. Base State (A)
- Upstream `address-github-comments` was a 72-line initial outline noting that `gh pr view --comments` omits inline review threads and suggesting GraphQL inspection, but lacked detailed queries, mutations, classification schemas, and execution workflows.

### 2. Curated Changes Applied (A -> B)
- **Renamed**: `address-github-comments` → `resolving-github-pr-feedback` to conform to the repository gerund phrase naming convention (`reviewing-github-prs`, `composing-commit-history`).
- **Standardized Repository Anatomy**:
  - Configured standard YAML frontmatter schema (`name`, `description`, `license`, `user-invocable`, `compatibility`, `allowed-tools`, `metadata`).
  - Added executive mission statement, ASCII workflow diagram, and 5 sequential execution phases.
- **Architectural Pairing with Reviewer Skill**:
  - Explicitly aligned the skill as the author-side complement to `reviewing-github-prs`.
- **Codified GraphQL Enumeration, Reply & Resolution**:
  - Injected exact, copy-pasteable GitHub GraphQL API queries for enumerating unresolved `reviewThreads`.
  - Added GraphQL mutations for `addPullRequestReviewThreadReply` and `resolveReviewThread`.
- **Triage Taxonomy**:
  - Formalized feedback classification into `FIX-NOW`, `CLARIFY`, and `DEFER`.
- **SHA-Bound Empirical Verification**:
  - Enforced local test execution bound to the updated `HEAD` commit SHA before replying or resolving threads.
- **Anti-Pattern Guardrails**:
  - Codified common mistakes: Conversation comment dumping, phantom resolution, drive-by scope creep, and resolving before pushing.

### 3. Resulting State (B)
- A self-contained, robust skill enabling developers and autonomous agents to systematically address, empirically verify, and cleanly resolve GitHub Pull Request review threads using the GitHub CLI.

### 4. Re-sync / Update Recipe
When upstream `sources/agentic-awesome-skills` updates:
1. Fetch latest changes in upstream:
   ```bash
   git -C sources/agentic-awesome-skills pull
   ```
2. Diff upstream `address-github-comments/` against base commit `6d4ea18`:
   ```bash
   git -C sources/agentic-awesome-skills diff 6d4ea18320984083107f07ff69587fa355ee94c0..HEAD -- skills/address-github-comments/
   ```
3. Evaluate updates to GitHub API query structures, comment parsing logic, or resolution workflows.
4. Integrate valuable additions into `skills/resolving-pr-feedback/SKILL.md` and `skills/resolving-pr-feedback/references/github-gh.md` while preserving repository frontmatter and phased structure.
5. Record the new upstream commit hash, date, and changes in this changelog.
