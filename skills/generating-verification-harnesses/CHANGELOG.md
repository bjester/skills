# Changelog & Provenance: generating-verification-harnesses

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-10-18] - Synthesis & Curation from pstack create-verification-skill (v0.15.26)

- **Upstream Repository**: `git@github.com:cursor/plugins.git`
- **Upstream Revision**: `0b8e952052d482ee6de06deebf14d590d77b1b34` (Release: `chore(pstack): bump to 0.15.26`), committed on 2026-10-18
- **Upstream Source Path**: `sources/cursor-plugins/pstack/skills/create-verification-skill/`

### 1. Base State (A)
- Upstream `create-verification-skill` provided a ~45-line generator for project-local Cursor skills (`.cursor/skills/verify-<app>/`) with Launch, Doctor, Drive, Evidence, Cleanup, and a seeded feature map.
- Enforced interviewing the repo instead of the user, executing the generated skill end-to-end once, and confirming that cleanup does not delete evidence.

### 2. Curated Changes Applied (A -> B)
- **Renamed**: `create-verification-skill` → `generating-verification-harnesses` following the repository gerund naming convention (`writing-specs`, `executing-plans`).
- **Standardized Repository Anatomy**:
  - Configured standard YAML frontmatter (`name`, `description`, `license`, `user-invocable`, `compatibility`, `allowed-tools`, `metadata`).
  - Added executive mission statement, ASCII workflow diagram, and 4 clear phases.
- **Platform-Agnostic Generation**:
  - Generalized from Cursor-only paths (`.cursor/skills/`) to standard local skill and agent directories (`.agents/skills/`, `.gemini/skills/`, or project test harnesses).
  - Codified the interview checklist across 5 dimensions: Surface, Launch, Driving, Evidence, and Isolation.
  - Standardized the living Feature Map template structure with explicit sections: User Journey, Navigation, Driving, Observable End State, and Gotchas.
- **Mandatory Live Proof Gate**:
  - Formalized the 4-step execution proof checklist (Launch $\rightarrow$ Doctor $\rightarrow$ Drive 1 feature $\rightarrow$ Capture Proof $\rightarrow$ Cleanup) with proof artifact survival checks.

### 3. Resulting State (B)
- A reusable meta-skill that enables agents to discover application mechanics in any unfamiliar codebase and author a robust, headless verification driver so future changes can be verified autonomously.

### 4. Re-sync / Update Recipe
When upstream `sources/cursor-plugins` updates `pstack`:
1. Fetch latest changes in upstream:
   ```bash
   git -C sources/cursor-plugins pull
   ```
2. Diff upstream `create-verification-skill/` against base commit `0b8e952`:
   ```bash
   git -C sources/cursor-plugins diff 0b8e952..HEAD -- pstack/skills/create-verification-skill/
   ```
3. Evaluate updates to driver generation sections or feature map schemas.
4. Port valuable additions into `skills/generating-verification-harnesses/SKILL.md` while preserving repository frontmatter and structure.
5. Run `make build` to verify packaging.
6. Record the new upstream commit hash, date, and changes in this changelog.
