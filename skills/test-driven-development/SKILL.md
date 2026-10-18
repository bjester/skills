---
name: test-driven-development
description: "Test-Driven Development (TDD) workflow enforcing strict red-green-refactor loops, public seam testing, minimal implementations, and prevention of testing anti-patterns before writing production code."
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
metadata:
  author: Blaine Jester
  version: "1.0"
---

# Test-Driven Development (TDD)

Purpose: Guide the disciplined development of new features, bug fixes, and architectural modifications through strict, test-first red-green-refactor cycles that produce robust, maintainable, and regression-proof software.

## Prerequisites & Core Philosophy

- **The Iron Law**: **NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST**. If you did not watch the test fail for the expected reason, you do not know if it tests the right behavior or if it passes by coincidence.
- **Delete Unverified Code**: If production code was authored before writing its corresponding failing test, delete that production code immediately and restart test-first.
- **Reference Shared Software Engineering Guidelines**: Always consult:
  - The `engineering-software` skill for F.I.R.S.T. test properties (Fast, Independent, Repeatable, Self-Validating, Timely), Clean Architecture boundaries, and legacy code seams.
  - `testing-anti-patterns.md` to prevent mock coupling, tautological assertions, and test pollution.
  - `mocking-guidelines.md` for boundary isolation rules and mockability design.
- **Announce at Start**: State clearly: *"I am using the test-driven-development skill to implement this change test-first."*

---

## Seams: Where Tests Belong & Designing for Testability

A **Seam** is a place where you can observe, verify, or alter program behavior without editing internal implementation mechanics or violating encapsulation.

### The Testability Invariant: "Listen to the Test"

**Test friction is design feedback.** If a piece of critical business logic or complex branching feels impossible to test through its current interface, **do not leave it untested under the excuse that "it's private."**

Instead, recognize that difficult-to-test logic indicates an architectural need for a seam:
- The class/routine is taking on multiple responsibilities (SRP violation).
- A domain concept, policy, or calculation is trapped inside a host class as a "private helper" when it deserves to be a first-class, testable abstraction.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                   SEAM DESIGN: GREENFIELD vs. LEGACY                     │
└──────────────────────────────────────────────────────────────────────────┘

         ┌─────────────────────────────────┴─────────────────────────────────┐
         ▼                                                                   ▼
  [GREENFIELD / NEW CODE]                                             [EXISTING / LEGACY CODE]
  "Extract the Trapped Abstraction"                                   "Surgical Seam Engineering"
  ─────────────────────────────────                                   ───────────────────────────
  • Decompose trapped logic into a standalone,                         • Do not attempt high-risk structural rewrites
    focused component (Value Object, Strategy,                          without a safety net.
    Policy Engine, or Domain Service).                                • Use Sprout Class / Sprout Method for new logic.
  • Expose a clean, cohesive public interface.                        • Use Wrap Method / Wrap Class for decorators.
  • Inject the collaborator via Dependency Injection.                 • Use Package-Private / Internal / Protected
  • Test the new component's public seam 100% test-first.               visibility (e.g. `[InternalsVisibleTo]`, `_` module)
                                                                        or Extract and Override / Subclass and Override.
```

### Strategy A: Greenfield / New Code (Extracting Abstractions)
- **Don't reach into private methods with reflection or test hacks**: If a private helper within a newly authored class contains non-trivial logic (e.g. tiered pricing algorithm, custom string parsing, permission matrix calculation), extract it into its own cohesive class or module.
- **Compose via Dependency Injection**: The parent class receives the extracted collaborator through its constructor or parameters. Now both the extracted policy and the orchestrator have simple, 100% testable public seams.

### Strategy B: Existing / Legacy Code (Seam Engineering)
When working in existing code (code lacking comprehensive tests per Michael Feathers):
1. **Sprout Method / Sprout Class**: Write newly added or heavily modified logic in a fresh, standalone class/function covered by 100% test-first unit tests. Invoke it from the legacy code via a single call.
2. **Package-Private / Internal Visibility**: In languages supporting module or package boundaries (Go internal, Kotlin/C# `internal`, Java package-private, Python `_protected`), widen visibility to package-level so unit tests in the same package can test the routine directly without exposing it to external consumers.
3. **Subclass and Override / Extract and Override**: Extract tightly coupled dependencies (direct database queries, static singletons, system clock calls) into a protected method, and override it in a test-specific subclass.
4. **Characterization Tests**: Write tests against the nearest observable seam to lock down existing behavior before refactoring.

### Seam Invariants
1. **Agree on Seams First**: Clarify the public boundary under test before writing test code.
2. **Vertical Slicing (Tracer Bullets)**: Never write all tests upfront (horizontal slicing). Build one vertical slice at a time: **one failing test → one minimal implementation → verify green → refactor → repeat**.
3. **Survive Refactoring**: A well-placed test reads like a specification (e.g. `test('user can checkout with valid cart')`) and continues passing cleanly when internal algorithms or helper routines are refactored.

---

## The Rigorous Red-Green-Refactor Cycle

```
       ┌────────────────────────────────────────────────────────┐
       │                        TDD CYCLE                       │
       └───────────────────────────┬────────────────────────────┘
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         ▼                                                   ▼
     [1. RED]                                         [2. VERIFY RED]
   Write one focused,                              Run test suite. Confirm it
   failing unit/integration test.                  FAILS for expected reason.
         │                                                   │
         └─────────────────────────┬─────────────────────────┘
                                   ▼
                              [3. GREEN]
                         Write minimal production
                         code to satisfy the test.
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         ▼                                                   ▼
  [4. VERIFY GREEN]                                   [5. REFACTOR]
Run test suite. Confirm all                        Clean up structure, remove
tests pass cleanly (100% green).                   duplication. Stay 100% green.
```

### Step 1: RED — Write a Failing Test
- Write a single, focused test defining the desired observable behavior.
- Use descriptive, behavioral test titles: `test('retries failed network requests 3 times with backoff')`.
- Assert against independent, known-good literals (never recompute expected values using production code formulas).
- Use real domain objects wherever possible; mock only external system boundaries per `mocking-guidelines.md`.

### Step 2: VERIFY RED — Watch It Fail
- **MANDATORY**: Run the specific test command.
- Confirm the test **fails** (not crashes due to invalid test syntax or broken imports).
- Confirm the failure message matches the exact missing feature or broken invariant.
- *If the test passes immediately*: You are testing existing functionality or the test is tautological. Fix or delete the test.

### Step 3: GREEN — Write Minimal Implementation
- Write the simplest, most direct code that satisfies the failing test.
- Adhere strictly to **YAGNI** (You Aren't Gonna Need It):
  - Do not add speculative parameters, unrequested configuration flags, or premature abstractions.
  - Do not implement subsequent features not yet exercised by a failing test.

### Step 4: VERIFY GREEN — Watch It Pass
- Run the focused test to confirm it now passes cleanly.
- Run the broader project test suite to verify no existing functionality was broken.
- Ensure test execution produces pristine output (zero unhandled warnings, unhandled promise rejections, or error logs).

### Step 5: REFACTOR — Clean Up Under Safety Net
- With 100% green tests guarding behavior:
  - Eliminate code duplication (DRY).
  - Clarify variable and function names.
  - Extract deep, cohesive helper functions adhering to Single Level of Abstraction (SLAP).
- **The Two-Hats Discipline**: Never add new features or alter observable behavior during refactoring.

---

## Good vs. Bad Tests Matrix

| Quality | ✅ Good Test Pattern | ❌ Bad Test Pattern |
| :--- | :--- | :--- |
| **Interface Seam** | Tests public contract: `createUser({ email })` returns user with active state. | Bypasses interface: queries raw database rows directly or spies on private helpers. |
| **Expected Values** | Independent literal: `expect(total).toBe(105.00)`. | Tautological: `expect(total).toBe(items.reduce(...))`. |
| **Mocking** | Mocks external Stripe HTTP gateway at boundary. | Mocks internal collaborator classes within same module. |
| **Focus** | Tests one distinct invariant or state transition. | Monolithic multi-assert test testing 10 unrelated scenarios. |
| **Resilience** | Remains green when internal helper functions are refactored. | Shatters on harmless renaming of private methods. |

---

## Why Order Matters & Common Rationalizations

| Excuse / Rationalization | Reality & True Impact |
| :--- | :--- |
| *"I'll write the tests after the code to make sure it works."* | Tests written after code are biased by the implementation, test what you built rather than what is required, and are never observed catching a defect. |
| *"This change is too simple to need TDD."* | Simple code introduces subtle edge-case bugs. Authoring a 3-line test takes under 30 seconds. |
| *"Deleting this unverified code is wasteful (sunk cost)."* | Unverified code is unhedged technical debt. Deleting and rewriting test-first takes less time than debugging production regressions. |
| *"I already manually tested it in the browser/terminal."* | Manual verification is ad-hoc, unrecorded, and cannot be re-executed automatically in CI on future commits. |
| *"TDD is dogmatic; being pragmatic means writing tests later."* | TDD is the pinnacle of pragmatic engineering: it accelerates delivery by eliminating multi-hour debugging thrashing. |

---

## Red Flags — Stop, Delete & Restart

If you encounter any of the following triggers, **STOP immediately, delete the unverified production code, and restart test-first**:

- Production code authored before writing the failing test.
- A newly written test passes on the first run without code changes.
- Inability to articulate why a test failed during the RED phase.
- Adding methods to production classes solely for test teardown (see `testing-anti-patterns.md`).
- Asserting on mock object internals (`*-mock` IDs, mock call counts) rather than system output.
- Writing multiple tests before running the first one.

---

## Verification Checklist

Before declaring any feature or bug fix complete:

- [ ] Every new public function, endpoint, or behavior is covered by a test.
- [ ] Every test was observed failing for the correct reason before implementation.
- [ ] Production code contains only the minimal logic required to satisfy tests (no YAGNI violations).
- [ ] All tests pass cleanly across the entire repository test suite.
- [ ] No test anti-patterns present (no test-only production methods, tautological asserts, or over-mocking).
- [ ] External boundaries mocked cleanly per `mocking-guidelines.md`.
- [ ] Terminal and test output is pristine with zero unexpected error logs or warnings.
