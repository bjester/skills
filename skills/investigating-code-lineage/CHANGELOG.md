# Changelog & Provenance: investigating-code-lineage

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-10-18] - Synthesis & Curation from pstack why (v0.15.26)

- **Upstream Repository**: `git@github.com:cursor/plugins.git`
- **Upstream Revision**: `0b8e952052d482ee6de06deebf14d590d77b1b34` (Release: `chore(pstack): bump to 0.15.26`), committed on 2026-10-18
- **Upstream Source Path**: `sources/cursor-plugins/pstack/skills/why/`

### 1. Base State (A)
- Upstream `why` provided a ~100-line investigative harness designed to discover MCP tools across 7 evidence categories, establish a code anchor via git blame and PR inspection, spawn parallel investigator subagents, and synthesize findings with epistemic confidence language.
- Relied on Cursor-specific subagent models (`grok-4.7-xhigh-fast`, `claude-opus-5-5-xhigh`) and separate referenced prompt templates.

### 2. Curated Changes Applied (A -> B)
- **Renamed**: `why` → `investigating-code-lineage` to align with the repository gerund naming convention (`diagnosing-bugs`, `reviewing-code`).
- **Standardized Repository Anatomy**:
  - Configured standard YAML frontmatter (`name`, `description`, `license`, `user-invocable`, `compatibility`, `allowed-tools`, `metadata`).
  - Added executive mission statement, ASCII workflow diagram, and 4 sequential phases.
- **Embedded Epistemic & Lineage Framework**:
  - Codified the 7 evidence categories directly into an inspection table.
  - Injected the defensive code heuristic: checking specifically for incidents and postmortems when encountering null guards, clamps, and retries.
  - Formalized epistemic confidence tiers into explicit labels: Facts, Inferences, and Guesses.
- **Decision Guardrails Matrix**:
  - Embedded the *Preserve / Change / Avoid / Risk* constraints matrix into the standardized reporting format.

### 3. Resulting State (B)
- A self-contained, high-signal skill for codebase archaeology and intent discovery, ensuring developers and autonomous agents uncover historical production context before modifying critical legacy logic.

### 4. Re-sync / Update Recipe
When upstream `sources/cursor-plugins` updates `pstack`:
1. Fetch latest changes in upstream:
   ```bash
   git -C sources/cursor-plugins pull
   ```
2. Diff upstream `why/` against base commit `0b8e952`:
   ```bash
   git -C sources/cursor-plugins diff 0b8e952..HEAD -- pstack/skills/why/
   ```
3. Evaluate updates to evidence categories, MCP discovery logic, or synthesis prompts.
4. Integrate valuable updates into `skills/investigating-code-lineage/SKILL.md` while preserving repository frontmatter and structure.
5. Run `make build` to verify packaging.
6. Record the new upstream commit hash, date, and changes in this changelog.
