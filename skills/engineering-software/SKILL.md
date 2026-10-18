---
name: engineering-software
description: |
  Foundational software engineering invariants, Clean/Hexagonal architecture,
  deep module design, defensive programming, refactoring recipes, legacy seam
  mitigation, and production resilience. Activate when designing, writing,
  reviewing, or refactoring code.
license: MIT - https://github.com/bjester/skills/blob/main/LICENSE
user-invocable: true
compatibility: any software development project
allowed-tools:
  - read_file
  - write_file
  - grep
  - find_by_name
metadata:
  author: Blaine Jester
  version: "1.0"
---

# Engineering Software: Design, Execution, and the Evolution of Software

Synthesized from 14 foundational software engineering texts to guide system design, code craftsmanship, and architecture.

## Introduction & Foundational Scales

A single meta-problem unites software engineering: **managing cognitive load in the presence of inevitable change and production chaos.** This challenge spans four complementary scales:

1. **Macro-Scale & Resilience**: Distributed systems, storage models, fault domains, backpressure, and runtime stability.
2. **Strategic Domain & Architecture**: Bounded Contexts, Ubiquitous Language, and strict inward dependency isolation.
3. **Modularity & Depth Design**: Deep modules (simple interfaces hiding rich logic), information hiding, and orthogonality.
4. **Micro-Craftsmanship & Safety**: Clear naming, SLAP, refactoring mechanics, seam engineering, and test discipline.

### The 7 Universal Invariants

1. **Complexity Is the Enemy**: Eliminate anything that compounds cognitive load, amplifies changes, or creates unknown unknowns.
2. **Strict Inward Dependency Flow**: Core domain policies never depend on frameworks, UI, persistence, or I/O mechanisms.
3. **Deep Information Hiding**: Expose minimal, stable interfaces that encapsulate internal implementation volatility.
4. **Explicit Domain Ubiquity**: Speak the rigorous domain language of the specific bounded context—no generic "managers" or diluted abstractions.
5. **Preserve Behavior with Continuous Safety Nets**: Never rewrite blindly; establish characterization tests, locate seams, and refactor in micro-steps.
6. **Design for Production Hostility**: Assume remote calls and I/O will hang, fail, or corrupt; isolate blast radiuses.
7. **Strategic Over Tactical**: Invest continuous small efforts (10–20%) in clean design and boundaries; fix broken windows immediately.

---

## Section 1: Philosophy, Mindset & Complexity Management

- **Strategic vs. Tactical Programming**: Tactical programming prioritizes immediate feature delivery at the expense of compounding complexity debt. Strategic programming continually invests 10–20% in design clarity, clean boundaries, and documentation.
- **The 3 Symptoms of Complexity**:
  1. *Change Amplification*: A single conceptual change requires edits across many files.
  2. *Cognitive Load*: Completing a task requires holding too many disparate facts in memory.
  3. *Unknown Unknowns*: It is unobvious which lines must change or what side effects will occur.
- **Broken Windows Theory**: Neglected hacks or defects accelerate system-wide entropy. Fix rot immediately upon contact.
- **Orthogonality & Reversibility**: Changes to one component must not affect unrelated components. Keep decisions reversible by decoupling business rules from volatile third-party vendors, databases, or frameworks.
- **Defer Decisions**: Defer structural commitments (frameworks, storage engines) until domain requirements are crystalline.
- **Redesign from First Principles**: When integrating a major requirement or capability into an existing design, avoid reflexively bolting on adapters or pass-through wrappers. First ask: *"If this system were being written from scratch today with this requirement as a foundational assumption, what would we build?"* Design the target structure holistically, then execute the transition incrementally while preserving option value.
- **Core Guidance**: Measure design quality by cognitive load, avoid clever one-liners that obscure control flow, and eliminate architectural rot proactively.

---

## Section 2: Strategic Design & Domain Boundaries

- **Problem vs. Solution Space**:
  - *Problem Space*: Subdomains categorized into *Core Domain* (differentiating advantage), *Supporting Domain* (custom supporting logic), and *Generic Domain* (off-the-shelf commoditized logic).
  - *Solution Space*: Bounded Contexts—explicit linguistic and conceptual boundaries where a unified domain model applies.
- **Ubiquitous Language**: A shared, precise vocabulary used by domain experts and engineers within a single Bounded Context.

### Context Mapping Relationships

| Relationship | Plain Meaning | Example |
| :--- | :--- | :--- |
| **Upstream / Downstream** | Upstream dictates API/data; downstream adapts. | Payment gateway (Upstream) $\rightarrow$ Checkout service (Downstream). |
| **Shared Kernel** | Shared code/schema requiring joint coordination. | Shared library or common database table across services. |
| **Customer–Supplier** | Upstream cooperates and prioritizes downstream requests. | Platform team building endpoints for the Frontend team. |
| **Conformist** | Downstream accepts upstream schema directly without translation. | Adopting third-party SaaS payload directly as internal model. |
| **Anti-Corruption Layer (ACL)** | Translates and isolates foreign/legacy models from domain. | Adapter translating legacy COBOL mainframe records into domain entities. |
| **Open Host Service (OHS)** | Standardized public protocol/schema for multiple consumers. | Stripe API (REST/JSON) or AWS S3 SDK. |
| **Separate Ways** | Cut ties; duplicate solutions when integration costs exceed value. | Building an internal tax helper rather than integrating a costly enterprise suite. |

### Business Logic Archetypes

| Pattern | Complexity Level | Ideal Use Case |
| :--- | :--- | :--- |
| **Transaction Script** | Low (CRUD, procedural) | Simple procedural logic, scripts, data pipelines. |
| **Table Module** | Low to Medium (data-centric) | Record sets, table-driven structures. |
| **Domain Model** | Medium to High (rich behaviors) | Complex state transitions, business invariants. |
| **Service Layer** | Boundary orchestrator | Transaction demarcation, API coordinators. |

---

## Section 3: Tactical Modeling & Component Architecture

- **Deep vs. Shallow Modules**:
  - *Deep Module*: Small, simple interface concealing powerful internal logic (e.g. Unix file I/O `open/read/write/close` hiding block allocators and multi-tier buffers).
  - *Shallow Module*: Complex interface with trivial internal logic; pass-through wrappers that increase cognitive load without adding leverage.
- **The Dependency Rule (Hexagonal / Clean Architecture)**:
  - Dependencies must point strictly **inward**:  
    `Frameworks & Drivers (Web, DB, UI) ──► Interface Adapters (Controllers, Gateways) ──► Application / Use Cases ──► Entities / Core Domain`
  - Core domain policies must remain agnostic of SQL, HTTP, or serialization mechanisms.
- **Primitive Obsession**: Misusing generic primitives (`string`, `int`, `dict`) for domain concepts that carry invariants, validation, or behavior. Encapsulate them into typed Value Objects.
- **Tactical DDD Building Blocks**:
  - **Entity**: Defined by explicit identity and continuity over time, not mutable attributes.
  - **Value Object**: Immutable concept defined solely by attribute values; equality by value. Eliminates side-effects.
  - **Aggregate**: Cluster of associated entities and value objects forming a transactional consistency boundary.
    - *Rule 1*: Guard invariants strictly within aggregate boundaries.
    - *Rule 2*: Design small aggregates (Aggregate Root + minimal inner entities).
    - *Rule 3*: Reference other aggregates exclusively by Global Identifier (`Id`), never direct object reference.
    - *Rule 4*: Apply eventual consistency across aggregate boundaries via Domain Events.
  - **Domain Service**: Pure, stateless domain logic that naturally spans multiple entities or value objects.
  - **Repository**: Emulates in-memory collection of aggregate roots, abstracting persistence mechanisms.
- **Component Coupling & Cohesion Principles**:
  - *REP (Reuse/Release Equivalence)*: The granule of reuse is the granule of release.
  - *CCP (Common Closure)*: Group together classes that change for the same reasons and at the same times.
  - *CRP (Common Reuse)*: Avoid forcing callers to depend on things they do not use.
  - *SDP (Stable Dependencies)*: Depend in the direction of stability.
  - *SAP (Stable Abstractions)*: A component should be as abstract as it is stable.

---

## Section 4: Low-Level Craftsmanship, Naming & Routine Construction

- **Meaningful Naming**:
  - Reveal intent, domain terminology, and units of measure (`timeoutMs`, `remainingRetries`).
  - Eliminate noise words (`Data`, `Info`, `Manager`, `Helper`) and cryptic abbreviations.
  - Name functions as action verbs (`calculateTax`, `postPayment`) and classes as domain nouns (`Order`, `Customer`).
- **Routine Construction**:
  - **Single Responsibility Principle (SRP)**: Routines do one cohesive task.
  - **Single Level of Abstraction Principle (SLAP)**: Keep all statements within a routine at the same abstraction tier. Do not mix high-level workflow orchestration with low-level string slicing.
  - **Parameter Discipline**: Prefer 0–2 parameters. 3 requires clear justification; 4+ must be bundled into a Parameter Object or Value Object.
  - **Command-Query Separation (CQS)**: A routine should either mutate state (Command) or return data (Query), never both.
  - **Avoid Flag Arguments**: Boolean arguments indicate a function performing two distinct jobs. Split into explicit, dedicated routines.
- **Objects vs. Data Structures**:
  - *Objects*: Hide internal state behind abstractions and expose behavior.
  - *Data Structures*: Expose raw data without business behavior (DTOs, schemas).
  - Avoid hybrid classes that expose public getters/setters while executing complex business logic.
- **Pseudocode Programming Process (PPP)**: Draft and review high-level pseudocode before coding; convert validated pseudocode into routine structure and explanatory header comments.

---

## Section 5: Defensive Programming, Contracts & Error Handling

- **Design by Contract (DbC)**:
  - *Preconditions*: What must hold true before routine execution (caller responsibility).
  - *Postconditions*: What the routine guarantees upon completion.
  - *Class Invariants*: Conditions that remain true before and after every public operation.
- **Define Semantics, Not Suppressions**:
  - Redesign APIs so edge conditions become natural domain outcomes (e.g. idempotent delete, slice bounds clipping). Never catch unexpected exceptions to silently return fake or empty objects.
  - *Observability Invariant*: Fallbacks and default states must never be silent. Emit structured telemetry when fallbacks activate.
  - *Fail Fast Over Defensive Bloat*: Program defects and invariant breaches must crash early or bubble to top-level boundaries. A halted program causes less damage than corrupted data persisted silently.
- **Barricades vs. Internal Invariants**:
  - *Barricades*: Sanitize, parse, and validate untrusted data at public boundaries (HTTP, RPC, CLI, disk).
  - *Internal Invariants*: Enforce domain preconditions internally with assertions; do not swallow illegal state.
- **Error Handling Discipline**:
  - Use exceptions/results over integer error codes.
  - Never return `null` or accept `null` parameters; use Null Objects, empty collections, or `Option`/`Result` types.
  - Release resources deterministically via `try-with-resources`, `defer`, or RAII patterns.
  - Never catch generic `Exception` or swallow errors with empty `catch` blocks.

---

## Section 6: Refactoring Disciplines & Code Smell Taxonomy

- **Refactoring Definition**: Restructuring internal code structure without altering observable behavior to improve readability, reduce complexity, and simplify change.
- **The Two Hats Discipline**: Strictly separate the *Refactoring Hat* (restructuring code while tests remain green) from the *Adding Functionality Hat* (adding new tests and features). Never mix both in a single step.
- **When to Refactor**:
  - *Rule of Three*: 1st time write it; 2nd time notice duplication; 3rd time refactor.
  - *Preparatory Refactoring*: Make the change easy before making the easy change.
  - *Comprehension Refactoring*: Refactor while reading unfamiliar code to solidify understanding.

### Code Smell & Treatment Index

| Smell Category | Common Smells | Primary Refactoring Recipes |
| :--- | :--- | :--- |
| **Bloaters** | Long Method, Large Class, Primitive Obsession, Long Parameter List, Data Clumps | Extract Function, Replace Data with Object, Introduce Parameter Object, Extract Class |
| **OO Abusers** | Switch Statements, Refused Bequest, Alternative Classes w/ Different Interfaces | Replace Conditional with Polymorphism, Replace Type Code with Subclasses/State |
| **Change Preventers** | Divergent Change (1 class, many reasons to change), Shotgun Surgery (1 change, many classes) | Extract Class, Move Function/Field, Inline Class |
| **Dispensables** | Crutch Comments, Duplicate Code, Dead Code, Lazy Class, Speculative Generality | Extract Function, Inline Function, Remove Dead Code, Collapse Hierarchy |
| **Couplers** | Feature Envy, Inappropriate Intimacy, Message Chains, Middle Man | Move Function, Extract Method, Hide Delegate, Remove Middle Man |

---

## Section 7: Legacy Code Mitigation & Seam Engineering

- **Legacy Code Definition**: Code without automated tests. Without automated test coverage, engineers cannot know whether modifications improve or break system behavior.
- **The 5-Step Legacy Change Algorithm**:
  1. Identify change points.
  2. Find test points.
  3. Break dependencies.
  4. Write characterization tests.
  5. Make changes and refactor.
- **Seams**: Points where program behavior can be altered without editing code in place.
  - *Object Seam*: Polymorphic method calls overridden in subclasses, test doubles, or strategies.
  - *Link Seam*: Replacing linked libraries, classpath imports, or dependency injection bindings.
  - *Preprocessor Seam*: Macro definition substitutions (C/C++).
- **Characterization Tests**: Tests that document and lock down *actual current behavior* (including quirks and edge cases) prior to refactoring.
- **Dependency-Breaking Techniques**:
  - *Sprout Method / Sprout Class*: Author new logic in a fresh, isolated method/class with 100% test coverage; invoke with a single call from legacy code.
  - *Wrap Method / Wrap Class*: Decorate legacy invocations with pre/post operations without modifying the legacy method body.
  - *Extract and Override Call / Subclass and Override*: Extract hard dependencies into protected methods on the legacy class; override them with test doubles in test subclasses.
  - *Sensing and Separation*: Break dependencies to sense hidden output values (Sensing) or enable execution in test harnesses (Separation).

---

## Section 8: Production Resilience, Stability & Concurrency

- **The Cynical Architect Mindset**: Assume all remote dependencies will fail, hang indefinitely, leak resources, or return corrupted payloads.
- **Cascading Failures & Blast Radius**: Prevent single-point faults from exhausting shared thread pools, connections, or memory across upstream services.

### Stability Patterns Matrix

| Pattern | Mechanism & Operational Value |
| :--- | :--- |
| **Circuit Breaker** | Trips open upon repeated downstream failures to fail fast; periodically probes with half-open requests. |
| **Bulkhead** | Partitions resources (threads, CPU, memory) so a failing subsystem cannot starve other operations. |
| **Timeouts & Deadlines** | Bounded timeouts on all network calls; pass deadlines downstream to cancel expired operations. |
| **Retries w/ Jitter** | Exponential backoff combined with randomized jitter to prevent thundering herd retry storms. |
| **Fail Fast** | Validate prerequisites immediately; abort early rather than burning compute on doomed tasks. |
| **Shed Load & Backpressure** | Return HTTP 429/503 when buffers fill instead of queueing to an Out-Of-Memory (OOM) crash. |
| **Steady State** | Automatic resource reclamation without manual intervention (log rotation, connection pool scavenging). |
| **Idempotent Reconciliation** | Derive state changes from current vs. desired delta; safely converges on retries or crash recovery. |

- **Concurrency & State Management**:
  - *Shared-Nothing & Immutability*: Prefer immutable data structures and message-passing over shared mutable memory.
  - *Race Hazard Mitigations*: Use transactions, optimistic locking (version fields), or atomic operations.
  - *Deadlock Prevention*: Always acquire locks in a consistent, globally deterministic order.
  - *Operational Idempotency & Crash Reconciliation*:
    - *Diff-Against-State*: Derive each mutating step from the state that currently exists, not from what a prior run intended to do. Compare current to desired state and apply only the difference.
    - *Crash-Point Resilience*: If an operation halts halfway through, subsequent executions must recognize partial artifacts (temporary files, uncommitted records, half-written tables) as stale using intrinsic evidence (content hashes, atomic renames) rather than fragile timestamps.
    - *The 3-Question Invariant*: (1) What happens if this runs twice consecutively? (2) What happens if the previous run crashed at every intermediate step? (3) Does re-execution converge deterministically to the identical end state?

---

## Section 9: Data Architecture, Storage & Distributed Systems

- **The Reliability-Scalability-Maintainability Triad**:
  - *Reliability*: Tolerating hardware faults, software defects, and human mistakes.
  - *Scalability*: Measuring latency through p95, p99, and p99.9 percentiles under load growth.
  - *Maintainability*: Operability (visibility/telemetry), Simplicity (managing complexity), Evolvability (safe schema evolution).

### Storage Engine Paradigms

| Paradigm | Mechanism | Strengths | Trade-Offs | Real-World Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **B-Trees** | In-place updates to fixed-size pages (4KB). | Fast point reads, predictable read latency, transactional isolation. | Slower writes (random I/O, write amplification). | OLTP relational DBs (PostgreSQL, MySQL, SQLite). |
| **LSM-Trees / SSTables** | Sequential writes to memtable flushed to immutable disk files; merged via compaction. | Ultra-high write throughput, high disk compression. | Compaction CPU/disk overhead, slower multi-file reads. | High-throughput ingest, timeseries, event logs (Cassandra, RocksDB). |

### Transactions & Isolation Levels

| Isolation Level | Anomalies Prevented | Anomalies Still Possible | Mechanism | Recommended Scenario |
| :--- | :--- | :--- | :--- | :--- |
| **Read Committed** | Dirty reads, dirty writes. | Non-repeatable reads, phantom reads, write skew. | Row write locks; read locks released immediately. | Standard default for basic CRUD systems. |
| **Snapshot Isolation / MVCC** | Dirty reads, non-repeatable reads, phantom reads. | **Write skew** (disjoint updates violating joint invariant). | Multi-Version Concurrency Control (reads never block writes). | Analytical reporting, backups, complex dashboards. |
| **Serializable** | **All race conditions & anomalies**. | None. | Two-Phase Locking (2PL), serial execution, or SSI (Serializable Snapshot Isolation). | Financial transfers, double-booking prevention, inventory allocation. |

### Replication Topologies & Consensus

| Topology | Write Path | Read Path | Failure / Partition Behavior | When to Use |
| :--- | :--- | :--- | :--- | :--- |
| **Single-Leader** | Writes go to single leader node. | Reads served by leader or read replicas. | Failover requires election; laggy replicas cause stale reads. | Default choice for general web apps needing strong consistency. |
| **Multi-Leader** | Writes accepted across multiple regional leader nodes. | Local regional reads. | Requires conflict resolution (LWW, CRDTs); risk of divergence. | Multi-datacenter setups or offline-capable collaborative apps. |
| **Leaderless (Dynamo)** | Writes broadcast to $W$ quorum nodes. | Reads queried from $R$ quorum nodes ($W + R > N$). | Sloppy quorums, anti-entropy repair, eventual consistency. | High-availability systems that cannot tolerate write downtime. |

### Schema Evolution & Data Flow Invariants

- **Protobuf / Avro Tag Immutability**: Never alter the integer tag/ID of an existing field.
- **Deprecation & Field Deletion**: Never reuse an old field tag; explicitly mark deleted tag IDs as `reserved`.
- **Preserve Unknown Fields**: Ensure intermediary proxies and microservices pass unrecognized fields through without stripping them during serialization cycles.
- **Optionality by Default**: Treat every new field as optional with safe default fallbacks in existing consumers.
- **CAP & PACELC Trade-Offs**: If partitioned (P), choose Availability (A) vs. Consistency (C); Else (E), trade Latency (L) vs. Consistency (C).

---

## Section 10: Testing Strategies, Seams & Verification

- **Role of Tests**: Tests serve as **design tools, safety nets, and executable specifications**.
- **F.I.R.S.T. Test Properties**:
  - **F**ast: Sub-millisecond execution encourages continuous test runs.
  - **I**ndependent: Tests do not share mutable state or depend on execution order.
  - **R**epeatable: Deterministic in any environment (local, CI/CD, staging).
  - **S**elf-Validating: Boolean pass/fail output without manual log inspection.
  - **T**imely: Authored just before production code (TDD) or concurrently.
- **Testing Levels & The Test Pyramid**:
  - *Unit Tests*: Isolated verification of domain invariants without network/disk I/O.
  - *Integration Tests*: Verification of component interactions across database/container boundaries.
  - *Contract & Boundary Tests*: Schema validation against external third-party APIs.
  - *Characterization Tests*: Pinning existing legacy behavior before refactoring.
- **Avoid Test-Induced Damage (Over-Mocking)**:
  - Test observable public behavior and returned state, not private collaborator interactions.
  - Mock only at true external architectural boundaries (network, system clock, disk).

---

## Section 11: Resolving Architectural Tensions & Trade-Offs

Synthesizing 14 classic software engineering texts reveals apparent tensions that mature engineers and coding agents must navigate:

### Tension 1: Small Functions (Clean Code) vs. Deep Modules (Philosophy of Software Design)
- *The Conflict*: *Clean Code* advises tiny functions (<20 lines). *Ousterhout* warns that excessively fragmented routines cause "shallow modules" and "classitis", exploding cognitive tracing overhead.
- *The Resolution*: Create **deep modules for public abstraction boundaries** (powerful capabilities behind minimal, cohesive APIs). Within the private implementation of a deep module, decompose complex logic into helper routines adhering to SLAP. Avoid creating shallow wrapper classes that merely pass calls through.

### Tension 2: Rich Domain Model (DDD) vs. Transaction Script (PofEAA) vs. Event Streams (DDIA)
- *The Conflict*: DDD advocates rich encapsulated domain objects. PofEAA notes that simple CRUD is harmed by over-engineering a Domain Model. DDIA emphasizes decoupled data pipelines and immutable event logs.
- *The Resolution*: Match the archetype to domain complexity:
  - Simple CRUD / reporting $\rightarrow$ Transaction Script or Table Module.
  - High-complexity business rules / state machines $\rightarrow$ Rich Domain Model with Aggregates.
  - High-throughput asynchronous ingestion / sync $\rightarrow$ Event-Driven Dataflow / Stream Processing.

### Tension 3: Fail Fast (Pragmatic Programmer) vs. Graceful Degradation (Release It!)
- *The Conflict*: The Pragmatic Programmer urges crashing immediately on bugs. Release It! demands systems stay alive and degrade gracefully during partial outages.
- *The Resolution*:
  - *Programming bugs & broken domain invariants* $\rightarrow$ **Fail Fast & Crash Early** (prevents silent data corruption).
  - *External network, environmental, or upstream dependency failures* $\rightarrow$ **Isolate, Circuit Break, and Degrade Gracefully** (preserves user functionality).
