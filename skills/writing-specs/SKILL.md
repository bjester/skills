---
name: writing-specs
description: "You MUST use this to explore user intent, requirements, and design before turning those into reality: either the creation of corresponding specs/plans or any changes to software functionality, architecture, or behavior."
license: MIT - https://github.com/bjester/skills/blob/main/LICENSE
user-invocable: true
compatibility: a software project with git version control
allowed-tools:
  - read_file
  - write_file
  - grep
  - ask_user_question
  - task
metadata:
  author: Blaine Jester
  version: "1.0"
---

# Writing Specifications

Purpose: Turn ideas and requirements into robust, fully formed technical specifications and designs through collaborative dialogue before writing code or implementation plans.

## Prerequisites & Core Philosophy

- **Never code without an approved spec**: Code written without a specification is guessing. Writing a spec forces you to examine the problem, manage cognitive load, isolate failure modes, and surface implicit assumptions before writing code.
- **Manage cognitive load & complexity**: Complexity is the enemy (manifested through change amplification, cognitive load, and unknown unknowns). A good spec isolates bounded contexts, establishes deep modules, and adheres to strict inward dependency rules.
- **Reference Software Engineering Invariants**: Always adhere to the `engineering-software` skill for architectural patterns, boundary definitions (Clean/Hexagonal, DDD), defensive design, resilience strategies, and testing invariants.
- **Living Document, Authoritative State**: The specification is version-controlled and maintained alongside code. It defines the current, authoritative target state—not a historical audit log or changelog.
- **Memorialize Reasoning, Not Revisions**: When iterating through feedback loops, changes must **fully replace** existing instructions instead of appending revision markers, strikethroughs, or historical notes. Retaining superseded instructions creates detractors and conflicting context that degrade downstream LLM and engineer performance. Record the *reasoning* behind trade-offs and decisions (e.g., in Context or Alternate Solutions Considered), but keep all active operational requirements, schemas, and boundaries strictly singular and clean. Git preserves the edit history.

---

## Anti-Pattern: "This Is Too Simple To Need A Spec"

Every project or significant change goes through this process:
- A new CLI tool, component, API endpoint, data migration, refactor, or configuration change.
- "Simple" tasks are where unexamined assumptions cause the most rework and wasted time.
- For small changes, the spec can be concise (a few targeted sections), but you **MUST** present it and get explicit approval before advancing to implementation planning or coding.

---

## The Gated Spec-Driven Workflow

```
UNDERSTAND & DISCOVER ──► PROPOSE APPROACHES ──► DRAFT SPEC ──► SELF-REVIEW ──► USER APPROVAL ──► HANDOFF TO WRITING-PLANS
        │                         │                   │               │                │
        ▼                         ▼                   ▼               ▼                ▼
   1 Question/Msg            2-3 Options       Section-by-Section   4-Step Check    Hard Gate:        Next Skill:
   Surface Assumptions       w/ Tradeoffs      or Unified Doc       Inline Fixes    Wait for User     writing-plans
```

<HARD-GATE>
Do NOT invoke implementation skills, write production code, or create implementation plans until the specification document is written, self-reviewed, and explicitly approved by the user.
</HARD-GATE>

---

## The Decomposition Gate: Single Spec vs. Multi-Spec Series

Before drafting a specification, you MUST evaluate the scope against the **Decomposition Heuristic**.

### When to Split into Multiple Separate Specs
Split the initiative into separate, sequential specifications if ANY of the following apply:
1. **Distinct Bounded Contexts**: Different subdomains or vocabularies (e.g., `Identity/Auth` vs. `Billing/Payments` vs. `Reporting`).
2. **Independent Value & Deployability**: Subsystem A can be specified, planned, built, tested, and shipped independently of Subsystem B.
3. **Sequential Architecture Layers**: Subsystem B strictly depends on interfaces or schema migrations produced by Subsystem A (e.g., core domain engine vs. consumer API vs. frontend UI).
4. **Cognitive / Context Overload**: The change spans multiple unrelated subsystems, touches >3 new aggregates/services, or defines >5 distinct new user workflows simultaneously.

### Multi-Spec Execution Flow
If splitting is required:
1. **Present the Initiative Breakdown**: Propose the decomposition in chat, listing sub-projects in dependency order (e.g., `Phase 1: Core Domain Models & Migrations`, `Phase 2: Ingestion API & Resilience Controls`, `Phase 3: Management UI`).
2. **Get User Confirmation**: Ask the user: *"This initiative spans multiple independent subsystems. I recommend splitting this into [N] separate specs. Should we focus on Spec 1: [<Name>] first?"*
3. **Execute Spec 1 Only**: Complete the full `writing-specs` → `writing-plans` lifecycle for Spec 1 before initiating Spec 2.
4. **Declare Subsequent Phases as Non-Goals**: Record Sub-projects 2 & 3 explicitly in Spec 1's `Non-Goals / Out of Scope` section to prevent scope creep.
5. **Register Phase Labels in the Glossary**: Explicitly define every coined phase or spec label (e.g., `Spec 2`, `Phase 3`) in Spec 1's Glossary. Specify its concrete referent, dependencies, and status (`planned` vs. `hypothetical`). Never assume numbered or named phases are self-explanatory.
6. **Explicitly Tag Inherited Constraints**: When decisions or boundaries in Spec 1 constrain a downstream phase, explicitly document the constraint and name the target phase (e.g., "Constraints inherited by Phase 2"). Avoid burying cross-phase constraints in local implementation details.

---

## Step-by-Step Process

### 1. Explore Context & Understand the Idea
- **Inspect current repository state**: Check relevant files, existing architecture, schemas, tests, and documentation before asking questions.
- **Run the Decomposition Gate**: Assess whether this initiative requires multiple specs before deep-diving into individual feature questions. If decomposed, focus all subsequent questions on Sub-project 1 only.
- **Ask clarifying questions**:
  - Ask **one question at a time** per message to avoid overwhelming the user.
  - Prefer multiple-choice options with clear recommendations when possible.
  - Focus on understanding: problem origin, user persona, business constraints, non-goals, and concrete success criteria.
- **Surface assumptions early and explicitly**:
  ```markdown
  ASSUMPTIONS I'M MAKING:
  1. Primary storage is PostgreSQL (using existing Prisma migrations).
  2. Authentication utilizes session cookies via Redis, not stateless JWTs.
  3. Out of scope: mobile responsiveness for this admin dashboard phase.
  -> Please correct me now if any assumption is inaccurate.
  ```
- **Reframe vague requirements into testable success criteria**:
  - Transform "Make it faster" -> "p95 response time < 100ms under 500 RPS; LCP < 1.5s".
  - Transform "Make it reliable" -> "Circuit breakers on upstream payment gateway with 3s timeout and exponential backoff/jitter".

### 2. Propose & Deliberate Approaches
- Propose **2–3 distinct architectural approaches** with explicit trade-offs.
- For each approach, consider the principles in the `engineering-software` skill:
  - **Module Depth & Cohesion**: Prefer deep modules (simple, minimal interfaces encapsulating complex logic) over shallow pass-through layers.
  - **Business Logic Archetype**: Choose appropriately (Transaction Script for simple CRUD vs. Domain Model / Aggregates for complex business invariants).
  - **Reversibility & Orthogonality**: Defer volatile framework/vendor lock-in where possible.
- **Ruthless YAGNI**: Strip out unnecessary features, premature abstractions, and speculative genericity from all proposed options.
- Lead with your recommended option and clearly articulate why.

### 3. Draft the Specification Document
Save specifications to `.specs/YYYY-MM-DD-<topic>-spec.md` (or the project's designated spec directory / user preference).

Follow the **Structured Technical Spec Template** detailed below.

### 4. Spec Self-Review Loop
Before presenting the completed spec for final sign-off, evaluate the draft critically:
1. **Placeholder Scan**: Search for and eliminate any "TODO", "TBD", "fill in later", or hand-waving phrases (e.g., "handle error appropriately" -> specify the exact error type and fallback behavior).
2. **Internal Consistency**: Verify data contracts match between layers (e.g., API payloads match database schema changes and frontend models).
3. **Architectural & Safety Verification**:
   - Are boundary dependencies pointing inward (Hexagonal/Clean Architecture)?
   - Are remote calls guarded by explicit timeouts, circuit breakers, and bounded retries?
   - Is error handling explicit without silent failures or empty catches?
   - Are test levels (Unit, Integration, Contract) clearly allocated?
4. **Boundary Clarity**: Ensure the three-tier operational boundary (Always / Ask First / Never) is populated.
5. **Coined-Label & Glossary Audit**: Audit all coined identifiers (phase/spec labels, named components, synthetic artifacts, and capitalized/backticked non-code terms). Ensure every label is registered in the Glossary with a clear referent and status. Flag any term mentioned without definition or defined only via passing inline context.
6. **Scope & Ambiguity Check**: Resolve any ambiguous statement into a concrete, deterministic rule. Fix issues inline.
7. **Detractor & Superseded Content Scan**: Confirm revisions have cleanly overwritten older instructions. Verify there are no lingering strikethroughs, inline revision markers ("Updated in v2: ..."), or contradictory guidance between newly modified sections and untouched sections.

### 5. User Review Gate & Feedback Iteration
Present the specification to the user:
> "The technical specification has been drafted and saved to `<path>`. Please review it and let me know if you would like any adjustments or if you approve proceeding to implementation planning."

Wait for explicit approval.

#### Incorporating User Feedback
When the user requests changes or iterations during the review loop:
- **Cleanly Overwrite, Do Not Append**: Fully replace invalidated requirements, schemas, contracts, and acceptance criteria in-place. Write the updated text as if it were the plan from the beginning.
- **Eliminate Detractors**: Never leave obsolete directives, strikethroughs, or historical revision logs (e.g., "Note: previously we considered X, but per feedback we do Y") inside operational sections. Obsolete text confuses downstream LLMs during planning and implementation.
- **Memorialize Reasoning in Strategic Sections**: If feedback altered a core architectural choice, capture the *why* in Section 2 (`Context & Motivation`) or Section 4 (`Alternate Solutions Considered` / rejected options). The *reasoning* is preserved for posterity, while operational sections remain clean and unambiguous.
- **Re-Verify Consistency**: Run the self-review loop across the entire document to ensure changes didn't introduce subtle contradictions with untouched sections before re-presenting to the user.

### 6. Terminal Transition: Implementation Planning
Once the spec is approved:
- Hand off exclusively to the **`writing-plans`** skill to create a step-by-step implementation plan.
- Do NOT jump directly into coding or skip the implementation planning stage.

---

## Technical Spec Structure & Template

Adapt the sections below based on project scale (small features use a lean subset; complex systems use the comprehensive structure):

````markdown
# Spec: [Project / Feature / Component Name]

## 1. Front Matter & Metadata
- **Status**: [Draft | In Review | Approved | Superseded]
- **Author(s)**: [Name/Agent]
- **Date**: [YYYY-MM-DD]
- **Last Updated**: [YYYY-MM-DD]
- **Issue/Ticket Reference**: [#123 / URL]
*(Do NOT add an in-document Changelog or Revision History table; git tracks document history).*

## 2. Introduction & Strategic Context
- **Overview / Problem Statement**: Summary of the user problem and the proposed solution.
- **Context & Motivation**: Why solve this now? How does this align with strategic goals and system architecture?
- **Ubiquitous Language & Glossary**: Define domain terms and coined spec labels:
  - *Domain Terms*: Rigorous business and domain vocabulary within this Bounded Context.
  - *Coined Document & System Labels*: Every synthetic identifier introduced by this spec (e.g., `Phase 2`, `Spec 2`, `the Ingestion Worker`, `the Probe Suite`). For each, specify its concrete referent, dependencies, and lifecycle status (`existing`, `planned`, or `hypothetical`).
- **Goals**: Concrete user and technical outcomes.
- **Non-Goals / Out of Scope**: Explicitly excluded requirements and features to prevent scope creep.
- **Assumptions**: Environmental, organizational, or architectural preconditions.

## 3. Proposed Architecture & Solution Design
- **Architecture Overview**: Subsystems, component boundaries, and inward dependency flow.
- **Data Models & Schema Changes**:
  - Entity / Value Object definitions and Aggregate consistency boundaries.
  - Schema migrations (SQL/NoSQL/Protobuf/Avro) with backward-compatibility & tag immutability rules.
- **Business Logic & Interfaces (Deep Modules)**:
  - Public interface signatures, contracts, preconditions, and postconditions.
  - State transitions, invariants, and pseudocode for complex workflows.
- **Cross-Boundary Communication**:
  - API schemas (REST, gRPC, GraphQL) and Context Mapping (e.g. ACL for upstream integrations).
  - Idempotency guarantees and event schemas.
- **Presentation / User Experience (if applicable)**:
  - UX flows, screen states (loading, empty, error, success), and accessibility requirements.

## 4. Resilience, Failure Modes & Edge Cases
- **Production Hostility & Blast Radius**:
  - Network/I/O timeouts, circuit breakers, and rate-limiting/backpressure mechanisms.
  - Fallback strategies with structured observability (no silent error suppression).
  - Concurrency controls (optimistic locking, transaction isolation levels).
- **Security & Privacy Considerations**: Input validation at boundaries (barricades), authentication/authorization, data protection.
- **Alternate Solutions Considered**: 2–3 rejected approaches and why they were discarded. (Memorialize the reasoning behind discarded designs and feedback-driven shifts here, rather than cluttering operational sections with revision history).

## 5. Verification & Testing Strategy
- **Test Pyramid Plan**:
  - **Unit Tests**: Domain invariant tests in total isolation from I/O.
  - **Integration Tests**: Component interaction and real database/container boundary tests.
  - **Contract / E2E Tests**: Public schema conformance and end-to-end scenarios.
  - **Legacy Seams & Characterization Tests** (if working in legacy code): Identified seams (Sprout/Wrap/Override).
- **Commands**: Full, copy-pasteable verification commands (build, test, lint, format).
  ```bash
  Build: <exact command>
  Test:  <exact command>
  Lint:  <exact command>
  ```

## 6. Execution Boundaries
- **Always Do**: [e.g., Run test suite before checkpoints, follow naming conventions, validate inputs at boundaries]
- **Ask First**: [e.g., Add new external dependencies, modify existing database schemas, introduce background jobs]
- **Never Do**: [e.g., Commit unencrypted secrets, swallow errors with generic catch blocks, bypass aggregate root boundaries]

## 7. Acceptance Criteria & Evaluation
- [ ] [Specific, measurable, testable condition 1]
- [ ] [Specific, measurable, testable condition 2]
- [ ] [Performance / Latency / Reliability metric target]

## 8. Open Questions & Deliberation
- [Unresolved questions requiring stakeholder / team consensus before or during execution]
````

---

## Operational Directives for the Agent

1. **Be Strategic, Not Purely Tactical**: Invest 10–20% of effort upfront in clean interface definitions and dependency decoupling to avoid compounding complexity debt.
2. **Prioritize Reader Cognitive Load**: Write clear, precise, and concise specs. Omit boilerplate; emphasize non-obvious invariants, schemas, and edge cases.
3. **Never Skip the Review Gate**: Always obtain explicit confirmation before handing off to `writing-plans`.
4. **Memorialize Reasoning, Not Revisions**: When revising a spec, always completely replace superseded instructions. Downstream coding agents treat every statement in a spec as an active invariant; leaving invalidated instructions or revision commentary creates detractors that derail execution. Capture the rationale for shifts in "Alternate Solutions Considered" or "Context & Motivation", but ensure all specifications define a single, authoritative target state.


