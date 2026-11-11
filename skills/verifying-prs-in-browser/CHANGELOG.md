# Changelog & Provenance: verifying-prs-in-browser

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-11-11] - Initial Curation: Conditional Live Browser PR Verification & Standalone Session Driver

- **Upstream Repository**: `https://github.com/learningequality/le-skills`
- **Upstream Revision**: `9dc3e40713b25f74509e01847cf80e6582421d70`, cloned from `main`
- **Integrated Sources**:
  - `sources/le-skills/skills/driving-a-browser/SKILL.md`
  - `sources/le-skills/scripts/drive-browser.py`
  - `sources/le-skills/skills/github-pr-review/manual-qa.md`

### 1. Base State (A)
- Upstream `driving-a-browser` drove persistent Playwright sessions via an external plugin script (`drive-browser.py` on `PATH`), returning viewport text snapshots on interaction commands, drained console JSON on `screenshot`, 1- and 2-step Vue `auth`, SPA `--container` scrolling, and axe-core `a11y` audits.
- Upstream `github-pr-review` (`Phase 3` and `manual-qa.md`) mandated browser verification on every UI diff and treated missing local devservers, missing Playwright binaries, missing test credentials, or absent `IMGUR_CLIENT_ID` environment variables as blocking PR review findings, while lacking untrusted-fork protections, signed-out router lifecycle probes, and Chrome DevTools MCP support.

### 2. Curated Changes Applied (A -> B)
- **Renamed**: `driving-a-browser` + `manual-qa.md` -> `verifying-prs-in-browser` per repository gerund naming conventions and specialized PR-verification scope.
- **Bundled `scripts/drive-browser.py`**: Vendored `sources/le-skills/scripts/drive-browser.py` byte-identically (`0755`, PEP 723 `uv run --script`) inside `skills/verifying-prs-in-browser/scripts/drive-browser.py` so the skill is self-contained across Claude Code, Codex, Gemini/Antigravity, and Vibe installations.
- **Standardized Frontmatter (`SKILL.md` `v1.0`)**: Applied repository YAML schema including workspace, process, and Chrome DevTools MCP tools in `allowed-tools`.
- **Added Conditional & Non-Blocking Safety Gates (Phases 1-2)**:
  - Fast `NOT_NEEDED` exit when a PR has no frontend, router, client SDK, or manual-QA surface.
  - `SKIPPED_UNTRUSTED` fork protection inspecting `package.json`/build lifecycle scripts before running untrusted code.
  - Explicit **Zero Personal-Profile Rule**: `drive-browser.py` uses Playwright's standalone Chromium (`~/.cache/ms-playwright/`) inside an ephemeral `browser.new_context()` and never touches personal browser profiles; secondary Chrome DevTools MCP usage checks `list_pages` first to confirm an isolated automation instance.
  - Non-blocking `SKIPPED_UNAVAILABLE` fallback when local devservers, databases, secrets, or browsers cannot run (removing mandatory `IMGUR_CLIENT_ID` and missing-devserver blockers so `reviewing-github-prs` completes static review normally with `COMMENT`).
- **Structured Five High-Signal Probes & PR Attribution (Phases 3-4)**: Combined diff-to-route scenario planning, multimodal `read_file` screenshot verification, signed-out deep-link vs. `RootVue`/`router.afterEach` ordering probes, axe-core WCAG AA `a11y` audits, sibling-route `Attributable to PR` vs. `Pre-existing` console/defect attribution, outbound network/redaction/consent checks, and mandatory session + `-PGID` process-group teardown.

### 3. Resulting State (B)
- Self-contained, profile-isolated live browser verification skill (`v1.0`) usable standalone by authors or invoked conditionally by `reviewing-github-prs` without risking personal browser profiles or stalling static code reviews.

### 4. Known Upstream Behaviors (Preserved for Byte Parity)
- **Unpinned `axe-core@latest` CDN fetch and cache (`scripts/drive-browser.py:668-669`, `:825-840`)**: `cmd_a11y` loads `axe-core@latest` from jsDelivr on unrestricted pages and caches `~/.drive-browser/axe-core.min.js` without invalidation on CSP-restricted pages, so `a11y` results can drift across machines or dates. Tracked upstream in [`learningequality/le-skills#145`](https://github.com/learningequality/le-skills/issues/145).
- **CLI `auth` credential flags (`scripts/drive-browser.py:1346-1347`)**: `auth` accepts `--username` and `--password` as CLI arguments (briefly visible in local process listings). `SKILL.md` restricts `auth` flags to non-sensitive local test/fixture credentials.

### 5. Re-sync / Update Recipe
```bash
git -C sources/le-skills fetch origin
git -C sources/le-skills log -p 9dc3e40713b25f74509e01847cf80e6582421d70..origin/main -- \
  skills/driving-a-browser/ scripts/drive-browser.py skills/github-pr-review/manual-qa.md
```
