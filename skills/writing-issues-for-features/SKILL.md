---
name: writing-issues-for-features
description: |
  Authors actionable, non-prescriptive feature request, enhancement, and architectural
  issues on GitHub (gh) or Gitea (gt) after researching a codebase, including
  vertical-slice spec and epic decomposition. Enforces forge selection, duplicate
  search, scope non-goals, Plain prose, DEEP AI disclosure, and safe --body-file
  submission. Use for features and epics, not bugs (use writing-issues-for-bugs).
license: MIT - https://github.com/bjester/skills/blob/main/LICENSE
user-invocable: true
compatibility: Git repositories hosted on GitHub (gh) or Gitea (gt)
allowed-tools:
  - read_file
  - write_file
  - run_command
  - grep
  - ask_user_question
  - task
metadata:
  author: Blaine Jester
  version: "2.0"
---

# Writing Issues: Features

Purpose: Draft and submit actionable, well-structured feature, enhancement, and architectural issues on GitHub (`gh`) or Gitea (`gt`) without prescribing implementation details.

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. SELECT FORGE & SLICE SCOPE: Resolve gh or gt, search & slice stories │
└────────────────────────────────────┬────────────────────────────────────┘
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. DRAFT FEATURE CONTRACT: Define outcomes, non-goals & acceptance      │
└────────────────────────────────────┬────────────────────────────────────┘
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3. DE-SLOP SCAN: Verify Plain prose, word-swaps & non-prescriptive spec │
└────────────────────────────────────┬────────────────────────────────────┘
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 4. SAFE --body-file SUBMIT: Create tickets in dependency order via CLI  │
└─────────────────────────────────────────────────────────────────────────┘
```

1. **Select Forge & Slice Scope**: Run the Forge Selection Gate in [references/forge-cli.md](references/forge-cli.md) to choose `gh` or `gt` (`--no-input`), search open and closed issues for duplicates (`gh issue list --search "<keywords>" --state all --limit 20` or `gt issue list -S "<keywords>" --state all -L 20 --no-input --json number,title,state,url`), and slice multi-ticket epics vertically.
2. **Draft Feature Contract**: Populate the Feature Issue Template below with observable outcomes, public contracts, explicit non-goals, measurable acceptance criteria, and architectural pointers.
3. **De-Slop Scan**: Verify every section against `writing-technical-docs` (Plain mode), [references/word-swaps.md](references/word-swaps.md), and the Self-Review Checklist below before submission.
4. **Safe `--body-file` Submit**: Write each drafted body to `/tmp/issue-body.md`, confirm with the user before creating tickets, and submit in dependency order via `gh issue create --title "<Title>" --body-file /tmp/issue-body.md` or `gt issue create --no-input --title "<Title>" --body-file /tmp/issue-body.md`.

> [!IMPORTANT]
> Always pass `--no-input` on every `gt` command and submit issue bodies via `--body-file` rather than inline `--body "..."` strings so shell interpolation cannot corrupt backticks or code blocks.

---

## Prerequisites & Core Philosophy

- **Select Forge & Verify Target**: Follow [references/forge-cli.md](references/forge-cli.md) to resolve the target repository and select `gh` (GitHub) or `gt` (Gitea) before invoking any CLI command.
- **Specify What & Why, Not How**: Describe the desired behavior, user outcomes, and technical boundaries. Leave the concrete implementation choices to the developer.
- **Reference Shared Issue Guidelines**: Consult [references/issue-guidelines.md](references/issue-guidelines.md) for writing principles, DOs/DON'Ts, duplicate search, safe `--body-file` submission, and the DEEP AI disclosure framework.
- **Apply Plain Technical Prose**: Load the `writing-technical-docs` skill (Plain mode) and consult [references/word-swaps.md](references/word-swaps.md) to write clear, active sentences with zero em-dashes, negative parallelisms, or AI filler.
- **Incorporate Foundational Software Principles**: Consult the `engineering-software` skill for architectural boundaries (DDD bounded contexts, deep modules, schema evolution, and resilience).

---

## When to Use

- You have a feature specification, RFC, or product requirement.
- You have explored the repository and identified relevant architectural layers.
- You need to create a trackable, actionable work item for engineering.

**When NOT to Use:**
- Bug reports or defect investigations (use `writing-issues-for-bugs` instead).
- Speculative feature ideas without prior problem research or codebase exploration.

---

## Issue Title Guidelines

Focus on the **user or system capability gained**, not the code modification:

- ✅ **Good**: `Tracking Self-Referential FK Order in Store`
- ✅ **Good**: `Add sync filter parameter to cleanupsyncs command`
- ✅ **Good**: `Allow sync operations to modify dynamic filter contexts`
- ❌ **Bad**: `Add _self_ref_order field to AbstractStore`
- ❌ **Bad**: `Update SyncableModelRegistry.get_model_querysets`

---

## Feature Issue Template

````markdown
## Overview
[One-sentence summary of the feature and what capability it provides.]

### Background & Motivation
[Context explaining why this is needed now, the problem it solves, and how it aligns with system strategy.]

### User Story / Use Case
> As a [type of user/consumer],
> I want [capability],
> So that [benefit/outcome].

### Description & Expected Outcomes
[Detailed description of what the system should do. Describe user interactions, workflows, and key outcomes.]

### Value Add & Impact
[Concrete user impact, developer velocity improvement, or technical debt reduction.]

## Deliverables & Contracts
The feature should deliver the following capabilities:
- [Verifiable outcome or capability 1 using active verbs]
- [Verifiable outcome or capability 2]
- [Public interface or API contract definitions without prescribing internal implementation]

### Non-Goals / Out of Scope
- [Explicitly excluded behavior, deferred capability, or out-of-scope requirement 1]
- [Explicitly excluded behavior 2]

### Acceptance Criteria
- [ ] [Measurable, testable condition 1]
- [ ] [Measurable, testable condition 2]
- [ ] [Performance / reliability / compatibility metric target]

## Technical Pointers & Architecture
- **Target Components / Context**: [Relevant modules, e.g. `src/services/billing/`, `morango/sync/`]
- **Related Patterns**: [Reference existing patterns or precedent in the codebase]
- **Data Model & Schema Considerations**: [Note if schema migrations, backward compatibility, or tag immutability apply]
- **Resilience & Failure Modes**: [Timeouts, error handling barricades, circuit breakers if integrating with remote I/O]

## Notes & Tradeoffs
- **Dependencies**: [Blocked by or blocks #issue]
- **Testing Requirements**: [Special testing considerations: integration tests, matrix tests, performance benchmarks]
- **Tradeoffs & Alternatives Considered**: [Known limitations or rejected approaches]
- **Compatibility & Migrations**: [Backwards compatibility, deprecation windows, migration requirements]

## Metadata
**Complexity**: [Low | Medium | High]  
**Target Branch**: [main | develop | release-vX.Y]  
**Labels**: `enhancement`, `area:backend` (optional)

## AI Usage
[Disclose AI assistance following the DEEP framework: Disclose, Engage critically, Edit, Process sharing.]
````

---

## Decomposing a Spec or Epic into Multiple Issues (Vertical Slicing)

When breaking down a broad spec or epic into discrete GitHub or Gitea issues:

1. **Slice Vertically (Tracer Bullets)**: Never file horizontal layer tickets (*"Ticket 1: DB schema"*, *"Ticket 2: API"*, *"Ticket 3: UI"*). Each issue must deliver a narrow, end-to-end verifiable slice (or isolate a prerequisite prefactoring step: *"Make the change easy, then make the easy change"*).
2. **Confirm the Issue Breakdown First**: Present the numbered list of proposed issues (`Title`, `Scope summary`, `Blocked by`, `Requirements covered`) to the user for confirmation before creating tickets on GitHub or Gitea.
3. **Publish in Dependency Order**: Create foundational or blocker issues first via `gh issue create --title "<Title>" --body-file /tmp/issue-body.md` (GitHub) or `gt issue create --no-input --title "<Title>" --body-file /tmp/issue-body.md` (Gitea). Capture their real `#issue` numbers and populate `Dependencies: Blocked by #<real-id>` in downstream tickets.

---

## Self-Review Checklist Before Submitting

- [ ] **Outcome-Oriented Title**: Does the title describe the capability rather than the code fix?
- [ ] **No Implementation Prescriptions**: Are deliverables phrased as behaviors and public contracts without copy-pasting internal algorithms or classes?
- [ ] **Measurable Acceptance Criteria**: Can QA or an engineer write tests directly from the criteria?
- [ ] **Technical Orientation Provided**: Are pertinent modules and precedent patterns cited?
- [ ] **Zero AI Slop (`writing-technical-docs`)**: Verified against `writing-technical-docs` and [references/word-swaps.md](references/word-swaps.md) (zero em-dashes, negative parallelisms, or trailing `, -ing` fluff)?
- [ ] **AI Disclosure Included**: Is AI involvement stated transparently?
- [ ] **Duplicate Search & Safe CLI Creation**: Did you select the target forge per [references/forge-cli.md](references/forge-cli.md), search existing issues (`gh issue list --search "<keywords>"` or `gt issue list -S "<keywords>" --no-input`), and submit in dependency order via `--body-file` (`gh issue create --body-file` or `gt issue create --no-input --body-file`) per [references/issue-guidelines.md](references/issue-guidelines.md)?
