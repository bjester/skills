---
name: using-gitea-cli
description: "Drives Gitea instances (gitea.com or self-hosted) using gt, the official Gitea CLI: inspects pull request CI checks and failed Actions job logs, reruns or dispatches workflows, manages issues, pull requests, comments, inline reviews, merges, releases, and wikis, searches repositories, scripts CI with GITEA_TOKEN, and calls raw endpoints via gt api. Use for Gitea CLI operations, Gitea Actions, .gitea/workflows, or migrating from the older tea CLI. Pair with reviewing-prs, writing-prs, resolving-pr-feedback, writing-issues-for-bugs, or writing-issues-for-features for structured engineering workflows."
license: MIT - https://github.com/bjester/skills/blob/main/LICENSE
user-invocable: true
compatibility: Gitea repositories (gitea.com or self-hosted Gitea 28+) using git and the official gt CLI
allowed-tools:
  - read_file
  - write_file
  - run_command
  - grep
metadata:
  author: Blaine Jester
  version: "1.0"
---

# Using Gitea CLI

Purpose: Drive Gitea instances safely and non-interactively with the official gt CLI across CI inspection, repository operations, issues, pull requests, releases, wikis, and REST API calls.

`gt` drives a Gitea instance from the shell and replaces the older `tea` CLI. Its subcommands resemble `gh`, but flags, JSON fields, and defaults differ. Check `gt <command> --help` (which lists `JSON FIELDS`) or `gt schema <command>` instead of assuming `gh` or `tea` behavior.

## Workflow

```
1. PRE-FLIGHT FORGE & AUTH -> 2. NON-INTERACTIVE JSON READS -> 3. APPROVED MUTATIONS -> 4. EXIT-CODE & STATE VERIFY
             |                              |                            |                           |
             v                              v                            v                           v
   Verify Gitea remote,          Pass `--no-input --json`      Preview with `--dry-run`,   Branch on exit codes,
   `-R` fork target, and         and `--jq`, and raise `-L`    and get user approval       and verify remote URL
   active login via `gt api`     above default 30              before writes or `--yes`    and updated state
```

## Execution Phases

### Phase 1: Pre-Flight Forge, Target & Identity Verification

1. **Verify CLI and Credentials**: Run `gt --version` and `gt auth status --no-input --json host,user,active,credential_available,verified`. With `--json`, `gt auth status` exits `0` even when credentials fail, so check `credential_available`. Without `--json`, missing or rejected credentials exit `4`.
2. **Configure Headless CI Credentials**: In CI or scripts, export `GITEA_TOKEN` with `GITEA_CLI_HOST` (or `GITEA_INSTANCE_URL`). Environment credentials are never saved to disk. Never echo tokens or run interactive `gt auth login`.
3. **Resolve Active Identity**: Run `gt api user --jq .login --no-input` to confirm the active Gitea account before mutating resources. Under `GITEA_TOKEN`, `gt auth status --no-input --json` omits `user` unless you pass `--verify`.
4. **Verify Target Repository**: Run `gt repo view --no-input --json full_name` to confirm the target repository. `gt` infers the repository from Git remotes and prefers `upstream` over `origin` on fork checkouts. If you want to target the fork instead of `upstream`, pass `-R OWNER/REPO` (`gt help environment` lists full precedence).

> [!IMPORTANT]
> If you are migrating commands from `tea`, replace plural subcommands and `--output` (`tea pulls`, `tea login list`) with singular `gt` commands (`gt pr`, `gt auth status`) plus `--no-input` and `--json`.

### Phase 2: Non-Interactive Rules & Quick-Start Workflows

Follow these non-interactive rules on every `gt` invocation:

- **Disable Prompts**: Pass `--no-input` on every command so `gt` never waits for input or opens an implicit editor or browser. Never pass `--editor` or `--web`, because they open an editor or browser even with `--no-input`.
- **Structured JSON Output**: Read data with `--json` and filter with `--jq` instead of parsing human text output. `--jq` runs inside `gt` without an external `jq` binary and prints strings without quotes. Use `--template` when you want a Go template layout (`gt help formatting`). Unknown `--json` fields fail immediately and list the valid field names.
- **Comment Count Caveat**: Unlike `gh`, the `comments` JSON field on issues and pull requests returns an integer count, not comment text. Read comment bodies with `gt issue comment list` or `gt pr comment list`.
- **Pagination Defaults**: List commands stop at `-L 30` by default and exit `0` when empty. Raise `-L` (up to `1000`) or paginate with `--page` before concluding an item does not exist.
- **Branch Inference**: Pull request commands without a number act on the pull request for the current branch.

#### Inspect CI Checks and Failed Job Logs

Check pull request commit statuses and read failed Gitea Actions job logs directly:

```sh
gt pr checks 12 --no-input                     # exit 0 passed, 1 failed, 8 pending
gt pr checks 12 --no-input --json name,state,url --jq '.[] | select(.state != "success" and .state != "skipped" and .state != "pending")'
gt run logs https://gitea.example.com/OWNER/REPO/actions/runs/34/jobs/71 --no-input
```

An Actions check `url` points to its job URL, and `gt run logs` accepts that URL to print one job. From a run ID, inspect jobs, wait for completion, or retry flaky failures:

```sh
gt run list --branch feature/login --status failure -L 5 --no-input --json id,workflow,title,conclusion
gt run view 34 --no-input --json jobs --jq '.jobs[] | {name, conclusion}'
gt run logs 34 --failed --no-input
gt pr checks 12 --watch --no-input
gt run watch 34 --no-input
gt run rerun 34 --failed --no-input
```

Read [references/monitoring.md](references/monitoring.md) for runner diagnostics, timeouts, and artifact downloads.

#### Move from an Issue to a Pull Request

Read the issue and conversation comments, commit on a branch with `git`, and open a pull request:

```sh
gt issue view 17 --no-input --json number,title,body,labels,state
gt issue comment list 17 -L 100 --no-input --json author,body,created_at
git switch -c fix/issue-17
# edit, test, and commit locally
gt pr create --no-input --yes --title "fix: describe the change" --body-file - <<'EOF'
Explain what changed and why.

Closes #17
EOF
gt pr checks --watch --no-input
```

`gt pr create` pushes an unpushed local branch only when `--yes` is passed, so ask the user before pushing. Read [references/resources.md](references/resources.md) for fork workflows, issue templates, and AGit patch-queue options.

#### Post Comments and Inline Reviews

Submit multi-line bodies with `--body-file` (or `--body-file -` and a quoted heredoc) instead of `\n` escapes inside `--body`:

```sh
gt issue comment 17 --no-input --body-file - <<'EOF'
Reproduced on main. Fix is in #18.
EOF
gt pr comment 18 --edit-last --no-input --body "Updated after review."
gt pr review 18 --approve --no-input --body "Looks good."
gt pr review 18 --request-changes --no-input --comments-file inline.json --body "See inline comments."
```

`inline.json` must be a real file on disk containing a JSON array of `{"path", "body", "new_position"}` (or `old_position`) entries on diff lines. When `--commit` is omitted, `gt` checks diff membership before submitting the review and refuses lines outside diff hunks. Read [references/resources.md](references/resources.md) for pending reviews and thread resolution.

### Phase 3: Confirmation, Push & Mutation Safety

> [!WARNING]
> Without a terminal, confirmation prompts fail with exit code `2`. Pass `--yes` only after explicit user approval for that specific mutation.

1. **Preview Writes**: Pass `--dry-run` on Gitea-only write commands (`issue close`, `pr merge`, `release create`, `repo delete`) to inspect outgoing requests before asking for approval. `gt` masks secrets in `--dry-run` output as `[REDACTED]`.
2. **Gate `--yes` Actions**: Obtain user approval before passing `--yes` for deletes, merges, branch cleanup, pending reviews, or branch pushes.
3. **Gate Promptless Writes**: Closing or reopening an issue or pull request asks no confirmation prompt. Write calls through `gt api` (`POST`, `PATCH`, `PUT`, `DELETE`) also skip confirmations, so ask the user before sending them.

### Phase 4: Verification Checklist

1. **CLI & Auth**: Confirm `gt --version` succeeds, `gt auth status --no-input --json` shows `credential_available: true`, and `gt api user --jq .login --no-input` returns the expected account.
2. **Target Repository**: Confirm `gt repo view --no-input --json full_name` matches the intended repository before any write.
3. **Output & Approval Discipline**: Confirm every read uses `--json`, every command passes `--no-input`, and every remote write had prior user approval.
4. **Post-Write State**: Branch on exit codes rather than parsing error text. After `gt pr create`, run `gt pr view --no-input --json url` to report the pull request link.

## Task Reference

Load only the reference file needed for your active task:

| Task | Command | Reference |
| :--- | :--- | :--- |
| Checks of a pull request | `gt pr checks 12 --no-input` | [references/monitoring.md](references/monitoring.md) |
| Wait for checks | `gt pr checks 12 --watch --no-input` | [references/monitoring.md](references/monitoring.md) |
| Logs of failed or canceled jobs | `gt run logs 34 --failed --no-input` | [references/monitoring.md](references/monitoring.md) |
| Follow a running job | `gt run logs 34 --job build --follow --no-input` | [references/monitoring.md](references/monitoring.md) |
| Rerun failed or canceled jobs | `gt run rerun 34 --failed --no-input` | [references/monitoring.md](references/monitoring.md) |
| Download artifacts | `gt run download 34 --name build --no-input` | [references/monitoring.md](references/monitoring.md) |
| Read an issue with comments | `gt issue view 17 --comments --no-input` | [references/resources.md](references/resources.md) |
| Open an issue | `gt issue create --no-input --title T --body-file -` | [references/resources.md](references/resources.md) |
| Close or reopen an issue | `gt issue close 17 --comment C --no-input` | [references/resources.md](references/resources.md) |
| Open a pull request | `gt pr create --no-input --title T --body-file -` | [references/resources.md](references/resources.md) |
| Read a pull request diff | `gt pr diff 18 --no-input` | [references/resources.md](references/resources.md) |
| Comment on a pull request | `gt pr comment 18 --no-input --body-file -` | [references/resources.md](references/resources.md) |
| Review with inline comments | `gt pr review 18 --comment --comments-file inline.json --no-input` | [references/resources.md](references/resources.md) |
| Reply to an inline comment | `gt pr review reply 18 1234 --no-input --body-file -` | [references/resources.md](references/resources.md) |
| Merge a pull request | `gt pr merge 18 --squash --delete-branch --no-input --yes` | [references/resources.md](references/resources.md) |
| Edit or delete a wiki page | `gt wiki edit Home --no-input --body-file -` | [references/resources.md](references/resources.md) |
| View or edit a repository | `gt repo view --no-input --json full_name` | [references/resources.md](references/resources.md) |
| Search issues or pull requests | `gt search issue crash --owner OWNER --no-input` | [references/search.md](references/search.md) |
| View your open work | `gt status --no-input --json pull_requests,assigned_issues,mentions,failing_runs` | [references/search.md](references/search.md) |
| Script `gt` in CI | `GITEA_TOKEN` and `GITEA_CLI_HOST` | [references/automation.md](references/automation.md) |
| Dispatch a workflow | `gt workflow run ci.yml --ref main --no-input` | [references/automation.md](references/automation.md) |
| Call raw Gitea REST endpoints | `gt api 'repos/{owner}/{repo}/...' --no-input` | [references/api.md](references/api.md) |
| Author a Gitea Actions workflow | `.gitea/workflows/*.yaml` | [references/workflow-authoring.md](references/workflow-authoring.md) |

## Exit Codes

Branch on numeric exit codes instead of matching stderr text (`gt help exit-codes` lists every code, and `GITEA_CLI_ERROR_FORMAT=json` emits structured JSON errors on stderr):

| Code | Meaning |
| :--- | :--- |
| `0` | Success, including an empty list result |
| `1` | Command failure, a failed check in `gt pr checks`, or instance timeout (`http_timeout`) |
| `2` | Usage error, or an interactive confirmation prompt that requires `--yes` |
| `3` | Canceled action: declined confirmation or prompt, or an expired `--timeout` during watch |
| `4` | Authentication missing or rejected by the Gitea instance |
| `5` | `gt run watch` or `gt workflow run --follow` completed without `success` |
| `6` | Head commit mismatch (`gt run watch --expect-head` or `gt pr merge --match-head-commit`) |
| `8` | `gt pr checks` found checks still pending |
| `130` | Interrupted by `Ctrl-C` (`SIGINT`) |

## When Not to Use

- **Local Git Operations**: Use `git` directly for commits, rebases, stashes, and local branch management.
- **GitHub or Other Forges**: `gt` communicates only with Gitea instances. Use `gh` for GitHub repositories (`github.com` or GitHub Enterprise).
- **Structured Engineering Workflows**: Pair this capability skill with dedicated methodology skills instead of improvising templates or review criteria:
  - Drafting or updating pull request descriptions: use `writing-prs`.
  - Conducting multi-scale code reviews on pull requests: use `reviewing-prs`.
  - Triaging, fixing, and resolving inline review threads: use `resolving-pr-feedback`.
  - Researching and authoring bug or feature issues: use `writing-issues-for-bugs` or `writing-issues-for-features`.
- **Host Server Administration**: Editing server-side `app.ini` or OS services lies outside `gt`, apart from endpoints exposed via `gt admin`, `gt api`, and `gt runner`.

## Attribution

Portions of this skill and `references/*.md` are adapted from the official Gitea CLI (`gt`) under the MIT License. See [NOTICE.md](NOTICE.md) for upstream copyright and permission terms.
