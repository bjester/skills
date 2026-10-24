# Changelog & Provenance: analyzing-agent-sessions

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-10-24] - Synthesis & Curation from agentic-awesome-skills (v20.0.0)

- **Upstream Repository**: `https://github.com/sickn33/agentic-awesome-skills`
- **Upstream Revision**: `6d4ea18320984083107f07ff69587fa355ee94c0` (Release: `v20.0.0`), committed on 2026-04-20
- **Upstream Source Path**: `sources/agentic-awesome-skills/skills/analyze-project/`

### 1. Base State (A)
- Upstream `analyze-project` was a 449-line diagnostic document for Antigravity coding sessions that established session intent classifications, prompt sufficiency scoring, scope change classifications, rework shape patterns, root causes, severity scoring, and file clustering.
- It was framed around an informal slash command (`/analyze-project`) and mixed general metrics with platform-specific instructions.

### 2. Curated Changes Applied (A -> B)
- **Renamed**: `analyze-project` → `analyzing-agent-sessions` to align with the repository gerund phrase naming convention (`analyzing-blast-radius`, `investigating-code-lineage`).
- **Standardized Repository Anatomy**:
  - Configured standard YAML frontmatter schema (`name`, `description`, `license`, `user-invocable`, `compatibility`, `allowed-tools`, `metadata`).
  - Added executive mission statement, ASCII workflow diagram, and 5 sequential execution phases.
- **Embedded Forensic Taxonomy**:
  - Retained and streamlined the forensic taxonomy: Intent Classification (`DELIVERY`, `DEBUGGING`, `REFACTOR`, `RESEARCH`, `EXPLORATION`, `AUDIT_ANALYSIS`), Prompt Sufficiency Scoring (0–2 scale), Scope Delta Categorization (`Human`, `Discovered`, `Agent`), Rework Shapes (`Clean`, `Early Replan`, `Progressive Expansion`, `Reopen/Reclose`, `Late Verification Churn`, `Abandoned`), and Root Causes (`SPEC_AMBIGUITY`, `HUMAN_SCOPE_CHANGE`, `REPO_FRAGILITY`, `AGENT_ARCHITECTURAL_ERROR`, `VERIFICATION_CHURN`, `LEGITIMATE_TASK_COMPLEXITY`).
- **Codified Evidentiary Hierarchy**:
  - Formalized evidentiary precedence: Artifact content > Transcript tool events > Timestamps > Inference.
- **Structured Systemic Interventions**:
  - Partitioned post-mortem recommendations into 3 targeted categories: Prompting improvements, Repository health (code/test fixes), and Agent workflow guardrails (skill activations).

### 3. Resulting State (B)
- A self-contained, high-signal forensic skill for analyzing AI coding agent sessions and brain artifacts to diagnose execution breakdowns, prompt ambiguity, and repository friction hotspots.

### 4. Re-sync / Update Recipe
When upstream `sources/agentic-awesome-skills` updates:
1. Fetch latest changes in upstream:
   ```bash
   git -C sources/agentic-awesome-skills pull
   ```
2. Diff upstream `analyze-project/` against base commit `6d4ea18`:
   ```bash
   git -C sources/agentic-awesome-skills diff 6d4ea18320984083107f07ff69587fa355ee94c0..HEAD -- skills/analyze-project/
   ```
3. Evaluate updates to forensic classification patterns, prompt scoring criteria, or artifact analysis routines.
4. Integrate valuable additions into `skills/analyzing-agent-sessions/SKILL.md` while preserving repository frontmatter and phased structure.
5. Record the new upstream commit hash, date, and changes in this changelog.
