# Changelog & Provenance: handing-off-sessions

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-10-24] - Synthesis & Curation from agentic-awesome-skills (v20.0.0)

- **Upstream Repository**: `https://github.com/sickn33/agentic-awesome-skills`
- **Upstream Revision**: `6d4ea18320984083107f07ff69587fa355ee94c0` (Release: `v20.0.0`), committed on 2026-04-20
- **Upstream Source Paths**:
  - `sources/agentic-awesome-skills/skills/session-handoff/`
  - `sources/agentic-awesome-skills/skills/code-refactoring-context-restore/`

### 1. Base State (A)
- Upstream `session-handoff` provided a 6-step outgoing procedure and a worked example for writing handoff notes before compaction or session reset.
- Upstream `code-refactoring-context-restore` was a brief 50-line compatibility stub focusing on reading handoff evidence and checking repository status on resumption.
- The two sides of the session handoff (outgoing snapshot creation and incoming resumption reconciliation) existed as separate, fragmented skills without a shared protocol.

### 2. Curated Changes Applied (A -> B)
- **Synthesized & Renamed**: Merged outgoing snapshot creation and incoming resumption reconciliation into a single end-to-end protocol: `handing-off-sessions`, following the repository gerund naming convention.
- **Standardized Repository Anatomy**:
  - Implemented standard YAML frontmatter schema (`name`, `description`, `license`, `user-invocable`, `compatibility`, `allowed-tools`, `metadata`).
  - Added executive mission statement, bidirectional ASCII workflow diagram, and 6 phased execution steps partitioned across outgoing and incoming agents.
- **Codified the Epistemic Boundary**:
  - Enforced strict labeling of unexecuted code as `[UNVERIFIED]`.
  - Required exact commit SHA recording (`git rev-parse HEAD`) and empirical verification outputs for completed work.
- **Mandated Discarded Path Recording**:
  - Added dedicated documentation requirements for negative decisions and discarded approaches to prevent incoming agents from repeating known traps.
- **Reconciliation & Prompt Injection Defenses**:
  - Added explicit instructions for the incoming agent to reconcile the recorded SHA against current `git diff` and working tree state.
  - Added untrusted content boundary rules instructing agents not to treat saved handoffs or embedded foreign logs as executive prompt commands.
- **Defined Anti-Patterns**:
  - Formalized table of common failure modes: Chat Transcript Dumps, Phantom Passes, Omitted Dead Ends, and Vague Next Steps.

### 3. Resulting State (B)
- A self-contained, production-grade protocol for snapshotting working context before context resets (`/compact`, `/clear`) and flawlessly restoring execution in subsequent agent sessions.

### 4. Re-sync / Update Recipe
When upstream `sources/agentic-awesome-skills` updates:
1. Fetch latest changes in upstream:
   ```bash
   git -C sources/agentic-awesome-skills pull
   ```
2. Diff upstream sources against base commit `6d4ea18`:
   ```bash
   git -C sources/agentic-awesome-skills diff 6d4ea18320984083107f07ff69587fa355ee94c0..HEAD -- skills/session-handoff/ skills/code-refactoring-context-restore/
   ```
3. Evaluate updates to context snapshotting schemas, resumption workflows, or compaction heuristics.
4. Integrate valuable additions into `skills/handing-off-sessions/SKILL.md` while preserving repository frontmatter and phased structure.
5. Record the new upstream commit hash, date, and changes in this changelog.
