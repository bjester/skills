# Changelog & Provenance: writing-technical-docs

Tracks upstream sources, imported commit revisions, and curated repository modifications.

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
5. Run `make build` to verify output packaging.
6. Record the new upstream commit hash, date, and changes in this changelog.
