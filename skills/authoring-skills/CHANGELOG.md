# Changelog & Provenance: authoring-skills

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-10-24] - Synthesis & Curation from agentic-awesome-skills (v20.0.0)

- **Upstream Repository**: `https://github.com/sickn33/agentic-awesome-skills`
- **Upstream Revision**: `6d4ea18320984083107f07ff69587fa355ee94c0` (Release: `v20.0.0`), committed on 2026-04-20
- **Upstream Source Paths**:
  - `sources/agentic-awesome-skills/skills/effective-agent-skills/`
  - `sources/agentic-awesome-skills/skills/writing-skills/`
  - `sources/agentic-awesome-skills/skills/audit-skills/`

### 1. Base State (A)
- Upstream `effective-agent-skills` provided general background on agent skills, progressive disclosure levels, and the description-as-routing contract.
- Upstream `writing-skills` outlined skill templates, CSO (context search optimization), and anti-rationalization concepts, but was structured around external dependencies (Node.js, Graphviz dot, OpenCode paths) and informal checklists.
- Upstream `audit-skills` provided platform-specific security threat categories (Windows, Linux, macOS, Mobile) and non-intrusive static analysis principles, but lacked a standardized execution workflow and frontmatter integration.

### 2. Curated Changes Applied (A -> B)
- **Synthesized & Renamed**: Combined the complementary principles from `effective-agent-skills`, `writing-skills`, and `audit-skills` into a unified first-class skill: `authoring-skills`, adhering to the repository gerund phrase naming convention.
- **Standardized Repository Anatomy**:
  - Implemented standard YAML frontmatter schema (`name`, `description`, `license`, `user-invocable`, `compatibility`, `allowed-tools`, `metadata`).
  - Added executive mission statement, ASCII workflow diagram, and 5 sequential execution phases.
- **Codified Progressive Disclosure & Degree-of-Freedom Calibration**:
  - Formalized the 3-level progressive disclosure architecture (Level 1 Discovery, Level 2 Activation, Level 3 Execution).
  - Added calibration guidelines matching the degree of freedom in prompt instructions to task fragility (High, Medium, Low).
- **Embedded Anti-Rationalization Guardrails**:
  - Created an explicit table mapping common agent rationalizations to mandatory countermeasures to prevent shortcutting.
- **Embedded Capability-to-Purpose Static Security Analysis**:
  - Integrated non-intrusive static analysis threat categories directly into Phase 4: privilege tampering, file locking/DoS, arbitrary script piping, network egress/credential exfiltration, obfuscation, and mobile security misuse.
- **Verification Gates**:
  - Wired verification into repository validation tooling (`make validate` / `shinyskills`).

### 3. Resulting State (B)
- A self-contained, rigorous, and production-grade skill guiding developers and coding agents through authoring, structuring, packaging, and statically security-auditing agent skills.

### 4. Re-sync / Update Recipe
When upstream `sources/agentic-awesome-skills` updates:
1. Fetch latest changes in upstream:
   ```bash
   git -C sources/agentic-awesome-skills pull
   ```
2. Diff upstream sources against base commit `6d4ea18`:
   ```bash
   git -C sources/agentic-awesome-skills diff 6d4ea18320984083107f07ff69587fa355ee94c0..HEAD -- skills/effective-agent-skills/ skills/writing-skills/ skills/audit-skills/
   ```
3. Evaluate updates to authoring patterns, progressive disclosure guidelines, or static threat detection heuristics.
4. Integrate valuable updates into `skills/authoring-skills/SKILL.md` while maintaining repository frontmatter, plain technical style, and validation gates.
5. Record the new upstream commit hash, date, and modifications in this changelog.
