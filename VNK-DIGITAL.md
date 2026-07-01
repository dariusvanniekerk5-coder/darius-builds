# VNK Digital — Darius's business (memory note)

_Last updated: 1 July 2026. This note exists so future sessions know about the
business even when its own repo isn't in scope. Keep it updated._

## What it is
VNK Digital is Darius's registered business — the company behind the
Darius Builds agency work (web apps, AI, e-commerce, South Africa).

## Where it lives
- **Live site:** https://vnkdigital.co.za (custom domain connected, site up)
- **Netlify project:** `vnk-digital` (site id `99a735a3-9673-4263-a413-c01c2d5d004a`,
  team dev plan, deploys from `main`, latest deploy ready/current)
- **Netlify Forms: ENABLED** — if the contact form posts to Netlify Forms,
  lead submissions can be read via the Netlify connector. Worth checking for
  new leads when asked.
- **GitHub repo:** exists but was NOT in the 1 Jul 2026 session's repo scope —
  code could not be read or changed from that session.

## To do in the FIRST session started from the vnk-digital repo
1. Add a `CLAUDE.md` with Darius's standing memory requests (same content as
   the one in this repo — never assume he remembers, write everything down
   before session end, plain "where things stand" summaries, prompt phone
   reminders for time-sensitive things, no flashing content ever, extra care
   before destructive actions).
2. Add a `PROJECT-STATUS.md` as the single source of truth for the site.
3. Optional when asked: PWA conversion, rebuilt natively for VNK branding
   (do NOT transplant the Nourkrin PWA branch — it carries the whole Nourkrin
   site; see nourkrin-sa PR #1 for the pattern to follow instead).

## How Darius gives Claude access to it
Start the Claude Code session from the vnk-digital repo (or include it in the
session's repository scope). Bridging its code into another repo works but is
fiddly — direct scope is the way.
