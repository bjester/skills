---
name: engineering-with-agents
description: "Disciplines, behavioral guardrails, and operational heuristics for autonomous and paired agentic software engineering. Use when planning, implementing, refactoring, or verifying code with AI coding agents to prevent agent pathology, proxy verification, and cognitive debt."
license: MIT - https://github.com/bjester/skills/blob/main/LICENSE
user-invocable: true
compatibility: any software development project using AI agents or paired coding
allowed-tools:
  - read_file
  - write_file
  - run_command
  - grep
  - find_by_name
  - invoke_subagent
  - ask_user_question
metadata:
  author: Blaine Jester
  version: "1.1"
---

# Engineering with Agents: Disciplines for Autonomous and Paired LLM Development

Purpose: Provide actionable, high-leverage principles and operational guardrails that prevent autonomous coding agents and paired LLMs from introducing architectural debt, context degradation, proxy illusions, and mechanical thrashing.

```
┌─────────────────────────────────────────────────────────────────────────┐
│              AGENTIC SOFTWARE ENGINEERING CONTROL LOOP                  │
└─────────────────────────────────────────────────────────────────────────┘

  1. CONTEXT & SCOPE      ──► Cap tokens, delegate bulk reading, minimize diffs
            │                 (Guard Context, Laziness Protocol)
            ▼
  2. DESIGN & TYPES       ──► Side-by-side prototypes, illegal states unrepresentable
            │                 (Exhaust Design Space, Type System Discipline)
            ▼
  3. MIGRATION & REFACTOR ──► Single-wave execution, zero zombie adapters
            │                 (Migrate & Delete Legacy APIs)
            ▼
  4. VERIFICATION GATES   ──► Primary artifact checks, 2-edit test on behavior
            │                 (Prove It Works, Test Behavior Not Implementation)
            ▼
  5. STRUCTURAL LOCK-IN   ──► Encode corrections in lints/types, not prompt text
                              (Encode Lessons in Structure)
```

---

## Prerequisites & Operating Posture

When operating as an agent or pair-programming with an agent, adopt this default posture:

- **Candor Over Sycophancy ("No Is an Acceptable Answer")**: When invited to add scope, proposed an unsound design, or asked if an approach works, reply with unvarnished technical judgment. Decline, push back, or state *"this does not earn its place"* when true. Agreement is not the default.
- **Autonomy Boundaries (Reversible vs. Irreversible)**:
  - *Proceed Autonomously*: Writing code, creating throwaway tests, inspecting logs, refactoring within boundaries, and building helper scripts are reversible. Do not block the human on reversible implementation choices.
  - *Always Pause*: Dropping databases, running destructive migrations, force-pushing shared branches, publishing packages, or sending external communications are irreversible. Always require explicit human confirmation.
- **Evidence-Labeled Communication**: Label claims within the same sentence as *[Measured]*, *[Inferred]*, or *[Guessed]*. Never report an inference as a fact or hand an operator a verification check you could have run yourself.
- **Surface Assumptions & Competing Interpretations Upfront**: When a request has unstated requirements or multiple valid interpretations, state your assumptions explicitly and present the trade-offs before writing code—never pick silently and build on a guess.
- **Protected Paths & Secret Exclusion**: Never read, echo, or stage `.env*` secrets, private keys (`*.pem`, `*.key`), or credential stores; require explicit user confirmation before modifying CI/CD pipelines (`.github/workflows/`) or deployment infrastructure.

---

## Section 1: Context & Scoping Disciplines

Context window capacity and attention span are finite, scarce resources. Context bloat degrades reasoning quality, introduces compression artifacts, and causes instruction drift.

### 1. Guard the Context Window
- **Route Bulk Operations to Subagents**: Never dump multi-thousand-line log files, huge dependency dumps, or massive files directly into the primary reasoning session. Dispatch targeted, read-only subagents to search, filter, and extract concise findings.
- **Pass File Pointers, Not Inlined Blobs**: When delegating work to subagents, supply exact file paths, line ranges, and interface contracts rather than pasting full file contents into prompt arguments.
- **Size Phases and Turn Budgets**: Keep execution phases tightly bounded. If a task requires inspecting more than 10 files or running iterative sweeps, break it into distinct subagent phases and bring only consolidated conclusions back to the parent session.
- **Disjoint Subagent Write Ownership**: Parallel subagents must either be strictly read-only (research/review) or own completely disjoint file sets—never dispatch concurrent subagents that can edit the same file.

### 2. Laziness Protocol: Decision Consolidation & Diff Minimization
- **Consolidate Decisions Behind One Source of Truth**: Never duplicate a conditional decision or configuration branch across multiple call sites. Resolve the choice once behind a single authority and pass the resulting decision downstream as a simple, unambiguous flag or value.
- **Minimize the Diff**: Measure craftsmanship by the size and clarity of the resulting diff. The smallest change that solves the problem and preserves invariants strictly beats "elegant" multi-file boilerplate, gratuitous wrappers, or unprompted indirection.
- **Bias Toward Deletion**: Before adding new abstractions, ask what obsolete code or dead abstractions can be deleted.
- **Neighbor Conformity & Orphan Cleanup**: Read the target file and at least one neighboring module first to mirror local naming, error types, and utilities. Delete imports, variables, and helpers orphaned by *your* edit, strip `// Step N:` tutorial comments, and flag pre-existing dead code without bundling unrelated deletions.

---

## Section 2: Design & Type System Disciplines

### 1. Exhaust the Design Space
When encountering a novel interaction, architectural boundary, or product UX decision with **no established precedent in the codebase**:
- **Build 2–3 Competing Throwaway Prototypes**: Rather than speculating theoretically in text or committing to the first architecture that comes to mind, create 2–3 minimal, competing sketches or prototypes.
- **Compare Empirically**: Evaluate prototypes side-by-side against observable properties: latency, ergonomics, reader load, and UX feel.
- **Throw Away the Losers**: Pick the winning design based on empirical observation, discard the prototypes, and implement the chosen architecture cleanly with full tests.

> [!TIP]
> Prototyping is vastly cheaper in throwaway scratch files or quick UI mockups than in full production code with migrations and mocks.

### 2. Type System Discipline
Make the compiler and static type checker eliminate classes of bugs before code ever reaches runtime:
- **Brand Semantic Primitives**: Do not pass raw strings or integers for distinct domain concepts. A `UserId` and an `OrderId` may both be strings underneath, but they must never be interchangeable. Use branded types (e.g. `type UserId = string & { readonly __brand: unique symbol }`) or distinct newtypes/value objects. Validate once at creation, trust downstream.
- **External Data Is Untyped Until Parsed**: All RPC payloads, JSON blobs, HTTP queries, CLI arguments, config files, environment variables, and database rows are completely untyped upon arrival. Run every incoming payload through a parse/schema function at the system boundary that returns strongly typed, validated domain objects. Never cast (`as T`) without runtime validation.
- **Derive Types from Authoritative Schemas**: When a shape is owned by an authoritative source—Protobuf, OpenAPI, GraphQL schema, SQL migration, or design token file—derive code types directly from that schema using code generators. Never hand-roll parallel interfaces that can drift out of sync.

### 3. Defeating Systematic LLM Code Pathologies
1. **Guard the Boundary, Trust the Internal Contract**: Validate and parse untrusted inputs rigorously at system boundaries, but do not litter typed internal call graphs with impossible defensive null/type checks or broad `try/catch` blocks that swallow errors and return `null`.
2. **No Mock Fallbacks or Hardcoded "Success" in Production**: Never return canned fixtures, `{"status": "ok"}`, or silent no-ops in production code to make a caller or test pass; throw an explicit unimplemented error and report the blocker.
3. **Verify Imports & APIs Against the Lockfile**: Models frequently hallucinate package names and method signatures. Inspect the project's lockfile, installed package version, or existing repo callsites before invoking unfamiliar library APIs.
4. **Re-Derive & State Loop Contracts Before Coding (Never Copy-Adapt)**: LLMs introduce off-by-one, pointer-aliasing, and postcondition bugs when pattern-matching or copy-adapting adjacent functions. Before generating non-trivial loops, pointer mutations, or recursion, explicitly write down the boundary input cases (`empty, singleton, duplicates, zero/negative, overflow`), the 1-line loop invariant (`// inv:`), and the strictly decreasing termination measure (`// term:`).

---

## Section 3: Refactoring & Migration Disciplines

### 1. Migrate Callers Then Delete Legacy APIs (One-Wave Migrations)
When introducing a new internal API, interface, or module to replace an existing one within a repository you control:
- **Execute in a Single Coordinated Wave**: When no external third-party consumers depend on backward compatibility, **do not build temporary backward-compatibility layers, deprecation shims, or pass-through adapters**.
- **Migrate and Delete Together**:
  1. Introduce the new API and its contracts.
  2. Update all internal callers across the codebase to use the new API.
  3. Delete the old API and its obsolete implementation in the exact same wave.
  4. Update the test suite to assert the new contract, and ruthlessly delete tests that existed only to verify transitional or obsolete implementation details.
- **Prevent Zombie Adapters**: Transitional compatibility layers built during migrations frequently become permanent, confusing technical debt. Unless external consumers require versioned stability, eliminate the old path immediately.

---

## Section 4: Verification & Truth Disciplines

### 1. Prove It Works: Primary Artifact Verification
Never declare a task done, report success, or sign off on a change based on secondary proxies or self-reports.

```
┌─────────────────────────────────┬─────────────────────────────────┐
│     HOLLOW / PROXY "PROOF"      │      REAL OBSERVABLE PROOF      │
│          (UNACCEPTABLE)         │           (MANDATORY)           │
├─────────────────────────────────┼─────────────────────────────────┤
│ • "The file was written to disk"│ • Executed the binary or script │
│ • "The code compiles / lints"   │ • Inspected actual stdout/stderr│
│ • "The mock was called"         │ • Verified real DB row persisted│
│ • "File mtime updated"          │ • Checked live process status   │
│ • "Agent self-reports pass"     │ • Ran end-to-end user scenario  │
└─────────────────────────────────┴─────────────────────────────────┘
```

- **Check the Real Output Directly**: Run the command, curl the endpoint, inspect the rendered UI element, or query the database table. Directly observe the artifact that an end-user or external system interacts with.
- **Script the Check**: Whenever possible, turn verification into a deterministic, rerunnable script (`bash`, `node`, `pytest`). An automated verification script transforms an agent's *"trust me, it works"* assertion into a reproducible *"run this command to see it pass"* guarantee that human reviewers can rerun at zero marginal cost.

### 2. Test Behavior, Not Implementation
A test is an executable specification of what code delivers to its consumers (callers, users, external systems). It is not a spy on internal mechanics.

#### The Two-Edit Mental Test
Audit every test against two hypothetical changes:

1. **Break the Behavior**: Deliberately alter the return value, drop a side effect, or double-emit an event.
   - *Pass criteria*: The test **must fail**.
   - *Failure cause*: If the test still passes, the assertion is too loose, the expected value was tautologically computed by the code under test, or the test never actually executed the critical path.
2. **Change the Internals**: Completely restructure private helpers, internal data structures, or call order while keeping the public contract and observable results identical.
   - *Pass criteria*: The test **must continue to pass cleanly**.
   - *Failure cause*: If the test fails, it is tightly coupled to internal mechanics (e.g., verifying private method invocation counts or asserting on intermediate data). It will cause maintenance drag on every future refactor while catching zero bugs.

> [!IMPORTANT]
> Keep tests that fail on Edit 1 and pass on Edit 2. Rewrite or delete the rest. Assert on observable return values, persisted states, or payloads sent to true external architectural boundaries.

---

## Section 5: Meta-Engineering & System Evolution

### 1. Encode Lessons in Structure
Natural language instructions and prompt reminders degrade over time and rely on fragile LLM compliance.

- **Convert Instructions into Mechanical Structure**: Whenever you catch yourself repeating an instruction or correction for a second time, do not write a longer prompt. Encode the rule into:
  - A linter rule or custom AST check.
  - A strict compile-time type constraint or schema validator.
  - An automated pre-commit hook or CI pipeline gate.
  - A deterministic setup or migration script.
- **The Structural Corollary**: *If the fix can be structural, use ONLY the structural fix.* Prompt instructions and advisory comments are symptoms of missing structural constraints.
- **When Judgment Is Unavoidable**: If a rule inherently requires human or semantic judgment and cannot be automated mechanically, place the guidance into a visible skill, accompany it with an explicit failure mode example, and add a verification checkpoint.
- **Skill Routing Hygiene**: When encoding judgment into a `SKILL.md`, write the YAML `description` strictly as a trigger/routing contract (*what* + *when* + *anti-patterns*)—never summarize the step-by-step workflow in `description`, or agents will follow the summary shortcut and skip reading the skill body.

---

## Summary Checklist for Agent Operations

Before submitting work, verify adherence to these agentic disciplines:

- [ ] **Context Conserved**: Bulk file exploration was kept out of the main thread; diff is minimal and cohesive.
- [ ] **Decisions Consolidated**: Logic is governed by single sources of truth, not duplicated boolean flags.
- [ ] **Types Disciplined**: External data parsed at boundary; semantic primitives branded; no illegal states representable.
- [ ] **AI Code Pathologies Defeated**: Inputs validated at boundaries; zero mock production fallbacks; imports lockfile-verified; loop/recursion contracts derived explicitly.
- [ ] **Migrations Clean**: Internal changes migrated in one wave; zero zombie adapters or deprecated wrappers left behind.
- [ ] **Real Artifacts Verified**: Verified the primary runtime output directly with a rerunnable command (not just linter/compiler).
- [ ] **Tests Contract-Driven**: Every test passes the Two-Edit Mental Test (survives internal restructuring, fails on broken behavior).
- [ ] **Corrections Encoded**: Recurring guidance has been codified into tests, lints, or scripts rather than ephemeral chat text.
