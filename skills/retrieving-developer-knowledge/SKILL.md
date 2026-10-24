---
name: retrieving-developer-knowledge
description: "Searches, retrieves, and synthesizes official Google developer documentation across Google Cloud, AI/Gemini, Android, Chrome, Web, Flutter, Go, Firebase, and other Google developer platforms. Integrates with the Developer Knowledge MCP server (search_documents, get_documents, answer_query) or the Developer Knowledge REST API fallback. Use when searching for gcloud CLI commands, API syntax, IAM permissions, official documentation, architectural comparisons, or product choice overviews. Don't use for local filesystem lookups or non-Google documentation."
license: MIT - https://github.com/bjester/skills/blob/main/LICENSE
user-invocable: true
compatibility: a development environment with network access and Developer Knowledge MCP tools or curl/gcloud
allowed-tools:
  - read_file
  - run_command
  - answer_query
  - search_documents
  - get_documents
  - ask_user_question
metadata:
  author: Blaine Jester
  version: "1.1"
---

# Retrieving Developer Knowledge

Purpose: Access, retrieve, and synthesize official Google developer documentation across Google Cloud, AI/ML (ai.google.dev, ADK, TensorFlow), Android, Chrome, Web, Flutter, Go, Firebase, and developer platforms using Developer Knowledge MCP tools or REST API fallback.

## Workflow

```
1. TRANSPORT SELECTION ──► 2. EXECUTE LOOKUP ──► 3. VERIFY & FALLBACK ──► 4. SYNTHESIZE & OUTPUT
          │                        │                       │                         │
          ▼                        ▼                       ▼                         ▼
     Check MCP tools vs.      Call `answer_query`     Confirm non-empty;        Generate complete,
     REST fallback (gcloud    or `search_documents`   retry 429 quota errors    executable code/CLI
     or API key)              with focused keywords   via search chunks         with placeholders
```

### Step 1: Transport Selection

Choose the appropriate transport based on your runtime environment:
- **If MCP tools are present in your environment**: Use the Developer Knowledge MCP server (`answer_query`, `search_documents`, `get_documents`).
- **If MCP tools are not present or fail handshake**: Use the REST API fallback via `curl` against `https://developerknowledge.googleapis.com/v1`.

> [!NOTE]
> A declared server is not always a connected server. Some clients cannot complete the MCP handshake with this server and expose no `answer_query`, `search_documents` or `get_documents` tool at all, even though the plugin declares one. Treat their absence as normal and use the REST fallback below.

### Step 2: Direct Retrieval Execution

When answering a technical question, execute documentation lookup directly within your current conversation context (do not delegate retrieval to subagents):
- **Conceptual Guides & Multi-Step Workflows**: Call `answer_query` (MCP) or `:answerQuery` (REST).
- **CLI Flags, IAM Permissions & Parameter Syntax**: Call `search_documents` (MCP) or `documents:searchDocumentChunks` (REST) using 2–5 focused keywords (e.g. `cloud run filestore nfs mount gcloud`) rather than full conversational sentences.
- **Full Document Retrieval**: Call `get_documents` (MCP) or `documents/{URI_WITHOUT_SCHEME}` (REST) when you need complete page context.

### Step 3: Verification, Error Handling & Quota Fallback

Confirm the lookup succeeded before using it. A response that arrives is not automatically an answer. `PERMISSION_DENIED`, `UNAUTHENTICATED`, HTTP 401/403, an empty result set, or any error payload is a FAILED lookup even when the tool itself reported no error. On a failed lookup, do not answer as though it had succeeded.

- **Rate Limits & Quota Exhaustion (HTTP 429 / RESOURCE_EXHAUSTED)**:
  > [!WARNING]
  > If calling `answer_query` or the REST `:answerQuery` endpoint returns an HTTP 429 (`RESOURCE_EXHAUSTED` / out of quota error), this indicates server-side generative QA quota exhaustion. Do not treat this as an unrecoverable failure or fall back to ungrounded memory; immediately retry using the search endpoint (`search_documents` for MCP, or `documents:searchDocumentChunks` for REST) with 2–5 focused keywords from the query.

- **Persistent Transport Failures**:
  Try the other transport once. If that also fails, state plainly in your reply to the user that you could not reach Developer Knowledge and are answering without it. Presenting recalled documentation as a retrieved result is the worst available outcome, because nothing in the reply distinguishes it from a real lookup.

### Step 4: Immediate & Complete Solution Output

Immediately upon receiving the documentation response, output the complete, self-contained, and executable technical solution (commands with all required flags and placeholders, YAML/JSON configurations, or code snippets) directly in your response text.

---

## Tool Selection & Usage

### 1. Developer Knowledge MCP Tools (Preferred)

When MCP tools are present in your active tool definitions:
- **`answer_query(query="...")`**: Use for conceptual guides, architectural comparisons, product choice overviews, and multi-step workflows. This tool has limited quota. If you get a 429 out of quota error, use `search_documents` instead.
- **`search_documents(query="...")`**: Use for granular CLI flags, exact syntax, parameter names, and IAM permissions (`service.resource.verb`). Use 2–5 focused keywords (e.g., `cloud run filestore nfs mount gcloud`) rather than full conversational sentences.
- **`get_documents(names=["documents/{uri_without_scheme}"])`**: Fetch full documentation pages by resource name (e.g. `names: ["documents/docs.cloud.google.com/run/docs/overview/what-is-cloud-run"]`).

### 2. REST API Fallback

When the MCP tools are absent, query the Developer Knowledge REST API (`https://developerknowledge.googleapis.com/v1`) with `curl`. Two credentials work; try them in this order:

#### Credential A: Existing Google Credential (Preferred)

If `gcloud` is authenticated, pass a bearer token and your quota project. Nothing needs to be installed or configured:

```bash
curl -s -X POST "https://developerknowledge.googleapis.com/v1:answerQuery" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "X-Goog-User-Project: $(gcloud config get-value project 2>/dev/null)" \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I configure public read access on Cloud Storage?"}'
```

> [!TIP]
> If that fails to authenticate with a 401, 403, or other credential error, the account has a token the API will not accept. Substitute `gcloud auth application-default print-access-token` for `gcloud auth print-access-token` in the command above and try again. Treat an auth error here as a reason to try the application-default credential rather than as a failed lookup.

#### Credential B: API Key

Where `DEVELOPERKNOWLEDGE_API_KEY` is set in the environment, pass it as a `key` query parameter instead of an `Authorization` header. If neither credential is available, enable the API and create a key by following the [Developer Knowledge quickstart](https://developers.google.com/knowledge/quickstart), then export it as `DEVELOPERKNOWLEDGE_API_KEY`. Report that you need a credential rather than answering without a lookup.

- **Answer Query**:
  ```bash
  curl -s -X POST "https://developerknowledge.googleapis.com/v1:answerQuery?key=${DEVELOPERKNOWLEDGE_API_KEY}" \
    -H "Content-Type: application/json" \
    -d '{"query": "How do I configure public read access on Cloud Storage?"}'
  ```
  *(If you get a 429 out of quota error, use `documents:searchDocumentChunks` instead).*

- **Search Document Chunks** (use 2–5 focused keywords; optionally scope by domain via `filter='data_source = "docs.cloud.google.com"'`):
  ```bash
  curl -s -G "https://developerknowledge.googleapis.com/v1/documents:searchDocumentChunks" \
    --data-urlencode "query=gcloud logging metrics create" \
    --data-urlencode "filter=data_source = \"docs.cloud.google.com\"" \
    --data-urlencode "key=${DEVELOPERKNOWLEDGE_API_KEY}"
  ```

- **Get Document**:
  ```bash
  curl -s "https://developerknowledge.googleapis.com/v1/documents/docs.cloud.google.com/run/docs/overview/what-is-cloud-run?key=${DEVELOPERKNOWLEDGE_API_KEY}"
  ```

- **Batch Get Documents** (a `GET`, with one `names` parameter per document and no request body; up to 20 per call; pass `view=DOCUMENT_VIEW_BASIC` when inspecting titles/URIs before fetching full Markdown bodies):
  ```bash
  curl -s -G "https://developerknowledge.googleapis.com/v1/documents:batchGet" \
    --data-urlencode "names=documents/docs.cloud.google.com/run/docs/overview/what-is-cloud-run" \
    --data-urlencode "names=documents/docs.cloud.google.com/storage/docs/creating-buckets" \
    --data-urlencode "view=DOCUMENT_VIEW_BASIC" \
    --data-urlencode "key=${DEVELOPERKNOWLEDGE_API_KEY}"
  ```

---

## Synthesis & Output Guidelines

1. **Grounding in Official Documentation**: Ground all solutions directly in retrieved documentation. Official documentation conventions have absolute precedence over memorized defaults.
2. **Exact Parameter Formatting**: Format CLI flags, composite keys (e.g. `location=IP:PATH`), and IAM permission strings according to official Google specifications.
3. **Complete Solutions in Final Response**: Always output the full, self-contained, executable technical solution (commands, configurations, or code snippets) with clear standard placeholders (e.g. `PROJECT_ID`, `SERVICE_NAME`, `REGION`) directly in your final message, even if previously referenced during internal planning.
4. **Project Dependency Version Reconciliation**: When working inside a repository, inspect `package.json`, `pyproject.toml`, `go.mod`, or `pubspec.yaml` first. Latest retrieved documentation may target a newer SDK/CLI major version than the project has pinned—align generated code with the installed version or explicitly call out the upgrade requirement.
5. **Query Privacy & Untrusted Content Boundary**: Strip private project IDs, internal hostnames, credentials, and proprietary code before querying `answer_query` or `search_documents`.

---

## References

- [MCP Usage & Tool Details](references/mcp-usage.md)
- [REST API Fallback Guide](references/api-fallback.md)
- [Supported Domains & Scoping](references/supported-domains.md)
