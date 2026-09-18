---
name: orchestrator-loop
description: Break a brain-dumped list of multiple independent tasks into specs, delegate them to parallel subagents via the Agent tool, review each result against its spec and send back fixes until it holds up, then report one consolidated summary to the user. Use when the user dumps several things they need done at once and wants them parallelized or delegated, or explicitly asks to "orchestrate", "delegate to sub-agents", "run this as an orchestrator loop", or "spec this out and have workers build it". Not for a single simple task — spawning subagents only pays off when there are multiple genuinely independent chunks of work.
---

# Orchestrator Loop

Turns a pile of tasks into a plan, farms the independent pieces out to
parallel subagents, checks their work against spec, and only then reports
back — so the orchestrating conversation spends its own budget on planning
and review instead of doing every task itself serially.

This is a pattern for *this* conversation to follow using the `Agent` tool,
not a separate program. Spawning subagents has real cost — it trades your
own token budget for subagent budget and wall-clock time, it doesn't make
the work free. Reserve it for cases where the task list actually benefits:
several independent, parallelizable chunks of nontrivial work. A single
task, or tasks that all depend on each other's output, don't need this —
just do them directly.

## Process

1. **Intake.** Get the full task list. If the user brain-dumped it, work
   from that; if they only described one thing, ask what else is in scope
   before spinning up the machinery, or just do it directly if it's really
   one task. Split the list into discrete specs — each one scoped so a
   fresh subagent with zero conversation history could execute it without
   guessing at context. For each spec, write down: what to do, why it
   matters, which files/areas it touches, and what "done" looks like. This
   mirrors the Agent tool's own prompting guidance — a terse instruction
   produces shallow work, a briefed one doesn't.

2. **Delegate.** Group specs by independence. Tasks that don't depend on
   each other's output go out together: call `Agent` for each of them in
   the *same* response so they actually run in parallel, not one after
   another. Tasks that depend on a prior task's result wait for that
   result first. Use `run_in_background` unless your very next action
   depends on a specific subagent's result and nothing else is useful to
   do meanwhile — the default is background so independent work can
   proceed without blocking on it. Track the list with `TaskCreate` /
   `TaskUpdate` if the number of specs is large enough that keeping it in
   your head risks dropping one.

3. **Review loop.** When a subagent reports back, check its result against
   the spec you gave it, not just against "did it produce something" —
   does it actually satisfy the requirement, does it cut corners, does it
   match the repo's existing conventions. Never fabricate or assume a
   result before the real completion notification arrives; if you're
   tempted to guess what a background agent will say, that's the signal to
   wait instead. If the result falls short, send back a specific,
   concrete fix request (what's wrong, not just "try again") — either to
   the same subagent via `SendMessage` if it's still addressable, or a
   fresh one with full context otherwise. Repeat per task until it holds
   up. Cap this at a small number of rounds per task (2-3 is usually
   enough) — a task that keeps failing past that point is a signal to stop
   looping and raise it to the human rather than grinding indefinitely.

4. **Report to the human.** Once every task is verified, give one
   consolidated summary covering what was done across all of them —
   what changed, where, and any task that got kicked back to the human
   instead of resolved. Don't narrate each subagent's blow-by-blow; the
   user wants the outcome, not the transcript.

## Non-goals

- Don't reach for this on a single task, or on tasks that are so tightly
  coupled they can't be split — the overhead of spec-writing and review
  isn't worth it, just do the work.
- Don't skip the review step because a subagent reported success — a
  subagent's own summary describes what it intended to do, not
  necessarily what it verified. Check the actual result before trusting it.
- Don't loop review/fix cycles forever on a stuck task — surface it to the
  human with what was tried and what's blocking it.
