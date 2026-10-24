# Changelog & Provenance: pairing-with-adhd

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-10-24] - Session Handoff Bookmark Blocks & Epistemic Uncertainty Retention

- **Upstream Sources**: Curated from `session-handoff` and `ui-review`.

### 1. Curated Changes Applied
- **`SKILL.md`**:
  - Added the 4-line **Bookmark Block** convention grounded in `git status` under Rule 5 (Restate state every turn) for task pauses and session boundaries: (1) Done & Verified, (2) Tried & Discarded, (3) Open Loops (`[Human]` vs. `[Agent]`), and (4) First Action On Return.
  - Updated pre-send checklist item 4 to retain explicit epistemic uncertainty tags (`[Unverified]`, `[Inferred]`) while removing empty hedging words.
  - Updated pre-send checklist item 5 to explicitly ban figurative idioms ("circle back", "get the ball rolling") in favor of literal actions alongside corporate slop words.

---

## [2026-09-16] - Curation from i-have-adhd & Integration with Plain English

- **Upstream Repository**: `https://github.com/ayghri/i-have-adhd.git`
- **Upstream Revision**: `b15d0be`, committed on 2026-09-16
- **Upstream Source Path**: `sources/i-have-adhd/skills/i-have-adhd/`

### 1. Base State (A)
- Upstream `i-have-adhd` provides a human-AI interaction skill designed for ADHD cognitive ergonomics: leading with next action, numbered tasks, state restatements, concrete time estimates, visible wins, and zero conversational fluff.
- Lacks formal syntactic and linguistic rules around sentence length, condition placement, modal ambiguity, or AI slop vocabulary.

### 2. Curated Changes Applied (A -> B)
- **Renamed**: `i-have-adhd` → `pairing-with-adhd` to match repository gerund authoring conventions (`executing-plans`, `reviewing-code`) and clarify its role as an interactive pairing protocol.
- **Injected Plain English Disciplines (from ASD-STE100 / SimpleEnglish)**:
  - **Condition before command**: Required stating conditions before commands with a comma ("If tests pass, deploy") to avoid reader backtracking.
  - **Modal restrictions**: Banned ambiguous modals (`should`, `would`, `could`, `may`) to eliminate hesitation; enforced imperatives and `must`/`can`.
  - **Sentence length budget**: Capped individual instructions, sentences, and list items at 20 words.
  - **Banned em-dashes**: Replaced `—` with explicit relational conjunctions ("because", "but", "so") to prevent spliced thoughts.
  - **Consistent terminology**: Enforced one word, one meaning across turns.
  - **Anti-slop vocabulary**: Wired shared reference `references/word-swaps.md` into pre-send checks to purge corporate AI filler words.
- **Shared Reference Wiring**:
  - Configured `Makefile` to link `references/word-swaps.md` as a shared reference into `pairing-with-adhd`.

### 3. Resulting State (B)
- An interaction protocol combining ADHD cognitive ergonomics (action-first, visual lists, state restatements, 5-step caps) with Plain English syntactic clarity (short sentences, condition-first, modal discipline, zero buzzwords).

### 4. Re-sync / Update Recipe
When upstream `sources/i-have-adhd` is updated:
1. Fetch latest changes in upstream:
   ```bash
   git -C sources/i-have-adhd pull
   ```
2. Diff upstream `SKILL.md` against the base commit `b15d0be`:
   ```bash
   git -C sources/i-have-adhd diff b15d0be..HEAD -- skills/i-have-adhd/
   ```
3. Review improvements to interaction rules, exception handling, or prompt phrasing.
4. Port updates into `skills/pairing-with-adhd/` while preserving:
   - The skill name `pairing-with-adhd`.
   - The `## Plain English Disciplines` section.
   - The shared reference to `references/word-swaps.md`.
5. Run `make build` to verify output packaging.
6. Record the new upstream commit hash, date, and changes in this changelog.
