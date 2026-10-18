---
name: analyzing-blast-radius
description: "Discovers hidden downstream breakages, cross-system side effects, and lifecycle risks beyond symbol search (grep). Formulates the single load-bearing safety fact and proves it with executable code. Use before shipping changes or when reviewing untrusted diffs."
license: MIT - https://github.com/bjester/skills/blob/main/LICENSE
user-invocable: true
compatibility: a software project with git version control
allowed-tools:
  - read_file
  - write_file
  - run_command
  - grep
  - find_by_name
  - invoke_subagent
metadata:
  author: Blaine Jester
  version: "1.0"
---

# Analyzing Blast Radius: Beyond Symbol Search to Executable Proof

Purpose: Identify hidden, non-obvious failure modes and downstream breakages across runtime lifecycles, wire formats, and external dependencies before code ships, proving safety with executable checks rather than speculative prose.

```
┌────────────────────────────────────────────────────────────────────────┐
│                   BLAST RADIUS DISCOVERY WORKFLOW                      │
└────────────────────────────────────────────────────────────────────────┘

  1. DIFF DECONSTRUCTION  ──► Unpack implicit contract and timing changes
             │
             ▼
  2. ISOLATE SAFETY FACT  ──► Find the single fact the change's safety depends on
             │
             ▼
  3. LOOK BEYOND GREP     ──► Trace wire formats, DB columns, lifecycles, flags
             │
             ▼
  4. ASCEND CERTAINTY     ──► Elevate from assertions to runnable proof (Level 4/5)
             │
             ▼
  5. EXECUTABLE REPORT    ──► Deliver findings with runnable reproduction/check
```

---

## Core Philosophy: The Fallacy of Grep

Listing direct callers via symbol search (`grep`) is not blast radius analysis. Any basic tool can locate callsites in seconds. Real blast radius analysis uncovers **the breakages that grep cannot show you**:

- Runtime lifecycle mismatches (e.g., Solid.js reactivity vs. React reconciliation, microtask queues, teardown/unmount hooks).
- Wire format and serialization shifts (JSON payload fields consumed by separate microservices or frontend clients).
- Database column reads by external reporting jobs or analytics pipelines.
- Distributed assumptions (feature-flag interactions, cache eviction storms, connection pool starvation).
- Implicit timing dependencies or race hazards.

> [!WARNING]
> A blast radius writeup that merely *sounds* convincing is dangerous. It reads as authoritative whether true or false. Never rely on narrative reassurance. Identify the core facts the change's safety depends on and prove them by executing real code.

---

## The 5-Level Certainty Ladder

For every safety-critical claim, establish how far down this ladder your verification has reached, and state the level explicitly:

| Level | Verification Tier | Evidentiary Standard | Trustworthiness |
|:---:|:---|:---|:---:|
| **Level 1** | **Agent Assertion** | *"I reviewed the code and confirmed it won't break."* | **Worthless** on its own. |
| **Level 2** | **Code Pointer** | Points to specific `file:line` references in the repository or third-party library source. | Weak; shows mechanism exists, not that it holds. |
| **Level 3** | **Formal Failure Trace** | Walks the failure path step-by-step to demonstrate the bad case is unreachable. | Moderate; vulnerable to hidden assumptions. |
| **Level 4** | **Executable Script** | Runs a standalone script or test that imports real code and fails loud if the assumption is false. | **High**; objective and reproducible. |
| **Level 5** | **Live App Reproduction** | Exercises the exact flow within the fully booted, running application. | **Gold Standard**; definitive proof. |

Always aim to reach **Level 4** or **Level 5**. Level 4 is usually a concise script (`node`, `python`, `bash`) that imports the relevant module and tests the precise edge case.

---

## Execution Phases

### Phase 1: Deconstruct the Change
1. Read the full changeset (`git diff main...HEAD` or uncommitted diff).
2. Catalogue symbols added, modified, and deleted.
3. Identify what the code now does differently—especially the parts the diff does not spell out (altered default parameters, shifted execution order, changed return types, side-effect timing).

### Phase 2: Formulate the Single Load-Bearing Safety Fact
Most changes that appear risky depend on a **single fundamental fact** to be safe:
- *"This cache eviction call only purges items already marked expired and never evicts hot entries."*
- *"This database column rename is backward-compatible because the query layer falls back to the old column name if null."*
- *"This event emitter runs asynchronously on the next tick, so all listeners are guaranteed to be registered."*

Spend primary analytical effort isolating this single load-bearing fact. If this fact holds true, the majority of speculative risks collapse simultaneously.

### Phase 3: Investigate Where Grep Stops
Systematically audit the blind spots of static text search:
1. **Pinned Dependency Reality**: Inspect the pinned versions, transitive lockfiles, and local vendor patches of imported libraries. Verify exact behavior against library source code rather than assumptions.
2. **Lifecycle & Concurrency Realities**: Check when callbacks execute (microtasks vs. macrotasks, unmount hooks, transaction commit hooks). Does teardown cancel pending asynchronous tasks?
3. **Cross-Boundary Schemas**: Follow data across processes—JSON APIs, IPC messages, database columns, Kafka/RabbitMQ events, and configuration files read by other services.
4. **Feature Flags & State Combinations**: Identify what happens if this code runs with feature flag X disabled, or while a migration is halfway applied.

### Phase 4: Ascend to Executable Proof
Author a minimal, deterministic script or automated test that proves or disproves the load-bearing safety fact:
1. Write a script that imports the actual production module.
2. Provide input that exercises the boundary condition or edge case.
3. Assert that the bad outcome does not occur.
4. Execute the script and record its output.

### Phase 5: Multi-Model Adversarial Check (For Wide/Critical Diffs)
For wide refactors, core cryptographic/auth changes, or high-throughput concurrency:
- Dispatch the diff to two independent LLM models.
- Ask: *"What single downstream invariant does this change violate outside the modified files?"*
- Compare findings; multi-model agreement indicates high-probability blast radius.

---

## Output Report Structure

Deliver the blast radius analysis in this structured format:

```markdown
# Blast Radius Assessment: [Feature / PR Name]

## 1. What It Actually Does
[Concise summary of functional changes, emphasizing non-obvious runtime differences.]

## 2. The Load-Bearing Safety Fact
- **Statement**: [The single fact the change's safety depends on]
- **Verification Level**: [Level 4: Executable Script / Level 5: Live App]
- **Evidence**: [Script command and exact output proving the fact holds]

## 3. High-Confidence Risks
| Risk Description | Target `file:line` | Likelihood | Impact | Verification / Mitigation |
|:---|:---|:---:|:---:|:---|
| [Specific failure mode] | `path/to/file.ts:123` | High/Med/Low | High/Med/Low | [Executable check or fix] |

## 4. Cleared Risks
- [Item audited, why it appeared risky, and the exact code/schema fact that clears it.]

## 5. Pre-Merge Verification Script
```bash
# Executable script demonstrating safety
node -e "..."
```
```
