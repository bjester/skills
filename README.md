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

The repository currently provides curated skills across the software lifecycle:

| Skill | Purpose | Key Capabilities |
| :--- | :--- | :--- |
| **[`auditing-security`](skills/auditing-security/)** | Defensive Security Audits & Guidance | 6-phase vulnerability discovery harness (Cloudflare): reconnaissance, coverage ledger, adversarial verifier testing, and 10 domain attack companions with zero-dependency validators. Supports both conversational guidance and full autonomous audits. |
| **[`analyzing-blast-radius`](skills/analyzing-blast-radius/)** | Hidden Breakage & Blast Radius Analysis | Discovers lifecycle, wire format, and runtime hazards beyond symbol search (`grep`). Isolates the single load-bearing safety fact and ascends the 5-level certainty ladder to executable proof. |
| **[`investigating-code-lineage`](skills/investigating-code-lineage/)** | Codebase Archaeology & Intent Discovery | Discovers historical intent and incident scar tissue behind defensive/unintuitive code across 7 evidence sources (git, issues, docs, chat, traces) with strict epistemic confidence. |
| **[`generating-verification-harnesses`](skills/generating-verification-harnesses/)** | Autonomous Verification Driver Generator | Inspects unfamiliar codebases to generate project-local headless verification drivers (`verify-<app>`) with Launch, Doctor, Drive, Evidence, and living Feature Maps. |
| **[`writing-specs`](skills/writing-specs/)** | Specification & Architecture Design | Collaborative requirements elicitation, bounded context isolation, deep module design, and verifiable acceptance criteria before coding. |
| **[`writing-plans`](skills/writing-plans/)** | Implementation Planning | Decomposes approved specifications into ordered, bite-sized tasks with explicit TDD steps and verification checkpoints. |
| **[`executing-plans`](skills/executing-plans/)** | Plan Execution & TDD | Guides task-by-task plan execution with pragmatic red-green-refactor loops, multi-scale reviews, and verification gates. Supports both inline and subagent execution. |
| **[`software-engineering`](skills/software-engineering/)** | Foundational Software Invariants | Synthesizes 14 classic software engineering texts across 4 scales: macro-resilience, strategic DDD/Clean boundaries, deep modularity, and craftsmanship. |
| **[`engineering-with-agents`](skills/engineering-with-agents/)** | Disciplines for Autonomous & Paired LLM Development | Operational guardrails for agentic software engineering: context guarding, laziness protocol, side-by-side prototyping, branded types, one-wave migrations, primary artifact verification, and two-edit behavioral tests. |
| **[`diagnosing-bugs`](skills/diagnosing-bugs/)** | Systematic Debugging & Diagnostics | 6-phase hypothesis-driven diagnosis loop, tight automated feedback loops, load-bearing minimization, root-cause tracing, 4-layer defense in depth, and secret redaction. |
| **[`test-driven-development`](skills/test-driven-development/)** | Test-Driven Development (TDD) | Strict red-green-refactor discipline, public seam testing, vertical tracer bullets, and testing anti-pattern prevention before writing production code. |
| **[`reviewing-code`](skills/reviewing-code/)** | Local Code Review | Analyzes git diffs, working tree changes, and branches against foundational software engineering invariants across 4 architectural scales with multi-model adversarial review. |
| **[`reviewing-github-prs`](skills/reviewing-github-prs/)** | GitHub PR Review | Uses GitHub CLI (`gh`) to inspect pull requests, perform comprehensive multi-scale code reviews, and post structured, actionable review feedback. |
| **[`composing-commit-history`](skills/composing-commit-history/)** | Git Commit Curation | Uses `git reset --soft` and selective staging to transform messy working trees or WIP commits into clean, atomic, review-ready git history. |
| **[`replaying-file-revisions`](skills/replaying-file-revisions/)** | Revision Sequence Replay | Reconstructs and replays chronological iterations of specific files (e.g., prompt iterations, algorithm tuning, database migrations) into cohesive history. |
| **[`retrieving-developer-knowledge`](skills/retrieving-developer-knowledge/)** | Google Developer Knowledge Retrieval | Searches, retrieves, and synthesizes official Google documentation across Google Cloud, Gemini/AI, Android, Web, Go, and Firebase via MCP tools or REST API fallback. |
| **[`writing-github-issues-for-features`](skills/writing-github-issues-for-features/)** | Feature Issue Authoring | Authors clear, non-prescriptive GitHub feature requests focusing on observable outcomes, user requirements, and technical boundaries. |
| **[`writing-technical-docs`](skills/writing-technical-docs/)** | Technical Documentation & ASD-STE100 | Enforces Simplified Technical English and plain English rules for documentation, specifications, runbooks, and release notes to eliminate AI slop and ambiguity. |
| **[`pairing-with-adhd`](skills/pairing-with-adhd/)** | Action-First ADHD Pairing & Dialogue | Shapes interactive AI-human communication: leads with runnable next actions, numbers tasks (max 5), restates state, and eliminates conversational filler with Plain English discipline. |
| **[`learning-equality`](skills/learning-equality/)** | Learning Equality Conventions | Engineering guidelines for Learning Equality repositories: Django Values ViewSets, KolibriAuth permissions, KDS components, Vue Composition API, WCAG 2.2 AA, and RTLCSS. |

---

## Shared Engineering References

Shared references located in `references/` provide deep domain context and cross-cutting standards:

- **[`references/decision-log-template.tsv`](references/decision-log-template.tsv)**: Append-only decision ledger schema (`ts`, `phase`, `decision`, `why`, `evidence`, `result`) for multi-phase and unattended agent plan execution.
- **[`references/github-issue-guidelines.md`](references/github-issue-guidelines.md)**: Quality standards, DOs/DON'Ts, and the DEEP AI disclosure framework for issue authoring.
- **[`references/word-swaps.md`](references/word-swaps.md)**: Slop-to-plain word mappings and syntactic AI tell eradication rules shared across documentation and communication skills.

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
│   ├── decision-log-template.tsv
│   ├── github-issue-guidelines.md
│   └── word-swaps.md
├── skills/                    # Canonical source definitions for each skill
│   ├── analyzing-blast-radius/
│   │   ├── CHANGELOG.md
│   │   └── SKILL.md
│   ├── auditing-security/
│   │   ├── CHANGELOG.md
│   │   ├── SKILL.md
│   │   ├── RECONNAISSANCE.md
│   │   ├── HUNTING.md
│   │   ├── VALIDATION-AND-REPORTING.md
│   │   ├── ATTACK-CLASSES.md
│   │   ├── report-schema.json
│   │   ├── validate-coverage-ledger.cjs
│   │   └── ... (10 domain companions & validators)
│   ├── composing-commit-history/
│   │   └── SKILL.md
│   ├── diagnosing-bugs/
│   │   ├── CHANGELOG.md
│   │   ├── SKILL.md
│   │   ├── condition-based-waiting.md
│   │   ├── defense-in-depth.md
│   │   ├── root-cause-tracing.md
│   │   ├── examples/
│   │   │   └── condition-based-waiting-example.ts
│   │   └── scripts/
│   │       ├── find-polluter.sh
│   │       └── hitl-loop.template.sh
│   ├── engineering-with-agents/
│   │   ├── CHANGELOG.md
│   │   └── SKILL.md
│   ├── executing-plans/
│   │   ├── CHANGELOG.md
│   │   └── SKILL.md
│   ├── generating-verification-harnesses/
│   │   ├── CHANGELOG.md
│   │   └── SKILL.md
│   ├── investigating-code-lineage/
│   │   ├── CHANGELOG.md
│   │   └── SKILL.md
│   ├── learning-equality/
│   │   └── SKILL.md
│   ├── pairing-with-adhd/
│   │   ├── CHANGELOG.md
│   │   └── SKILL.md
│   ├── replaying-file-revisions/
│   │   └── SKILL.md
│   ├── retrieving-developer-knowledge/
│   │   ├── CHANGELOG.md
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── api-fallback.md
│   │       ├── mcp-usage.md
│   │       └── supported-domains.md
│   ├── reviewing-code/
│   │   ├── CHANGELOG.md
│   │   └── SKILL.md
│   ├── reviewing-github-prs/
│   │   ├── CHANGELOG.md
│   │   └── SKILL.md
│   ├── software-engineering/
│   │   ├── CHANGELOG.md
│   │   └── SKILL.md
│   ├── test-driven-development/
│   │   ├── SKILL.md
│   │   ├── mocking-guidelines.md
│   │   └── testing-anti-patterns.md
│   ├── writing-github-issues-for-bugs/
│   │   └── SKILL.md
│   ├── writing-github-issues-for-features/
│   │   └── SKILL.md
│   ├── writing-plans/
│   │   └── SKILL.md
│   ├── writing-specs/
│   │   └── SKILL.md
│   └── writing-technical-docs/
│       ├── CHANGELOG.md
│       ├── SKILL.md
│       └── references/
│           ├── rule-catalog.md
│           ├── strict-vocabulary.md
│           └── use-cases.md
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
