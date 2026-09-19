# Reel review: instagram.com/reel/DdcN448SbN3

Source: https://www.instagram.com/reel/DdcN448SbN3/ (51.0s)

## What it is

A direct-to-camera pitch for a specific tool, cut with motion-graphics
overlays (dashboard mockups, a "model switching..." carousel, token
counters). No terminal session, config file, or command is actually shown
running — everything is a rendered mockup, not a screen recording of the
tool in use. It closes on a comment-gated CTA ("Comment AI, and I'll send
you the full setup") rather than a link, which is the same lead-gen pattern
flagged in the previous review (`reviews/DYAnUJCpCep.md`): claims first,
proof gated behind an off-platform DM.

**Claims made in the reel:**
- "Some guy on GitHub" made Claude Code "free with basically unlimited
  usage."
- A tool called **OmniRoute** connects Claude Code to 200+ AI models and
  gives "up to 2 billion free tokens a month."
- The moment a Claude Code session limit is hit, OmniRoute auto-routes the
  job to the next available model so the session "never stops."
- It compresses prompts by up to 90% before they reach the model.

## Verification (source-level, not the reel's word)

OmniRoute is real: `github.com/diegosouzapw/OmniRoute`, MIT licensed,
created February 2026, and genuinely large — roughly 58–68k stars and
550+ contributors by search-engine-cache snapshots in Sept 2026 (one
review site notes viral posts about it have also *overstated* its star
count in the other direction, e.g. quoting "12,000" when the real number
was 5x that — so treat any specific number, including the reel's "2
billion tokens," as unverified marketing math from the project's own
README, not an independently audited figure). It works as advertised at a
high level: a local-first AI gateway/proxy that Claude Code, Cursor, and
other agents point at instead of talking to Anthropic directly, with
provider fallback and prompt-compression features.

**This is also where it stops looking like a simple router and starts
looking like a real risk to run against a live coding session:**

- **Critical unauthenticated RCE — GHSA-hf57-cqmx-p4gr / CVE-2026-88062
  (CVSS 9.5), published 2026-09-03.** The `POST /api/acp/agents`
  "custom ACP agent" endpoint accepts attacker-controlled `binary` and
  `versionCommand` fields with no executable allowlist and runs them via
  `execFileSync` — arbitrary code execution on the machine running the
  gateway. Exploitable with no auth at all if `requireLogin=false`
  (a real default in some setups), or with a leaked/guessed management
  credential otherwise. No confirmed-patched version number was visible
  on the project's own security-advisory page as of this review.
- **Socket.dev flagged the npm package (v3.8.5) for supply-chain risk**
  (score 48/100): six AI-flagged potential-malware fragments, two
  obfuscated code blocks, and install scripts, plus specific flagged
  behaviors — an active MITM/TLS-interception component that installs a
  custom root CA, credential harvesting from the OS keychain via
  `keytar`, cloud sync of provider credentials to a remote endpoint, and
  privileged PowerShell elevation. As of this review that GitHub issue
  (#2863) shows no maintainer response recorded; a separate secondary
  source claims two vulnerabilities were closed in v3.8.6, but that
  fix was not independently confirmed against the flagged behaviors
  above — the two sources disagree and neither is a primary changelog
  entry, so treat this as unresolved rather than fixed.
- **A separate issue (#258) reports 3 critical, 2 high, and 4 low code
  vulnerabilities** found in the codebase, independent of the above.
- The project's own docs describe an *optional* transparent MITM proxy
  (`TPROXY`) with a per-site certificate authority as a real, documented
  feature (not just a false-positive scanner flag) — i.e. installing it
  is expected to mean trusting a locally-generated CA to decrypt your
  TLS traffic if you turn that feature on.

None of this makes OmniRoute a hoax — it's a genuine, popular, MIT project
that does what the reel describes at a functional level. But the thing
being pitched here is a local proxy that sees every prompt, every line of
code, and (per the flagged behaviors above) potentially every provider
credential your coding agent handles, and it currently carries a critical,
unauthenticated remote-code-execution advisory plus an unresolved
supply-chain flag on a past release. That is a materially different risk
profile from the plugins/skills vetted in the prior review, which were
either static prompts or ran with your own existing credentials rather
than intermediating all of them.

## Why nothing was built or vendored from this reel

Same standard as `reviews/DYAnUJCpCep.md`: the `/watch` → `/skill-from-video`
pipeline turns a **demonstrated procedure** into a runnable skill, and
this reel demonstrates nothing — it's motion-graphics claims about a
third-party tool, gated behind a comment-for-DM funnel rather than a link
shown on screen. There is also no world in which this repo installs a
network proxy with a documented MITM/root-CA capability and an open
critical RCE advisory as part of vetting a reel. If a low-risk, no-proxy
way to try free-tier model fallback is wanted later, that's a separate,
deliberate decision — not something to wire up because a reel said to
comment "AI."

## Bottom line for anyone who saw this reel

- Don't run `diegosouzapw/OmniRoute` against a machine or repo with real
  secrets or production code until GHSA-hf57-cqmx-p4gr has a confirmed
  patched version you've verified yourself, `requireLogin` is enabled
  with a strong management password, the custom ACP agent endpoint is
  disabled if unused, and you've decided for yourself whether you're
  comfortable with its optional MITM/root-CA feature.
- "2 billion free tokens" and specific star counts are the project's own
  marketing, not a verified figure — don't repeat them as fact.
- The reel's CTA ("comment AI" for the "full setup") is an engagement/DM
  funnel, not a demonstration; the real project is public on GitHub and
  doesn't require commenting on a video to find.
