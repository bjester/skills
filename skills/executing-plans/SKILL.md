---
name: executing-plans
description: "Executes approved implementation plans task-by-task. Supports both primary-agent inline execution and subagent-driven execution with pragmatic TDD and verification gates."
license: MIT - https://github.com/bjester/skills/blob/main/LICENSE
user-invocable: true
compatibility: a software project with git version control
allowed-tools:
  - read_file
  - write_file
  - run_command
  - grep
  - find_by_name
  - ask_user_question
  - task
  - invoke_subagent
metadata:
  author: Blaine Jester
  version: "1.1"
---

# Executing Plans

Purpose: Guide the execution of an approved implementation plan task-by-task, supporting both primary-agent inline execution and subagent delegation, with pragmatic TDD, thorough multi-scale code reviews, and rigorous verification gates.

## Prerequisites & Core Philosophy

- **Approved Plan Required**: You MUST have an approved implementation plan (typically created via `writing-plans`). If requirements or the plan are ambiguous, resolve them before touching code.
- **Pre-Flight Critical Plan Audit**: Before starting Task 1, audit the plan's referenced file paths, symbols, interfaces, and environmental assumptions against the live codebase to catch drift, stale assumptions, or contradictions upfront.
- **Reference Software Engineering & Review Invariants**: Always consult:
  - The `engineering-software` skill for architectural boundaries, defensive error semantics, resilience patterns, refactoring recipes, and testing invariants (F.I.R.S.T.).
  - The `reviewing-code` skill for multi-scale code review checklists and the subagent review prompt template.
- **Announce at Start**: "I'm using the executing-plans skill to implement this plan."

---

## 1. Contextual TDD: Pragmatic Testing by Work Type

TDD is a design tool and safety net, but its application must be pragmatic based on whether you are building greenfield structures, extending existing logic, or modifying legacy code:

```
┌───────────────────────────────────────────────────────────────────────────┐
│                           WORK CLASSIFICATION                             │
└─────────────────────────────────────┬─────────────────────────────────────┘
                                       │
        ┌─────────────────────────────┼─────────────────────────────┐
        ▼                             ▼                             ▼
  1. GREENFIELD DATA          2. BUSINESS LOGIC &           3. EXISTING CODE &
  MODELS & FOUNDATIONS        NEW WORKFLOWS                 LEGACY SYSTEMS
  ────────────────────        ───────────────────           ──────────────────
  • Implement models,         • Strict TDD: Write           • Identify seams (Sprout /
    schemas & migrations        failing unit test for         Wrap / Override).
    first.                      invariants & business rules. • Write characterization
  • Verify via schema         • Verify red (failure).         tests before modifying.
    validation / integration  • Implement minimal logic.    • Refactor with the
    tests (no tautological    • Verify green (pass).          Two Hats discipline.
    "class exists" mocks).
```

### Strategy A: Greenfield Foundations & Data Models
- **No Tautological Tests**: Do not write tests that merely assert a class or table exists before defining it.
- **Model Validation Tests**: Focus tests on structural invariants, default constraints, serialization/deserialization, and schema migration integrity.

### Strategy B: Core Business Logic & Workflows (Strict TDD)
- **Red-Green-Refactor**:
  1. Write a failing unit test asserting specific invariant behavior (e.g. edge-case calculation, validation rejection, state transition).
  2. Run the test to confirm it fails for the expected reason (Red).
     - **Red-Phase Unexpected-Pass Halt**: If a newly written test passes on the first run before implementation, **HALT immediately**—either the test assertion is tautological/misconfigured or the behavior already exists.
  3. Write the minimal code to satisfy the invariant (Green).
  4. Refactor if needed while keeping tests green.
- **Test Observable Behavior**: Avoid test-induced damage (over-mocking). Test public contract behavior and state rather than internal private method calls.

### Strategy C: Modifying Existing Code & Legacy Systems (Seam Engineering)
- **Legacy Code Definition**: Code without automated tests.
- **The Legacy Change Algorithm**:
  1. Identify change points and test points.
  2. Find or create a **Seam** (`Object Seam`, `Link Seam`, `Sprout Method/Class`, or `Wrap Method/Class`).
  3. Write **Characterization Tests** to lock down existing behaviors (including quirks/bugs) before changing anything.
  4. Make surgical changes and refactor under the safety net.
- **Two Hats Discipline**: Never swap between adding new functionality and refactoring structure in the same step.

---

## 2. Execution Pathways: Subagent vs. Inline

Choose or confirm the execution mode at the start of the session:

```
                         ┌───────────────────────┐
                         │ EXECUTION MODE CHOICE │
                         └───────────┬───────────┘
                                     │
                 ┌───────────────────┴───────────────────┐
                 ▼                                       ▼
    [Path 1: Subagent-Driven]               [Path 2: Primary-Agent Inline]
    • Fresh subagent per task.              • Single session, sequential.
    • Isolated context & review.            • Step-by-step verification.
    • Best for large, modular plans.        • Best for tightly coupled changes.
```

### Path 1: Subagent-Driven Execution (Recommended for Modular Plans)
When subagent capabilities (`invoke_subagent`) are available:
1. **Per-Task Dispatch**:
   - Provide the subagent with the exact task requirements, target files, interface contracts, and global constraints.
   - Do NOT paste entire session histories; pass isolated task briefs.
2. **Implementer Execution**:
   - Subagent applies Contextual TDD, modifies files, and runs verification commands.
   - Subagent reports status (`DONE`, `DONE_WITH_CONCERNS`, or `BLOCKED`) with test output evidence.
3. **Task Review Gate (Early Code Review & Two-Stage Review Ordering)**:
   - **Distrust the Subagent's Self-Report**: Never accept a subagent's claim of completion at face value. Inspect the actual `git diff` and changed file list directly.
   - **Stage 1 — Spec Compliance & Deterministic Gates**: Verify every task requirement is met, zero out-of-scope files or unrequested features were added, and fast deterministic gates (tests, typecheck, linter) pass *before* evaluating architecture or style.
   - **Stage 2 — Four-Scale Code Review**: Perform a thorough code review against the 4 scales in the `reviewing-code` skill (optionally dispatching a dedicated review subagent using the Subagent Review Prompt template). Check for: invariant breaches, missing timeouts/circuit breakers, shallow wrappers, error swallowing, or over-mocked tests.
   - If findings or regressions exist, re-dispatch fix cycles to the implementer before proceeding to dependent tasks.

### Path 2: Primary-Agent Inline Execution (Direct Session)
When executing inline in the current session:
1. **Task-by-Task Focus**: Execute one task at a time from the plan.
2. **Step Execution**:
   - Step 1: Write failing test (or characterization test for existing code).
   - Step 2: Run test command to confirm expected failure.
   - Step 3: Write minimal implementation adhering to Clean Architecture & Deep Module principles.
   - Step 4: Run test command to confirm pass.
   - Step 5: Run project build/lint checks.
3. **Checkpoints & Self-Review**: Mark review checkpoints after each logical task. Run a quick 4-scale self-review check against the `reviewing-code` skill to ensure no complexity or resilience debt was introduced before beginning the next task.

---

## 3. Incremental Implementation Rules

Adhere to these core execution invariants during code generation:

1. **Rule 0: Simplicity & Depth First**:
   - What is the simplest thing that works? Prefer deep modules (simple API hiding rich internal logic) over shallow pass-through wrappers.
   - Avoid speculative abstractions or generic event buses for single-use cases.
2. **Rule 1: Scope Discipline & Cleanliness**:
   - Touch ONLY files designated by the current task.
   - Do not perform drive-by refactoring in unrelated files. Note potential improvements as separate future tasks.
   - Maintain active intolerance for architectural rot—eliminate dead code, remove empty catches, and avoid `null` returns across boundaries.
3. **Rule 2: Defensive & Resilient Boundaries**:
   - Validate and sanitize untrusted inputs at public barricades.
   - Enforce explicit timeouts, circuit breakers, and bounded retries for all remote I/O calls.
   - Emit structured telemetry/logs when fallbacks trigger (no silent error suppression).
4. **Rule 3: Keep It Compilable**:
   - Never leave the repository in a broken build or failing test state at the end of a task increment.
5. **Rule 4: Build the Lever Over Manual Churn (Script the Sweep)**:
   - When a task involves non-trivial, repetitive edits across multiple files (such as updating 10+ callsites to a new signature, mechanical structural renames, or broad schema migrations), **do not edit files manually one by one**.
   - *Author a deterministic script or codemod*: Build the tool that performs or verifies the changes.
   - *First-Unit Proof*: Perform the transformation manually on a single unit to establish and refine the exact recipe. Then author the script/codemod, execute it across the remaining targets, and verify that diffs match expectations.
   - *Reviewability*: A deterministic script transforms "trust me, I edited 30 files manually" into a concise, auditable artifact that a reviewer can inspect and rerun for free.
   - *Lever Over Fan-Out*: A single deterministic script running locally in one pass beats spawning multiple subagents to hand-apply repetitive mechanical edits.
6. **Rule 5: Keep a Decision Ledger for Multi-Phase or Unattended Runs**:
   - For complex, multi-phase, or unattended executions, maintain a single canonical, append-only TSV decision log at `.plans/decisions.tsv` (or `.audit/<plan-slug>.tsv`) using the schema from `references/decision-log-template.tsv`:
     ```tsv
     ts	phase	decision	why	evidence	result
     ```
   - *Pointer-Based Evidence*: Log significant forks, completed task increments, and verification outcomes. Evidence must be an exact pointer (`commit SHA`, `file:line`, test command output, or artifact path)—never speculative prose.
   - *Append-Only History*: Never edit or erase prior history. If an approach is reverted or modified, append a new row recording the pivot, the trigger, and the resulting state.
   - *Paused Session Resumption*: When resuming an interrupted plan, reconcile `.plans/decisions.tsv` against `git status` and `git diff` to verify whether the last logged task finished cleanly or left partial uncommitted state.
   - *End-of-Run Transcript Audit*: Before handing back, audit the log against the actual session actions to ensure all entries reflect real, verified execution without missing forks or unproven assertions.

---

## 4. Verification & Review Gate

After each task (and at the completion of all tasks), execute the verification suite:

```markdown
- [ ] Task acceptance criteria met
- [ ] Focused unit / integration tests pass
- [ ] Repository test suite passes
- [ ] Type checking / linter passes without errors
- [ ] Build succeeds cleanly
- [ ] 4-Scale Code Review check passed (no 🚨 Blockers or ⚠️ Architecture debt per the reviewing-code skill)
```

---

## 5. When to Stop and Escalate

**STOP executing and ask the user for clarification when:**
- An unresolvable blocker is encountered (missing external dependency, broken environment).
- A hidden contradiction between the plan and codebase architecture is uncovered.
- Verification commands fail repeatedly despite fix attempts.
- A structural change to the database schema or core API contract is needed that wasn't in the plan.
- A meaningful deviation from a plan or task occurs-- an LLM agent should not make decisions at execution time that invalidate the plan's or user's decisions.
