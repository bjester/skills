---
name: analyzing-agent-sessions
description: "Forensic root-cause analyzer for Antigravity coding agent sessions and brain artifacts. Classifies rework shapes, scope deltas, prompt sufficiency, and root causes across agent errors, repo fragility, and specification ambiguity."
license: MIT - https://github.com/bjester/skills/blob/main/LICENSE
user-invocable: true
compatibility: an environment with access to Antigravity brain session artifacts
allowed-tools:
  - read_file
  - write_file
  - run_command
  - grep
  - find_by_name
metadata:
  author: Blaine Jester
  version: "1.0"
---

# Analyzing Agent Sessions: Forensic Root-Cause Analysis for Coding Agents

Purpose: Conduct post-mortem forensic analysis of AI coding agent sessions, brain artifacts, and transcripts to uncover why sessions churned or drifted, classifying rework shapes, prompt sufficiency deficits, and repository friction hotspots.

```
┌────────────────────────────────────────────────────────────────────────┐
│                   AGENT SESSION FORENSIC WORKFLOW                      │
└────────────────────────────────────────────────────────────────────────┘

  1. DISCOVERY & INDEX  ──► Inventory brain artifacts, transcripts, & metadata
             │
             ▼
  2. CLASSIFY INTENT    ──► Determine session intent (DELIVERY, DEBUG, REFACTOR, etc.)
             │
             ▼
  3. REWORK & SCOPE     ──► Trace artifact version churn (.resolved.N) & scope deltas
             │
             ▼
  4. ROOT CAUSE AUDIT   ──► Classify primary root causes (SPEC, REPO, AGENT, VERIFY)
             │
             ▼
  5. HOTSPOT REPORT     ──► Cluster friction across files & output systemic improvements
```

---

## Core Philosophy: Beyond Superficial Blame

When an AI coding agent session drifts, takes too many turns, or fails to complete, diagnosing the breakdown requires looking beyond surface errors. Sessions churn for three distinct reasons:

1. **Specification Ambiguity**: The initial prompt lacked acceptance criteria, non-goals, or file boundaries, forcing the agent to guess.
2. **Repository Fragility**: Hidden architectural coupling, brittle or flaky test harnesses, undeclared environment variables, or missing build targets caused legitimate changes to fail unexpectedly.
3. **Agent Architectural Error**: The agent hallucinated symbols, selected wrong files, fell into proxy verification loops, or drifted into unrequested cleanup.

Forensic session analysis identifies the true root causes and produces evidence-backed recommendations to eliminate repository friction and optimize future workflows.

---

## Execution Phases

### Phase 1: Artifact Discovery and Session Indexing

1. **Locate Brain Directory**:
   Inspect session artifacts located in `<appDataDir>/brain/<conversation-id>/` (or `~/.gemini/antigravity-cli/brain/<conversation-id>/`).
2. **Inventory Core Artifacts**:
   - `task.md`: Active task checklists and progress states.
   - `implementation_plan.md`: Proposed and updated implementation plans.
   - `walkthrough.md`: Verification summaries and completion reports.
   - `transcript.jsonl` (and `transcript_full.jsonl`): Chronological log of user prompts, model reasoning, and tool calls.
   - `*.metadata.json`: Artifact titles, creation timestamps, and user-facing flags.
3. **Track Snapshot Versions**:
   Identify resolved artifact snapshots (`task.md.resolved.0 ... N`, `implementation_plan.md.resolved.0 ... N`).
   > [!NOTE]
   > Snapshot counts (`.resolved.N`) indicate replanning frequency and iteration signals, not automatic failure. An agent adapting to legitimate discoveries will generate resolved versions naturally.

---

### Phase 2: Intent Classification & Prompt Sufficiency

1. **Classify Primary Session Intent**:
   Determine the underlying mission before judging session efficiency:
   - `DELIVERY`: Narrow, well-defined feature or bugfix.
   - `DEBUGGING`: Investigating an unknown error or regression.
   - `REFACTOR`: Internal structural reorganization without changing public contracts.
   - `RESEARCH`: Evaluating libraries, tools, or architectural trade-offs.
   - `EXPLORATION`: Open-ended prototyping, spikes, or creative design.
   - `AUDIT_ANALYSIS`: Security, accessibility, or code quality assessment.

   *Intent Calibration*: Never penalize an `EXPLORATION` or `RESEARCH` session for multiple plan revisions. Conversely, a `DELIVERY` session with repeated replanning signals friction.

2. **Evaluate Prompt Sufficiency**:
   Score the opening user prompt across six dimensions (0 = Absent, 1 = Partial, 2 = Explicit):
   - **Clarity**: Are goals and success states explicitly stated?
   - **Boundedness**: Are explicit non-goals and scope limits provided?
   - **Testability**: Are concrete verification commands or criteria defined?
   - **Architectural Specificity**: Are target directories, files, or symbols identified?
   - **Constraint Awareness**: Are existing invariants, backwards-compatibility requirements, or performance bounds stated?
   - **Dependency Awareness**: Are external services, environment variables, or credentials identified?

   *Sufficiency Bands*:
   - High (9–12): Highly bounded, testable prompt.
   - Medium (5–8): Understandable goal, but missing boundaries or verification criteria.
   - Low (0–4): Vague or unconstrained instruction ("fix this", "make it better").

---

### Phase 3: Scope Delta and Rework Shape Analysis

1. **Classify Scope Delta**:
   Distinguish where new tasks originated during execution:
   - **Human-Added Scope**: The user injected new requests or expanded the task mid-session.
   - **Necessary Discovered Scope**: Technical prerequisites uncovered during investigation (e.g., fixing an unmigrated database schema required for the feature).
   - **Agent-Introduced Scope**: The agent volunteered unrequested refactors, unnecessary renamings, or speculative enhancements.

2. **Determine Rework Shape**:
   Identify the geometric progression of the session:
   - **Clean Execution**: Single plan revision, steady task progression, clean walkthrough.
   - **Early Replan then Stable Finish**: Initial plan adjusted after discovery, followed by smooth execution.
   - **Progressive Scope Expansion**: Tasks continually added across turns without a clear ceiling.
   - **Reopen/Reclose Churn**: Tasks repeatedly marked done, reopened due to failures, and toggled back and forth.
   - **Late-Stage Verification Churn**: Implementation finished early, but the session looped on failing tests, linters, or type-checks.
   - **Abandoned Mid-Flight**: Session ended abruptly with unfinished tasks and no walkthrough.

---

### Phase 4: Root Cause Audit & Evidentiary Standard

Assign the primary root cause for any session that exhibited churn, replanning loops, or abandonment:

| Root Cause Category | Diagnostic Pattern |
|:---|:---|
| `SPEC_AMBIGUITY` | The opening ask lacked boundaries, target files, or verification criteria, leading to agent guessing. |
| `HUMAN_SCOPE_CHANGE` | Scope expanded because the user altered goals or redirected the agent mid-session. |
| `REPO_FRAGILITY` | Brittle test harnesses, hidden coupling, undocumented dependencies, or environment breaks forced excessive churn. |
| `AGENT_ARCHITECTURAL_ERROR` | Agent selected wrong files, hallucinated non-existent APIs, or used fundamentally flawed designs. |
| `VERIFICATION_CHURN` | Code changes were correct, but test suites or verification commands produced false negatives or proxy failures. |
| `LEGITIMATE_TASK_COMPLEXITY` | Revisions were naturally expected given the inherent algorithmic or architectural difficulty of the task. |

#### Evidentiary Precedence
Support every root-cause assignment with verified evidence:
1. Direct artifact text and diffs (`task.md`, `implementation_plan.md`).
2. Exact transcript events and tool execution outputs (`transcript.jsonl`).
3. Timestamps and file modification metadata.
4. Qualitative inference (lowest precedence; must be labeled as inference).

---

### Phase 5: Repository Hotspots & Systemic Recommendations

1. **Cluster Subsystem Friction**:
   Group struggle across sessions by directory, file, or component. Identify whether churn clusters around specific files (e.g., `tests/fixtures/`, legacy service modules).
2. **Calculate Session Severity Score (0–100)**:
   - Completion Failure (0–25)
   - Replanning Intensity (0–15)
   - Scope Instability (0–15)
   - Rework Shape Severity (0–15)
   - Prompt Sufficiency Deficit (0–10)
   - Root Cause Friction Impact (0–10)
   - Hotspot Recurrence (0–10)

3. **Deliver Actionable Systemic Recommendations**:
   Format findings into three distinct intervention categories:
   - **Prompting Improvements**: Specific constraints, non-goals, or acceptance criteria the user should include in future prompts.
   - **Repository Health**: Code health interventions (e.g., decoupling tangled modules, stabilizing flaky tests, adding a deterministic `verify-*` script).
   - **Agent Workflow Guardrails**: Specific skills to invoke for similar tasks (e.g., running `analyzing-blast-radius` before modifying legacy files, or `test-driven-development` when implementing complex logic).
