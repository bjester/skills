# Changelog & Provenance: writing-specs

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-10-24] - Hypothesis-Attached Questions, Steelmanned Alternatives, Non-Drivers & Exit Triggers

- **Upstream Repository**: `https://github.com/sickn33/agentic-awesome-skills`
- **Upstream Revision**: `6d4ea18320984083107f07ff69587fa355ee94c0` (Tag: `v20.0.0`), committed on 2026-04-20
- **Integrated Sources**:
  - `sources/agentic-awesome-skills/skills/interview-me/`
  - `sources/agentic-awesome-skills/skills/idea-to-blueprint/`

### 1. Base State (A)
- Guided collaborative requirements elicitation, bounded context isolation, deep module design, and acceptance criteria authoring before implementation planning.
- Clarifying questions did not mandate pairing a codebase-grounded hypothesis (`Q:` + `Hypothesis:`), and the spec template lacked explicit *Architectural Non-Drivers* and measurable *Exit Triggers* for simplified v1 designs.

### 2. Curated Changes Applied (A -> B)
- **`SKILL.md`**:
  - **Step 1 (`Explore Context & Understand the Idea`)**: Added **Attach a Codebase-Grounded Hypothesis (`Q:` + `Hypothesis:`)** and **Unpack Sophistication-Signaling Buzzwords** (translating vague adjectives into concrete v1 targets or explicit Non-Drivers).
  - **Step 2 (`Propose & Deliberate Approaches`) & Section 4 (`Alternate Solutions Considered`)**: Required steelmanning rejected options by stating what the rejected option would have bought, why cost outweighed benefit under current constraints, and the measurable **Exit Trigger** that would justify revisiting it.
  - **Spec Template (Sections 2 & 3)**: Added **Architectural Non-Drivers** to Non-Goals and **Mechanical Boundary Enforcement & Exit Triggers** to Proposed Architecture.
  - Bumped `metadata.version` to `1.1`.

### 3. Resulting State (B)
- Lower-friction requirements discovery grounded in codebase hypotheses, paired with anti-overengineering guardrails (*Architectural Non-Drivers* and *Exit Triggers*).

### 4. Re-sync / Update Recipe
```bash
git -C sources/agentic-awesome-skills fetch origin
git -C sources/agentic-awesome-skills log -p 6d4ea18320984083107f07ff69587fa355ee94c0..origin/main -- \
  skills/interview-me/ skills/idea-to-blueprint/
```
