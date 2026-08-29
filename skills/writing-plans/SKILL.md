---
name: writing-plans
description: Use this to write an implementation plan when you have a spec or requirements for a multi-step task, before touching code
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

# Writing Plans

Purpose: Guide an LLM agent to decompose an approved specification or requirements document into an ordered, bite-sized, and verifiable implementation plan before touching code.

## Prerequisites & Core Philosophy

- **Approved Spec Required**: You MUST have a validated specification or approved requirements document (e.g. created via `writing-specs` or provided by the user). If requirements are ambiguous or incomplete, do not write a plan—direct the user to `writing-specs` first.
- **Reference Shared Software Engineering Invariants**: Always consult `references/software-engineering.md` for architectural boundaries (Clean/Hexagonal), deep module interface design, defensive contracts, and testing disciplines.
- **Code Conciseness Invariant (Avoid Verbatim Code Dumps)**: Do NOT write complete production code implementations verbatim in the plan document. Describe the change precisely in prose, specifying exact `file:line` locations, function signatures, data shapes, and test assertions. Include short code blocks ONLY for genuinely novel, tricky, or non-obvious algorithms and assertions.
- **Save Location**: Save plans to `.plans/YYYY-MM-DD-<feature-name>.md` (or a user-specified directory).
- **Announce at Start**: "I'm using the writing-plans skill to create the implementation plan."

---

## 1. The Foundation Principle: Data Models First

Before building business logic or presentation layers, **prioritize data model changes as the initial tasks**:

```
1. DATA MODEL & SCHEMA (Foundations, Migrations, Invariants, Entities/Value Objects)
                            │
                            ▼
2. CORE BUSINESS LOGIC (Domain Services, Aggregates, Workflows, Boundary Adapters)
                            │
                            ▼
3. PRESENTATION & INTEGRATION (APIs, UI Components, Telemetry & Integration Tests)
```

- **Why Data Models First?** Data structures, schemas, and domain aggregates provide the structural framing and invariant rules upon which all business workflows depend.
- **Schema Evolution Invariants**:
  - Follow tag/field immutability (never renumber existing Protobuf/Avro tags or change column semantics).
  - Explicitly mark deleted or deprecated fields.
  - Ensure migrations are backward-compatible and safe for rollout.
- If the feature requires **no schema or data model changes**, state this explicitly in the plan overview and proceed directly to core domain logic.

---

## 2. Decomposition & Vertical Slicing

Map the dependency graph bottom-up, then slice features vertically into bite-sized deliverables:

- **Vertical Slicing**: Avoid massive horizontal layers (e.g., building all DB tables, then all APIs, then all UI). Build end-to-end verifiable feature slices where each task produces an independently testable unit of software.
- **Task Right-Sizing**:
  - Target **S to M** task sizing (touching 1–4 files, completable in a single focused session).
  - Split any task touching >5 files or containing multiple compound steps ("and" in the title).
  - Fold configuration, setup, and scaffolding directly into the task that requires them.

---

## 3. Incremental Plan Construction

Draft and present the plan to the user **incrementally**:

1. **Present the Decomposition First**: Show the file structure map and the ordered list of task titles + one-line summaries. Get the breakdown confirmed before drafting task details.
2. **Draft Task-by-Task**: Present tasks in chat, confirm alignment or adjustments, then move to the next.
3. **Assemble the Plan Document**: Write the final markdown plan file only after task alignment is confirmed.

---

## 4. Plan Document Template & Structure

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** Execute this plan task-by-task. Each task ends with a verification step and a review checkpoint.

**Goal:** [One sentence describing what this builds]

**Architecture & Core Approach:** [2-3 sentences referencing bounded context, module depth, and boundary flow]

**Tech Stack & Key Libraries:** [Exact frameworks, libraries, versions]

## Global Constraints & Boundaries
- **Always Do**: [e.g., Run test suite before checkpoints, maintain SLAP, validate inputs at public boundaries]
- **Ask First**: [e.g., Database schema drops, adding external dependencies]
- **Never Do**: [e.g., Swallow errors with generic catch blocks, bypass aggregate boundaries, commit secrets]

---

## File Structure & Responsibility Map
- `src/models/exact_model.py`: [Entity/schema definitions and domain invariants]
- `src/services/exact_service.py`: [Business workflow orchestration and boundary adapters]
- `tests/unit/test_exact_model.py`: [Isolated unit tests for invariants and state transitions]

---

## Task Breakdown

### Phase 1: Data Model & Schema Foundations

#### Task 1: [Data Model / Schema / Migrations]
**Files:**
- Create: `src/models/user_account.py`
- Modify: `alembic/versions/xxxx_add_user_account.py`
- Test: `tests/models/test_user_account.py`

**Interfaces & Data Shapes:**
- Consumes: [Existing types/tables relied upon]
- Produces: [New schemas, Entity/Value Object signatures, validation rules]

**Steps:**
- [ ] **Step 1: Write failing model/migration test** — assert table constraints, default values, and schema invariants.
- [ ] **Step 2: Run test to verify failure** (`pytest tests/models/test_user_account.py -v`).
- [ ] **Step 3: Implement minimal schema & domain model** in `src/models/user_account.py` (describe fields, types, and constraints precisely in prose; include code snippets ONLY for non-obvious validation rules).
- [ ] **Step 4: Run test to verify pass** (`pytest tests/models/test_user_account.py -v`).
- [ ] **Checkpoint:** Review boundary covering migration + data model. (Marker only — do not auto-commit).

---

### Phase 2: Core Domain Logic & Business Rules

#### Task 2: [Domain Service / Workflow]
**Files:**
- Create: `src/services/account_service.py`
- Test: `tests/services/test_account_service.py`

**Interfaces:**
- Consumes: `UserAccount` from Task 1
- Produces: `AccountService.register_user(data: UserRegistrationInput) -> UserAccount`

**Steps:**
- [ ] **Step 1: Write failing unit test** for business rule invariants (e.g. duplicate email rejection, password strength).
- [ ] **Step 2: Run test to verify failure** (`pytest tests/services/test_account_service.py -v`).
- [ ] **Step 3: Implement service business logic** in `src/services/account_service.py` (describe orchestration, error mappings, and timeout/resilience boundaries in prose).
- [ ] **Step 4: Run test to verify pass** (`pytest tests/services/test_account_service.py -v`).
- [ ] **Checkpoint:** Review boundary covering domain logic.

---

### Phase 3: Integration, Public Interfaces & Polish

#### Task 3: [API Endpoints / Boundary Adapters]
**Files:**
- Modify: `src/api/routes.py:45-80`
- Test: `tests/integration/test_routes.py`

**Steps:**
- [ ] **Step 1: Write failing integration test** against mock server or test client.
- [ ] **Step 2: Run test to verify failure**.
- [ ] **Step 3: Wire route handler to `AccountService`**, mapping HTTP status codes and error payloads.
- [ ] **Step 4: Run test to verify pass**.
- [ ] **Checkpoint:** Final verification across all test suites.
```

---

## 5. Guidelines for Task Writing

### Code Conciseness (No Verbatim Dumps)
- **Describe, don't regurgitate**: An agent implementing a plan does not need entire 50-line boilerplate classes printed into markdown. It needs:
  - Exact file paths and line number anchors (`file:line`).
  - Precise function/method signatures with parameter and return types.
  - Key invariants, state transition rules, and expected error cases.
  - Specific assertion expectations for tests.
- **When code blocks ARE appropriate**:
  - Complex regex patterns or custom parsing logic.
  - Tricky algorithmic state transitions or mathematical formulas.
  - Non-obvious test assertion structures.

### No Placeholders
Never use placeholder phrases:
- *Forbidden*: "TODO", "TBD", "fill in later", "handle error appropriately", "write tests for the above".
- *Required*: State the exact exception class to catch, the HTTP status code to return, the specific boundary to isolate, or the exact test assertion to write.

### Checkpoints Are Markers
Checkpoints represent logical boundaries where an implementer verifies tests, builds clean artifacts, and pauses for human or subagent review. Do NOT write automated `git commit` commands into plan steps.

---

## 6. Self-Review Checklist

Before finalizing the plan, check:
1. **Data Models First**: Are database schemas, migrations, entities, and value objects scheduled before dependent business rules?
2. **Spec Coverage**: Does every requirement and success criterion in the spec map to a task?
3. **No Verbatim Dumps**: Is the plan crisp and concise without printing hundreds of lines of obvious boilerplate code?
4. **Exact Commands & Paths**: Are all verification commands copy-pasteable with exact flags and target test paths?
5. **No Placeholders**: Are all error handlers, types, and assertions concretely defined?

---

## 7. Execution Handoff

After the user approves the plan:
> "Implementation plan complete and saved to `<path>`. Ready to proceed with implementation task-by-task."

