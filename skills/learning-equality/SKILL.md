---
name: learning-equality
description: |
  Engineering guidelines and conventions for Learning Equality repositories
  (Kolibri, Studio, KDS, ricecooker, kolibri-data-portal, le-utils), including
  Django ValuesViewset, KolibriAuth declarative permissions, le-utils constants,
  KDS component reuse, Vue Composition API, WCAG 2.2 AA accessibility, and
  RTLCSS rules. Activate when designing, developing, testing, or reviewing code
  in Learning Equality repositories.
license: MIT - https://github.com/bjester/skills/blob/main/LICENSE
user-invocable: true
compatibility: Learning Equality repositories (github.com/learningequality/*)
allowed-tools:
  - read_file
  - run_command
  - grep
  - find_by_name
metadata:
  author: Blaine Jester
  version: "1.0"
---

# Learning Equality Engineering Guidelines

Standards, architectural patterns, and review conventions for repositories under the **Learning Equality** organization (https://github.com/learningequality/).

## Organization Detection

When working on or reviewing a repository, determine if these guidelines apply by checking the git remote:

```bash
# Check if any git remote points to learningequality
git remote -v | grep -i 'learningequality'
```

If the remote matches `github.com[:/]learningequality/` (e.g. Kolibri, Kolibri Studio, kolibri-design-system, ricecooker, kolibri-data-portal, le-utils), apply these conventions alongside the `software-engineering` and `reviewing-code` skills, as well as the repository's own `AGENTS.md`.

---

## 1. Backend Architecture (Python & Django)

### API Endpoints & Values Viewsets
- **Values-Derivation Viewsets**: List/detail endpoints in Django web apps (Kolibri, Studio, kolibri-data-portal) should inherit from the repository's `ValuesViewset` / `ReadOnlyValuesViewset` base rather than raw DRF `ModelViewSet`/`GenericViewSet` to prevent N+1 queries and over-fetching.
- **Field Slicing**: Serializers and `.values()` tuples should declare only the specific columns consumed by clients.
- **Deferred / Nested Data**: Check for cartesian products on joined multi-nested serializers and batch queries using repo helpers.

### Permissions & Scoping
- **Declarative Object Permissions**: In apps with declarative permissions (e.g., `KolibriAuthPermissions`), object-level access is enforced on the model, not by ad-hoc view checks.
- **List Endpoint Filtering**: List endpoints must apply the permission-scoping filter backend (e.g. `KolibriAuthPermissionsFilter`) to avoid leaking unauthorized rows.

### Querysets & Migrations
- **Deterministic Pagination**: Sliced/paginated querysets must have deterministic ordering. Always check `Meta.ordering` on the model before flagging missing `.order_by()`.
- **N+1 Prevention**: Flag new related-field loops missing `select_related` or `prefetch_related`.
- **Django Migrations**: Model changes require a migration. Data migrations (`RunPython`) must provide `reverse_code` and batch operations for large tables.
- **Field Types**: Check for repo-specific field types (e.g., `DateTimeTzField`, syncable `UUIDField` primary keys).

### Background Tasks & Shared Constants
- **Task Framework**: Asynchronous jobs must route through the repo's task system—permission-checked at enqueue, inputs validated, and kept off high-priority user paths.
- **Shared Content Constants (`le-utils`)**: In content-ecosystem repos (Kolibri, Studio, ricecooker), content kinds, licenses, languages, and file formats must be imported from `le_utils.constants` (`file_formats`, `format_presets`, `content_kinds`, `licenses`) rather than hardcoded.

### Internationalization (Backend)
- **Strings on Default Branch Only**: User-facing backend translation strings should only be added on the default branch targeting future releases, not on release/patch branches.

---

## 2. Frontend Architecture (Vue.js, SCSS & KDS)

### Kolibri Design System (KDS) & Component Reuse
- **KDS First**: Search for existing `K*` components (`KButton`, `KModal`, `KTable`, `KSelect`, `KCircularLoader`, `KIcon`) before building custom UI controls.
- **Icon Tokens**: Use `<KIcon :icon="...">` instead of raw `<svg>` or `<img>` tags (handles RTL flipping automatically).
- **Global KDS Imports**: Do not flag missing imports for globally registered `K*` components in templates.

### Composition API & State
- **Composition API Required**: New components must use `<script setup>` or `setup()` with `ref`, `reactive`, and `computed`.
- **Vuex Deprecation**: Avoid creating new Vuex stores or adding to existing ones; use `use*` composables for state sharing.
- **Lifecycle Cleanup**: Timers, polling loops, and event listeners must be cleaned up in `onUnmounted` (check `@vueuse/core` helpers).

### Theme Tokens & Styling Rules
- **Theme Tokens**: Never hardcode colors/hex values. Use `$themeTokens` and `$themePalette`.
- **Layout & Responsive Helpers**: Use `KGrid` for grid layouts and `responsive-window` / `responsive-element` rather than raw CSS `@media` queries or arbitrary floats.
- **Scoped Styles**: Style blocks must be `<style scoped>`. Avoid unscoped global selectors and ID selectors.

### Accessibility (WCAG 2.2 AA)
- **Accessible Names**: Every interactive element (buttons, links, inputs) must have a visible label or `aria-label`/`aria-labelledby`.
- **Semantic Elements**: Never attach click handlers to generic `<div>` or `<span>` tags—use native `<button>` or `<a>`.
- **Keyboard Navigation**: Ensure Tab navigation order is logical and modal dialogs/drawers manage and restore focus.
- **Form Controls**: All inputs must have associated `<label for="...">` or wrapping labels, with help/error text linked via `aria-describedby`.

### RTL Support (Right-to-Left)
- **No Directional Inline Styles**: RTLCSS flips `<style>` blocks but cannot flip inline styles. Avoid `style="margin-left: 8px"` or `:style="{ marginLeft }"`. Use scoped CSS classes, CSS logical properties (`margin-inline-start`), or `isRtl`-aware computed properties.
- **User/Content Text**: Wrap dynamic content and user-generated text with `dir="auto"`.

### Frontend Internationalization (i18n)
- **`createTranslator`**: All user-visible strings must be registered via `createTranslator` with translator context metadata.
- **ICU Message Syntax**: Numbers, counts, and dates must be interpolated *inside* the translated string using ICU plural format (`'{count, plural, one {item} other {items}}'`), never concatenated via JS string addition.

### Frontend Testing
- **Vue Testing Library**: Author unit tests with `@testing-library/vue` on Jest. Query elements by accessible role/label (`screen.getByRole('button', { name: ... })`) rather than CSS classes or DOM internals.
- **Jest DOM Matchers**: Use `toBeInTheDocument()`, `toBeDisabled()`, `toHaveTextContent()`.
- **Avoid Stubbing**: Render real child components where possible; avoid mocking KDS components.
