# Use cases beyond documentation

STE was built for aircraft maintenance manuals. The same properties transfer to any text where a misreading has a cost: one meaning per word, short sentences, condition-first commands. Each case below names the mode and the adaptations.

## Error messages and CLI output

Mode: procedural. An error message is an instruction to a stressed reader at 2 a.m., so it is the highest-value target.

Pattern: state what happened (simple past), state the cause if known, give the command or condition that fixes it.

> Before: Oops! Something went wrong while attempting to establish a connection. Please ensure your credentials are properly configured and try again.
> After: Connection to the database failed. The password for user `app` was not correct. Set `DB_PASSWORD` and connect again.

## Runbooks and standard operating procedures

Mode: procedural, with the 20-word limit enforced hard. An on-call runbook is a maintenance manual, which is what STE was made for.

- Every step is imperative, one instruction per step, condition first.
- A warning comes before its step: command first, risk second.
- An operator under pager stress reads each sentence once, so the 20-word limit is not negotiable.
- List required access roles, CLI tools, and target cluster/environment before Step 1.
- State the expected output that confirms each command succeeded before the operator runs the next step.
- End with measurable recovery verification, a rollback procedure, and an escalation condition.

## READMEs and onboarding guides

Mode: descriptive for system overviews (25-word limit), procedural for setup steps (20-word limit).

- Verify every command, script, environment variable, and default against `Makefile`, `package.json`, `pyproject.toml`, or `.env.example`—never invent flags or commands.
- State prerequisites, required runtimes, and credential configurations before the first installation command.
- Keep setup steps linear, copy-pasteable, and deterministic.

## Architecture Decision Records (ADRs)

Mode: descriptive.

- Structure records into 5 standard sections: `Status`, `Context`, `Decision`, `Alternatives Considered`, and `Consequences`.
- Apply the 25-word limit to context and rationale sentences.
- Never delete superseded ADRs—update status and mark `Superseded by ADR-NNN`.

## Incident reports and postmortems

Mode: descriptive, simple past only. A timeline in present perfect ("we have identified") hides when things happened.

> Before: We have identified an issue that may have impacted some users' ability to access the service.
> After: Between 14:02 and 14:31 UTC, 12% of requests failed. A deploy at 14:00 removed the cache warmup step.

STE bans hedges such as "may have impacted". The report states what is known and says "unknown" for the rest. It reads more honest because it is.

## Commit messages and PR descriptions

Mode: imperative subject line, descriptive body. The convention already matches STE. Apply the word swaps and the 25-word limit to the body. Delete "this PR aims to".

## API changelogs and release notes

Mode: descriptive. One entry, one change, one sentence where possible. A "Breaking:" entry follows the warning pattern, command first: "Update your calls to `v2/users`. The `name` field split into `first_name` and `last_name`."

## Software specifications and BDD scenarios

Mode: descriptive and behavioral. Describing software behavior like "X should do Y" is standard in software engineering.

- Use "should" to state observable software behavior and acceptance criteria: "The auth service should reject expired tokens."
- Keep sentences short and clear (the 25-word limit still applies).
- Distinguish between human procedural rules (which use "must" or imperative mood: "You must run the migration") and software behavioral expectations (which can use "should").

## Instructions for AI agents (prompts, AGENTS.md, skills)

Mode: procedural. A system prompt is a procedure for a reader that cannot ask questions, which is the exact reader STE was designed for.

- One instruction per sentence keeps each rule quotable and hard to half-follow.
- One word, one meaning stops the model from treating "check", "verify", and "validate" as three operations.
- A condition first ("If the build fails, stop") beats a trailing condition, which models drop.
- No "should". A model reads "should" as optional. Write "must" or delete the rule.

## Support macros and status-page updates

Mode: descriptive, 25-word limit. Non-native readers are the majority of many user bases. Not "we sincerely apologize for any inconvenience this may have caused" but "The API was down for 18 minutes. Uploads made during this time were saved and will process today."

## Translation and localization prep

Mode: strict. The original purpose of STE was English that non-native maintenance crews can read, and it doubles as pre-editing for machine translation. One meaning per word plus complete grammar (articles, "that") removes most translation ambiguity. If your docs get localized, STE cuts the error rate and the cost.

## UI copy and empty states

Mode: procedural, hard length limits. Buttons and labels are technical names and are exempt. Body copy follows the rules: "No projects yet. Create a project to start."

## Where STE does not fit

Marketing pages, launch posts, blog voice, brand writing. STE deletes persuasion on purpose. Write those in your own voice. Then use STE for the docs that the landing page links to.
