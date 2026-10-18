# Changelog & Provenance: reviewing-code

Tracks upstream sources, imported commit revisions, and curated repository modifications.

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
