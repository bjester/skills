---
name: generating-verification-harnesses
description: "Inspects any software project's architecture, surfaces, and scripts to generate an autonomous, project-local verification driver (verify-<app>). Bootstraps headless test harnesses (Playwright/CDP, PTY/tmux, curl) with Launch, Doctor, Drive, and living Feature Maps. Use when an app lacks a scripted, end-to-end verification pathway for agents."
license: MIT - https://github.com/bjester/skills/blob/main/LICENSE
user-invocable: true
compatibility: any software development project with runnable entrypoints
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

# Generating Verification Harnesses: Bootstrapping Autonomous Project Drivers

Purpose: Inspect an unfamiliar codebase and bootstrap a permanent, project-local verification skill (`verify-<app>`) that enables autonomous agents and human developers to launch, drive, inspect, and verify the host application headlessly without manual intervention.

```
┌────────────────────────────────────────────────────────────────────────┐
│             VERIFICATION HARNESS GENERATION WORKFLOW                   │
└────────────────────────────────────────────────────────────────────────┘

  1. INTERVIEW THE REPO   ──► Deduce surface, boot command, harness, isolation
             │
             ▼
  2. COMPOSE DRIVER SKILL ──► Author Launch, Doctor, Drive, Evidence, Cleanup
             │
             ▼
  3. SEED FEATURE MAP     ──► Map primary user journeys and observable outcomes
             │
             ▼
  4. LIVE PROOF GATE      ──► Execute generated harness end-to-end before handoff
```

---

## Core Philosophy: The Verification Bottleneck

Autonomous agents fail or hallucinate when they lack a deterministic way to interact with the software they modify. If verification requires a human to click in a browser or paste sample input into a terminal, the human operator becomes an agonizing bottleneck.

> [!IMPORTANT]
> Write the generated verification driver for the *next* agent, not for a human. It will be read cold, mid-task, by an agent that has never seen the application before. It must contain concrete commands and selectors—zero placeholders.

---

## Phase 1: Interview the Repository, Not the User

Discover the application's operating mechanics directly from the codebase. Ask the user only what cannot be observed from the files:

1. **Surface**: What does a user actually touch?
   - Web frontend (browser / DOM)
   - CLI / TUI tool (terminal streams / PTY)
   - Backend API / Daemon (HTTP / gRPC / IPC)
   - Desktop application (Electron / native window)
   - Mobile application (simulator / emulator)
2. **Launch Mechanics**: How does the local environment start?
   - Inspect `package.json`, `Makefile`, `docker-compose.yml`, or `Procfile`.
   - Identify local ports, mandatory environment variables, seed data scripts, and database migrations.
   - *Requirement*: Launch must reach a fully usable state from an empty data directory.
3. **Driving Mechanism**: How can an agent interact with it programmatically?
   - *Web/Electron*: Playwright, Puppeteer, or Chrome DevTools Protocol (CDP).
   - *CLI/TUI*: `tmux`, `expect`, `pty`, or child process pipes.
   - *Services*: `curl`, HTTP client scripts, or gRPC payloads.
4. **Evidence Capture**: What tangible artifacts prove behavior?
   - Screenshots, terminal session recordings, response JSON, database rows, structured logs, and exit codes.
5. **Instance Isolation**: Can multiple test instances run concurrently?
   - Check port bindings and data directories. If the app cannot run parallel instances safely, mandate single-instance exclusivity in the driver skill.

---

## Phase 2: Author the Project Driver Skill

Create the repository-local skill file (e.g. `.agents/skills/verify-<app>/SKILL.md` or `.gemini/skills/verify-<app>/SKILL.md`):

```markdown
---
name: verify-<app>
description: "Drives <app> end-to-end to verify UI, CLI, and API behavior."
---

# Verify <App Name>

## 1. Launch
- **Start Command**: `[exact command, e.g. npm run dev or make run]`
- **Readiness Probe**: `[specific log output, e.g. "Server listening on port 3000"]`
- **Teardown**: `[exact termination command, e.g. kill by PID]`

## 2. Doctor (Pre-flight Health Check)
A single read-only probe answering: *"Is this instance currently healthy and worth driving?"*
- Checks: Process is up, port is listening, database connection is valid, auth tokens are initialized.

## 3. Drive (Interaction Harness)
- Harness recipes using stable identifiers (ARIA labels, data-testid, exact CLI subcommands).
- Avoid fragile coordinates or timing sleeps; use condition polling.

## 4. Evidence (Proof Standards)
- What artifacts to capture and where to save them (e.g. `artifacts/verification/`).
- Standard: Must verify observable side effects (persisted records, network payloads) in addition to UI state.

## 5. Cleanup
- Gracefully shut down spawned background processes.
- Remove scratch database files or temporary configs.
- **Rule**: Never delete the captured proof artifacts during cleanup!
```

---

## Phase 3: Seed the Living Feature Map

Create a `features/` directory beside the driver skill with a `README.md` index and one file per primary user journey (seed the top 3–5 core features):

```markdown
# Feature: [Feature Name]

## 1. User Journey Overview
What the feature delivers from the end-user's point of view.

## 2. How to Reach It
The exact navigation path, route, or CLI subcommand.

## 3. Driving with the Harness
The executable commands or headless scripts to exercise the happy path and primary edge case.

## 4. Observable End State (What Proves It Works)
The tangible facts that prove success: database row created, status 200 returned, DOM element visible.

## 5. Gotchas & Edge Cases
Environmental quirks, mandatory preconditions, or rate limits.
```

---

## Phase 4: The Mandatory Live Proof Gate

Before declaring the verification harness complete:

- [ ] **Run End-to-End**: Execute the generated driver skill yourself once:
  1. Run the Launch command.
  2. Run the Doctor check to confirm readiness.
  3. Drive **one** mapped feature to completion.
  4. Capture proof artifacts (screenshot, log, or exit code).
  5. Run Cleanup.
- [ ] **Verify Artifact Survival**: Confirm that proof artifacts still exist on disk after cleanup runs.
- [ ] **Zero Placeholders**: Confirm no `<TODO>` or placeholder strings remain in the driver or feature files.

> [!CAUTION]
> A verification harness that was never run is merely a speculative draft. It is not complete until proven against the running app.
