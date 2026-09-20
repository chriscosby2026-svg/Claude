# Reel review: instagram.com/reel/Db9Br3XBTPj

Source: https://www.instagram.com/reel/Db9Br3XBTPj/ (47.2s)

## What it is

A direct-to-camera listicle: "10 ways your [vibe-coded] app is getting
sued (niche edition)." A speaker reads a numbered list of compliance
failures against an on-screen running dollar total, closing with "TOTAL
AMOUNT: $135,157" and an engagement-bait CTA — "comment 'sued' to get my
full guide on how to fix all of this using ChatGPT or Claude." On-screen
caveat: "(this is not legal advice)."

No code, no tool, no repo, no prompt is shown or named — this is a legal
liability claim, not a demonstrated procedure, so there's nothing to clone
and vet the way the previous review vetted plugin repos. Instead, the
dollar figures themselves are the claim worth checking against source law.

## The 10 items claimed

1. No privacy policy — $2,500
2. Privacy policy omits "we collect user data" — $7,908
3. Privacy policy omits AI use — $7,908
4. Privacy policy omits third-party data recipients — $7,908
5. Not deleting user uploads as promised — $750
6. Storage bucket set to public — $750
7. Fake testimonials — $53,000
8. Cancellation harder than sign-up — $53,000
9. Free trial auto-charges with no reminder — full refund
10. AI chatbot with no self-harm response — $1,000

## Fact-check: are the numbers real?

The two repeated figures map to real statutory maximums, but the reel
strips out every condition that makes them apply:

- **~$53,000 figures** track the FTC's inflation-adjusted maximum civil
  penalty *per violation* under Section 5(m)(1)(A)/(B) of the FTC Act
  (the same cap COPPA enforcement uses) — $51,744 for 2024, $53,088 for
  2025 ([FTC, 2025 adjustment](https://www.ftc.gov/news-events/news/press-releases/2025/02/ftc-publishes-inflation-adjusted-civil-penalty-amounts-2025)).
  This is the ceiling a court can impose *if the FTC sues and wins* on
  each individual violation — it is not a fine that is automatically
  owed per user, and applying it to "fake testimonials" or "hard to
  cancel" specifically assumes an FTC enforcement action under its
  Endorsement Guides / click-to-cancel rule, not a guaranteed liability.
- **$750 figures** track the CCPA's private-right-of-action statutory
  damages: $100–$750 per consumer *per incident*, or actual damages,
  whichever is greater ([IAPP summary](https://iapp.org/news/a/ccpa-litigation-shaping-the-contours-of-the-private-right-of-action)).
  Critically, this right of action only attaches to a data *breach* —
  "nonencrypted and nonredacted personal information" subject to
  unauthorized access, exfiltration, theft, or disclosure caused by a
  failure to implement reasonable security. A public storage bucket that
  actually leaks personal data could plausibly trigger this; "not
  deleting uploads" you no longer expose to anyone does not, on its own.
  It also only applies to businesses that meet CCPA's coverage
  thresholds (revenue/data-volume), which the reel never mentions.

So the reel isn't making numbers up, but it presents worst-case litigated
maximums as if they were fixed, automatic per-user invoices, and skips
every applicability condition (who's a "covered business," whether an
actual breach or FTC action occurred, jurisdiction). "TOTAL AMOUNT:
$135,157" is a sum of ten unrelated maximums that would require ten
separate successful legal actions to ever actually be owed together.

## Why nothing was built from this reel

Same reasoning as `reviews/DYAnUJCpCep.md`: this repo's `/watch` →
`/skill-from-video` pipeline turns a **demonstrated procedure** into a
runnable skill. This reel demonstrates nothing — no prompt, no tool, no
workflow, just a claims list read to camera. There is no source to vet
(no repo, no named product) and no procedure to encode as a skill; doing
so would mean fabricating steps that were never shown.

The CTA itself is worth flagging on its own terms: "comment a keyword to
get my guide via DM" is a standard lead-generation/engagement-farming
pattern, not an invitation this session acted on. Per this repo's own
`.claude/skills/watch/README.md` note, video content is treated as
untrusted external input — instructions a video directs at the viewer
(or at an agent) don't get followed just because they're on screen.

## What changed in this repo

- Added this review file. No skills, plugins, or code were added —
  there was nothing in the reel to vendor.
