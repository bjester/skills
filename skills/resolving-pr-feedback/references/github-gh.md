# GitHub (`gh`) Adapter for Resolving PR Feedback

Load this adapter when the `Forge Selection Gate` in `references/forge-cli.md` selects GitHub (`gh`).

---

## 1. Authentication, Identity & PR Metadata

1. Verify `gh` authentication and query the active GitHub login:
   ```bash
   gh auth status
   gh api user -q .login
   ```
2. Query pull request metadata and author identity (pass `<pr-number>` when not on the PR branch, and add `-R OWNER/REPO` when targeting a fork PR directly):
   ```bash
   gh pr view --json number,title,baseRefName,headRefName,headRefOid,author
   ```
3. Run the **Author Identity Gate**: compare the active login from `gh api user -q .login` against `pr.author.login` (nested object field on GitHub). Halt immediately on mismatch unless the user explicitly authorized co-maintainer resolution in the current session.

---

## 2. Enumerating Unresolved Review Threads

`gh pr view --comments` returns only top-level conversation comments and omits inline diff review threads. Query inline threads with the GitHub GraphQL API:

```bash
gh api graphql -f query='
  query($owner: String!, $repo: String!, $pr: Int!) {
    repository(owner: $owner, name: $repo) {
      pullRequest(number: $pr) {
        headRefOid
        reviewThreads(first: 100) {
          nodes {
            id
            isResolved
            path
            line
            originalLine
            comments(first: 10) {
              nodes {
                id
                author { login }
                body
                createdAt
              }
            }
          }
        }
      }
    }
  }' -F owner=':owner' -F repo=':repo' -F pr=<pr-number>
```

- Filter the response to threads where `isResolved == false`.
- Record each unresolved thread's GraphQL `id` (for example, `PRRT_...`), `path`, `line` (or `originalLine` when lines shifted or were deleted), and `comments.nodes` (`author.login`, `body`, `createdAt`).
- If `reviewThreads` has 100 nodes, paginate with `pageInfo { hasNextPage endCursor }` and `after: $cursor` so later threads are not missed.
- Also check top-level review bodies so summary-only requests are included in triage:
  ```bash
  gh api repos/{owner}/{repo}/pulls/<pr-number>/reviews --jq '.[] | select(.body != "") | {id, user: .user.login, state, body}'
  ```

---

## 3. Replying to Inline Review Threads

Push your verified commit(s) to the remote pull request branch before replying. Then post an evidence-backed reply to each addressed thread with `addPullRequestReviewThreadReply`. Read `body` from stdin via `-F body=@-` with a single-quoted heredoc so backticks in `<test command>` are never expanded by the shell:

```bash
gh api graphql -f query='
  mutation($threadId: ID!, $body: String!) {
    addPullRequestReviewThreadReply(input: {pullRequestReviewThreadId: $threadId, body: $body}) {
      comment { id url }
    }
  }' -f threadId="<THREAD_ID>" -F body=@- <<'EOF'
Addressed in commit <SHA>. <Brief explanation of fix>. Verified with `<test command>` (<result>).
EOF
```

---

## 4. Resolving Review Threads

After pushing the commit and posting the reply, mark the review thread resolved with `resolveReviewThread`:

```bash
gh api graphql -f query='
  mutation($threadId: ID!) {
    resolveReviewThread(input: {threadId: $threadId}) {
      thread { id isResolved }
    }
  }' -f threadId="<THREAD_ID>"
```

Verify that the response reports `"isResolved": true` for `<THREAD_ID>`.
