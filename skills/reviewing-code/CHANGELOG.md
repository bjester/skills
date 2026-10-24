# Changelog & Provenance: reviewing-code

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-10-24] - Intent Packets, Blame on Deleted Guards, Concept-Count Test & Semantic DRY

- **Integrated Sources**:
  - `review-swarm`
  - `code-review-and-quality`
  - `differential-review`
  - `repo-native-refactor`
  - `five-axis-code-review`
  - `review-and-simplify-changes`
  - `error-debugging-multi-agent-review`

### 1. Base State (A)
- Supported 4-scale evaluation, blast-radius cross-checks, and multi-model agreement mapping.
- Lacked explicit pre-review intent framing and triage heuristics for risk-surface vs line count.
- Had no explicit directive to audit deleted/weakened checks (`-` lines) via git history.
- Did not distinguish syntactic duplication from semantic DRY or relocation of complexity from reduction.

### 2. Curated Changes Applied (A -> B)
- **Pre-Review Triage Rules (Step 1)**:
  - Added Intent Packet requirement: 3-bullet pre-review statement of intended changes, invariants to remain unchanged, and rollout/compatibility constraints.
  - Added risk-surface triage rule: evaluate depth by risk domain (auth, crypto, concurrency, serialization, guards) rather than line count.
  - Added blame on deleted/weakened guards (`-` lines): mandate `git log -S` / `git blame` or `investigating-code-lineage` before approving removed checks, timeouts, or locks.
- **Scale 1 (Macro-Scale, Resilience & Concurrency)**:
  - Added Evidence-Grounded Performance Only: mandate concrete algorithmic or I/O bottlenecks over unbounded input and ban data-free speculation.
- **Scale 2 (Strategic Architecture & Domain Boundaries)**:
  - Added Repository Conformity check: ensure diffs reuse canonical repository helpers, error envelopes, and patterns rather than introducing parallel mechanisms.
- **Scale 3 (Modularity & Depth Design)**:
  - Added The Concept-Count Test: check if refactoring reduces working memory concepts or merely relocates complexity into new files/wrappers.
  - Added Semantic DRY check: consolidate code only when shared domain owner, invariant, and change reason exist.
  - Added Resulting File Health ("Decompose, Then Add"): check if small diffs tip already-bloated modules over healthy boundaries.
- **Scale 4 (Micro-Craftsmanship)**:
  - Added Orphaned Dead Code & Redundant Derived State checks.
  - Added Observable Text & Error Contract Preservation (Hyrum's Law).
- **Multi-Model Adversarial Review Protocol (`interrogate`)**:
  - Added Rule 4 (Central Reproduction & Root-Cause Deduplication): verify leads empirically against codebase before reporting and deduplicate by root cause.
- Bumped version metadata to `1.2`.

### 3. Resulting State (B)
- A hardened code review skill that enforces rigorous pre-review triage, protects historical safety guards, grounds performance feedback in evidence, and guards modular simplicity against false DRY and complexity relocation.

---

## [2026-10-18] - Comment Hygiene & Multi-Model Adversarial Review from pstack (v0.15.26)

- **Upstream Repository**: `git@github.com:cursor/plugins.git`
- **Upstream Revision**: `0b8e952052d482ee6de06deebf14d590d77b1b34` (Release: `chore(pstack): bump to 0.15.26`), committed on 2026-10-18
- **Upstream Source Paths**:
  - `sources/cursor-plugins/pstack/skills/no-comments/`
  - `sources/cursor-plugins/pstack/skills/interrogate/`
  - `sources/cursor-plugins/pstack/skills/blast-radius/`

### 1. Base State (A)
- Provided 4-scale software engineering review checklists, standard 4-tier finding taxonomy (`🚨 Blocker`, `⚠️ Architecture`, `💡 Tactical Suggestion`, `✅ Positive Highlights`), and subagent review prompt templates.
- Lacked explicit rules against narrative code commentary and workaround sermons.
- Single-model subagent reviews were vulnerable to shared blind spots.

### 2. Curated Changes Applied (A -> B)
- **Scale 4 (Micro-Craftsmanship) - Strict Comment Hygiene**:
  - Enforced that comments are reserved strictly for non-obvious, unchangeable external constraints (vendor quirks, hardware/wire protocols).
  - Outlawed play-by-play narrative comments and workaround sermons in favor of self-documenting code and structural types/lints.
- **Scale 5 (Verification) - Blast Radius Cross-Reference**:
  - Injected blast radius analysis check referencing the `analyzing-blast-radius` skill and 5-level certainty ladder.
- **Multi-Model Adversarial Review Protocol (`interrogate`)**:
  - Added multi-model review protocol: dispatching prompts to 2+ distinct LLM families simultaneously.
  - Injected the Agreement Map: consensus findings across competing models represent high-confidence blockers.
  - Codified Lead Judgment triage (Act On, Consider, Noted, Dismissed).

### 3. Resulting State (B)
- A comprehensive local code review framework augmented with comment cleanliness, blast-radius verification, and multi-model adversarial review capabilities.

### 4. Re-sync / Update Recipe
When upstream `sources/cursor-plugins` updates `pstack`:
1. Fetch latest changes in upstream:
   ```bash
   git -C sources/cursor-plugins pull
   ```
2. Diff upstream skills against base commit `0b8e952`:
   ```bash
   git -C sources/cursor-plugins diff 0b8e952..HEAD -- pstack/skills/no-comments/ pstack/skills/interrogate/
   ```
3. Evaluate updates to review rubrics, triage standards, or comment rules.
4. Integrate relevant additions into `skills/reviewing-code/SKILL.md` while preserving the 4-scale review philosophy.
5. Run `make build` to verify packaging.
6. Record the new upstream commit hash, date, and changes in this changelog.
