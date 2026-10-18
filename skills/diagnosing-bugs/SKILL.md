---
name: diagnosing-bugs
description: "Systematic diagnosis and debugging loop for bugs, test failures, unexpected behaviors, and performance regressions. Use when diagnosing, debugging, or fixing defects before proposing or writing code changes."
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

# Diagnosing Bugs: Systematic Debugging & Defect Investigation

Purpose: Provide a rigorous, hypothesis-driven, evidence-based debugging workflow for diagnosing software bugs, race conditions, test failures, and performance regressions without speculative guess-and-check thrashing.

## Prerequisites & Core Philosophy

- **The Iron Law**: **NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST**. Quick patches and symptom masks waste time, create new defects, and compound technical debt.
- **Reference Software Engineering Guidelines**: Consult the `software-engineering` skill for architectural boundaries, characterization testing, legacy seams (`Sprout`/`Wrap`/`Override`), and defensive error semantics.
- **Announce at Start**: State clearly: *"I am using the diagnosing-bugs skill to systematically investigate and resolve this issue."*

```
┌──────────────────────────────────────────────────────────────────────────┐
│                   SYSTEMATIC BUG DIAGNOSIS WORKFLOW                      │
└──────────────────────────────────────────────────────────────────────────┘

  PHASE 1: BUILD FEEDBACK LOOP  ──► Tight, automated red-capable command.
            │
  PHASE 2: REPRODUCE & MINIMIZE ──► Load-bearing repro & backward data tracing.
            │
  PHASE 3: HYPOTHESIZE (3–5)    ──► Ranked, falsifiable predictions.
            │
  PHASE 4: TARGETED INSTRUMENT  ──► Tagged probes `[DEBUG-XXXX]` & REPL.
            │
  PHASE 5: FIX & DEFEND IN DEPTH──► Seam test, root-cause fix, 4-layer defense.
            │
  PHASE 6: CLEANUP & AUDIT      ──► Strip debug tags, verify full suite.
```

---

## Redact Sensitive Information

When executing commands, reading logs, capturing traces, or presenting diagnostic evidence:
- **Redact every secret or credential**: replace with `<REDACTED>`.
- Bind test harnesses and scripts to environment variables rather than hardcoding tokens into terminal commands.
- If redacted output obscures critical diagnostic signal, explicitly ask the user for assistance.

---

## Phase 1: Build a Feedback Loop

**The fundamental rule of debugging**: If you have a fast, automated pass/fail signal for the defect, finding the root cause is mechanical. If you lack a tight feedback loop, no amount of staring at code will save you.

Do NOT guess or theorize before building this loop.

### 10 Feedback Loop Archetypes (Ordered by Preference)

1. **Failing automated test** at the nearest natural seam: unit, integration, or end-to-end.
2. **HTTP / curl script** against a running local service or dev server.
3. **CLI command invocation** with fixture inputs, comparing stdout/stderr against expected snapshots.
4. **Headless browser script** (Playwright / Puppeteer) asserting on DOM state, console errors, or network responses.
5. **Trace / Payload replay**: Replaying a saved network request, webhook payload, or event stream in isolation.
6. **Throwaway test harness**: A minimal standalone script spinning up a targeted subsystem or service in isolation.
7. **Property / Fuzz loop**: Running hundreds of randomized inputs to trigger intermittent or numerical edge cases.
8. **Automated bisection harness**: Scripting `git bisect run` between known-good and known-bad revisions.
9. **Differential loop**: Running identical input through two configurations or versions to diff output streams.
10. **Human-in-the-loop (HITL) script**: Last resort. When manual user interaction is unavoidable, drive the human operator via `scripts/hitl-loop.template.sh`.

### Tighten the Feedback Loop

Once constructed, optimize the loop:
- **Speed**: Run in seconds, not minutes (narrow test scope, skip unrelated service boots).
- **Determinism**: Eliminate timing flakes, pin timestamps, seed random number generators, mock external network calls.
- **Sharp Signal**: Assert on the exact broken invariant, not a generic "did not crash" exit code.

### Non-Deterministic & Intermittent Bugs

For flaky or timing-dependent bugs, **raise the reproduction rate**:
- Loop the trigger 50–100 times in a loop.
- Apply concurrent stress or CPU throttling.
- Replace arbitrary sleeps with condition polling (see `condition-based-waiting.md`).

### Phase 1 Completion Gate

Phase 1 is complete ONLY when you have identified **one single command** that:
- [ ] Is **Red-Capable**: Drives the exact code path and fails on the user's exact symptom.
- [ ] Is **Deterministic**: Produces consistent failure across consecutive runs.
- [ ] Is **Fast**: Executes in seconds.
- [ ] Is **Automated**: Runs unattended without manual clicking (unless structured via HITL template).

---

## Phase 2: Reproduce, Minimize & Trace Data Flow

Run the feedback loop, confirm the red state, and isolate the failure context:

### 1. Confirm Symptom Fidelity
Verify that the failure mode matches the user's reported symptom, not an unrelated adjacent error.

### 2. Minimize to Load-Bearing Elements
Shrink the reproduction payload, configuration, and execution path:
- Cut input parameters, mock dependencies, and steps one at a time.
- Re-run the loop after each reduction.
- **Completion criteria**: Every remaining element in the repro is *load-bearing* (removing any single element makes the test pass).

### 3. Multi-Component Boundary Evidence
In distributed or layered architectures (e.g. CLI → API → Domain → DB):
- Instrument each boundary layer to log what enters and exits.
- Run once to locate the exact layer boundary where valid state becomes corrupt.

### 4. Backward Call Chain Tracing
When errors surface deep in the stack, follow the technique in `root-cause-tracing.md`:
- Trace backward from the symptom point through each caller frame.
- Identify where the corrupt parameter or invalid assumption originated.
- Fix at the root source, not at the deep symptom point.

---

## Phase 3: Form Ranked Hypotheses

Generate **3 to 5 distinct, ranked hypotheses** before modifying any code. Avoid premature anchoring on the first plausible explanation.

### Falsifiable Hypothesis Structure
Every hypothesis must make an explicit, falsifiable prediction:

> *"If **[Root Cause X]** is the cause, then **[Making Minimal Change Y]** will eliminate the failure, while **[Changing Variable Z]** will exacerbate it."*

### Hypothesis Guidelines
- Compare the broken code against similar working patterns elsewhere in the codebase.
- Check recent commits (`git log -p`, `git diff`) and dependency updates.
- Share the ranked list with the user when appropriate to leverage domain knowledge.

---

## Phase 4: Targeted Instrumentation & Probing

Test hypotheses systematically by changing **one variable at a time**:

1. **Inspection Tools**:
   - Use interactive debuggers or REPLs where available.
   - Insert targeted log probes at boundaries that distinguish competing hypotheses.
2. **Tagged Logging Discipline**:
   - Prefix every temporary log probe with a unique identifier: `[DEBUG-XXXX]` (e.g. `[DEBUG-4a8f]`).
   - Tagged logs enable 100% clean removal via a single `git grep` in Phase 6.
3. **Performance Regressions & Explain the Number**:
   - Never debug performance issues with speculative print statements.
   - Establish an explicit baseline benchmark, profile CPU/memory allocations, inspect database query plans (`EXPLAIN ANALYZE`), and bisect revisions.
   - **Explain the Number ('Why Not Double?')**: Before trusting, reporting, or acting on any measured speedup, throughput, or latency metric:
     - *Name the Limiter*: Explicitly name the resource or code path that bounds the result (CPU core execution, lock contention, memory bandwidth, disk I/O, network RTT, or load generator limits). Derive it from a profile or OS counters taken during the run, mapped back to source lines. If you cannot explain why the number is not twice as good, you do not know what you measured.
     - *Rule Out Non-Work Artifacts*: Systematically rule out cached data, skipped iterations, compiler dead-code elimination, noise, or benchmark harness overhead.
     - *Record Distribution*: Always document the run count, variance/spread (p50/p95/p99), and the named limiter alongside the reported number.

---

## Phase 5: Implement Fix, Defense-in-Depth & Regression Safety

### 1. Regression Test Mandate
Turn the minimized repro from Phase 2 into a permanent automated regression test at the correct architectural seam before applying the fix.
- If modifying legacy code without tests, locate a seam (`Sprout Method`, `Wrap Method`, `Subclass and Override`) per the `software-engineering` skill.

### 2. Single Surgical Root-Cause Fix
- Address the verified root trigger directly.
- Avoid bundling refactorings, drive-by formatting, or unrelated improvements into the fix.

### 3. Defense-in-Depth Verification
Apply the 4-layer validation strategy detailed in `defense-in-depth.md`:
- **Layer 1 (Entry Boundary)**: Reject invalid inputs at API/CLI gateways.
- **Layer 2 (Domain Invariants)**: Enforce structural preconditions in domain services/entities.
- **Layer 3 (Environment Guards)**: Restrict hazardous operations outside designated contexts (e.g. test temp directories).
- **Layer 4 (Telemetry)**: Record structured forensics when fallbacks or edge cases fire.

### 4. Attack the Premise & The 3-Fix Escalation Rule
- **Attack the Premise (2-Fix Gate)**: When two successive fixes sharing the same underlying premise fail the verification gate, **suspect the premise, not the fixes**.
  1. *Write the Premise Down*: Explicitly state the single unspoken assumption or belief that both failed fixes took for granted.
  2. *Test the Premise Directly*: Devise a minimal observation or probe that yields a different outcome if the premise is false. Stop: do NOT author a third fix until the premise has been tested against runtime evidence.
  3. *Eliminate the Condition*: If the premise is falsified, address the root condition rather than authoring compensatory cleanup code or redundant guards.
- **The 3-Fix Escalation Rule**:
  - If ≥ 3 fixes fail or each fix reveals new coupling/breakages: **STOP IMMEDIATELY**.
  - 3+ failed fixes indicates an architectural design flaw or invalid system assumption, not a simple localized defect. Escalate to the user to deliberate architectural refactoring vs. patching symptoms.

---

## Phase 6: Cleanup & Documentation Audit

Before declaring the defect resolved:

- [ ] **Original Feedback Loop Passes**: The Phase 1 feedback loop runs green against the full, un-minimized scenario.
- [ ] **Regression Suite Passes**: The newly authored regression test passes cleanly.
- [ ] **Full Test Suite Passes**: No regressions across the broader repository test suite.
- [ ] **All Debug Probes Removed**: Search for temporary tags (`git grep '\[DEBUG-'`) and confirm zero matches.
- [ ] **Throwaway Scripts Cleaned Up**: Standalone test harnesses or bisection scripts removed or relocated.
- [ ] **Flaky Timeouts Replaced**: Any arbitrary sleeps replaced with condition polling (see `condition-based-waiting.md`).
- [ ] **Root Cause Documented**: Clearly explain the verified root cause, the mechanism of failure, and the fix in the commit message or PR summary.

---

## Red Flags & Rationalization Traps

| Rationalization | Reality & Required Action |
| :--- | :--- |
| *"The bug seems simple; I don't need a formal feedback loop."* | Simple bugs have root causes too. Rushing without a loop leads to thrashing. |
| *"I'll apply a quick fix now and investigate root cause later."* | Quick patches mask root causes and create fragile edge cases. Follow Phase 1. |
| *"I'll write the regression test after confirming the fix works."* | Tests written after code are biased by the implementation and often test the wrong seam. |
| *"Let's change several things at once to see if it starts working."* | Changing multiple variables obscures causation and introduces hidden bugs. Change one variable at a time. |
| *"One more quick attempt..." (after 2+ failed fixes)* | 3+ failed fixes is an architectural signal. Stop and question fundamentals. |

---

## Companion Tools & Guides

- **`root-cause-tracing.md`**: Guide for tracing bugs backward through deep call stacks.
- **`defense-in-depth.md`**: 4-layer validation model for making defects structurally impossible.
- **`condition-based-waiting.md`**: Principles for deterministic async test waiting without arbitrary sleeps.
- **`scripts/find-polluter.sh`**: Bisection script to locate tests that pollute global/shared state.
- **`scripts/hitl-loop.template.sh`**: Structured human-in-the-loop bash runner for manual UI/auth testing.
- **`examples/condition-based-waiting-example.ts`**: Reference TypeScript helpers for condition polling.
