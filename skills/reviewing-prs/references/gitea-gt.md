# Gitea (`gt`) Adapter for Pull Request Reviews

This reference defines the official Gitea CLI (`gt`, targeting Gitea 28+) commands for [SKILL.md](../SKILL.md). Pass `--no-input` on every `gt` command, never pass `--editor` or `--web`, and complete the `Forge Selection Gate` and `Reviewer Identity Gate` in `references/forge-cli.md` before staging or publishing any remote review.

---

## Step 1: Identity, PR Context, Threads, Issues & CI Queries

Run these read-only commands (raising `-L` above the default `30` limit on list queries) to inspect the active reviewer login, pull request metadata, commits, threads, linked issues, and CI status:

```bash
# Query active Gitea account login (never echo GITEA_TOKEN or token values)
gt api user --jq .login --no-input

# Fetch PR metadata (author, base, and head are flat strings, with NO commits field)
gt pr view <id> --no-input --json number,title,body,state,draft,url,base,head,head_sha,mergeable,review_decision,reviews,author

# List PR commits via local git or the Gitea REST endpoint
git log origin/<base>..<head_sha> --oneline
gt api --no-input --paginate 'repos/{owner}/{repo}/pulls/<num>/commits'

# Fetch general conversation comments (gt pr view --comments --no-input rejects --json, and comments in JSON is an integer count)
gt pr comment list <num> -L 100 --no-input --json id,author,body,created_at

# Fetch prior review summary bodies, states, and reviewed commits
gt pr review list <num> -L 100 --no-input --json id,author,state,commit,body,submitted_at

# Fetch existing inline review threads (resolver == "" means unresolved, and deleted-line anchors appear on old_line)
gt pr review comments <num> -L 1000 --no-input --json id,review_id,path,line,old_line,author,resolver,body,created_at

# Inspect linked issue requirements and acceptance criteria
gt issue view <num> --no-input --json number,title,body,labels

# Inspect CI check statuses and failed job logs
gt pr checks <num> --no-input --json name,state,url
gt run logs <job-url-or-run-id> --failed --no-input
```

- **Schema & Flag Rules (`gt` vs. `gh`)**:
  - `gt pr view --no-input --json ...` returns `author`, `base`, and `head` as **flat strings**, not nested objects.
  - `gt pr view --no-input` has **no** `commits` JSON field. Passing `commits` to `--json` fails validation. Use `git log origin/<base>..<head_sha> --oneline` or `gt api --no-input --paginate 'repos/{owner}/{repo}/pulls/<num>/commits'` instead.
  - Prefer `gt api user --jq .login --no-input` over `gt auth status --no-input --json`, because `GITEA_TOKEN` environment credentials leave `user` empty without `--verify`.
  - On forked repositories, `gt` targets `upstream` over `origin`. Pass `-R OWNER/REPO` when targeting the fork itself and verify with `gt repo view --no-input --json full_name`.
- **Reviewer Identity Gate (`gt`)**: Before staging (`Mode A`) or publishing (`Mode B`) a review to Gitea, compare `gt api user --jq .login --no-input` against the flat `author` string from `gt pr view --no-input` case-insensitively. If they match, abort immediately before calling `gt pr review --no-input`:
  `Active gt account '<gt_user>' matches PR author '<author>'. Switch to a reviewer account before posting a review to Gitea.`

---

## Step 2: Diff Retrieval & Hunk Line Bounds

Retrieve changed file paths and the unified pull request diff:

```bash
# List changed files
gt pr diff <num> --name-only --no-input

# Fetch full unified diff (or narrow to one file with --path <file>)
gt pr diff <num> --no-input
gt pr diff <num> --path <file> --no-input
```

Verify inline comment positions against active diff hunks (`@@ -os,oc +ns,nc @@`):

1. Inline comments in `gt` take **either** `"new_position": <line>` **or** `"old_position": <line>` (exact XOR, never both on the same comment object):
   - **Additions, modifications, or unchanged context lines**: Set `"new_position": <line>`, where `<line>` falls within `[ns, ns + nc - 1]` in the new file.
   - **Deletions**: Set `"old_position": <line>`, where `<line>` falls within `[os, os + oc - 1]` in the old file.
2. When `--commit` is omitted, `gt` fetches the pull request diff and validates diff membership before submitting the review, rejecting lines outside the diff. Passing `--commit` skips this check and lets Gitea store off-diff comments without showing them in the diff. Do not pass `--commit` when submitting inline comments, and do not guess line numbers. Displace any finding outside active diff hunks into `### Comments on Lines Outside Diff` inside `/tmp/review-summary.md`.

---

## Step 3: Local Checkout

`gt pr checkout --no-input` switches the local working tree. Inspect diffs to `Makefile`, `package.json` scripts, `conftest.py`, `.github/workflows/`, and `.gitea/workflows/` first, and ask the user before running if local uncommitted modifications exist:

```bash
gt pr checkout <num> --no-input
```

---

## Step 5: Review Files, Pending-Fold Pre-Check & Submission Modes

### 1. Check for an Existing Pending Review First

Before submitting a review, inspect existing reviews on the pull request:

```bash
gt pr review list <num> --no-input --json id,state,author
```

If a `PENDING` review already exists for the active user, running `gt pr review --no-input` without `--pending` folds and publishes that pending draft (exiting with code `2` unless `--yes` is passed). Check this list first so staged draft comments are never published unintentionally.

### 2. Write Summary Body and Inline Comments Files

Write the formatted summary body (ending with `*Generated by <agent harness> using model <model>*`) to `/tmp/review-summary.md`, and write diff-verified inline comments to a real file `/tmp/inline-comments.json` (`--comments-file` rejects `-` stdin):

```json
[
  {
    "path": "src/clients/payment.py",
    "new_position": 42,
    "body": "🚨 **Blocker (Must-Fix)**: Remote network calls must specify an explicit, bounded deadline.\n\n**Principle**: Scale 1: Macro Resilience / Explicit Timeouts\n\n```python\n# Suggested fix:\nresponse = self.http_client.post(url, json=payload, timeout=5.0)\n```"
  }
]
```

If zero diff-verified inline comments exist, omit `--comments-file` from the `gt pr review --no-input` command.

### 3. Stage or Publish the Review

Immediately before submitting, confirm the pull request head has not moved since your review (`gt pr view <num> --no-input --json head_sha --jq .head_sha` must still equal `<head_sha>`, else abort and inspect the new commits). Omit `--commit` on `gt pr review`: `gt` binds the review to the current pull request head by default and only validates inline comment diff positions when `--commit` is omitted.

- **Mode A: Pending Review (Default & Recommended)**:
  ```bash
  test "$(gt pr view <num> --no-input --json head_sha --jq .head_sha)" = "<head_sha>"
  gt pr review <num> --pending \
    --body-file /tmp/review-summary.md \
    --comments-file /tmp/inline-comments.json \
    --no-input
  ```
  This stages a **Pending** review on `<head_sha>` with diff-validated inline comments. Present the drafted summary and pull request files URL to the user. The staged review can later be published in the Gitea web UI or from the CLI:
  ```bash
  gt pr review submit <num> --approve|--request-changes|--comment --no-input
  ```

- **Mode B: Autonomous / Published Submission**:
  When the user explicitly instructs direct publication without staging, pass the verdict flag selected by the `Strict Approval Gate` in [SKILL.md](../SKILL.md):
  ```bash
  test "$(gt pr view <num> --no-input --json head_sha --jq .head_sha)" = "<head_sha>"
  gt pr review <num> --request-changes|--comment|--approve \
    --body-file /tmp/review-summary.md \
    --comments-file /tmp/inline-comments.json \
    --no-input
  ```
  `--request-changes` requires a non-empty summary body, and `--comment` requires a summary body or inline comments (omit `--comments-file` when zero inline comments exist).
