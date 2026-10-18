---
name: investigating-code-lineage
description: "Investigates historical intent, design motivation, and architectural lineage behind unintuitive, legacy, or defensive code. Dynamically discovers evidence across source control, issue trackers, documentation, and telemetry with strict epistemic confidence. Use before modifying, refactoring, or deleting legacy code."
license: MIT - https://github.com/bjester/skills/blob/main/LICENSE
user-invocable: true
compatibility: a software project with git version control and optional MCP tools
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

# Investigating Code Lineage: Historical Archaeology & Intent Discovery

Purpose: Reconstruct the authentic business, architectural, and operational forces that produced existing code before modifying, refactoring, or deleting it, preventing the accidental revival of historical bugs.

```
┌────────────────────────────────────────────────────────────────────────┐
│                   CODE LINEAGE INVESTIGATION HARNESS                   │
└────────────────────────────────────────────────────────────────────────┘

  1. CODE ANCHORING       ──► Blame, patch history, PR extraction (`gh pr view`)
             │
             ▼
  2. SOURCE DISCOVERY     ──► Discover available tools across 7 evidence categories
             │
             ▼
  3. PARALLEL EVIDENCE    ──► Query git, issues, docs, chat, traces, telemetry
             │
             ▼
  4. EPISTEMIC SYNTHESIS  ──► Classify findings into Facts, Inferences, and Guesses
             │
             ▼
  5. CONSTRAINTS MATRIX   ──► Generate Preserve / Change / Avoid / Risk boundaries
```

---

## Core Philosophy: Respect the Defenses

When engineers or coding agents encounter code that looks strange, defensive, or overly complex (e.g. nested null checks, obscure timeouts, specific retry thresholds, fallback handlers), the naive impulse is to clean it up or remove it. 

> [!CAUTION]
> Defensive code is almost always the scar tissue of a painful past production incident. Deleting it without understanding its lineage guarantees you will resurrect the exact production failure it was authored to prevent.

Before altering non-trivial legacy logic, perform **codebase archaeology** to establish:
1. *What incident, race condition, or vendor quirk forced this specific shape?*
2. *Is that forcing function still alive in the current production environment?*

---

## The 7 Evidence Categories

Dynamically inspect the environment and available MCP tools. Query across these 7 evidence categories:

| Category | Primary Sources & Tools | Archetype of "Why" Uncovered |
|---|---|---|
| **1. Source Control** | `git blame`, `git log -p`, `gh pr view`, code comments | Implementation-time rationale captured during code review. |
| **2. Issue Trackers** | Linear, Jira, GitHub Issues, Plane | The product, customer, or business forcing function. |
| **3. Long-Form Docs** | Notion, Confluence, Google Docs, RFC directories | Architecture Design Records (ADRs) and pre-implementation trade-offs. |
| **4. Team Communications** | Slack, Discord, PR review threads | Real-time emergency deliberation that never made it into official docs. |
| **5. Observability** | Datadog, Grafana, Honeycomb, Prometheus | Infrastructure reality (latency spikes, thread pool exhaustion, 429s). |
| **6. Error Tracking** | Sentry, Bugsnag, Rollbar | The exact stack traces and unhandled exceptions that forced defensive logic. |
| **7. Analytics Warehouses**| BigQuery, Snowflake, ClickHouse, postmortems | Experiment results, data migrations, or postmortem analysis documents. |

---

## Execution Phases

### Phase 1: Establish the Code Anchor
Before querying external sources, build an unambiguous anchor from git history:
1. Identify the exact target file and line ranges.
2. Run `git blame -L <start>,<end> <file>` to identify the commits that last touched the logic.
3. Trace full history across renames:
   ```bash
   git log --follow -p -L <start>,<end>:<file>
   ```
4. Extract PR numbers from merge commit subjects (`(#1234)`) and commit messages.
5. If GitHub CLI (`gh`) is available, fetch the full PR body and review discussion:
   ```bash
   gh pr view <pr-number> --json title,body,author,createdAt,mergedAt,comments,reviews
   ```

### Phase 2: Tool & Environment Discovery
Inspect available environment tools and MCP servers to identify which evidence categories can be queried:
- Source control is always available via `git` and `gh`.
- Check for connected MCP tools (issue trackers, document search, error logs).
- Note any unavailable categories as documented search gaps rather than skipping silently.

### Phase 3: Targeted Parallel Investigation
Query matching sources focusing on the identified commit dates, PR numbers, author names, and key domain symbols:
- **Defensive Logic Heuristic**: If the target code contains null checks, clamps, retries, or error catchers, specifically search for past incident reports, postmortems, or customer escalation tickets within $\pm 2$ weeks of the commit date.
- **Avoid Recency Bias**: The most recent commit often only touched formatting or imported a new helper. Follow the trail back to the commit that originally introduced the behavior.

### Phase 4: Epistemic Confidence Separation
Synthesize evidence using strict epistemic standards:
- **Verified Facts**: Direct quotes from PR discussions, explicit postmortems, git commit messages, or verified tests. Must carry a direct pointer (`file:line`, PR link, commit SHA).
- **Reasonable Inferences**: Deductions supported by circumstantial evidence (e.g., commit coincided with a major database migration). Must be labeled explicitly as `[Inferred]`.
- **Open Questions & Guesses**: Unverified hypotheses where the paper trail is silent. Never present an inference or guess as an established fact.

---

## Output Report Structure

Deliver the lineage investigation in this structured format:

```markdown
# Code Lineage Investigation: [Symbol / Module / Logic]

## 1. Target Code & Historic Anchor
- **Location**: `path/to/file.ts#L45-L68`
- **Origin Commit**: `3a9f1c2` (Authored by @developer on YYYY-MM-DD)
- **Origin PR / Ticket**: PR #456 ("Fix race condition during payment webhook retry")

## 2. Verified Historical Rationale (Facts)
[Direct facts, citations from PR bodies, issue descriptions, or commit messages explaining why this code was introduced.]

## 3. Reasonable Inferences
- **[Inferred]**: [Plausible contextual conclusions drawn from surrounding commits or architectural shifts.]

## 4. What Remains Unknown / Gaps
- [Evidence categories that were unavailable or returned null results.]

## 5. Decision & Modification Guardrails
If planning to refactor or touch this code, adhere to these constraints:
- **PRESERVE**: [Invariants, fallback behaviors, or guarantees that must remain intact.]
- **CHANGE**: [Accidental complexity or obsolete workarounds that are safe to update.]
- **AVOID**: [Approaches that were tried in the past and failed.]
- **RISK**: [The specific failure mode that will recur if this code is removed without replacement.]
```
