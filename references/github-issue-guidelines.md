# Shared Guidelines for Writing GitHub Issues

This reference outlines universal principles, quality standards, and shared conventions for authoring high-quality GitHub issues (features, bugs, and technical tasks).

---

## Core Philosophy: Specify What & Why, Not How

A GitHub issue exists to define **requirements, intent, scope, and acceptance criteria**. It is a contract of expected behavior between product, triage, and engineering—not an implementation script.

1. **Describe Observable Behavior**: State what the system does now and what it should do instead.
2. **Leave Implementation to the Developer**: Do not dictate code changes, internal algorithm mechanics, private variable names, or specific `if` checks.
3. **Provide Technical Orientation Without Prescriptions**: Point to relevant modules, interfaces, and known patterns (`file:line`, class names) to accelerate orientation without restricting the developer's solution space.

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

When drafting technical issues, incorporate key software engineering invariants:

1. **Inward Dependencies & Bounded Contexts**: Respect domain boundaries. Clarify if an issue touches Core Domain logic, an Anti-Corruption Layer (ACL), or an external adapter.
2. **Data Model Integrity**: If data structures are modified, highlight schema evolution rules (field immutability, backward-compatible defaults, idempotency).
3. **Resilience & Production Hostility**: For network/remote integrations, state expectations for timeouts, error boundaries, retries, and observable telemetry (no silent suppression).
4. **Verification & Regression Safety**: Specify required test levels (unit tests for domain invariants, integration tests for DB/API boundaries, characterization tests for legacy regressions).

---

## AI Disclosure & Transparency (The DEEP Framework)

When drafting issues with AI assistance, always disclose AI involvement transparently and adhere to the **DEEP Framework**:

- **D - Disclose**: Explicitly state that AI was used to draft or refine the issue.
- **E - Engage Critically**: Question generated assertions; verify code references and claims against the actual repository.
- **E - Edit**: Refine and tighten output—remove hallucinations, boilerplate, and robotic repetition.
- **P - Process Sharing**: Briefly describe how AI was prompted/used.

### Example Disclosures:
> *AI Usage: I used Gemini to help synthesize reproduction logs and rough notes into this issue. I verified the referenced files and reproduction steps manually.*
>
> *AI Usage: Drafted with Claude based on bug report discussion. Requirements and acceptance criteria were edited and verified against the codebase.*

---

## Pre-Submission Duplicate Check & Safe CLI Creation

1. **Search for Duplicates First**: Before filing a new issue, search existing open and closed issues so duplicate reports are avoided and related issue numbers can be linked:
   ```bash
   gh issue list --search "<keywords>" --state all --limit 20
   ```
2. **Submit via `--body-file` (Never Inline `--body "..."`)**: Draft the issue Markdown to a scratch file (for example, `/tmp/issue-body.md`), present it for user confirmation when interactive, and pass `--body-file` to `gh issue create` so backticks, code blocks, and stack traces are never corrupted by shell interpolation:
   ```bash
   gh issue create --title "<Title>" --body-file /tmp/issue-body.md --label "<label>"
   ```

---

## Universal Checklist for Issue Quality

- [ ] **Title**: Summarizes expected outcome or broken behavior (not implementation).
- [ ] **Why**: Business value, user impact, or failure severity is explicitly justified.
- [ ] **What**: Observable behaviors and acceptance criteria are measurable and verifiable.
- [ ] **Technical Pointers**: Relevant files/classes referenced without prescribing code snippets.
- [ ] **Edge Cases & Compat**: Backwards compatibility, migrations, and environmental constraints noted.
- [ ] **No Code Dumps**: Contains zero prescriptive implementation code or copy-pasted solutions.
- [ ] **Duplicate Search & Safe Submission**: Checked `gh issue list --search` for duplicates and submitted via `gh issue create --body-file`.
- [ ] **AI Disclosure**: DEEP framework statement included if AI was used.
