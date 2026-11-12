# Shared Guidelines for Forge CLI Selection and Identity Gates

This reference defines the target-resolution sequence, active account checks, and identity gates for repository skills. Skills use `gh` for GitHub repositories and `gt` for Gitea repositories. Before executing any remote issue, pull request, or review command, run the selection gate below.

---

## Forge Selection Gate

Follow these steps in order to resolve the target repository and select the forge CLI binary:

1. **Explicit URL Precedence**: If the user supplies an issue or pull request URL, extract the hostname and `OWNER/REPO` directly from that URL.
2. **Git Remote Resolution**: If the user supplies no URL, inspect `git remote -v`. If `upstream` is present, select `upstream`. Otherwise select `origin`. Both `gh` and `gt` target `upstream` over `origin` on forks. When operating on the fork repository itself, pass `-R OWNER/REPO` explicitly. Verify target resolution with `gh repo view --json nameWithOwner` or `gt repo view --no-input --json full_name`.
3. **CLI Binary Selection**:
   - **GitHub (`gh`)**: If the target host is `github.com`, matches `GH_HOST`, or succeeds under `gh auth status --hostname <host>`, select `gh`. Verify authentication with `gh auth status` (or `gh auth status --hostname <host>` for GitHub Enterprise).
   - **Gitea (`gt`)**: Otherwise inspect `gt auth status --no-input --json host,credential_available`, `GITEA_CLI_HOST`, `GITEA_INSTANCE_URL`, and `.gitea/`. Compare normalized hostnames because `host` in `gt auth status --no-input --json` is a full instance URL (`https://...`), whereas SSH remotes yield a bare hostname. If the target hostname matches a Gitea instance with configured credentials (`credential_available == true`), select `gt` and confirm token validity with `gt api user --jq .login --no-input` (or `gt auth status --verify --no-input --json`). Pass `--no-input` on every `gt` command. Never pass `--editor` or `--web`. Pass `--yes` only after explicit user approval.
   - **Unmatched Host or Missing Credentials**: Never hardcode private, LAN, or Tailscale Gitea hostnames. If neither CLI matches the target host or credentials are missing, halt immediately. Ask the user which forge CLI and host configuration apply. Never run `gh` against Gitea or `gt` against `github.com`. Never invoke interactive `gh auth login` or `gt auth login`.

---

## Active Identity Lookup

Before mutating issues, pull requests, or reviews, query the active CLI login. Never echo token environment variables (`GH_TOKEN`, `GITEA_TOKEN`) or pass tokens on command lines.

- **GitHub (`gh`)**: Run `gh api user -q .login`.
- **Gitea (`gt`)**: Run `gt api user --jq .login --no-input`. Prefer this query over `gt auth status --no-input --json` because `GITEA_TOKEN` environment credentials leave `user` empty unless you pass `--verify`.

---

## Identity Gates

Repository workflows separate author mutations from reviewer verdicts. Before sending any write request, verify that the active CLI account matches the required role. If a bot override or stale token violates that boundary, halt immediately.

### Author Identity Gate

Before mutating a pull request, run the author check for your workflow:

- **Pull Request Creation and Editing (`writing-prs`)**: Compare the active CLI login against `git config user.name` and `git config user.email`. If a dedicated bot or reviewer account (`*-bot` or `*bot`) is active on human commits, halt immediately. If a human account is active on bot commits without explicit user direction, halt immediately as well. Save the drafted Markdown locally and ask the user whether to switch credentials.
- **Review Thread Resolution (`resolving-pr-feedback`)**: Compare the active CLI login against the pull request author login. Read `pr.author.login` on `gh`, or read the flat `author` string from `gt pr view --no-input --json author`. If the logins do not match, halt immediately with a hard failure before committing, pushing, replying, or resolving threads. If the user explicitly authorizes co-maintainer resolution in the current session, you can proceed across mismatched logins.

> [!WARNING]
> Do not switch credentials automatically with `gh auth switch`, `gh auth login`, or `gt auth login`. Report the active login and expected author login, then wait for user instruction.

### Reviewer Identity Gate

Before staging or publishing a remote review in `reviewing-prs`, enforce the self-review block:

1. Query the active CLI login and the pull request author login (`pr.author.login` on `gh`, or flat string `author` on `gt`).
2. Before staging (`Mode A: Pending Review`) or publishing (`Mode B: Published Submission`) to GitHub or Gitea, compare both logins case-insensitively.
3. If the logins match, abort immediately with a hard failure before submitting.
4. Local chat-only pull request analysis without remote submission remains permitted.

---

## Key Schema & Flag Differences (`gh` vs. `gt`)

`gt` mirrors `gh` subcommand names, but its JSON schemas, pagination limits, and review flags differ. Follow this boundary map across all dual-forge skills:

| Capability | GitHub (`gh`) | Gitea (`gt` with `--no-input`) |
| :--- | :--- | :--- |
| **Active CLI user login** | `gh api user -q .login` | `gt api user --jq .login --no-input` (`gt auth status --no-input --json` leaves `user` empty under `GITEA_TOKEN` without `--verify`) |
| **Configured hosts check** | `gh auth status`, `gh auth status --hostname <host>`, or `GH_HOST` | `gt auth status --no-input --json host,user,active,credential_available` (compare normalized hostnames against `host` URLs) or `GITEA_CLI_HOST` |
| **PR metadata & author** | `gh pr view <id> --json number,title,body,baseRefName,headRefName,headRefOid,url,closingIssuesReferences,author,commits` (`author.login` is nested) | `gt pr view <id> --no-input --json number,title,body,state,draft,url,base,head,head_sha,mergeable,review_decision,reviews,author` (`author`, `base`, and `head` are flat strings, with no `commits` field) |
| **PR commit list** | `gh pr view <id> --json commits` or `git log` | `git log origin/<base>..<head_sha> --oneline` or `gt api --no-input --paginate 'repos/{owner}/{repo}/pulls/<num>/commits'` |
| **Conversation comments** | `gh pr view <id> --comments` | `gt pr comment list <id> -L 100 --no-input --json id,author,body,created_at` and `gt issue comment list <id> -L 100 --no-input --json id,author,body,created_at` (`comments` in JSON is an integer count, and `--comments` rejects `--json`) |
| **Pagination default** | Varies by subcommand (`--limit 30` on `list`) | Stops at `-L 30` by default (raise `-L` up to `1000` or pass `--page` before concluding items are missing) |
| **Duplicate issue search** | `gh issue list --search "<keywords>" --state all --limit 20` | `gt issue list -S "<keywords>" --state all -L 20 --no-input --json number,title,state,url` |
| **Inline review threads** | `gh api repos/{owner}/{repo}/pulls/<num>/comments` or GraphQL `reviewThreads` (`isResolved` boolean, `line`, `originalLine`) | `gt pr review comments <num> -L 1000 --no-input --json id,review_id,path,line,old_line,author,resolver,body,created_at` (group by `[.path, .line, .old_line]`; unresolved when `all(.resolver == "")`; uses `old_line` for deleted lines) |
| **Stage or publish review** | `gh api repos/{owner}/{repo}/pulls/<num>/reviews --method POST --input payload.json` (omit `event` for pending, set `event` to publish) | Re-verify `head_sha`, then run `gt pr review <num> --pending --body-file summary.md --comments-file inline.json --no-input` (omit `--commit` so `gt` validates diff lines before submitting; pass `--approve`, `--request-changes`, or `--comment` to publish) |
| **Reply & resolve thread** | GraphQL `addPullRequestReviewThreadReply` and `resolveReviewThread` | `gt pr review reply <num> <root-id> --no-input --body-file -` and `gt pr review resolve <num> <root-id> --no-input` (`resolve` rejects `--json` and `--jq`) |
