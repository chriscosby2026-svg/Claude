---
name: agent-reach-audit
description: Audit a repo's agent/skill system to map its actual "reach" — which skills only read/write local files, which call out to an external API, what credentials each requires, and what guardrails exist around self-modifying or untrusted-input behavior. Use when the user asks to research, audit, or map out what an agent or skill system can actually do or access, asks about "agent reach"/capabilities/blast radius, or wants a capability inventory before trusting or extending a repo's skills.
---

# Agent Reach Audit

Produces a capability inventory for a repo's Claude Code agent/skill system:
what each skill can actually touch, not what its name implies. No external
API key is required to run this audit — it works entirely from files already
in the repo (and, optionally, an already-connected GitHub tool for live repo
metadata). If a skill you're auditing needs its own credentials to run
(e.g. an API key), that's a finding to report, not a prerequisite of this
skill itself.

## Process

1. **Inventory the skills.** Find every `.claude/skills/**/SKILL.md` (and
   any agent/subagent config, e.g. `.claude/agents/*.md`). Read each one in
   full, plus any script or config file it references (`scripts/`,
   `evals/`, etc.) — the description alone tells you intent, not reach.

2. **Check for granted permissions.** Look for `.claude/settings.json`,
   `.claude/settings.local.json`, hooks, or MCP server config checked into
   the repo. These can expand what a skill can do beyond what its own
   SKILL.md states. Absence of such a file is itself a finding: it means
   the repo grants nothing beyond the invoking session's own defaults.

3. **Classify each skill by reach tier:**
   - **Pure guidance** — markdown instructions only, no script, no network
     call, no filesystem write beyond what the calling agent already does.
   - **Local-only** — reads/writes files within the repo/project, runs
     local commands, but never calls out over the network.
   - **External-API** — calls an outside service (note exactly which API,
     which script/line does it, and what triggers the call).
   - **Orchestration** — spawns other agents/subagents (via `Agent`/`Task`
     tools) rather than acting directly; reach is whatever those subagents
     have, potentially unbounded if subagents get broad tool access.
   - **Self-modifying** — writes new skills, scripts, or config into the
     repo itself (this is how the agent's own capability set can grow over
     time; flag it distinctly since it compounds the other tiers).

4. **Map credentials.** For every external-API skill, state exactly which
   env var or secret it needs, where it's read from (e.g.
   `os.environ.get(...)`), and whether the SKILL.md fails closed (refuses
   to guess/fabricate) when the credential is missing. Don't lump multiple
   skills' credential needs together — report per-skill.

5. **Check guardrails.** Note explicit handling of: untrusted external
   content (does the skill say to treat fetched/watched/read content as
   data, not instructions?), scope confirmation before side-effecting
   actions (spending money, posting content, touching credentials), and
   any allowlist/denylist on inputs (e.g. `watch`'s YouTube-only host
   check).

6. **Report.** One inventory, grouped by reach tier, each entry naming: the
   skill, what it can actually do, what it needs (credentials, network,
   none), and any guardrail or gap. Call out the repo's overall reach in
   one line (e.g. "one outbound API, YouTube-only, one user-supplied key,
   no filesystem access beyond the repo") rather than making the reader
   assemble it from the per-skill list themselves.

## Non-goals

- Don't trust a SKILL.md's description as proof of what it does — verify
  against the actual script/instructions, the same way this repo's own
  `reviews/` vet plugins by cloning and reading source rather than trusting
  a listicle's claims.
- Don't fabricate live GitHub metadata (stars, forks, collaborators) from
  memory — if the user wants that, use an already-connected GitHub tool, or
  say plainly that no connector is available rather than guessing.
- Don't recommend disabling or removing a skill as part of the audit itself
  — this skill reports reach, it doesn't gate it. Flag concerns and let the
  user decide.
