# Changelog & Provenance: engineering-with-agents

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-10-24] - Empirical AI Anti-Pathologies, Pre-Write Algorithmic Rituals & Subagent Isolation

- **Upstream Repository**: `https://github.com/sickn33/agentic-awesome-skills.git`
- **Upstream Revision**: `6d4ea183` (Release: `v20.0.0`), committed on 2026-10-24
- **Upstream Source Paths**:
  - `sources/agentic-awesome-skills/clean-code-guard/`
  - `sources/agentic-awesome-skills/invariant-guard/`
  - `sources/agentic-awesome-skills/andrej-karpathy/`
  - `sources/agentic-awesome-skills/ai-coding-agent-guardrails/`
  - `sources/agentic-awesome-skills/effective-agent-skills/`
  - `sources/agentic-awesome-skills/agentflow/`

### 1. Base State (A)
- Focused on high-level agentic principles (context budgeting, two-edit behavioral testing, primary artifact verification, one-wave refactor migrations, and structural lesson encoding).
- Lacked guardrails for common autoregressive LLM failure modes (hallucinated imports, broad catch/null swallows, mock fallbacks in production, copy-adapt algorithm drift, and concurrent subagent race conditions on file edits).
- Lacked trigger/routing hygiene guidelines for skill descriptions.

### 2. Curated Changes Applied (A -> B)
- **Prerequisites & Operating Posture**:
  - Added requirements to surface unstated assumptions and trade-offs upfront instead of guessing.
  - Codified protected path protections (never stage `.env*` or private keys; require confirmation for CI/CD workflow modifications).
- **Section 1 (Context & Scoping Disciplines)**:
  - Injected **Disjoint Subagent Write Ownership** into context guarding (parallel subagents must be read-only or have strictly disjoint file sets).
  - Added **Neighbor Conformity & Orphan Cleanup** to the Laziness Protocol (mirror neighboring module patterns, purge orphaned imports, strip tutorial comments, isolate dead code cleanup).
- **Section 2 (Design & Type System Disciplines)**:
  - Added `### 3. Defeating Systematic LLM Code Pathologies`: boundary-only parsing vs. internal contract trust, prohibition of production mock fallbacks, lockfile verification of third-party APIs, and explicit derivation of loop invariants/termination variants before generating loops/recursion.
- **Section 5 (Meta-Engineering & System Evolution)**:
  - Added **Skill Routing Hygiene**: writing `description` purely as trigger/routing conditions rather than summarizing execution steps to prevent agent shortcutting.
- **Summary Checklist**:
  - Added verification item for defeating systematic AI code pathologies.

### 3. Resulting State (B)
- A battle-tested agent engineering framework hardened against hallucination drift, copy-adapt bugs, subagent concurrency conflicts, and skill routing degradation.

### 4. Re-sync / Update Recipe
When upstream `sources/agentic-awesome-skills` updates:
1. Fetch latest changes in upstream:
   ```bash
   git -C sources/agentic-awesome-skills pull
   ```
2. Diff upstream skills against base commit `6d4ea183`:
   ```bash
   git -C sources/agentic-awesome-skills diff 6d4ea183..HEAD -- clean-code-guard/ invariant-guard/ ai-coding-agent-guardrails/ effective-agent-skills/
   ```
3. Evaluate new empirical failure modes or prompt-level rituals.
4. Integrate actionable heuristics into `skills/engineering-with-agents/SKILL.md` while preserving separation from timeless engineering principles in `engineering-software`.

---

## [2026-10-18] - Synthesis & Curation from pstack (v0.15.26)

- **Upstream Repository**: `git@github.com:cursor/plugins.git`
- **Upstream Revision**: `0b8e952052d482ee6de06deebf14d590d77b1b34` (Release: `chore(pstack): bump to 0.15.26`), committed on 2026-10-18
- **Upstream Source Path**: `sources/cursor-plugins/pstack/skills/`

### 1. Base State (A)
- Upstream `pstack` shipped 24 micro-principles as individual standalone skills prefixed with `principle-*` (e.g. `principle-guard-the-context-window`, `principle-prove-it-works`, `principle-test-behavior-not-implementation`), integrated tightly into Cursor-specific `/poteto-mode` agent triggers.
- Most micro-principles contained 5–30 lines of text with Cursor-specific metadata (`disable-model-invocation: true`).
- Principles were intended to be steered via shorthand phrases in prompt turns rather than operating as unified, standalone engineering frameworks.

### 2. Curated Changes Applied (A -> B)
- **Consolidated into Unified Skill**:
  - Synthesized 8 target agentic principles into a cohesive, structured skill named `engineering-with-agents` adhering to the repository gerund naming convention.
  - Included target principles:
    - `principle-encode-lessons-in-structure`
    - `principle-exhaust-the-design-space`
    - `principle-guard-the-context-window`
    - `principle-laziness-protocol`
    - `principle-migrate-callers-then-delete-legacy-apis`
    - `principle-prove-it-works`
    - `principle-test-behavior-not-implementation`
    - `principle-type-system-discipline`
- **Standardized Repository Anatomy**:
  - Added standard YAML frontmatter (`name`, `description`, `license`, `user-invocable`, `compatibility`, `allowed-tools`, `metadata`).
  - Structured document into an executive mission statement, ASCII workflow diagram, 5 thematic sections, and an operational summary checklist.
- **Injected Operational Disciplines**:
  - Extracted and codified practical agent operating guardrails from `poteto-mode` and its architecture guides:
    - Candor over sycophancy ("No is an acceptable answer").
    - Explicit autonomy boundaries (reversible vs. irreversible actions).
    - Evidence-labeled communication (`[Measured]`, `[Inferred]`, `[Guessed]`).
- **Distributed Domain-Specific Principles**:
  - Dispatched other valuable pstack principles directly into existing repository skills:
    - `attack-the-premise` and `explain-the-number` into `skills/diagnosing-bugs/`.
    - `build-the-lever` into `skills/executing-plans/`.
    - `make-operations-idempotent` and `redesign-from-first-principles` into `skills/engineering-software/`.

### 3. Resulting State (B)
- A self-contained, high-signal engineering skill that equips both autonomous agents and paired human-agent sessions with actionable mental models for context budgeting, two-edit behavioral testing, primary artifact verification, one-wave refactor migrations, and structural lesson encoding.

### 4. Re-sync / Update Recipe
When upstream `sources/cursor-plugins` updates `pstack`:
1. Fetch latest changes in upstream:
   ```bash
   git -C sources/cursor-plugins pull
   ```
2. Diff upstream principle skills against base commit `0b8e952`:
   ```bash
   git -C sources/cursor-plugins diff 0b8e952..HEAD -- pstack/skills/principle-*
   ```
3. Evaluate any changes or additions to the 8 core principles or underlying playbooks.
4. Integrate valuable updates into `skills/engineering-with-agents/SKILL.md` while preserving repository frontmatter and section structure.
5. Run `make build` to verify packaging.
6. Record the new upstream commit hash, date, and changes in this changelog.
