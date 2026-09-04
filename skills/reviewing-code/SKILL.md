---
name: reviewing-code
description: "Perform rigorous code reviews across git working tree diffs, staged changes, branches, PRs, or targeted modules. Evaluates software across 4 scales (macro-resilience, strategic architecture, modular depth, craftsmanship/tests) with structured checklists, finding taxonomies, and report templates."
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
  version: "1.1"
---

# Reviewing Code (Local Review)

Purpose: Perform rigorous, local code reviews across uncommitted changes, branches, or specific modules before committing, opening pull requests, or merging.

## Prerequisites & Core Philosophy

- **Core Review Goal**: The ultimate purpose of code review is **managing reader and maintainer cognitive load in the presence of inevitable change and production chaos**.
  1. *Complexity Is the Enemy*: Watch for change amplification, high cognitive load, and unknown unknowns.
  2. *Review at Multiple Scales*: Do not get trapped in superficial syntax or formatting nitpicks. Evaluate changes top-to-bottom across all 4 scales of software engineering.
  3. *Question-Driven Analysis & Evidence Bar*: Ground all findings in concrete codebase evidence (reading surrounding callers, models, and tests—not just the diff hunk). If a behavior cannot be conclusively confirmed, phrase it as a question or suggestion rather than an assertive blocker.
  4. *Actionable & Constructive*: Every finding must explain *why* (citing the engineering invariant or failure mode) and offer a specific remediation or refactoring recipe.
  5. *Be Strategic, Not Dogmatic*: Understand the difference between critical invariant violations and subjective stylistic preferences.
- **Reference Software Engineering Invariants**: Consult the `software-engineering` skill for foundational architectural rules (Clean/Hexagonal), modular depth, defensive programming, refactoring recipes, resilience patterns, and testing invariants.
- **Organization-Specific Guidelines**: Check if the repository belongs to a recognized organization:
  ```bash
  git remote -v
  ```
  - If the remote points to **Learning Equality** (`github.com[:/]learningequality/`), also consult the `learning-equality` skill for Django values-viewsets, KDS component reuse, declarative permissions, WCAG accessibility, and RTLCSS rules.

---

## Local Review Workflow

```
1. SCOPE TARGETS ──► 2. EXECUTE 4-SCALE REVIEW ──► 3. VERIFY WITH TOOLS ──► 4. DELIVER REPORT & REMEDIATION
        │                         │                          │                          │
        ▼                         ▼                          ▼                          ▼
   Working tree,             Check against              Run tests, linter,         Present findings,
   staged diff, branch,      the 4-scale review         and build suite for        offer interactive
   or target files           checklists                 empirical evidence         remediations
```

### Step 1: Determine the Review Scope

Identify the target of the review:
- **Working Tree / Uncommitted Changes**:
  ```bash
  git status
  git diff
  ```
- **Staged Changes Only**:
  ```bash
  git diff --cached
  ```
- **Branch vs. Base**:
  ```bash
  git diff main...HEAD
  ```
- **Specific Module / Files**:
  Inspect the specified files and their immediate callers, dependencies, and corresponding test files.

### Step 2: Conduct Multi-Scale Analysis

Evaluate the changes against the checklists in this skill:
1. **Macro-Scale & Resilience**: Timeouts, circuit breakers, bounded retries, resource cleanup (RAII/defer), concurrency safety, no silent error suppression.
2. **Strategic Architecture**: Inward dependency flow, bounded contexts, ubiquitous language, ACLs for external dependencies.
3. **Modularity & Depth Design**: Deep modules vs. shallow wrappers, information hiding, orthogonality, SRP.
4. **Micro-Craftsmanship & Smells**: Single Level of Abstraction (SLAP), Command-Query Separation (CQS), parameter limits (<3), Primitive Obsession, code smells.
5. **Verification & Test Value**: F.I.R.S.T. properties, asserting observable behavior vs. over-mocking, legacy characterization safety nets.

### Step 3: Run Empirical Verification Commands

Run the repository's verification tools to gather hard evidence before finalizing the review:
- Unit & integration tests (`pytest`, `npm test`, `cargo test`, `go test ./...`, etc.)
- Type checkers (`mypy`, `tsc`, `pyright`, etc.)
- Linters & static analysis (`ruff`, `eslint`, `golangci-lint`, etc.)
- Build commands (`make build`, `cargo build`, `npm run build`, etc.)

### Step 4: Format and Present Findings

1. Structure the review report using the standard template in this skill.
2. Categorize all findings by severity:
   - `🚨 Blocker (Must-Fix)`
   - `⚠️ Architecture & Design (Should-Fix)`
   - `💡 Tactical Suggestion (Optional)`
   - `✅ Positive Highlights`
3. Clearly cite exact file paths and line ranges (`path/to/file#L10-L25`).
4. Provide concrete code diffs or refactoring recipes for all blockers and design issues.
5. Offer to assist the developer in interactively applying the recommended fixes.

---

## The 4 Scales of Code Review

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       THE 4 SCALES OF CODE REVIEW                           │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
         ┌─────────────────────────────┼─────────────────────────────┐
         ▼                             ▼                             ▼
   1. MACRO-SCALE &              2. STRATEGIC ARCHITECTURE     3. MODULARITY &
   RESILIENCE                    & BOUNDARIES                  DEPTH DESIGN
   ──────────────────            ─────────────────────────     ───────────────
   • Timeouts & deadlines        • Strict inward dependency    • Deep vs. shallow
   • Circuit breakers & retries    flow (Clean/Hexagonal)        modules (minimal API,
   • Blast radius containment    • Bounded context integrity     rich functionality)
   • Concurrency & race hazards  • Domain model vs. script     • Information hiding
   • No silent error suppression • Ubiquitous language          • Orthogonality & DRY
                                       │
                                       ▼
                         4. MICRO-CRAFTSMANSHIP, SAFETY & TESTS
                         ──────────────────────────────────────
                         • Single Level of Abstraction (SLAP) & CQS
                         • Parameter discipline (<3) & primitive obsession
                         • Code smell taxonomy & refactoring recipes
                         • Test value lens & over-mocking checks
```

---

## Comprehensive Review Checklist by Scale

Consult the `software-engineering` skill for full definitions of foundational invariants:

### Scale 1: Macro-Scale, Resilience & Concurrency
- [ ] **Timeouts & Deadlines**: Does every remote, network, database, or RPC call have an explicit, bounded timeout? Are deadlines propagated downstream?
- [ ] **Blast Radius & Fault Isolation**: Are circuit breakers, bulkheads, or rate limiters isolating volatile external services?
- [ ] **Retry Discipline**: Are retries bounded and configured with exponential backoff and randomized jitter to prevent thundering herd outages?
- [ ] **Resource Lifecycle & Leaks**: Are sockets, file handles, DB connections, and locks strictly cleaned up via RAII, `defer`, or `try-with-resources`?
- [ ] **Concurrency & Race Hazards**: Is shared mutable state eliminated? Are race conditions, lost updates, or deadlock hazards prevented via transactions, atomic types, or optimistic locking?
- [ ] **No Silent Error Suppression**: Are catch blocks catching specific exceptions rather than generic `Exception`? Do fallbacks emit structured telemetry/metrics?

### Scale 2: Strategic Architecture & Domain Boundaries
- [ ] **Inward Dependency Rule**: Does core domain logic remain pure and isolated from frameworks, databases, HTTP protocols, UI, and external SDKs?
- [ ] **Archetype Fit**: Is the logic organized appropriately for its complexity (Transaction Script for simple CRUD vs. Rich Domain Model / Aggregates for complex business rules)?
- [ ] **Ubiquitous Language**: Does naming reflect clear, precise domain terms rather than vague generic terms (`Manager`, `Helper`, `Processor`, `Data`, `Info`)?
- [ ] **Context Mapping & Anti-Corruption**: Are external upstream payloads translated via an Anti-Corruption Layer (ACL) rather than leaking raw third-party schemas directly into core domain entities?

### Scale 3: Modularity & Depth Design
- [ ] **Deep Modules**: Do new classes, modules, or services provide significant functionality behind a small, simple, stable interface? Or are they "shallow wrappers" that add cognitive overhead without doing real work?
- [ ] **Information Hiding**: Are internal implementation details, data structures, and volatile assumptions encapsulated and kept private?
- [ ] **Orthogonality & Change Amplification**: Will a change to this module ripple across unrelated files (Shotgun Surgery), or are changes localized?
- [ ] **Single Responsibility (SRP)**: Does each component have one clear reason to change?

### Scale 4: Micro-Craftsmanship, Routine Construction & Code Smells
- [ ] **Single Level of Abstraction (SLAP)**: Does each function maintain a uniform level of abstraction, or does it mix high-level business orchestration with low-level string manipulation or raw byte juggling?
- [ ] **Command-Query Separation (CQS)**: Do methods either mutate state or return data, without doing both unexpectedly?
- [ ] **Parameter & Argument Discipline**: Are functions limited to 0–2 parameters (3+ bundled into Parameter Objects)? Are boolean flag arguments avoided in favor of explicit, intention-revealing methods?
- [ ] **Primitive Obsession**: Are domain concepts with validation/invariants (e.g., `EmailAddress`, `Money`, `OrderId`) encapsulated into Value Objects instead of raw strings/integers?
- [ ] **Defensive Contracts**: Are preconditions validated at public system barricades? Are internal invariants asserted rather than silently patched with fake fallback values?
- [ ] **Code Smell Detection**: Are classic smells present (Bloaters, Object-Orientation Abusers, Change Preventers, Dispensables, Couplers)? Are standard refactoring recipes applied?

### Scale 5: Verification, Seams & Test Value Lens
- [ ] **F.I.R.S.T. Properties**: Are tests fast, independent, repeatable, self-validating, and timely?
- [ ] **Test Value & Behavior Focus**:
  - Does the test assert observable public behavior rather than asserting framework plumbing, input fixtures, or trivial declarations?
  - Does the test assert outcomes rather than merely asserting mocks (`assert_called_with` without checking results)?
  - Does the test avoid pinning private implementation details that would shatter on safe internal refactorings?
- [ ] **Legacy Seam Discipline**: When modifying legacy code (code lacking test coverage), are changes protected by characterization tests and clean seams (*Sprout Method*, *Wrap Method*, *Extract and Override*)?
- [ ] **Two Hats Discipline**: Are refactoring changes kept distinct from behavioral/feature additions?

---

## Scope & Constraint Verification

When a change is linked to an issue or specification:
1. **File Scope**: Check if modified files exceed the stated scope. Unrelated drive-by modifications should be separated.
2. **Feature Scope**: Check if new, uncalled-for abstractions, helpers, or speculative features were introduced without necessity (YAGNI).
3. **Implementation Constraints**: If the spec or issue called for reusing specific patterns or code paths, verify that the author reused them rather than reimplementing parallel divergent copies.

---

## Delta Reviews (Re-Reviewing Iterations)

When re-reviewing after new commits have been pushed in response to a previous review:

### 1. Classify Prior Findings by Status
- **RESOLVED**: Code was updated at the specified location and directly addresses the finding.
- **CONTESTED**: The author replied with technical rationale disagreeing with the finding.
- **ACKNOWLEDGED**: The author replied agreeing or deferring (e.g., "out of scope / follow-up ticket").
- **UNADDRESSED**: No code change and no discussion addressing the finding.

### 2. Persistence & Deduplication Policy
- **Blockers**: Always re-raise unaddressed or contested blockers until resolved.
- **Suggestions / Nits**: If acknowledged by the author, do not re-raise. Only re-raise if completely unaddressed or if a new instance of the issue was introduced.
- **Thematic Deduplication**: If new code introduces the same issue already raised elsewhere in the PR or review, reference the existing finding rather than posting redundant duplicate comments.

---

## Dependabot & Dependency Update Reviews

When reviewing automated dependency updates (e.g., Dependabot / Renovate):

1. **Freshness Gate**: Verify the branch is mergeable and not stale. If stale (>30 days or conflicts), request a rebase before conducting a full review.
2. **Semver Risk Classification**:
   - **Patch (`x.y.1 -> x.y.2`)**: Bug fixes. Skim changelog; approve if CI passes.
   - **Minor (`x.1.0 -> x.2.0`)**: Features/deprecations. Check for opt-in behavioral changes.
   - **Major (`1.x -> 2.x`)**: Breaking changes. Full changelog review; verify necessary migration steps were performed.
   - **Grouped Updates**: Evaluate each package individually; risk equals the highest-risk member.
3. **Lockfile & Code Migration Discipline**:
   - Do not manually read generated lockfile diffs line-by-line.
   - Verify that any breaking changes identified in the changelog are paired with corresponding codebase migrations in the same PR.

---

## Finding Taxonomy & Severity Tiers

Structure all review findings into 4 clear tiers:

| Tier | Meaning & Trigger |
| :--- | :--- |
| **🚨 Blocker (Must-Fix)** | Invariant bugs, data corruption/loss, security vulnerabilities, missing timeouts/circuit breakers on remote I/O, race conditions, silent error swallowing, circular dependencies, outward domain dependencies violating Clean Architecture, unfulfilled acceptance criteria. |
| **⚠️ Architecture & Design (Should-Fix)** | Shallow modules, leaky abstractions, Primitive Obsession, violating SLAP/CQS, over-mocked brittle tests, missing characterization tests for legacy modifications, bloated parameter lists (>3), unaddressed breaking migrations in dependency updates. |
| **💡 Tactical Suggestion (Optional)** | Non-critical naming improvements, minor DRY opportunities, small refactoring opportunities that improve readability without blocking merge. |
| **✅ Positive Highlights** | Well-designed deep interfaces, excellent domain modeling, elegant seam extractions, or robust test invariants. |

---

## Standard Review Output Template

```markdown
# Code Review: [Target / PR Title / Feature Name]

## 1. Executive Summary
- **Overall Assessment**: [APPROVE | REQUEST_CHANGES | COMMENT]
- **Summary**: [2-3 sentences summarizing the intent of the change, architectural alignment, and key takeaways.]
- **Impact Surface**: [Files touched, core subsystems affected, and risk profile.]

---

## 2. Principle-Grounded Findings

### 🚨 Blocker (Must-Fix)
- **[Finding Title]** (`path/to/file.ext:L123-L135`)
  - **Principle**: [e.g., Production Hostility / Explicit Timeouts, Inward Dependency Rule, No Silent Error Suppression]
  - **Issue**: [Concise explanation of the defect or risk with concrete code evidence]
  - **Remediation / Suggested Change**:
    ```language
    // Concrete code or pseudocode showing the fix
    ```

### ⚠️ Architecture & Design (Should-Fix)
- **[Finding Title]** (`path/to/file.ext:L45-L60`)
  - **Principle**: [e.g., Deep Modules, Single Level of Abstraction (SLAP), Test Value Lens]
  - **Issue**: [Explanation of the architectural smell]
  - **Remediation / Suggested Change**:
    ```language
    // Concrete refactoring suggestion
    ```

### 💡 Tactical Suggestions & Polish (Optional)
- **[Suggestion]** (`path/to/file.ext:L88`): [Brief note and optional fix]

### ✅ Positive Highlights
- **[Strength]**: [Commendation of deep interface, clear naming, or solid test coverage]

---

## 3. Verification & Test Suite Status
- **Test Command**: `<exact test command executed>`
- **Result**: [Passed / Failed / Not Executable]
- **Test Quality Assessment**: [Evaluation of test value, assertion strength, and absence of over-mocking]

## 4. Next Steps
- [ ] [Clear checklist of action items for the author]
```

---

## Subagent / Self-Review Prompt Template

Use this prompt template when dispatching a subagent (or running an inline self-review) to evaluate a task increment during implementation or plan execution:

```markdown
You are a Software Engineering Code Reviewer. Your task is to perform a rigorous code review of the changes made for: [Task Name / Feature Description].

### Review Context:
- Target files: [List of modified/created files]
- Task Requirements / Acceptance Criteria: [Summary of expected behavior]
- Review Standards: Follow the reviewing-code and software-engineering skills.

### Instructions:
1. Examine the modified files and their git diff.
2. Check for organization-specific guidelines (e.g. `git remote -v` matching learningequality -> consult the `learning-equality` skill).
3. Evaluate the code across the 4 Scales of Code Review:
   - Scale 1 (Macro): Remote timeouts, error swallowing, resource cleanup, concurrency safety.
   - Scale 2 (Architecture): Inward dependency flow, domain model purity, bounded contexts.
   - Scale 3 (Modularity): Deep modules vs shallow wrappers, information hiding, orthogonality.
   - Scale 4 (Craftsmanship & Tests): SLAP, CQS, parameter limits, Primitive Obsession, Test Value lens (observable behavior vs over-mocking).
4. Run project verification commands (tests, linter, build).
5. Report your review findings using the 4-tier taxonomy:
   - 🚨 Blocker (Must-Fix)
   - ⚠️ Architecture & Design (Should-Fix)
   - 💡 Tactical Suggestion (Optional)
   - ✅ Positive Highlights
6. Conclude with a clear status verdict: `APPROVED`, `CHANGES_REQUESTED`, or `BLOCKED`.
```

---

## Operational Directives for the Agent

1. **Evidence-Based Findings**: Base feedback on observable code paths and empirical test/linter runs.
2. **Actionable Suggestions**: Never point out an issue without explaining *why* it matters and demonstrating a concrete alternative.
3. **Check Compilability First**: Always run tests before reviewing to verify whether the baseline is working or already broken.
