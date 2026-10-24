# Changelog & Provenance: writing-github-issues-for-features

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-10-24] - Non-Goals Template Section & Vertical-Slice Multi-Issue Decomposition

- **Upstream Repository**: `https://github.com/sickn33/agentic-awesome-skills`
- **Upstream Revision**: `6d4ea18320984083107f07ff69587fa355ee94c0` (Tag: `v20.0.0`), committed on 2026-04-20
- **Integrated Sources**:
  - `sources/agentic-awesome-skills/skills/to-issues/`
  - `sources/agentic-awesome-skills/skills/create-issue-gate/`
  - `sources/agentic-awesome-skills/skills/issues/`

### 1. Base State (A)
- Guided authoring of non-prescriptive feature request issues with user stories, deliverables, contracts, and acceptance criteria.
- Lacked an explicit `### Non-Goals / Out of Scope` subsection inside the issue template and had no workflow for decomposing an approved spec or epic into a dependency-ordered sequence of vertical-slice issues.

### 2. Curated Changes Applied (A -> B)
- **`SKILL.md`**:
  - Added `### Non-Goals / Out of Scope` to `## Deliverables & Contracts` in the Feature Issue Template.
  - Added `## Decomposing a Spec or Epic into Multiple Issues (Vertical Slicing)` covering vertical tracer-bullet slicing, user confirmation of the proposed breakdown, and dependency-order creation via `gh issue create --body-file` to populate real `Blocked by #<id>` links.
  - Bumped `metadata.version` to `1.1`.
- **`references/github-issue-guidelines.md` (Shared Reference)**:
  - Added `## Pre-Submission Duplicate Check & Safe CLI Creation`.

### 3. Resulting State (B)
- Supports both single feature ticket authoring with explicit scope boundaries and multi-issue vertical-slice epic decomposition.

### 4. Re-sync / Update Recipe
```bash
git -C sources/agentic-awesome-skills fetch origin
git -C sources/agentic-awesome-skills log -p 6d4ea18320984083107f07ff69587fa355ee94c0..origin/main -- \
  skills/to-issues/ skills/create-issue-gate/ skills/issues/
```
