---
name: verifying-prs-in-browser
description: |
  Conditional live browser and devserver verification for pull requests and local
  UI branches using bundled scripts/drive-browser.py (standalone Playwright
  persistent sessions and axe-core WCAG AA audits) or Chrome DevTools MCP. Plans
  scenarios from diffs and linked issues, inspects screenshots multimodally,
  probes signed-out deep links, console errors, and network/consent payloads,
  attributes defects (Attributable to PR vs. Pre-existing), tears down sessions
  cleanly, and exits gracefully without blocking code review when unavailable.
license: MIT - https://github.com/bjester/skills/blob/main/LICENSE
user-invocable: true
compatibility: Local development environments with app runtime and uv/Playwright or Chrome DevTools MCP
allowed-tools:
  - read_file
  - write_file
  - run_command
  - manage_task
  - grep
  - find_by_name
  - list_pages
  - new_page
  - select_page
  - close_page
  - navigate_page
  - wait_for
  - take_snapshot
  - take_screenshot
  - click
  - fill
  - evaluate_script
  - list_console_messages
  - list_network_requests
metadata:
  author: Blaine Jester
  version: "1.0"
---

# Verifying Pull Requests in Browser

Purpose: Verify frontend, routing, accessibility, and client-side telemetry behavior in an isolated browser session when warranted, while exiting cleanly without blocking static code review whenever browser testing is unnecessary or unavailable.

## Outcome Workflow

```
                     ┌────────────────────────────────────────┐
                     │       1. APPLICABILITY & TRUST GATE    │
                     └───────────────────┬────────────────────┘
                                         │
            ┌────────────────────────────┼────────────────────────────┐
            ▼ (No UI/browser surface)    ▼ (Untrusted fork scripts)   ▼ (UI/router/SDK/manual QA)
    [ NOT_NEEDED ]             [ SKIPPED_UNTRUSTED ]       ┌──────────────────────────┐
 (Instant zero-cost exit)     (Report & continue review)   │ 2. SCENARIO PLAN, SERVER │
                                                           │    & ISOLATED TRANSPORT  │
                                                           └────────────┬─────────────┘
                                                                        │
                                                  ┌─────────────────────┴─────────────────────┐
                                                  ▼ (Env/DB/secrets/sandbox/browser blocked)  ▼ (Ready)
                                       [ SKIPPED_UNAVAILABLE ]                     ┌──────────────────────────┐
                                    (Teardown & continue review)                   │ 3. TARGETED UI PROBES    │
                                                                                   │  • Reviewer guidance/ACs │
                                                                                   │  • Signed-out deep link  │
                                                                                   │  • Multimodal + a11y AA  │
                                                                                   │  • Console attribution   │
                                                                                   │  • Network/consent calls │
                                                                                   └────────────┬─────────────┘
                                                                                                ▼
                                                                                   ┌──────────────────────────┐
                                                                                   │ 4. MANDATORY TEARDOWN    │
                                                                                   │    [ PASSED | FAILED ]   │
                                                                                   └──────────────────────────┘
```

---

## Phase 1: Applicability, Untrusted-Code Gate & Scenario Plan

1. **Fast Applicability Check (`NOT_NEEDED` vs. `RUN`)**:
   - Browser verification is **not** needed on every PR. Inspect `git diff --name-only` and the PR description first:
   - **Return `NOT_NEEDED` immediately** (launching zero servers or browsers) when the diff modifies only backend, SQL, CLI, library, CI, or documentation files with no browser-observable surface and no manual UI steps in `Reviewer guidance`.
   - **Proceed (`RUN`)** when the diff touches templates/components (`.vue`, `.jsx`, `.tsx`, `.svelte`, `.html`), styles (`.css`, `.scss`, `.less`), client routers (`beforeEach`, `afterEach`), root session/auth wrappers (`RootVue`), browser SDKs/analytics/consent hooks, or explicit manual browser steps in `Reviewer guidance`.

2. **Untrusted Fork Safety Gate (`SKIPPED_UNTRUSTED`)**:
   - > [!CAUTION]
     > On external fork PRs, inspect diffs to `package.json`, `Makefile`, bundler configs, and `.env*` files before running any install, build, or server command. If the PR introduces untrusted lifecycle hooks (`preinstall`, `postinstall`), arbitrary shell commands, or secret exfiltration, **do not execute them**. Return `SKIPPED_UNTRUSTED` immediately so static review continues safely.

3. **Diff-to-Route Scenario Plan**:
   - Before launching a browser, trace modified components, views, and stylesheets to their route URLs (`grep` route tables and parent views).
   - Write a short, numbered scenario list combining:
     - Explicit steps in the PR's `Reviewer guidance`.
     - Linked issue acceptance criteria and any attached design mockups or checklists.
     - Touched routes, interactive states (empty, error, loading, modal/dropdown), and signed-out redirects.

---

## Phase 2: Devserver Readiness, Standalone Profile Isolation & Non-Blocking Fallback

1. **Devserver Detection & Safe Launch**:
   - Check for an existing project verification driver (`.agents/skills/verify-*/SKILL.md` or `.gemini/skills/verify-*/SKILL.md`) or `AGENTS.md` startup instructions first and reuse its exact Launch, Readiness, and Teardown commands.
   - Resolve `scripts/drive-browser.py` relative to the directory containing this `SKILL.md` file. Run `uv run --script scripts/drive-browser.py detect-servers` (from this skill's directory, or pass its resolved absolute path) before starting a server so you do not accidentally test a stale server left running on another branch.
   - Detect package managers from lockfiles (`pnpm-lock.yaml`, `yarn.lock`, `package-lock.json`, `uv.lock`) and check `.env.example`, test fixtures, `Makefile`, or `README.md` for local test credentials. Never print live `.env` secrets.
   - Ensure compiled frontend assets are fresh if not served in watch mode, and wait for a concrete readiness log line or HTTP response rather than `networkidle` (HMR WebSockets and SSE keep connections open indefinitely).

2. **Zero Personal-Profile Rule & Transport Selection**:
   - > [!IMPORTANT]
     > **Zero Personal-Profile Rule**: Never pass a user's personal browser profile directory (`~/.config/google-chrome`, `~/.config/chromium`, `~/Library/Application Support/Google/Chrome`) and never navigate or interact with a user's personal daily-driver browser session.
   - **Transport A: Bundled `scripts/drive-browser.py` (Primary Default)**:
     - Invoked via `uv run --script scripts/drive-browser.py` (resolved relative to this `SKILL.md` directory). Automatically installs Playwright's standalone Chromium binary (`~/.cache/ms-playwright/`) on first run and opens a fresh, ephemeral in-memory `browser.new_context()` with zero access to personal cookies, extensions, or saved passwords. *(If a slow network exceeds the 15-second daemon startup window during a first-time Chromium download, run `uv run --with playwright playwright install chromium` once first.)*
     - Core session commands (`export DRIVE_BROWSER_SESSION=pr-<id>` or pass `--session pr-<id>`, resolving `scripts/drive-browser.py` against this skill's directory):
       ```bash
       uv run --script scripts/drive-browser.py start --session pr-123
       uv run --script scripts/drive-browser.py open --session pr-123 "http://localhost:8000/route" --no-wait-for-idle
       uv run --script scripts/drive-browser.py auth --session pr-123 --auth-url "http://localhost:8000/login/" --username admin --password secret
       uv run --script scripts/drive-browser.py click --session pr-123 "text=Save"
       uv run --script scripts/drive-browser.py scroll --session pr-123 --container ".content-wrapper" --by 500
       uv run --script scripts/drive-browser.py resize --session pr-123 --width 412 --height 915
       uv run --script scripts/drive-browser.py screenshot --session pr-123 --output /tmp/pr-123-state.png
       uv run --script scripts/drive-browser.py a11y --session pr-123 --level AA
       uv run --script scripts/drive-browser.py js --session pr-123 "window.location.pathname"
       uv run --script scripts/drive-browser.py stop --session pr-123
       ```
     - Pass only non-sensitive local fixture or dummy credentials to `scripts/drive-browser.py auth` (`--username` and `--password` appear briefly in local process listings). Never pass real user or shared staging passwords.
   - **Transport B: Chrome DevTools MCP (Secondary Option)**:
     - Use when `chrome-devtools-mcp` tools are active and fine-grained outbound request inspection (`list_network_requests`) is needed or `uv`/Playwright cannot run.
     - Always call `list_pages` first to confirm the MCP browser is an isolated automation instance (`about:blank` or `localhost` tabs only). If personal tabs are open, **do not interact with that browser**; switch to Transport A or return `SKIPPED_UNAVAILABLE`.

3. **Non-Blocking Fallback Invariant (`SKIPPED_UNAVAILABLE`)**:
   - > [!NOTE]
     > Keep setup strictly bounded. Do **not** spend review turns provisioning Docker daemons, external databases, unseeded fixtures, missing OAuth/API keys, or debugging sandbox port/browser restrictions, and never treat missing local infrastructure or absent image-upload keys as a PR defect.
   - If the devserver or browser transport cannot run due to environment constraints rather than a bug introduced by the PR, execute Phase 4 teardown immediately and return `SKIPPED_UNAVAILABLE: <one-line reason>` so `reviewing-github-prs` completes static review normally (`COMMENT` + `Verification Status` note).

---

## Phase 3: Five High-Signal Probes & PR Attribution

Run the probes relevant to the PR's changed files:

1. **Probe 1: `Reviewer guidance`, Linked Issue ACs & Design Mockups**:
   - Navigate using compact viewport text snapshots returned by `open`, `click`, `fill`, and `wait` (or `take_snapshot` in MCP).
   - For single-page apps rendering inside scrollable containers (`overflow-y: auto`), scroll the container explicitly (`scroll --container "<selector>" --by 500`).
   - For stateful transitions, animations, or multi-step flows where motion matters, capture video (`start-recording` / `stop-recording`) alongside before/after screenshots.

2. **Probe 2: Signed-Out Deep-Link & Lifecycle Ordering**:
   - Whenever routes, router hooks (`beforeEach`, `afterEach`), or mounted session wrappers (`RootVue`) are modified, open a protected deep link in a clean unauthenticated session *before* calling `auth`.
   - Verify both the login redirect **and** that zero premature API requests or phantom analytics pageviews fired before the redirect completed.

3. **Probe 3: Multimodal Visual, Responsive/RTL & `a11y` Audit**:
   - **Read Every Screenshot Multimodally**: Taking a screenshot without reading it with `read_file` is not verification. Snapshots confirm DOM structure; reading the `.png` confirms visual layout, contrast, clipping, overlapping columns, and alignment against any linked issue mockups.
   - When layout, responsive styles, or directional rules changed, verify narrow viewports (`resize --width 412 --height 915`) and switch to an RTL locale (such as Arabic) to verify icon/layout mirroring.
   - Run `scripts/drive-browser.py a11y --level AA` (axe-core WCAG AA) or inspect `take_snapshot` + `list_console_messages` (`types: ["issue"]`) on every affected route, checking accessible names, heading hierarchy, and keyboard focus management. Note that bundled `scripts/drive-browser.py` fetches `axe-core@latest` and caches `~/.drive-browser/axe-core.min.js` without invalidation, so delete that cached file if local rules appear stale.

4. **Probe 4: Console Diagnostics & PR Attribution Check**:
   - Inspect the drained `console` JSON array returned by every `scripts/drive-browser.py screenshot` call (or `list_console_messages` in MCP). Do not dismiss errors without evidence.
   - Before raising any console error, `a11y` violation, or visual glitch as a PR defect, visit an **unmodified sibling route** to classify attribution:
     - **`Attributable to PR`**: Error stack trace references changed files, violation sits on a new/modified element, or failure occurs only on affected routes. Report as `🚨 Blocker` or `⚠️ Architecture & Design`.
     - **`Pre-existing`**: Identical error or violation reproduces on unmodified routes and unchanged components. Do **not** block the PR; mention briefly as context only if helpful.
     - **`Indeterminate`**: Phrase as `❓ Question` with exact reproduction steps.

5. **Probe 5: Outbound Network, Redaction & Consent Payloads**:
   - When API calls, analytics trackers (`posthog`, GTM), URL redactors (`before_send`), or consent listeners (`Cookiebot`) change, inspect `list_network_requests` (MCP) or evaluate client state (`scripts/drive-browser.py js`) to verify sensitive path/query parameters are redacted and opted-out or absent-SDK states emit zero tracking payloads.

---

## Phase 4: Mandatory Teardown & Structured Verification Report

1. **Deterministic Cleanup (Always Runs on Every Exit Path)**:
   - Stop the browser session (`uv run --script scripts/drive-browser.py stop --session <id>` or `close_page`).
   - Terminate any devserver or watcher spawned during this session by process group (`kill -- -<PGID>` or `manage_task kill`) and confirm the port is released so zero orphan daemons leak across reviews. Keep captured proof screenshots in `/tmp` or scratch if referenced.

2. **Structured Output for `reviewing-github-prs` or Standalone Use**:
   - Report concise Plain English (`writing-technical-docs` compliant, zero em-dashes) with one of five statuses:
     - `PASSED`: List exact routes/scenarios verified, multimodal visual & `a11y` AA check status, and console/network cleanliness.
     - `FAILED`: List each `Attributable to PR` defect with exact reproduction steps, console/network/a11y evidence, and mapped `file:line` pointers.
     - `NOT_NEEDED`: One-line note that no UI, router, client SDK, or manual-QA surface was touched.
     - `SKIPPED_UNAVAILABLE: <reason>`: One-line environmental reason (caller completes static review normally and withholds `APPROVE`).
     - `SKIPPED_UNTRUSTED: <reason>`: One-line untrusted-fork script warning (caller completes static review safely).
