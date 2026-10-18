# Changelog & Provenance: executing-plans

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-10-18] - Build the Lever from pstack (v0.15.26)

- **Upstream Repository**: `git@github.com:cursor/plugins.git`
- **Upstream Revision**: `0b8e952052d482ee6de06deebf14d590d77b1b34` (Release: `chore(pstack): bump to 0.15.26`), committed on 2026-10-18
- **Upstream Source Path**: `sources/cursor-plugins/pstack/skills/principle-build-the-lever/`

### 1. Base State (A)
- Provided task-by-task plan execution protocols supporting contextual TDD (greenfield, business logic, legacy seams), subagent vs. inline pathways, incremental implementation rules, and 4-scale code review checkpoints.
- Left the mechanics of broad, repetitive, or multi-callsite plan edits to manual execution, increasing the risk of mechanical errors and hallucinated variations across files.

### 2. Curated Changes Applied (A -> B)
- **Section 3 (Incremental Implementation Rules)**:
  - Injected **Rule 4: Build the Lever Over Manual Churn (Script the Sweep)**:
    - Directed agents to author deterministic scripts, codemods, or generators for non-trivial, repetitive edits across multiple files (updating 10+ callsites, structural renames, schema updates) rather than editing files manually one by one.
    - Codified the **First-Unit Proof** protocol: perform the transformation manually on a single unit to refine the recipe, author the script/codemod, run it, and confirm diff equivalence before executing across all targets.
    - Articulated reviewability value: a script turns *"trust me, I edited 30 files manually"* into an auditable artifact that human reviewers can rerun.
    - Enforced that a deterministic local script running in one pass beats spawning multiple subagents to hand-apply mechanical changes.
  - Injected **Rule 5: Keep a Decision Ledger for Multi-Phase or Unattended Runs (`show-me-your-work`)**:
    - Established an append-only TSV decision ledger at `.plans/decisions.tsv` based on `references/decision-log-template.tsv`.
    - Enforced pointer-based evidence (commits, line numbers, test outputs) over prose summaries.
    - Added mandatory end-of-run transcript auditing to verify that logged decisions reflect actual execution.
- **Shared Reference Wiring**:
  - Wired `references/decision-log-template.tsv` via `Makefile` into `output/skills/executing-plans/references/`.

### 3. Resulting State (B)
- A robust plan execution harness that prioritizes deterministic automation, verifiable tooling, and transparent append-only decision ledgers over manual repetitive file edits and unreviewable autonomous runs.

### 4. Re-sync / Update Recipe
When upstream `sources/cursor-plugins` updates `pstack`:
1. Fetch latest changes in upstream:
   ```bash
   git -C sources/cursor-plugins pull
   ```
2. Diff upstream principle skills against base commit `0b8e952`:
   ```bash
   git -C sources/cursor-plugins diff 0b8e952..HEAD -- pstack/skills/principle-build-the-lever/
   ```
3. Evaluate updates to lever patterns, codemod recipes, or tool authoring guidance.
4. Integrate relevant additions into `skills/executing-plans/SKILL.md` while preserving execution pathways and TDD strategies.
5. Run `make build` to verify packaging.
6. Record the new upstream commit hash, date, and changes in this changelog.
