# Changelog & Provenance: test-driven-development

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-10-24] - Test-Friction Design Remedies & Typed Partial<T> Fixture Builders

- **Upstream Repository**: `https://github.com/sickn33/agentic-awesome-skills`
- **Upstream Revision**: `6d4ea18320984083107f07ff69587fa355ee94c0` (Tag: `v20.0.0`), committed on 2026-04-20
- **Integrated Sources**:
  - `sources/agentic-awesome-skills/skills/test-driven-development/`
  - `sources/agentic-awesome-skills/skills/code-showcase-testing-patterns/`

### 1. Base State (A)
- Enforced strict Red-Green-Refactor loops, public seam testing, vertical tracer bullets, and anti-pattern guardrails (`mocking-guidelines.md`, `testing-anti-patterns.md`).
- Lacked a diagnostic lookup table translating specific test-authoring pain points into concrete architectural remedies, and Anti-Pattern 4 (`Incomplete / Partial Mocks`) lacked the idiomatic `Partial<T>` spread factory pattern.

### 2. Curated Changes Applied (A -> B)
- **`SKILL.md`**:
  - Added `### Translating Test Friction into Design Remedies` mapping four common test-writing friction signals (*Don't know how to start test*, *Mocking 4+ collaborators*, *50+ lines of fixture setup*, *Unreachable complex private helper*) to their structural design fixes.
  - Bumped `metadata.version` to `1.1`.
- **`testing-anti-patterns.md`**:
  - Enhanced Anti-Pattern 4 (`Incomplete / Partial Mocks`) with the typed `buildUserFixture(overrides: Partial<User> = {}): User` spread factory pattern (`{ ...defaultUser, ...overrides }`) so tests highlight only assertion-relevant overrides while preserving 100% schema completeness.

### 3. Resulting State (B)
- Connects TDD feedback directly to deep module refactoring and provides ergonomic, schema-complete test data builders.

### 4. Re-sync / Update Recipe
```bash
git -C sources/agentic-awesome-skills fetch origin
git -C sources/agentic-awesome-skills log -p 6d4ea18320984083107f07ff69587fa355ee94c0..origin/main -- \
  skills/test-driven-development/ skills/code-showcase-testing-patterns/
```
