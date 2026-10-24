# Changelog & Provenance: engineering-software

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-10-24] - Classical Contracts, Wrong-Abstraction Inlining & Dependency Tension Curation

- **Upstream Repository**: `https://github.com/sickn33/agentic-awesome-skills.git`
- **Upstream Revision**: `6d4ea183` (Release: `v20.0.0`), committed on 2026-10-24
- **Upstream Source Paths**:
  - `sources/agentic-awesome-skills/invariant-guard/`
  - `sources/agentic-awesome-skills/clean-code-guard/`

### 1. Base State (A)
- DbC taxonomy codified preconditions, postconditions, and class invariants, but lacked loop invariants and termination variant guarantees.
- Refactoring guidelines included the Rule of Three, preparatory refactoring, and code smells, but did not distinguish domain knowledge DRY from incidental code duplication, nor define wrong-abstraction re-inlining and cognitive complexity limits.
- Architectural tensions addressed Clean Code vs. deep modules, DDD vs. transaction scripts, and fail-fast vs. degradation, but lacked an explicit tension resolving Generic Subdomain reuse against zero-dependency supply-chain resilience.

### 2. Curated Changes Applied (A -> B)
- **Section 5 (Defensive Programming, Contracts & Error Handling)**:
  - Added *Loop Invariants & Termination Variants* to the Design by Contract (DbC) pillar (`Loop Invariant ∧ Exit Condition ⇒ Postcondition`), ensuring invariant gaps in complex multi-pass algorithms are explicitly closed.
- **Section 6 (Refactoring Disciplines & Code Smell Taxonomy)**:
  - Added **Knowledge DRY vs. The Wrong Abstraction (Sandi Metz Corollary)**: distinguishing knowledge/intent duplication from textual coincidence, codifying re-inlining of bloated abstractions, and setting cyclomatic complexity `≤ 10` and nesting depth `≤ 5`.
- **Section 11 (Resolving Architectural Tensions & Trade-Offs)**:
  - Added **Tension 4: Generic Subdomain Reuse (Avoid NIH) vs. Supply-Chain & Maintenance Surface (Zero-Dependency Bias)**, favoring native standard libraries for mechanics `< 15` lines and third-party dependencies strictly for deep domain/protocol complexity.

### 3. Resulting State (B)
- A rigorously hardened engineering foundation incorporating classical Hoare-Dijkstra contract verification, Sandi Metz abstraction pragmatism, and supply-chain risk balancing while keeping all LLM-specific operational rituals encapsulated in `engineering-with-agents`.

### 4. Re-sync / Update Recipe
When upstream `sources/agentic-awesome-skills` updates:
1. Fetch latest changes in upstream:
   ```bash
   git -C sources/agentic-awesome-skills pull
   ```
2. Diff upstream skills against base commit `6d4ea183`:
   ```bash
   git -C sources/agentic-awesome-skills diff 6d4ea183..HEAD -- invariant-guard/ clean-code-guard/
   ```
3. Evaluate updates to invariant assertions, refactoring heuristics, or complexity bounds.
4. Port timeless software engineering principles into `skills/engineering-software/SKILL.md` while routing LLM-specific guardrails to `skills/engineering-with-agents/SKILL.md`.

---

## [2026-10-18] - Renamed to Gerund Convention (`engineering-software`)

- Renamed skill from `software-engineering` to `engineering-software` to adhere to repository gerund phrase conventions (`<verb-ing>-<noun>`).
- Updated skill frontmatter, title, and cross-skill references across the repository.

---

## [2026-10-18] - Operational Idempotency & First-Principles Redesign from pstack (v0.15.26)

- **Upstream Repository**: `git@github.com:cursor/plugins.git`
- **Upstream Revision**: `0b8e952052d482ee6de06deebf14d590d77b1b34` (Release: `chore(pstack): bump to 0.15.26`), committed on 2026-10-18
- **Upstream Source Paths**:
  - `sources/cursor-plugins/pstack/skills/principle-make-operations-idempotent/`
  - `sources/cursor-plugins/pstack/skills/principle-redesign-from-first-principles/`

### 1. Base State (A)
- Synthesized from 14 foundational software engineering texts (Fowler, Evans, Ousterhout, Nygard, Kleppmann, Beck, Feathers, Martin, etc.) covering 4 architectural scales, 7 universal invariants, Clean/Hexagonal architecture, and distributed storage systems.
- Mentioned idempotency only in passing as an error-semantic example ("idempotent delete") without articulating state reconciliation or mid-crash recovery rules.
- Addressed refactoring and change through legacy seams and Fowler recipes without an explicit design heuristic for rethinking architectures from scratch when absorbing major new requirements.

### 2. Curated Changes Applied (A -> B)
- **Section 1 (Philosophy, Mindset & Complexity Management)**:
  - Injected **Redesign from First Principles**: When integrating a major requirement or new capability, avoid reflexively bolting on adapters, shims, or pass-through wrappers. First ask: *"If this system were being written from scratch today with this requirement as a foundational assumption, what would we build?"* Design the target structure holistically, then execute the transition incrementally.
- **Section 8 (Production Resilience, Stability & Concurrency)**:
  - Added **Idempotent Reconciliation** to the *Stability Patterns Matrix* (deriving state changes from current vs. desired delta to safely converge on retries or crash recovery).
  - Codified **Operational Idempotency & Crash Reconciliation** under *Concurrency & State Management*:
    - *Diff-Against-State*: Derive each mutating step from the state that currently exists, not from what a prior run intended to do.
    - *Crash-Point Resilience*: Recognize partial artifacts as stale using intrinsic evidence (content hashes, atomic renames) rather than fragile timestamps.
    - *The 3-Question Invariant*: (1) What happens if this runs twice consecutively? (2) What happens if the previous run crashed at every intermediate step? (3) Does re-execution converge deterministically to the identical end state?

### 3. Resulting State (B)
- A comprehensive foundational engineering standard that pairs deep module design and hexagonal boundaries with rigorous operational idempotency and first-principles architectural evolution.

### 4. Re-sync / Update Recipe
When upstream `sources/cursor-plugins` updates `pstack`:
1. Fetch latest changes in upstream:
   ```bash
   git -C sources/cursor-plugins pull
   ```
2. Diff upstream principle skills against base commit `0b8e952`:
   ```bash
   git -C sources/cursor-plugins diff 0b8e952..HEAD -- pstack/skills/principle-make-operations-idempotent/ pstack/skills/principle-redesign-from-first-principles/
   ```
3. Evaluate updates to idempotency formulas or first-principles reasoning.
4. Port valuable additions into `skills/engineering-software/SKILL.md` while preserving the 4-scale structure and foundational text synthesis.
5. Run `make build` to verify packaging.
6. Record the new upstream commit hash, date, and changes in this changelog.
