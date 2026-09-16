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

- Give each skill a clear purpose and trigger description in `SKILL.md`.
- Keep a skill self-contained unless a document is genuinely reusable across
  skills. Put broadly reusable material in `references/`; keep all other
  documents and tools with the skill that uses them.
- Adapt upstream ideas into the curated files in this repository instead of
  changing files under `sources/`.
- When a skill needs a shared reference, explicitly declare it in the
  `Makefile` using that skill's `<skill-name>_REFERENCES` variable and add the
  skill name to `REFERENCE_SKILLS`. Reference paths are relative to
  `references/` and are preserved in the built skill package.

## Vendoring and upstream tracking

When adapting or importing a skill from `sources/`:

- Differentiate the destination skill name under `skills/<skill-name>/` from
  the upstream name whenever local modifications, rule loosenings, or
  cross-skill integrations are introduced.
- Maintain a `skills/<skill-name>/CHANGELOG.md` tracking:
  - Upstream repository URL, commit hash, commit date, and release tag.
  - Base state (A) of the upstream skill at that revision.
  - Curated changes applied (A -> B), detailing modified rules, injected
    disciplines, and reference wiring.
  - Resulting state (B) and operational purpose.
  - A repeatable rebase/update recipe (exact `git` commands) for future
    agents to inspect diffs and re-apply changes when upstream updates.
- Keep skill-specific reference files in `skills/<skill-name>/references/`,
  and promote only cross-skill references to top-level `references/` declared
  in the `Makefile`.
- Update the catalog table and directory structure in `README.md` when
  adding or renaming skills.

## Building and validating

- Run `make build` after changing skills, shared references, or the
  `Makefile`. It creates a complete package under `output/skills/`.
- Run `make copy-references` to build only the explicitly declared shared
  reference copies.
- Run `make clean` to remove generated `output/` files.
- Confirm a changed shared reference appears at
  `output/skills/<skill-name>/references/<reference-path>` after packaging.
