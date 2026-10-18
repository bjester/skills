# Changelog & Provenance: analyzing-blast-radius

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-10-18] - Synthesis & Curation from pstack blast-radius (v0.15.26)

- **Upstream Repository**: `git@github.com:cursor/plugins.git`
- **Upstream Revision**: `0b8e952052d482ee6de06deebf14d590d77b1b34` (Release: `chore(pstack): bump to 0.15.26`), committed on 2026-10-18
- **Upstream Source Path**: `sources/cursor-plugins/pstack/skills/blast-radius/`

### 1. Base State (A)
- Upstream `blast-radius` provided a concise ~50-line instruction prompt emphasizing finding breakages that grep won't show you, isolating the one safety fact, ascending the certainty ladder (levels 1-5), and avoiding narrative-only writeups.
- Bound tightly to Cursor-specific rules, model presets, and informal phrasing.

### 2. Curated Changes Applied (A -> B)
- **Renamed**: `blast-radius` → `analyzing-blast-radius` to conform to repository gerund naming conventions (`reviewing-code`, `diagnosing-bugs`).
- **Standardized Repository Anatomy**:
  - Configured standard YAML frontmatter (`name`, `description`, `license`, `user-invocable`, `compatibility`, `allowed-tools`, `metadata`).
  - Added executive mission statement, ASCII workflow diagram, and 5 structured phases.
- **Codified the 5-Level Certainty Ladder**:
  - Formalized the evidentiary tiers into an explicit markdown table: Level 1 (Agent Assertion), Level 2 (Code Pointer), Level 3 (Formal Failure Trace), Level 4 (Executable Script), and Level 5 (Live App Reproduction).
- **Structured Reporting Framework**:
  - Provided a standardized markdown reporting template: Functional Changes, Load-Bearing Safety Fact, High-Confidence Risks table, Cleared Risks, and Pre-Merge Verification Script.

### 3. Resulting State (B)
- A self-contained, rigorous skill for analyzing change impact beyond textual symbol matching, proving safety via executable scripts and verifiable runtime evidence.

### 4. Re-sync / Update Recipe
When upstream `sources/cursor-plugins` updates `pstack`:
1. Fetch latest changes in upstream:
   ```bash
   git -C sources/cursor-plugins pull
   ```
2. Diff upstream `blast-radius/` against base commit `0b8e952`:
   ```bash
   git -C sources/cursor-plugins diff 0b8e952..HEAD -- pstack/skills/blast-radius/
   ```
3. Evaluate updates to blast-radius heuristics or verification patterns.
4. Integrate valuable additions into `skills/analyzing-blast-radius/SKILL.md` while preserving repository frontmatter and structure.
5. Run `make build` to verify packaging.
6. Record the new upstream commit hash, date, and changes in this changelog.
