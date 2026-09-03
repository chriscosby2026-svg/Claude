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
