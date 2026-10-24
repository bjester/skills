---
name: writing-github-issues-for-features
description: "Use when creating GitHub issues to track feature requests, enhancements, or architectural work after researching a codebase."
license: MIT - https://github.com/bjester/skills/blob/main/LICENSE
user-invocable: true
compatibility: a software project hosted on GitHub
allowed-tools:
  - read_file
  - run_command
  - grep
  - ask_user_question
  - task
metadata:
  author: Blaine Jester
  version: "1.1"
---

# Writing GitHub Issues: Features

Purpose: Facilitate the creation of actionable, well-structured GitHub issues for new features, enhancements, and architectural capabilities without prescribing implementation details.

## Prerequisites & Core Philosophy

- **Specify What & Why, Not How**: Describe the desired behavior, user outcomes, and technical boundaries. Leave the concrete implementation choices to the developer.
- **Reference Shared Issue Guidelines**: Consult `references/github-issue-guidelines.md` for writing principles, DOs/DON'Ts, and the DEEP AI disclosure framework.
- **Incorporate Foundational Software Principles**: Consult the `engineering-software` skill for architectural boundaries (DDD bounded contexts, deep modules, schema evolution, and resilience).

---

## When to Use

- You have a feature specification, RFC, or product requirement.
- You've explored the repository and identified relevant architectural layers.
- You need to create a trackable, actionable work item for engineering.

**When NOT to Use:**
- Bug reports or defect investigations (use `writing-github-issues-for-bugs` instead).
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

When breaking down a broad spec or epic into discrete GitHub issues:

1. **Slice Vertically (Tracer Bullets)**: Never file horizontal layer tickets (*"Ticket 1: DB schema"*, *"Ticket 2: API"*, *"Ticket 3: UI"*). Each issue must deliver a narrow, end-to-end verifiable slice (or isolate a prerequisite prefactoring step: *"Make the change easy, then make the easy change"*).
2. **Confirm the Issue Breakdown First**: Present the numbered list of proposed issues (`Title`, `Scope summary`, `Blocked by`, `Requirements covered`) to the user for confirmation before creating tickets on GitHub.
3. **Publish in Dependency Order**: Create foundational/blocker issues via `gh issue create --body-file` *first*, capture their real `#issue` numbers, and populate `Dependencies: Blocked by #<real-id>` in downstream tickets.

---

## Self-Review Checklist Before Submitting

- [ ] **Outcome-Oriented Title**: Does the title describe the capability rather than the code fix?
- [ ] **No Implementation Prescriptions**: Are deliverables phrased as behaviors and public contracts without copy-pasting internal algorithms or classes?
- [ ] **Measurable Acceptance Criteria**: Can QA or an engineer write tests directly from the criteria?
- [ ] **Technical Orientation Provided**: Are pertinent modules and precedent patterns cited?
- [ ] **AI Disclosure Included**: Is AI involvement stated transparently?

