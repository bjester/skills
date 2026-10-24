# Changelog & Provenance: writing-technical-docs

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-10-24] - Technical Precision, Runbook Guardrails, README & ADR Patterns

- **Upstream Sources**: Curated from `tech-writing-proofread`, `runbook-creation`, `readme`, and `documentation-and-adrs`.

### 1. Curated Changes Applied
- **`SKILL.md`**:
  - Expanded Rule 2 with proper noun casing standards (`PostgreSQL`, `GitHub`, `TypeScript`, `macOS`, `GraphQL`), backtick wrapping for commands, flags, paths, and environment variables, and explicit `[verify: confirm whether X or Y]` ambiguity markers to prevent guess-work rewrites.
- **`references/use-cases.md`**:
  - Expanded `Runbooks and standard operating procedures` with pre-flight environment/role declarations, command success output verification, measurable recovery validation, rollbacks, and escalation conditions.
  - Added `READMEs and onboarding guides` use case mandating grounding of all commands, flags, scripts, and environment defaults against repo manifests (`Makefile`, `package.json`, etc.).
  - Added `Architecture Decision Records (ADRs)` use case specifying the 5 canonical sections (`Status`, `Context`, `Decision`, `Alternatives Considered`, `Consequences`) and deprecation linking (`Superseded by ADR-NNN`).

---

## [2026-10-18] - BDD Behavioral Language Allowance for Software Engineering

### 1. Motivation
- ASD-STE100 strictly forbids ambiguous modals like "should" to prevent ambiguity in operational instructions.
- In software engineering, describing system behaviors (e.g., "X should do Y", "it should return 404") is standard practice in specifications, acceptance criteria, and Behavior-Driven Development (BDD).
- Distinguishing between human procedural instructions (which require imperative mood or "must") and software behavioral expectations allows engineers to express testable software behavior without violating Plain English principles.

### 2. Curated Changes Applied
- **`SKILL.md`**:
  - Relaxed modal rule 5 under `## The Document` to explicitly permit "should" for BDD-style phrasing and behavioral specifications (e.g., "X should do Y", "it should return 404").
  - Updated step 2 under `## Self-Check Before You Deliver` to exempt BDD behavioral specifications when auditing documents for "should".
  - Bumped version metadata to `2.2.0-curated`.
- **`references/rule-catalog.md`**:
  - Documented the BDD exception under Section 3 (Modals).
  - Added an entry to *The modal ladder* mapping `should (behavioral spec / BDD)` to permitted software expectations.
- **`references/use-cases.md`**:
  - Added the `Software specifications and BDD scenarios` use case defining how to apply BDD phrasing alongside short sentences and plain grammar while reserving "must" for human procedures.

---

## [2026-10-18] - Enrichment of word-swaps.md from pstack unslop (v0.15.26)

- **Upstream Repository**: `git@github.com:cursor/plugins.git`
- **Upstream Revision**: `0b8e952052d482ee6de06deebf14d590d77b1b34` (Release: `chore(pstack): bump to 0.15.26`), committed on 2026-10-18
- **Upstream Source Path**: `sources/cursor-plugins/pstack/skills/unslop/`

### 1. Curated Changes Applied
- **Enriched Shared Reference `references/word-swaps.md`**:
  - Injected abstract AI metaphor nouns (`substrate`, `vector`, `locus`, `nexus`, `primitive`, `bedrock`, `modality`, `gold-plating`, `evacuate`, `flywheel`).
  - Codified 7 syntactic and stylistic AI tell eradication rules: em-dash elimination (`—`), colon-as-connector bans, superficial -ing participial phrases, vague attributions, false ranges, chatbot pleasantries/sycophancy, and "say what it does, not how it feels".

---

## [2026-09-16] - Curation from SimpleEnglish v2.1.0

- **Upstream Repository**: `https://github.com/AminBlg/SimpleEnglish.git`
- **Upstream Revision**: `79b590f` (Tag: `v2.1.0`), committed on 2026-09-16
- **Upstream Source Path**: `sources/SimpleEnglish/skills/simple-english/`

### 1. Base State (A)
- Upstream `SimpleEnglish` v2.1.0 provided a streamlined ~1,700-token prompt with two registers: *The Document* and *The Reply*.
- The *Reply* register completely forbade bullet lists, bold spans, headers, and tables in chat (`search for a line that starts with - and remove each one`).
- Maintained 53 rules in `references/rule-catalog.md` and dictionary rulings in `references/strict-vocabulary.md`.
- Removed old `references/checklist.md`.

### 2. Curated Changes Applied (A -> B)
- **Renamed**: `simple-english` → `writing-technical-docs` to match the repository's gerund authoring skill conventions (`writing-specs`, `writing-plans`).
- **Loosened Chat Reply Restrictions**:
  - Replaced the strict ban on bullet lists, bold spans, and formatting with readability guidelines.
  - Allowed structured vertical lists and code blocks in chat explanations and document reviews to support scanning and clarity.
  - Preserved requirements for direct answers in the first sentence, zero conversational pleasantries, and complete grammar.
- **Enhanced Document List Guidelines**:
  - Clarified that numbered and bulleted vertical lists are encouraged for sequences, procedures, prerequisites, and parallel options, while continuing to enforce the 20/25-word limit per item and single-instruction rules.
- **Shared Reference Extraction**:
  - Promoted `references/word-swaps.md` to top-level `references/word-swaps.md` in the repository, shared with `pairing-with-adhd` and declared in `Makefile`.
- **References Included**:
  - Copied `references/rule-catalog.md`, `references/strict-vocabulary.md`, and `references/use-cases.md` into `skills/writing-technical-docs/references/`.

### 3. Resulting State (B)
- A focused technical documentation skill providing ASD-STE100 discipline for written artifacts (READMEs, specifications, runbooks, error messages, PR descriptions), while supporting natural, structured developer chat interaction without arbitrary formatting restrictions.

### 4. Re-sync / Update Recipe
When upstream `sources/SimpleEnglish` is updated:
1. Fetch latest changes in upstream:
   ```bash
   git -C sources/SimpleEnglish pull
   ```
2. Diff upstream `SKILL.md` against the base commit `79b590f`:
   ```bash
   git -C sources/SimpleEnglish diff 79b590f..HEAD -- skills/simple-english/
   ```
3. Evaluate changes to rule formulations, word mappings, or reference files.
4. Apply upstream improvements to `skills/writing-technical-docs/` while preserving:
   - The skill name `writing-technical-docs`.
   - The loosened chat list and formatting rules in `## Chat Explanations & Reviews`.
   - The shared reference wiring to `references/word-swaps.md`.
   - The allowance for BDD language ("should") in software behavioral specifications.
5. Run `make build` to verify output packaging.
6. Record the new upstream commit hash, date, and changes in this changelog.
