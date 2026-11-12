# Shared Guidelines for Writing Issues

This reference defines universal principles, quality standards, and shared conventions for authoring GitHub and Gitea issues. Apply these rules across features, bug reports, and technical tasks. Follow `references/forge-cli.md` first to resolve the target repository and select `gh` or `gt`.

---

## Core Philosophy: Specify What & Why, Not How

An issue defines requirements, intent, scope, and acceptance criteria. It is a contract of expected behavior between product, triage, and engineering, not an implementation script.

1. **Describe Observable Behavior**: State what the system does now and what it should do instead.
2. **Leave Implementation to the Developer**: Do not dictate code changes, internal algorithm mechanics, private variable names, or specific `if` checks.
3. **Provide Technical Orientation Without Prescriptions**: Point to relevant modules, interfaces, and known patterns (`file:line`, class names) without restricting the solution space of the developer.
4. **Plain Technical Prose & De-Slopping**: Apply the `writing-technical-docs` skill (Plain mode) and `references/word-swaps.md`. Write short active sentences with concrete verbs, zero em-dashes, zero negative parallelisms, and zero trailing `, -ing` participial fluff.

---

## Writing Principles: DOs and DON'Ts

| Aspect | DO | DON'T |
| :--- | :--- | :--- |
| **Title** | Describe the outcome or missing behavior:<br>• *"Store should track self-referential FK order"*<br>• *"Add sync filter argument to cleanupsyncs command"* | Dictate implementation or internal mechanics:<br>• *"Add _self_ref_order field to AbstractStore"*<br>• *"Refactor serialize.py to handle parent-child relationships"* |
| **Deliverables** | Use action verbs specifying observable contracts:<br>• *"Command supports `--sync-filter` parameter"*<br>• *"Rejects expired tokens with 401 Unauthorized"* | Write raw code or internal pseudocode:<br>• *"Add `if sync_filter:` in `__init__`"*<br>• *"Call `compute_order()` from loop"* |
| **References** | Point to files, interfaces, and existing precedents:<br>• *"Similar to pattern in `morango/sync/stream/serialize.py`"*<br>• *"Blocked by #14129"* | Prescribe line-by-line implementation scripts or rewrite snippets. |
| **Scope & Boundaries** | Explicitly define edge cases, backward compatibility, and out-of-scope items. | Leave assumptions unstated or assume edge cases are obvious. |

---

## Architectural & Invariant Guidelines (from Software Engineering Digest)

When drafting technical issues, incorporate these software engineering invariants:

1. **Inward Dependencies & Bounded Contexts**: Respect domain boundaries. Clarify whether an issue touches Core Domain logic, an Anti-Corruption Layer (ACL), or an external adapter.
2. **Data Model Integrity**: When data structures change, state schema evolution rules (field immutability, backward-compatible defaults, idempotency).
3. **Resilience & Production Hostility**: For network or remote integrations, state expectations for timeouts, error boundaries, retries, and observable telemetry (no silent suppression).
4. **Verification & Regression Safety**: Specify required test levels (unit tests for domain invariants, integration tests for DB/API boundaries, characterization tests for legacy regressions).

---

## AI Disclosure & Transparency (The DEEP Framework)

When drafting issues with AI assistance, disclose AI involvement transparently and follow the DEEP Framework:

- **D (Disclose)**: Explicitly state that AI assisted with drafting or refining the issue.
- **E (Engage Critically)**: Question generated assertions and verify code references and claims against the actual repository.
- **E (Edit)**: Refine and tighten output to remove hallucinations, boilerplate, and robotic repetition.
- **P (Process Sharing)**: Briefly describe how you prompted AI and verified its output.

### Example Disclosures

When AI tools assist with drafting, include a brief disclosure blockquote at the end of the issue body:

- > *AI Usage: I used Gemini to help synthesize reproduction logs and rough notes into this issue. I verified the referenced files and reproduction steps manually.*
- > *AI Usage: Drafted with Claude based on bug report discussion. Requirements and acceptance criteria were edited and verified against the codebase.*

---

## Pre-Submission Duplicate Check & Safe CLI Creation

1. **Select Forge CLI and Verify Target**: Follow `references/forge-cli.md` to select `gh` (GitHub) or `gt` (Gitea) and confirm the target repository.
2. **Search for Duplicates First**: Before filing a new issue, search open and closed issues to prevent duplicates and link related tickets:
   - **GitHub (`gh`)**:
     ```bash
     gh issue list --search "<keywords>" --state all --limit 20
     ```
   - **Gitea (`gt`)**:
     ```bash
     gt issue list -S "<keywords>" --state all -L 20 --no-input --json number,title,state,url
     ```
3. **Submit via `--body-file` (Never Inline `--body "..."`)**: Write the drafted Markdown to `/tmp/issue-body.md`. When running interactively, ask the user for confirmation before submitting. Pass `--body-file` so shell interpolation never corrupts backticks, code blocks, or stack traces:
   - **GitHub (`gh`)**:
     ```bash
     gh issue create --title "<Title>" --body-file /tmp/issue-body.md --label "<label>"
     ```
   - **Gitea (`gt`)**:
     ```bash
     gt issue create --no-input --title "<Title>" --body-file /tmp/issue-body.md --label "<label>"
     ```

---

## Universal Checklist for Issue Quality

- [ ] **Title**: Summarizes expected outcome or broken behavior (not implementation).
- [ ] **Why**: Business value, user impact, or failure severity is explicitly justified.
- [ ] **What**: Observable behaviors and acceptance criteria are measurable and verifiable.
- [ ] **Technical Pointers**: Relevant files and classes referenced without prescribing code snippets.
- [ ] **Edge Cases & Compat**: Backward compatibility, migrations, and environmental constraints noted.
- [ ] **No Code Dumps**: Contains zero prescriptive implementation code or copy-pasted solutions.
- [ ] **Plain Prose & De-Slop Scan**: Verified against `writing-technical-docs` and `references/word-swaps.md` (zero em-dashes, zero negative parallelisms, zero AI filler).
- [ ] **Duplicate Search & Safe Submission**: Checked `gh issue list --search` or `gt issue list -S --no-input` for duplicates, and submitted via `gh issue create --body-file` or `gt issue create --no-input --body-file`.
- [ ] **AI Disclosure**: DEEP framework statement included when AI assisted with drafting.
