# Changelog & Provenance: resolving-github-pr-feedback

Tracks upstream sources, imported commit revisions, and curated repository modifications.

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
4. Integrate valuable additions into `skills/resolving-github-pr-feedback/SKILL.md` while preserving repository frontmatter and phased structure.
5. Record the new upstream commit hash, date, and changes in this changelog.
