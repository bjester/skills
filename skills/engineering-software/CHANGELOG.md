# Changelog & Provenance: engineering-software

Tracks upstream sources, imported commit revisions, and curated repository modifications.

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
