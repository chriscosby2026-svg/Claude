# Reel review: instagram.com/reel/Da5be6dJ6Fi

Source: https://www.instagram.com/reel/Da5be6dJ6Fi/ (66.2s)

## What it is

A two-character comedy skit (AI-voiced Peter Griffin and Stewie, over
looping Minecraft parkour footage) pitching a specific tool through
dialogue rather than direct-to-camera claims, cut with GitHub-page and
architecture-diagram overlays. As with both prior reviews in this
directory, nothing is actually run on screen — it's mockups and diagrams
— and it closes on the same off-platform funnel pattern: "join my
broadcast channel or check my Telegram from bio" instead of naming or
linking the repo, despite the dialogue calling the tool "open source" and
"#1 on GitHub" in the same breath.

**Claims made in the reel:**
- A tool called **RUFLO** (on-screen text also shows `claude-flow@v3`) is
  "ranked number one on GitHub," free, and "almost nobody knows about it."
- It spins up 60+ specialized AI agents ("queen" agents managing teams,
  "tactical" agents doing the work: researching, coding, testing,
  reviewing) that share a collective memory and "get better after every
  run."
- It automatically routes simple tasks to cheap models and complex tasks
  to powerful ones, cutting token usage "up to 50%" and extending Claude
  Code usage "by 250%."

## Verification (source-level, not the reel's word)

Unlike the previous two reels reviewed here, this one names a genuinely
well-established project, not a sudden-appearance one. **RUFLO is real**:
`github.com/ruvnet/ruflo`, MIT licensed, 72.8k stars / 8.6k forks. It's
the current name for **Claude Flow**, built by Reuven Cohen ("rUv"), which
has been public since roughly June 2025 — over a year of history, not a
brand-new repo riding a single viral post. The on-screen `claude-flow@v3`
text and the dialogue's "RUFLO" both refer to the same project mid-rename.
The core claims hold up structurally: 60+ role-based agents, swarm
topologies, a shared learning memory store (AgentDB), and cost-based model
routing are real, documented features, not invented for the reel. As
before, treat the specific numbers ("up to 50%," "250%") as the project's
own unaudited marketing math, not an independently verified benchmark.

**Security history is real and mixed, but — unlike the OmniRoute
review — shows an active pattern of disclosure and response, not silence:**

- **CVE-2026-59726 "RufRoot" (CVSS 10.0)**, affecting all versions before
  3.16.3: the default docker-compose deployment exposed an MCP bridge
  (`POST /mcp`, `POST /mcp/:group`) to the network with no authentication,
  giving an unauthenticated attacker 233 tools including
  `terminal_execute` — shell access in the bridge container, provider API
  key theft, and the ability to poison the AgentDB learning store.
  Reported June 30, 2026; **the maintainer shipped a fix within 24 hours**,
  in v3.16.3.
- **An obfuscated preinstall script shipped in versions
  3.1.0-alpha.55–3.5.2** that silently deleted npm cache files and
  directories matching certain patterns — a genuine supply-chain incident,
  only removed after external disclosure, not maintainer-initiated.
- **A March 2026 community security audit (issue #1375)** additionally
  alleged: a prompt-injection payload hidden in MCP tool descriptions that
  tried to get Claude to add the repo owner as a contributor without
  consent; `.swarm` files and background processes persisting after
  uninstall; open SQL-injection, path-traversal, and prototype-pollution
  reports; a community security-fix PR closed without merging; and no
  `SECURITY.md` at the time. No maintainer response to that specific issue
  was visible as of this review.
- **Against that history**, the project is under active, current
  development — latest release v3.42.4 was published 2026-09-17 (two days
  before this review), and the last several releases (v3.42.0–v3.42.4)
  specifically call out security hardening: Sybil-attack prevention and
  identity verification for hive-mind swarms, MCP governance enforcement,
  and Windows argument-escaping fixes. That's a materially different
  signal than a flagged issue sitting untouched.

**Net assessment:** more credible and better-maintained than the tool in
`reviews/DdcN448SbN3.md`, but not something to run with default settings
against a machine holding real credentials. The attack surface is large
by design (a multi-agent harness that executes shell commands, opens
network bridges, and installs via `npx`/a piped install script), it has a
documented history of both a maliciously-obfuscated shipped preinstall
script and a CVSS-10 unauthenticated-RCE default deployment, and at least
one audit's findings (prompt-injection-driven unauthorized repo
contribution, persistent post-uninstall artifacts) don't have a visible
maintainer response on record.

## Why nothing was built or vendored from this reel

Same standard applied in both prior reviews: `/watch` → `/skill-from-video`
turns a **demonstrated procedure** into a skill, and this reel demonstrates
nothing on screen — a comedy dialogue over unrelated gameplay footage,
diagrams, and a bio-link/Telegram funnel instead of a shown command or
repo link. Nothing was installed, run, or vendored here either.

## Bottom line for anyone who saw this reel

- The named project is real, mature, and MIT-licensed — this isn't a
  fabrication or an overnight star-farmed clone. It's a reasonable thing
  to *investigate* for real multi-agent Claude Code work.
- Before running it against anything with real secrets: pin to a version
  well past 3.16.3 (currently v3.42.4), never expose its MCP bridge to an
  untrusted network (the default docker-compose config has done this
  before), review what `npx ruflo@latest init` actually executes rather
  than piping the installer blind, and read issue #1375's findings
  yourself rather than taking either the reel's or this review's word for
  their current status.
- The reel's numbers ("50% token savings," "250% more usage," "#1 on
  GitHub") are the project's own claims relayed through a skit, not a
  benchmark anyone here independently verified.
- Same funnel pattern as the last two reviews: real information (a repo
  name) is withheld from the reel itself in favor of a Telegram/bio-link
  CTA. The actual source is public — `github.com/ruvnet/ruflo` — and
  didn't need to be gated behind a broadcast channel.
