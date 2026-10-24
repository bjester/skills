# Curated LLM Skills

This repository is the canonical home for curated and customized LLM skills,
the reference documents they use, and their supporting tools. Make changes to
the repository-owned content here; generated packages are disposable.

## Repository layout

- `skills/<skill-name>/` contains a skill. Its `SKILL.md` is the skill's
  entrypoint; keep skill-specific assets, changelogs, and tools beside it.
- `references/` contains reference documents shared by more than one skill.
- `sources/` contains read-only upstream projects used for research and
  inspiration. Do not modify, package, or treat their contents as this
  repository's maintained skill definitions.
- `output/` is generated packaging output. Never edit it directly.

## Authoring skills

- **Naming**: Use the gerund phrase convention (`<verb-ing>-<noun>`, e.g.,
  `writing-specs`, `reviewing-code`, `diagnosing-bugs`, `retrieving-developer-knowledge`).
- **Standard YAML Frontmatter**: Every `SKILL.md` must define the following
  required metadata keys:
  ```yaml
  ---
  name: <skill-name>
  description: "<trigger conditions, scope, capabilities, and anti-patterns>"
  license: MIT - https://github.com/bjester/skills/blob/main/LICENSE
  user-invocable: true
  compatibility: <target environment / tool prerequisites>
  allowed-tools:
    - <tool-1>
    - <tool-2>
  metadata:
    author: Blaine Jester
    version: "1.0"
  ---
  ```
- **Document Anatomy**:
  - Title: `# <Skill Name>` in title case matching the skill's role.
  - Purpose: `Purpose: <one-sentence executive mission statement>`.
  - Workflow: An ASCII workflow diagram visualizing phases and feedback loops.
  - Phased Execution: Numbered, sequential steps with explicit verification gates.
  - Visual hierarchy: Use GitHub-style alerts (`> [!NOTE]`, `> [!TIP]`, `> [!WARNING]`).
- **Self-Contained References**: Keep a skill self-contained unless a document is
  genuinely reusable across skills. Put broadly reusable material in `references/`;
  keep all other documents and tools with the skill that uses them.
- **Shared References Wiring**: When a skill needs a shared reference, explicitly
  declare it in the `Makefile` using that skill's `<skill-name>_REFERENCES` variable
  and add the skill name to `REFERENCE_SKILLS`. Reference paths are relative to
  `references/` and are preserved in the built skill package.
- **`engineering-software` vs. `engineering-with-agents` Boundary**:
  - `engineering-software` captures timeless, human-relatable software engineering
    principles, architectural invariants, Design by Contract, and refactoring
    disciplines that apply equally to human and agent engineers.
  - `engineering-with-agents` captures LLM-specific behavioral guardrails,
    prompt-level rituals, context hygiene, and countermeasures against
    autoregressive agent pathologies (e.g., proxy verification, pattern-matching
    drift, cognitive debt).
  - When curating or adapting guidance that blends both, split the timeless
    computer science principle into `engineering-software` and the agent-specific
    procedural guardrail into `engineering-with-agents`.

## Vendoring and upstream tracking

When adapting or importing a skill from `sources/`:

- Differentiate the destination skill name under `skills/<skill-name>/` from
  the upstream name whenever local modifications, rule loosenings, or
  cross-skill integrations are introduced. Follow the gerund naming convention.
- **Import & Standardization Checklist**:
  1. **Rename**: Convert upstream name to the repository gerund phrase convention.
  2. **Standardize Frontmatter**: Replace upstream frontmatter with the repository
     YAML schema (`license`, `user-invocable`, `compatibility`, `allowed-tools`,
     `metadata`).
  3. **Structure Document**: Ensure Title `# <Name>`, `Purpose:`, ASCII workflow
     diagram, and phased steps are present.
  4. **Encapsulate References**: Retain skill-specific references in
     `skills/<skill-name>/references/`; promote only cross-skill references to
     top-level `references/` declared in `Makefile`.
  5. **Create `CHANGELOG.md`**: Maintain `skills/<skill-name>/CHANGELOG.md` tracking:
     - Upstream repository URL, commit hash, commit date, and release tag.
     - Base state (A) of the upstream skill at that revision.
     - Curated changes applied (A -> B), detailing modified rules, injected
       disciplines, and reference wiring.
     - Resulting state (B) and operational purpose.
     - A repeatable rebase/update recipe (exact `git` commands) for future
       agents to inspect diffs and re-apply changes when upstream updates.
  6. **Update Catalog & Tree in `README.md`**: Update both the Skills Catalog
     table and the repository structure tree in `README.md`.
  7. **Build & Validate**: Run `make build` **and** `make validate`. Confirm
     all files and references are packaged in `output/skills/<skill-name>/` and
     validation exits 0.

## Building and validating

- Run `make build` after changing skills, shared references, or the
  `Makefile`. It creates a complete package under `output/skills/`.
- Run `make validate` after changing skills, shared references,
  `.shinyskills.toml`, or the `Makefile`; it must exit 0.
- Run `make copy-references` to build only the explicitly declared shared
  reference copies.
- Run `make clean` to remove generated `output/` files.
- Confirm a changed shared reference appears at
  `output/skills/<skill-name>/references/<reference-path>` after packaging.
