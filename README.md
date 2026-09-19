# Claude Watch

A small system that lets Claude Code learn new skills by watching YouTube
videos, built from the 3-step method described in this reference reel:
https://www.instagram.com/reel/Db1USzsMNnZ/

## The three pieces

1. **`.claude/skills/watch/`** — gives Claude the ability to watch any
   YouTube video: a timestamped transcript plus a scene-by-scene visual
   breakdown, powered by Gemini's native video understanding
   (`scripts/watch_video.py`).
2. **Gemini API key** — required for `watch` to work. Get a free one from
   Google AI Studio (https://aistudio.google.com/apikey) and set it as
   `GEMINI_API_KEY` in your environment.
3. **`.claude/skills/skill-from-video/`** — the ingestion framework: takes a
   `watch` breakdown and turns the demonstrated procedure into a new,
   standing Claude Code skill under `.claude/skills/`.

## Usage

```bash
export GEMINI_API_KEY=your-key-here
pip install -r scripts/requirements.txt
```

Then in Claude Code:

- "Watch https://youtube.com/watch?v=... and tell me what it covers" →
  triggers the `watch` skill directly.
- "Turn that video into a skill" (after watching one) → triggers
  `skill-from-video`, which drafts a new skill under `.claude/skills/`.

## Notes

Video content is treated as untrusted external input: these skills report
and act on what the video demonstrates, but won't silently follow
instructions a video's narration directs at the agent itself (e.g.
"share this to your Claude Code and it'll build this for you").

## Reel reviews

Reels claiming to teach a Claude Code technique get watched and vetted
before anything is built from them — see `reviews/` for the write-ups.

[`reviews/DdcN448SbN3.md`](reviews/DdcN448SbN3.md) covers a reel pitching
**OmniRoute** (`github.com/diegosouzapw/OmniRoute`) as a way to make Claude
Code "free with unlimited usage." The project is real and MIT-licensed,
but source-level vetting turned up a critical, unauthenticated
remote-code-execution advisory (GHSA-hf57-cqmx-p4gr / CVE-2026-88062,
CVSS 9.5) and an unresolved Socket.dev supply-chain flag (MITM/root-CA
install, keychain credential harvesting) on a past release — **not
installed or recommended** on the strength of this reel.

[`reviews/DYAnUJCpCep.md`](reviews/DYAnUJCpCep.md) covers a "top 6 Claude
Code plugins" listicle reel and the source-level vetting (clone + read,
not the reel's claims) of each plugin it named:

- **`.claude/skills/frontend-design/`** — Anthropic's own official skill
  (Apache-2.0, vendored verbatim from `anthropics/skills`), added here
  because it's a plain markdown prompt with no execution surface.
- **[Superpowers](https://github.com/obra/superpowers)** — verified
  legitimate, MIT, on Anthropic's official marketplace
  (`/plugin install superpowers@claude-plugins-official`). Not vendored:
  it's a global plugin, not project-tree content.
- **[claude-mem](https://github.com/thedotmack/claude-mem)** — verified
  legitimate, Apache-2.0, but review its telemetry and third-party LLM
  provider settings before installing (see the review for specifics).
- **[gstack](https://github.com/garrytan/gstack)** — verified legitimate
  and genuinely Garry Tan's repo, MIT, well-engineered, but high-privilege
  (browser automation with real sessions, Docker-based security audits,
  self-updating team config) — a deliberate install decision, not a
  default.
