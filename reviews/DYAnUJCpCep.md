# Reel review: instagram.com/reel/DYAnUJCpCep

Source: https://www.instagram.com/reel/DYAnUJCpCep/ (93.6s)

## What it is

A "top 6 tools" listicle presented direct-to-camera: a speaker names six
Claude Code plugins/skills, gives each a one-sentence pitch plus a
follower/star-count flex, and closes with an engagement-bait CTA ("DM me
the word 'skill'"). No prompt, command, or before/after output is shown for
any of them — there's nothing demonstrated on screen, only claims.

Named in the reel:

1. **Superpowers** (`github.com/obra/superpowers`) — claimed to keep Claude
   from "jumping around" in code via a plan → write → test → review loop.
2. **frontend-design** — an Anthropic-built skill for higher-quality UI
   output.
3. **Code review** — described as 5 parallel agents checking code from
   different angles.
4. **Security review** — scans a codebase for vulnerabilities before ship.
5. **claude-mem** (`github.com/thedotmack/claude-mem` or similar) — a
   persistent-memory/compression system across Claude Code sessions.
6. **gstack** — a Gary Tan (Y Combinator) plugin bundling ~23 role-specific
   skills (exec, engineering, distribution, etc.).

## Why nothing was built from this one

This repo's `/watch` → `/skill-from-video` pipeline exists to turn a
**demonstrated procedure** into a runnable skill. This reel demonstrates
no procedure — it's a set of pointers to other people's existing
plugins, asserted rather than shown. Running it through that pipeline
would mean fabricating steps that were never actually shown, so it's
flagged here as a discovery list instead of a build task.

Two of the six items (`code-review`, `security-review`) already exist as
skills available to this session; they weren't sourced from this reel.
The other four (`superpowers`, `frontend-design`, `claude-mem`, `gstack`)
are third-party repos/plugins this review did not vendor in, since pulling
in another project's code on the strength of a single unverified promo
reel — without reading its source, license, or checking for anything
unsafe — isn't something to do without asking first.

## Suggested follow-up

If any of the four are wanted in this repo, the next step is to fetch and
read each one's actual source/README (not just the reel's claims) before
deciding whether to add it as a skill, a git submodule, or just a link in
the README.
