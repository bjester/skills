# Changelog & Provenance: auditing-security

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-10-24] - Agent Supply Chain Trust Classes & Removed Guard Blame

- **Integrated Sources**:
  - `audit-skills`

### 1. Base State (A)
- Covered MCP trust inheritance, server identity confusion, and metadata trust.
- Did not explicitly address local supply-chain attacks via rogue agent skills, plugins, prompt bundles, or persistence hooks.
- Wildcard git history guidance mentioned reverted fixes but lacked concrete directives to run `git log -S` or `git blame` against removed validation checks or sanitizers in scoped diffs.

### 2. Curated Changes Applied (A -> B)
- **AI & LLM Domain Attack Classes (`AI-AND-LLM.md`)**:
  - Added "Agent skill, plugin, and prompt-bundle supply chain" attack class under MCP and sub-agent trust. Addresses capability-to-purpose mismatches, hidden instructions/payloads in bundled markdown, and local persistence hooks (`crontab`, `launchctl`, `systemd`, git hooks).
- **Core Attack Classes (`ATTACK-CLASSES.md`)**:
  - Expanded Wildcard git history bullet to instruct running `git log -S` / `git blame` on removed validation, auth checks, or sanitizers in scoped diffs to catch silent reversions of security fixes.

### 3. Resulting State (B)
- Enhanced defense-in-depth covering AI agent customization ecosystems and rigorous historical guard analysis during security audits.

---

## [2026-09-16] - Import from Cloudflare security-audit-skill

- **Upstream Repository**: `https://github.com/cloudflare/security-audit-skill.git`
- **Upstream Revision**: `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`, committed on 2026-09-14
- **Upstream Source Path**: `sources/security-audit-skill/skills/security-audit/`

### 1. Base State (A)
- Cloudflare's vulnerability discovery harness, seeded from their internal fleet-wide vulnerability discovery system.
- Structured across 6 execution phases: Reconnaissance, Coverage-led Hunting, Candidate Validation, Structured Output, Independent Record Verification, and Neutral Reporting.
- Supports dual operating modes: **Guidance mode** (default, conversational, targeted reviews without creating files) and **Full audit mode** (6-phase autonomous multi-agent audit with ledger tracking and file outputs).
- Includes 10 domain attack class companions:
  - `ATTACK-CLASSES.md`: Core web/API vulnerabilities, wildcards, obvious checks.
  - `AI-AND-LLM.md`: Prompt injection, tool use, memory poisoning, MCP trust.
  - `CLIENT-SIDE.md`: DOM injection, origin trust, UI redress, prototype pollution.
  - `CLOUD-AND-DEPLOYMENT.md`: IAM, IaC, containers, serverless, runtime configs.
  - `DATA-ISOLATION-AND-LIFECYCLE.md`: Multi-tenant isolation, cache poisoning, data lifecycle.
  - `DESKTOP-MOBILE-AND-LOCAL-IPC.md`: Native app boundaries, deep links, webviews, IPC.
  - `MEMORY-SAFETY-AND-BINARY.md`: Memory safety, bounds checking, unsafe blocks.
  - `PROTOCOLS-RPC-AND-MESSAGING.md`: gRPC, serialization, queues, event streams.
  - `RESOURCE-EXHAUSTION-AND-AVAILABILITY.md`: ReDoS, algorithmic complexity, quota spend.
  - `SUPPLY-CHAIN-AND-RELEASE.md`: Dependencies, CI/CD, signing, release integrity.
  - `WEB-PROTOCOL-AND-AUTH.md`: Request smuggling, cache deception, JWT/OAuth auth flows.
- Features zero-dependency Node.js validators (`validate-findings.cjs`, `validate-coverage-ledger.cjs`) backed by full test suites (`validate-findings.test.cjs`, `validate-coverage-ledger.test.cjs`) and a strict JSON schema (`report-schema.json`).

### 2. Curated Changes Applied (A -> B)
- **Renamed**: `security-audit` → `auditing-security` to adhere to repository naming conventions (gerund phrase authoring skills such as `writing-specs`, `diagnosing-bugs`, and `reviewing-code`).
- **Standardized Metadata**:
  - Added repository-standard YAML frontmatter to `SKILL.md`: `license: MIT`, `user-invocable: true`, `compatibility`, `allowed-tools`, and `metadata`.
  - Updated title to `# Auditing Security`.
- **Integrated into Build & Catalog**:
  - Added entry to catalog table and repository directory structure in `README.md`.
  - Packaged via `make build` into `output/skills/auditing-security/`.
- **Reworded validator invocations** (2026-10-22): The commands in `VALIDATION-AND-REPORTING.md` and `RECONNAISSANCE.md` now `cd` into the skill directory and use `./` script paths so `shinyskills` can resolve them as skill-relative references. Output paths must be absolute because the commands run from the skill directory. Dev-only test files (`*.test.cjs`) are left out of distributable packages by `make build`.

### 3. Resulting State (B)
- A complete, production-grade security auditing and guidance skill in `skills/auditing-security/`.
- Single-agent pairing sessions and interactive queries seamlessly use Guidance Mode without overhead.
- Full autonomous security audits leverage the complete multi-agent harness, coverage ledger, adversarial verification, and automated validator suites.

### 4. Re-sync / Update Recipe
When upstream `sources/security-audit-skill` is updated:
1. Fetch latest changes in upstream:
   ```bash
   git -C sources/security-audit-skill pull
   ```
2. Diff upstream `skills/security-audit/` against base commit `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`:
   ```bash
   git -C sources/security-audit-skill diff c1c8a8c1471069fb0e188eeaff69b8e8db6564a8..HEAD -- skills/security-audit/
   ```
3. Evaluate changes to orchestration, companions, schema, or validators.
4. Apply upstream improvements to `skills/auditing-security/` while preserving:
   - The skill name `auditing-security` in `SKILL.md` frontmatter and heading.
   - The standard YAML frontmatter fields (`license`, `user-invocable`, `compatibility`, `allowed-tools`, `metadata`).
5. Run the validator test suites:
   ```bash
   node skills/auditing-security/validate-findings.test.cjs
   node skills/auditing-security/validate-coverage-ledger.test.cjs
   ```
6. Run `make build` to verify output packaging.
7. Record the new upstream commit hash, date, and changes in this changelog.
