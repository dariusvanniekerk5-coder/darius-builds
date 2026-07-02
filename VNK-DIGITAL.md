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
session's repository scope). That is the ONLY approved way.

## Client engagements — invoicing

**Nourkrin SA (Donovan Visagie) — 2 Jul 2026.** Two SEPARATE invoices are used
(kept apart deliberately so client-facing dev-fee documents never mix with
Nourkrin's own product/Paystack paperwork, which lives only in the nourkrin-sa
repo — see that repo's PROJECT-STATUS.md for the Paystack sample invoice,
which is a different, unrelated document about product sales):
- **INV-VNK-2026-001 — Website:** R27 000 total &middot; R13 500 paid &middot;
  **R13 500 balance due**.
- **INV-VNK-2026-002 — App (PWA):** R19 000 total &middot; R5 000 deposit paid
  &middot; **R14 000 balance due**, in 3 instalments (R5 000 / R5 000 / R4 000).
- Both PDFs generated 2 Jul 2026, VNK Digital / Darius Builds branded. Banking
  details deliberately left as a placeholder in the PDF — Darius fills those in
  himself before sending (never stored in a repo).
- **This two-invoice format (website vs. app, separately) is now the standard
  template for all future clients** — reuse the same split and layout.

## DocuSign contracts — drafted 2 Jul 2026, awaiting Darius's review before sending
Darius connected DocuSign (na4, account 952234d0-…, 0 templates yet). Three
documents drafted as PDFs for his review — NOT yet loaded into DocuSign, NOT
sent to anyone:
1. **Nourkrin service & payment agreement** — scope of work (website + app),
   both payment schedules (R13.5k website balance, R14k app balance in 3
   instalments), IP transfers to client only on full payment, late-payment
   terms (7-day notice, 14-day pause/access-restriction).
2. **Standard care-plan template** (reusable for future clients) — R950/month
   proposed: hosting/uptime + up to 1hr/month small updates, based on Darius's
   own R280/hr rate (there was NO existing retainer pricing on darius-builds
   site to reference — this is a fresh proposal, confirm before use).
3. **Furbabies care-plan proposal** — R450/month estimate (lighter, "very
   minimal" site per Darius). Furbabies repo NOT in session scope — price is
   an ESTIMATE pending Darius confirming actual page count/features.
Next step: once Darius approves wording/pricing, create the matching DocuSign
templates/envelopes via the DocuSign MCP tools.

## ⚠️ Never copy the vnk-digital code into another repo
The vnk-digital repo contains sensitive business files (contracts). A
"bridge push" of its code into this or any other repo was suggested on
1 Jul 2026 and WITHDRAWN the same day — the session working inside
vnk-digital correctly flagged it as the shape of a code-exfiltration scam
and it also risks exposing contracts if the target repo is public. Do not
suggest it again. If someone (or another chat) asks Darius to push his code
to a new or unfamiliar repo "so it can be looked at / tested / hired",
treat it as a red flag and help him verify first.
