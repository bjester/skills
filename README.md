# Curated LLM Skills & Tooling

A canonical collection of modular, production-ready LLM agent skills, shared software engineering references, and build automation tooling.

This repository equips AI coding assistants and autonomous agents with structured methodologies for requirements gathering, architecture design, test-driven implementation, multi-scale code reviews, git commit curation, and issue authoring.

---

## Table of Contents

- [Overview](#overview)
- [Skills Catalog](#skills-catalog)
- [Shared Engineering References](#shared-engineering-references)
- [Tooling & Build System](#tooling--build-system)
  - [Makefile Targets](#makefile-targets)
  - [Agent Tooling Requirements](#agent-tooling-requirements)
- [Repository Structure](#repository-structure)
- [Workflow & Authoring Guide](#workflow--authoring-guide)
  - [Adding a New Skill](#adding-a-new-skill)
  - [Wiring Shared References](#wiring-shared-references)
  - [Packaging & Deployment](#packaging--deployment)
- [License](#license)

---

## Overview

Modern agentic software engineering requires moving beyond raw code generation to disciplined engineering workflows. These skills encode battle-tested engineering practices centered around a unifying principle: **managing cognitive load in the presence of inevitable change and production chaos**.

Each skill is a self-contained package containing:
- **`SKILL.md`**: The primary prompt specification with YAML metadata, execution phases, and verification gates.
- **`references/`**: Domain knowledge, engineering invariants, and checklists bundled into the skill during build packaging.

---

## Skills Catalog

The repository currently provides 9 curated skills:

| Skill | Purpose | Key Capabilities |
| :--- | :--- | :--- |
| **[`writing-specs`](skills/writing-specs/)** | Specification & Architecture Design | Collaborative requirements elicitation, bounded context isolation, deep module design, and verifiable acceptance criteria before coding. |
| **[`writing-plans`](skills/writing-plans/)** | Implementation Planning | Decomposes approved specifications into ordered, bite-sized tasks with explicit TDD steps and verification checkpoints. |
| **[`executing-plans`](skills/executing-plans/)** | Plan Execution & TDD | Guides task-by-task plan execution with pragmatic red-green-refactor loops, multi-scale reviews, and verification gates. Supports both inline and subagent execution. |
| **[`reviewing-code`](skills/reviewing-code/)** | Local Code Review | Analyzes git diffs, working tree changes, and branches against foundational software engineering invariants across 4 architectural scales. |
| **[`reviewing-github-prs`](skills/reviewing-github-prs/)** | GitHub PR Review | Uses GitHub CLI (`gh`) to inspect pull requests, perform comprehensive multi-scale code reviews, and post structured, actionable review feedback. |
| **[`composing-commit-history`](skills/composing-commit-history/)** | Git Commit Curation | Uses `git reset --soft` and selective staging to transform messy working trees or WIP commits into clean, atomic, review-ready git history. |
| **[`replaying-file-revisions`](skills/replaying-file-revisions/)** | Revision Sequence Replay | Reconstructs and replays chronological iterations of specific files (e.g., prompt iterations, algorithm tuning, database migrations) into cohesive history. |
| **[`writing-github-issues-for-features`](skills/writing-github-issues-for-features/)** | Feature Issue Authoring | Authors clear, non-prescriptive GitHub feature requests focusing on observable outcomes, user requirements, and technical boundaries. |
| **[`writing-github-issues-for-bugs`](skills/writing-github-issues-for-bugs/)** | Bug Report Authoring | Generates reproducible, structured bug reports and regression investigations without dictating internal implementation details. |

---

## Shared Engineering References

Shared references located in `references/` provide deep domain context and cross-cutting standards:

- **[`references/software-engineering.md`](references/software-engineering.md)**: A synthesis of 14 foundational software engineering texts spanning 4 architectural scales:
  1. *Macro-Scale & Resilience* (distributed systems, failure domains, backpressure, idempotency).
  2. *Strategic Domain & Architecture* (bounded contexts, hexagonal/clean boundaries, ubiquitous language).
  3. *Modularity & Depth Design* (deep modules, information hiding, interface minimization).
  4. *Micro-Craftsmanship & Safety* (clean code, error ergonomics, refactoring, test discipline).
- **[`references/code-review-guidelines.md`](references/code-review-guidelines.md)**: Multi-scale review checklists, severity taxonomies (`blocker`, `warning`, `suggestion`, `question`), Delta review processes, and subagent prompt templates.
- **[`references/github-issue-guidelines.md`](references/github-issue-guidelines.md)**: Quality standards, DOs/DON'Ts, and the DEEP AI disclosure framework for issue authoring.
- **[`references/learning-equality-guidelines.md`](references/learning-equality-guidelines.md)**: Domain-specific engineering guidelines for Learning Equality repositories (Django Values ViewSets, Kolibri permissions, frontend architecture).

---

## Tooling & Build System

The repository uses GNU `make` to manage packaging, dependency injection, and installation into agent environments.

### Makefile Targets

| Command | Description |
| :--- | :--- |
| `make build` | Cleans `output/`, copies skills to `output/skills/`, and packages declared shared references into each skill's `references/` directory. |
| `make copy-references` | Resolves and copies shared references declared in `Makefile` into the packaged skill folders. |
| `make install` | Builds the distribution packages and synchronizes them to `$(INSTALL_DIR)` (`~/.vibe/` by default) via `rsync`. |
| `make clean` | Removes generated files in `output/`. |
| `make sources` | Clones upstream open-source inspiration repositories into `sources/` (git-ignored). |

### Agent Tooling Requirements

Skills declare tool dependencies in their frontmatter (`allowed-tools`). The following tool capabilities power the skills:

- **File System**: `read_file` / `view_file`, `write_file` / `replace_file_content`.
- **Search & Inspection**: `grep` / `grep_search`, `find_by_name`, `list_dir`.
- **Execution & Version Control**: `run_command` (powers `git`, `gh` CLI, test runners like `pytest`/`jest`, linters).
- **Coordination & Subagents**: `invoke_subagent`, `task` / `manage_task`, `ask_user_question`.

---

## Repository Structure

```
.
├── AGENTS.md                  # Instructions and packaging rules for AI agents
├── Makefile                   # Build automation, packaging, and install targets
├── README.md                  # Repository documentation and catalog
├── references/                # Canonical shared engineering references
│   ├── code-review-guidelines.md
│   ├── github-issue-guidelines.md
│   ├── learning-equality-guidelines.md
│   └── software-engineering.md
├── skills/                    # Canonical source definitions for each skill
│   ├── composing-commit-history/
│   │   └── SKILL.md
│   ├── executing-plans/
│   │   └── SKILL.md
│   ├── replaying-file-revisions/
│   │   └── SKILL.md
│   ├── reviewing-code/
│   │   └── SKILL.md
│   ├── reviewing-github-prs/
│   │   └── SKILL.md
│   ├── writing-github-issues-for-bugs/
│   │   └── SKILL.md
│   ├── writing-github-issues-for-features/
│   │   └── SKILL.md
│   ├── writing-plans/
│   │   └── SKILL.md
│   └── writing-specs/
│       └── SKILL.md
├── output/                    # Generated build output (git-ignored, disposable)
│   └── skills/                # Packaged skills with injected references
└── sources/                   # Upstream research repositories (git-ignored)
```

---

## Workflow & Authoring Guide

### Adding a New Skill

1. Create a new directory under `skills/<skill-name>/`.
2. Author `skills/<skill-name>/SKILL.md` with:
   - YAML frontmatter: `name`, `description`, `license`, `user-invocable`, `compatibility`, `allowed-tools`, `metadata`.
   - Core philosophy and operational guidelines.
   - Step-by-step workflow phases and verification gates.
3. Keep skill-specific documentation or scripts inside `skills/<skill-name>/`.

### Wiring Shared References

If a skill needs a reference from `references/`:
1. Add the skill name to `REFERENCE_SKILLS` in `Makefile`.
2. Define the references using `<skill-name>_REFERENCES := <reference-file.md>`.
3. Run `make build` to verify the references are copied to `output/skills/<skill-name>/references/`.

### Packaging & Deployment

Build and install skills to the local agent environment:

```bash
# Build packaged output
make build

# Install to default location (~/.vibe/)
make install

# Install to a custom directory
make install INSTALL_DIR=/path/to/target/
```

---

## License

Curated skills in this repository are licensed under the MIT License. See individual `SKILL.md` headers for specific metadata and author details.
