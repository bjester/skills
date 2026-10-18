# Changelog & Provenance: diagnosing-bugs

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-10-18] - Attack the Premise & Explain the Number from pstack (v0.15.26)

- **Upstream Repository**: `git@github.com:cursor/plugins.git`
- **Upstream Revision**: `0b8e952052d482ee6de06deebf14d590d77b1b34` (Release: `chore(pstack): bump to 0.15.26`), committed on 2026-10-18
- **Upstream Source Paths**:
  - `sources/cursor-plugins/pstack/skills/principle-attack-the-premise/`
  - `sources/cursor-plugins/pstack/skills/principle-explain-the-number/`

### 1. Base State (A)
- Provided a rigorous 6-phase hypothesis-driven debugging loop, tight automated feedback loop archetypes, load-bearing minimization, tagged logging probes (`[DEBUG-XXXX]`), 4-layer defense-in-depth, and a 3-fix escalation rule.
- Did not specify a mechanism to detect and break premise fixation when multiple fix attempts fail before reaching the 3-fix escalation stop.
- Lacked explicit epistemic criteria for verifying performance regression benchmarks or ruling out non-work artifacts.

### 2. Curated Changes Applied (A -> B)
- **Phase 4 (Targeted Instrumentation & Probing)**:
  - Injected **Explain the Number ('Why Not Double?')**: Before trusting, reporting, or acting on any measured speedup, throughput, or latency metric:
    - *Name the Limiter*: Explicitly identify the resource or code path bounding the result (CPU core execution, lock contention, memory bandwidth, disk I/O, network RTT, or load generator limits) derived from profiling or OS counters mapped back to source lines.
    - *Rule Out Non-Work Artifacts*: Systematically verify that the measurement did not reflect cached data, skipped iterations, compiler dead-code elimination, noise, or benchmark harness overhead.
    - *Record Distribution*: Require documenting run count, variance/spread (p50/p95/p99), and the named limiter alongside the reported number.
- **Phase 5 (Implement Fix, Defense-in-Depth & Regression Safety)**:
  - Injected **Attack the Premise (2-Fix Gate)** ahead of the 3-fix escalation rule:
    - When two successive fixes sharing the same underlying premise fail the verification gate, suspect the premise itself rather than the fixes.
    - *Step 1*: Explicitly write down the single unspoken assumption or belief shared by both failed fixes.
    - *Step 2*: Devise a minimal observation or probe that yields a different outcome if the premise is false. Stop: do NOT author a third fix until the premise has been tested against runtime evidence.
    - *Step 3*: If the premise is falsified, eliminate the root condition rather than authoring compensatory cleanup code or redundant guards.

### 3. Resulting State (B)
- A battle-tested defect diagnosis workflow that actively prevents premise fixation and thrashing, and enforces scientific rigor when investigating performance regressions and speedups.

### 4. Re-sync / Update Recipe
When upstream `sources/cursor-plugins` updates `pstack`:
1. Fetch latest changes in upstream:
   ```bash
   git -C sources/cursor-plugins pull
   ```
2. Diff upstream principle skills against base commit `0b8e952`:
   ```bash
   git -C sources/cursor-plugins diff 0b8e952..HEAD -- pstack/skills/principle-attack-the-premise/ pstack/skills/principle-explain-the-number/
   ```
3. Evaluate any updates or refinements to premise-testing logic or performance measurement rubrics (e.g. `benchmark-checklist`).
4. Integrate improvements into `skills/diagnosing-bugs/SKILL.md` while preserving the 6-phase structure and defense-in-depth companions.
5. Run `make build` to verify packaging.
6. Record the new upstream commit hash, date, and changes in this changelog.
