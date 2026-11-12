# Gitea (`gt`) Adapter for Resolving PR Feedback

Load this adapter when the `Forge Selection Gate` in `references/forge-cli.md` selects Gitea (`gt`). Pass `--no-input` on every `gt` command. Never pass `--editor` or `--web`.

---

## 1. Authentication, Identity & PR Metadata

1. Verify Gitea host credentials and query the active Gitea login:
   ```bash
   gt auth status --no-input --json host,user,active,credential_available
   gt api user --jq .login --no-input
   ```
   > [!NOTE]
   > Always query `gt api user --jq .login --no-input` for the active account. Under `GITEA_TOKEN` environment credentials, `gt auth status --no-input --json` leaves `user` empty unless `--verify` is passed.

2. Query pull request metadata and author identity (pass `<pr-number>` when not on the PR branch, and add `-R OWNER/REPO` when targeting a fork PR directly):
   ```bash
   gt pr view --no-input --json number,title,base,head,head_sha,author
   ```

3. Run the **Author Identity Gate**: compare the active login from `gt api user --jq .login --no-input` against the flat string `author` from `gt pr view --no-input --json author`. Unlike GitHub, Gitea returns `author`, `base`, and `head` as flat strings rather than nested objects. Halt immediately on mismatch unless the user explicitly authorized co-maintainer resolution in the current session.

---

## 2. Enumerating Unresolved Review Threads

1. Query inline pull request review comments with `-L 1000`, group comments by conversation location (`[.path, .line, .old_line]`), and filter to unresolved threads:
   ```bash
   gt pr review comments <pr-number> -L 1000 --no-input --json id,review_id,path,line,old_line,author,resolver,body,created_at --jq 'group_by([.path, .line, .old_line]) | map(sort_by(.id) | select(all(.resolver == "")) | {root_id: .[0].id, path: .[0].path, line: .[0].line, old_line: .[0].old_line, comments: .})'
   ```
   - **Pagination Default (`-L 30`)**: `gt` list commands stop at 30 items by default. Pass `-L 1000` so review comments on larger pull requests are not truncated.
   - **Conversation Grouping & Root ID (`root_id`)**: `gt pr review comments` flattens every comment and reply across non-pending reviews without an `in_reply_to` field, and Gitea stores `resolver` on the root conversation comment. Grouping by `[.path, .line, .old_line]`, sorting by `.id`, and requiring `all(.resolver == "")` collapses multi-reply threads into a single work item, excludes follow-up replies on already-resolved threads, and exposes `root_id` (`.[0].id`) for `reply` and `resolve`.
   - **Line Anchors (`line` vs. `old_line`)**: Comments on added or unchanged lines populate `line`. Comments anchored to deleted lines populate `old_line` (with `line` set to `0`).

2. Inspect top-level review bodies so summary-only requests are included in triage:
   ```bash
   gt pr review list <pr-number> -L 100 --no-input --json id,author,state,body
   ```

3. If needed, inspect general pull request conversation comments separately (`gt pr view --comments` rejects `--json`, and `comments` in `gt pr view --json` is only an integer count):
   ```bash
   gt pr comment list <pr-number> -L 100 --no-input --json id,author,body,created_at
   ```

---

## 3. Replying to Inline Review Comments

Push your verified commit(s) to the remote pull request branch before replying. `gt pr review reply` requires **both** `<pr-number>` and `<root-id>` positional arguments. Pass `--body-file -` with a single-quoted heredoc (`<<'EOF'`) so backticks in `<test command>` are never corrupted by shell expansion:

```bash
gt pr review reply <pr-number> <root-id> --no-input --body-file - <<'EOF'
Addressed in commit <SHA>. <Brief explanation of fix>. Verified with `<test command>` (<result>).
EOF
```

---

## 4. Resolving Review Threads

After pushing the commit and posting the reply, mark the inline thread resolved with `gt pr review resolve` (passing both `<pr-number>` and `<root-id>`):

```bash
gt pr review resolve <pr-number> <root-id> --no-input
```

> [!WARNING]
> `gt pr review resolve` outputs plain text only and **rejects `--json` and `--jq`**. Do not append `--json` or `--jq` to this command. If you want structured confirmation afterward, re-run `gt pr review comments <pr-number> -L 1000 --no-input --json id,resolver` and check that `resolver` is non-empty for `<root-id>`.
