# Changelog & Provenance: learning-equality

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-11-11] - On-Demand Sync/Multi-DB and Frontend/Packaging Architectural References

- **Provenance**: Curated from forensic audit of Learning Equality PR reviews across `morango`, `kolibri-data-portal`, `kolibri`, and `nutritionfacts`.

### 1. Base State (A)
- `SKILL.md` (`v1.1`) covered core Django `ValuesViewset`, `KolibriAuth`, `le-utils`, KDS, Vue Composition API, WCAG 2.2 AA, and RTLCSS conventions inline, without on-demand references for Morango/multi-DB/legacy SQLite traps or multi-bundle `RootVue`/telemetry/workspace packaging rules.

### 2. Curated Changes Applied (A -> B)
- **`references/sync-and-databases.md`** *(added)*: Documented legacy Python/Django compatibility floors and SQLite < 3.32's 999 bound-variable ceiling, SQLite vs. PostgreSQL deferred-FK (`TransactionTestCase`), `execute_wrapper` vs. `in_atomic_block`, and single-table expression index rules, thread-local `django.db.connections[alias]` and `DATABASE_ROUTERS=[]` testing, and `Scope` partition ordering plus sibling-repo `CHANGELOG.md` contracts.
- **`references/frontend-and-packaging.md`** *(added)*: Documented multi-bundle `RootVue` `session.user_id` redirects vs. `router.afterEach` phantom pageviews, plain-object constant maps vs. `Object.freeze` on mutating SDK options, immutable analytics string-literal tests and defensive browser hooks, and pairing `"kolibri"` with `"kolibri-*"` in `pnpm-workspace.yaml` / `.github/dependabot.yml` plus built `.whl` metadata checks.
- **`SKILL.md`**: Added `Purpose:` statement, included `morango` and `nutritionfacts` in repository scope, wired conditional progressive-disclosure triggers under `## On-Demand Architectural References`, and bumped `metadata.version` to `1.2`.

### 3. Resulting State (B)
- Modular Learning Equality guidance (`v1.2`) keeping base activation compact while loading deep sync/database or frontend/packaging ecosystem traps on demand.

---

## [2026-10-24] - Tie-Breaker Deterministic Pagination & WCAG 2.2 AA Target/Contrast/Motion Rules

- **Upstream Repository**: `https://github.com/sickn33/agentic-awesome-skills`
- **Upstream Revision**: `6d4ea18320984083107f07ff69587fa355ee94c0` (Tag: `v20.0.0`), committed on 2026-04-20
- **Integrated Sources**:
  - `sources/agentic-awesome-skills/skills/api-patterns/`
  - `sources/agentic-awesome-skills/skills/ui-review/`

### 1. Base State (A)
- Encoded Learning Equality backend (Django `ValuesViewset`, `KolibriAuth`, `le-utils`) and frontend (KDS, Vue Composition API, WCAG 2.2 AA, RTLCSS) conventions.
- Deterministic pagination rule did not explicitly call out including a unique tie-breaker field alongside non-unique timestamps, and the Accessibility section lacked explicit WCAG 2.2 SC 2.5.8 target size, contrast ratio, non-color status, and `prefers-reduced-motion` criteria.

### 2. Curated Changes Applied (A -> B)
- **`SKILL.md`**:
  - Updated **Deterministic Pagination** under `### Querysets & Migrations` to require a unique tie-breaker key (e.g., `.order_by('created_at', 'id')`) so rows with identical timestamps cannot duplicate or skip across page boundaries.
  - Expanded `### Accessibility (WCAG 2.2 AA)` with **Target Size & Focus Visibility** (`24x24` CSS px minimum per SC 2.5.8, `44x44` px preferred for touch, visible `:focus-visible`) and **Contrast, Non-Color State & Motion** (`4.5:1` / `3:1` contrast ratios, pairing color with text or `<KIcon>`, and `prefers-reduced-motion`).
  - Bumped `metadata.version` to `1.1`.

### 3. Resulting State (B)
- Strengthened pagination determinism and concrete WCAG 2.2 AA verification criteria for Learning Equality repositories.

### 4. Re-sync / Update Recipe
```bash
git -C sources/agentic-awesome-skills fetch origin
git -C sources/agentic-awesome-skills log -p 6d4ea18320984083107f07ff69587fa355ee94c0..origin/main -- \
  skills/api-patterns/ skills/ui-review/
```
