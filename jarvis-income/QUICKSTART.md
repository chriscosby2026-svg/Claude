# Jarvis Income Quickstart: Short-Form Video + Copy for Local Businesses

Goal: first paid client in 7 days. Jarvis drafts and does the heavy lifting; YOU send, approve and deliver under your own name.

## The offer (one product, flat price)
"12 short videos a month for your business, scripted, voiced and captioned. $497/mo. First 3 videos free as a trial."
Targets: gyms, salons, restaurants, realtors, contractors, dentists.

## Day-by-day
- Day 1: Install Jarvis, get voice + Telegram working (see SETUP below). Pick ONE niche (e.g. salons in your city).
- Day 2: Ask Jarvis to research 30 businesses in that niche (name, Instagram, what they post, what's weak). Make 3 free sample videos for the best 3.
- Days 3-6: Send 20-30 personalized messages/day (Instagram DM, email, walk-ins). Lead with the free sample.
- Day 7: Follow up, take calls, close. Collect 50% upfront.
- In parallel: 5 Upwork proposals/day for "short-form video scripts/captions" gigs (Jarvis drafts, you send).

## Outreach DM (edit per business)
Hi {name}, I made a quick free video idea for {business} based on your recent posts: {link}. I make 12 of these a month for local businesses ($497, cancel anytime). Want me to make you 3 free ones to try?

## Upwork proposal template
Hi {client}, I read your post about {specific need}. I'd do {concrete deliverable} in {timeframe}. Here's a sample I made for a similar business: {link}. Questions: {1 smart question}. - {you}

## Jarvis agent instructions (paste as his system prompt)
You are my business assistant. Rules: draft only, never send, post, pay or sign up without my explicit approval. Tasks: (1) research local businesses and summarize weaknesses in their social content; (2) write 30-second video scripts with hook, body, CTA; (3) draft outreach DMs and Upwork proposals; (4) track leads in leads.csv with status; (5) each morning brief me on replies, follow-ups due, and today's targets.

## SETUP
curl -fsSL https://open-jarvis.github.io/OpenJarvis/install.sh | bash   # Windows: irm https://open-jarvis.github.io/OpenJarvis/install.ps1 | iex
jarvis doctor
jarvis init --preset morning-digest-minimal --force
jarvis connect gdrive
Use a separate Google account for Jarvis's work; keep your main inbox read-only.

## Rules to avoid bans
- Don't automate Fiverr/Upwork accounts or share them; you submit all work.
- Disclose AI use where platforms require it; get client approval before posting.
- No spam: personalize every message.

## Math
3 clients x $497 = ~$1,500/mo. 10 clients = ~$5,000/mo. Scale by raising prices, hiring an editor, and a niche-specific offer.
