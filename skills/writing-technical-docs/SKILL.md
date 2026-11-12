---
name: writing-technical-docs
description: |
  Write or rewrite technical documentation, pull request (PR) descriptions,
  GitHub and Gitea issues, code review comments, READMEs, runbooks, procedures, error
  messages, release notes, incident reports, ADRs, API guides, and specifications
  in plain, layman-readable English in the spirit of ASD-STE100 Simplified
  Technical English: short sentences, active voice, simple tenses, one word one
  meaning, condition before command, structured lists, and zero AI slop.
  Default mode is Plain. Strict mode applies full STE vocabulary compliance when
  the user names STE, ASD-STE100, or compliance. Also use when the user says
  "STE", "Simplified Technical English", "ASD-STE100", "plain English",
  "layman's terms", "explain it simply", "no jargon", "de-slop", "make this
  readable", "write for non-native readers", or asks for docs that translate well.
license: MIT - https://github.com/bjester/skills/blob/main/LICENSE
user-invocable: true
compatibility: claude-code cursor codex gemini-cli opencode antigravity
allowed-tools:
  - read_file
  - write_file
  - grep
  - find_by_name
metadata:
  author: Blaine Jester
  version: "2.4.1-curated"
  standard: ASD-STE100 Issue 9 (2025-01-15)
---

# Writing Technical Documentation

Purpose: Write clear, verifiable Plain English across technical documentation, specifications, READMEs, issues, pull requests, and code reviews with zero AI slop.

Write plain English that a smart reader outside your field understands on one read. The rules come from ASD-STE100, the controlled language aerospace uses so a tired mechanic cannot misread an instruction. Two registers exist: formal documents and conversational developer prose (chat replies, code reviews, and PR discussions). Each has its own rule set below.

## The Document

When writing or rewriting documentation, specifications, READMEs, ADRs, issues, or runbooks, apply these rules to the prose:

1. **Classify each passage.** Procedural text tells the reader what to do: imperative mood, 20 words per sentence, one instruction per sentence. Descriptive text explains: simple tenses, 25 words per sentence, one topic per paragraph, six sentences per paragraph at most. Per ASD-STE100 Rule 8.6, each backticked command/path/identifier, hyphenated unit, and parenthetical counts as one word.
2. **Never touch** code, identifiers, commands, flags, file paths, quoted errors, product names, or facts. Preserve official casing for proper nouns (`PostgreSQL`, `GitHub`, `TypeScript`, `macOS`, `GraphQL`) and wrap commands, flags, file paths, and environment variables in backticks. In `README`s and architecture guides, state durable policy and point to authoritative manifests (`pyproject.toml`, `package.json`, `Makefile`) instead of hardcoding volatile version pins or temporary *"not implemented yet"* status notes. If a source sentence is ambiguous and rewriting it could alter the meaning, mark `[verify: confirm whether X or Y]` rather than guessing.
3. **Condition before command, with a comma.** "If the build fails, read the log."
4. **Simple tenses, active voice.** No present perfect ("has completed" -> "completed"). No "-ing" verb after a comma (", making it easy" -> new sentence). Name the actor: "You run the migration."
5. **Modals: can, will, must.** Never should, would, may, might, could. A required "should" becomes "must". An optional one is deleted. *Exception*: In software engineering specifications, acceptance criteria, and test scenarios, Behavior-Driven Development (BDD) phrasing (for example, "X should do Y", "it should return 404") is allowed to specify expected software behavior.
6. **Complete grammar.** No contractions in formal documents, keep articles, keep "that". Short sentences, not telegraph style.
7. **No semicolons and no em-dashes.** Write two sentences, or name the relation ("because", "but", "so").
8. **One word, one meaning, for the whole document.** Do not alternate between `config`, `settings`, and `options` for the same file in one document. Standard engineering verbs (`verify`, `check`, `confirm`, `validate`) are permitted in Plain mode; replace `ensure` per `references/word-swaps.md` (`verify`, `check`, or `make sure that`), and reserve mandatory `"make sure that"` / `"configuration"` vocabulary locks for Strict mode. Break noun chains over three words with a preposition ("the timeout value for the connection pool").
9. **State what the reader needs before you name the action.** Define a concept term at its first use, under ten words, one per sentence. Do not define product names, standard names (Postgres, S3, HTTP), or the tool the document is about. Name the host, the flag, or the prior step that a command depends on: "Restart the `sync` service on the host that runs the job."
10. **State the fact, not its importance.** Delete words that carry no fact: simply, seamlessly, robust, powerful, comprehensive, leverage, crucial, "in order to", "it is worth noting", "this PR aims to". No "not just X, it is Y". No decorative triplets. No "in conclusion".
11. **Format for the eye, not for decoration.** Use numbered or bulleted vertical lists for sequences, options, or three or more parallel items: colon on the lead-in, uppercase start, one instruction per item. Bold lead-in labels on list items (`- **Timeout**: 30 seconds.`) are permitted for parallel named properties; never bold words mid-sentence for dramatic emphasis. Omit emojis unless required by a structured workflow schema (such as `reviewing-prs` severity badges). Outside repository templates (PRs, issues, ADRs), every heading must cover at least three sentences or a structured list/table.
12. **Warnings: command or condition first, then the risk.** "Do not run this against production. The command deletes rows."

Use American spelling. `references/word-swaps.md` maps overused AI words to plain ones. For an error message, runbook, incident report, release note, commit message, PR description, issue, or UI copy, read `references/use-cases.md` first.

**Before (real AI output):**

> **Connection timeouts.** If sqlpipe hangs or fails with `dial tcp: i/o timeout`, check that the host running sqlpipe can reach the Postgres port (usually 5432) — this is often a security group or firewall rule blocking the connection. If you're connecting to a managed database (RDS, Cloud SQL, etc.), confirm the instance allows connections from sqlpipe's IP.

**After (procedural, headed, numbered):**

> ## Connection timeouts
>
> sqlpipe stops with `dial tcp: i/o timeout` when it cannot connect to the Postgres port (5432 by default).
>
> 1. Verify that the host running sqlpipe can connect to the Postgres port. A firewall or security group usually blocks it.
> 2. If the database is managed (RDS, Cloud SQL), verify that the instance accepts connections from the IP of sqlpipe.

## Chat Explanations, Code Reviews & PR Discussions

When explaining technical concepts in chat, writing PR descriptions, or posting code review comments:

1. The first sentence gives the direct answer, summary outcome, or concrete defect. Do not restate the prompt or open with "This PR aims to".
2. Format cleanly for readability. Numbered steps, bulleted lists, and `- **Label**:` lead-ins are encouraged for sequences and parallel items; never bold words mid-sentence for emphasis.
3. No em-dashes (`—`) or spaced hyphen clause-splices (` - `). Name the relation ("because", "but", "for example") or write two sentences.
4. Define a concept term in a few words the first time you use it: "idempotent (safe to run twice)". Do not define product names.
5. Natural contractions (`don't`, `doesn't`, `isn't`, `won't`, `can't`) are permitted in chat, code reviews, and PR discussions. Never use conversational openers ("Certainly", "Great question") or closers ("I hope this helps", "Let me know").
6. Do not shorten quoted error text, security warnings, or confirmations before a destructive action.

**Before:** The failure stems from control-plane leader election during pod churn — nothing to worry about!
**After:** The pods restarted and the queue lost its leader for a short time. It recovered without help. You don't need to do anything.

## Self-Check Before You Deliver

1. **Chat, Reviews & PRs**: Search for conversational openers/closers, `—`, ` - `, `not just`, `aims to`, `ensure`, `, ensuring`, `, making`, `, highlighting`, and mid-sentence `**...**` emphasis. Verify the opening sentence states the direct answer, change intent, or concrete defect.
2. **Document**: Count the words in your three longest sentences (counting backticked code/paths and parentheticals as one word each). Split sentences over 20 (procedural) or 25 (descriptive). Search for `'`, `has been`, `should` (unless specifying software behavior or BDD scenarios), `may`, `;`, `—`, ` - `, `ensure`, `, ensuring`, `, making`, `, highlighting`, `not just`, `aims to`, mid-sentence `**...**` not acting as a `- **Label**:` list/key prefix, and any non-template heading covering fewer than three sentences or a structured list/table. Fix each hit. Verify each procedural step names the host, flag, or prior step the reader needs.

## Modes

**Plain** is the default and applies all rules above. **Strict** applies when the user names STE, ASD-STE100, or compliance: read `references/strict-vocabulary.md` before drafting, enforce strict dictionary verb/noun locks (`make sure that`, `configuration`, no bold lead-ins), and state once that no tool guarantees compliance. Chat replies stay Plain in every mode.

When asked to CHECK text instead of writing it, open `references/rule-catalog.md` first. Report each violation with the rule number quoted from that file, the offending text, and a compliant rewrite. Never cite a rule number from memory. When the user asks for compliance, end with one sentence: no tool can guarantee ASD-STE100 compliance, and the standard is a free download at asd-ste100.org.

## Limits

These rules are for facts and instructions, not marketing copy or brand writing: they delete persuasion by design. Say so, and offer them for the docs instead.

## References

- `references/rule-catalog.md`: the 53 rules of Issue 9 with software examples, for CHECK mode
- `references/strict-vocabulary.md`: the dictionary discipline for Strict mode
- `references/word-swaps.md`: slop-to-plain word map (shared reference)
- `references/use-cases.md`: mode and pattern for error messages, runbooks, incident reports, release notes, commits, PRs, issues, code reviews, agent prompts, UI copy, and translation prep
