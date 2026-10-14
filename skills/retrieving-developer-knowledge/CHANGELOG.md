# Changelog & Provenance: retrieving-developer-knowledge

Tracks upstream sources, imported commit revisions, and curated repository modifications.

## [2026-10-14] - Import and Standardization from Google Skills

- **Upstream Repository**: `https://github.com/google/skills.git`
- **Upstream Revision**: `05bf63a9a00c6eeaa657fcec9ad8f74183b96839`, committed on 2026-10-07
- **Upstream Source Path**: `sources/google-skills/skills/developers/retrieving-developer-knowledge/`

### 1. Base State (A)
- Upstream skill provides access to official Google developer documentation across Google Cloud, AI/ML (ai.google.dev, ADK, TensorFlow), Android, Chrome, Web, Flutter, Go, Firebase, and other Google developer platforms.
- Integrates with the Developer Knowledge Remote MCP server (`answer_query`, `search_documents`, `get_documents`) or REST API fallback (`developerknowledge.googleapis.com/v1`) using gcloud credentials or API keys.
- Bundles 3 reference guides: `references/mcp-usage.md`, `references/api-fallback.md`, and `references/supported-domains.md`.
- Lacks standardized repository metadata (`license`, `allowed-tools`, `compatibility`, `user-invocable`) and structured workflow diagram.

### 2. Curated Changes Applied (A -> B)
- **Standardized Metadata**:
  - Configured repository-standard YAML frontmatter: `license: MIT`, `user-invocable: true`, `compatibility`, `allowed-tools`, and `metadata`.
  - Preserved comprehensive description with clear trigger conditions and anti-patterns ("Don't use for local filesystem lookups or non-Google documentation").
- **Structured Workflow & Heading**:
  - Renamed top-level heading to `# Retrieving Developer Knowledge` with an explicit Purpose statement.
  - Added ASCII workflow diagram illustrating the 4-phase retrieval lifecycle: Transport Selection, Direct Retrieval, Verification & Quota Fallback, and Complete Solution Output.
  - Formatted error-handling, credential retries, and quota exhaustion procedures using GitHub-style alerts (`> [!NOTE]`, `> [!IMPORTANT]`, `> [!TIP]`).
- **Local Reference Encapsulation**:
  - Retained skill-specific references in `skills/retrieving-developer-knowledge/references/` in accordance with repository encapsulation guidelines.
- **Catalog & Packaging Integration**:
  - Added entry to Skills Catalog table and repository directory structure in `README.md`.
  - Verified package generation via `make build`.

### 3. Resulting State (B)
- A standardized, production-grade knowledge retrieval skill for Google platforms with consistent agent metadata, multi-transport support, and robust quota/auth fallback handling.

### 4. Re-sync / Update Recipe
When upstream `sources/google-skills` is updated:
1. Fetch latest changes in upstream:
   ```bash
   git -C sources/google-skills pull
   ```
2. Diff upstream against base commit `05bf63a9a00c6eeaa657fcec9ad8f74183b96839`:
   ```bash
   git -C sources/google-skills diff 05bf63a9a00c6eeaa657fcec9ad8f74183b96839..HEAD -- skills/developers/retrieving-developer-knowledge/
   ```
3. Evaluate updates to endpoints, supported domains, or MCP tool signatures.
4. Port improvements into `skills/retrieving-developer-knowledge/` while preserving:
   - The repository-standard YAML frontmatter and author metadata.
   - The heading `# Retrieving Developer Knowledge` and workflow diagram.
   - Encapsulation of skill-specific references.
5. Run `make build` to verify output packaging.
6. Record the new upstream commit hash, date, and changes in this changelog.
