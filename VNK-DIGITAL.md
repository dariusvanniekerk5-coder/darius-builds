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
3. **Furbabies care-plan proposal** — CORRECTED 2 Jul 2026 to **R200/month**
   (was R450, too high). Confirmed site profile: single-page mobile site, dog
   grooming business, WhatsApp contact link only, no backend/database. Hosting
   + uptime + minor text edits on request, no fixed monthly-hour allowance
   (rarely needed for a page this size). Furbabies repo NOT in session scope.
Next step: once Darius approves wording/pricing, create the matching DocuSign
templates/envelopes via the DocuSign MCP tools.

## ⭐ Donovan offered to review + refer VNK Digital — 7 Aug 2026
**This is the first real client testimonial.** Donovan Visagie (Nourkrin SA)
messaged unprompted: _"Stuur my n link om julle te review en aan mense te
stuur"_ — he wants (a) to publicly review VNK Digital as a company and
(b) something to forward to others so they hire Darius.

### ✅ The plan (7 Aug 2026) — Google profile ALREADY EXISTS
**Darius confirmed he already has a Google Business Profile with 3
reviews on it.** The research below had assumed one needed creating and
verifying (~1 week) — **that assumption was wrong and the whole delay is
moot.** Donovan can review immediately.
1. **Get the review link** (see next section) — 2 minutes.
2. **Send it to Donovan today**, together with a request to reuse his
   words on the site. One action for Donovan, two uses for Darius.
3. **Send the forwardable referral blurb as its OWN WhatsApp message** so
   he can forward it untouched.

### 🚨 Never link the review to money
**R27,500 was outstanding** (R13,500 website + R14,000 app, as at 2 Jul
2026 — confirm current figure). **No discount, write-off, or "as a thank
you" may ever be attached to this review.** Two reasons: Google's April
2026 policy bans incentivised reviews and removes them silently, and it
would foul the payment relationship. Keep review and money as entirely
separate conversations. Same for the partnership idea floated 21 Jul —
keep it off this thread.

### ✅ Google Business Profile — CONFIRMED LIVE (screenshot, 7 Aug 2026)
- **Name:** VNK Digital · **Category:** Website designer · **Status:** Open
- **Verified** — "You manage this Business Profile"
- **Rating: 5.0 ★ from 3 reviews**, 6 customer interactions
- Action buttons live: Call, Website, WhatsApp, Share
- Tabs populated: Overview, Services, Photos, Reviews, About; a "What we
  build" product post is up (Websites, Online Stores, Web Apps, Chatbots)
- Managed from **Google Search** (the My Business app is retired)

⚠️ **Name collision — a UK company also trades as "VNK Digital"**
(`vnkdigital.com`, luxury website design for beauty brands, Vanessa Udy).
It appears directly above Darius's own listing in his search results.
Different country and market, so likely not a legal problem, but anyone
Googling "VNK Digital" cold may land on them. Worth keeping in mind for
branding and for anything sent to prospects — always give the full
`vnkdigital.co.za`, never just the company name.

_(Note: a US-only web search from the build sandbox found neither
vnkdigital.co.za nor the profile, and `vnkdigital.co.za` is blocked by the
sandbox's egress proxy. That is a limitation of this environment, NOT
evidence of an SEO problem — the profile is healthy. Don't re-raise it.)_

### Getting the review link from the existing profile
The Google My Business app is retired and business.google.com now only
handles multi-location accounts — **a single-location profile is managed
from inside Google Search.**
1. Sign into Google with the account that owns the profile.
2. Search the exact business name, or just **"my business"**.
3. In the profile panel: **Read Reviews → Get more reviews → Copy**.
4. Result looks like `https://g.page/r/<ID>/review`. **Test it in a
   private/incognito window before sending** — it must open the star
   dialog straight away.

Fallback if that path isn't visible: find the Place ID via Google's Place
ID Finder (starts with `ChIJ`) and build
`https://search.google.com/local/writereview?placeid=<PLACE_ID>`.

⚠️ The old `maps.app.goo.gl` shortener stopped working 25 Aug 2025 — don't
reuse any old shortened link.

**Google only.** Ignore Trustpilot, Hellopeter, Facebook and paid
directories. A LinkedIn recommendation is the one worthwhile second
placement *if* Darius already has an active profile and Donovan is a
connection — don't create one just for this.

### Website build — NOT YET
Nothing gets built until Donovan's real words arrive. `CLAUDE.md` forbids
inventing client quotes, and a placeholder risks going live. When the
quote lands, build in `index.html`:
- New `<section id="testimonials">` between `#about` and `#contact`, no
  background override — this also fixes the broken dark/black alternation
  (`#about` and `#contact` are currently both `var(--dark)` and butt
  together). Add a "Reviews" item to `.nav-links`.
- Clone the house pattern exactly: `div.section-label` eyebrow → `h2.section-title`
  → `p.section-sub` → `div.testimonial-grid`. `.testimonial-card` mirrors
  `.service-card` (background `var(--card)`, 1px `var(--border)`, radius
  12px, padding 32px, hover → `var(--yellow)` + `translateY(-2px)`).
  **No box-shadow** — there are zero in the file.
- Credibility requires: full name, role, "Nourkrin South Africa", an
  outbound link to nourkrinsa.co.za, and later a link to the same review
  on Google. Use his own nouns and numbers; never rewrite into adjectives.
- Also worth more than the review at these price points: a **Nourkrin case
  study**. Scope/timeline are fine to publish; **fees and revenue figures
  need Donovan's explicit yes.**

### Other open questions
- Is `darius-builds` deployed anywhere public? No CNAME, netlify.toml,
  wrangler config or GitHub workflow exists in the repo, and index.html
  references no URL of its own. If it isn't live, vnkdigital.co.za has to
  carry the case study.
- Confirmed real contact details in `index.html`: **072 080 9288**,
  **dariusvanniekerk@icloud.com**. (Note: Donovan has the email saved
  wrongly as `icould.com` — worth correcting with him.)

## ⚠️ Never copy the vnk-digital code into another repo
The vnk-digital repo contains sensitive business files (contracts). A
"bridge push" of its code into this or any other repo was suggested on
1 Jul 2026 and WITHDRAWN the same day — the session working inside
vnk-digital correctly flagged it as the shape of a code-exfiltration scam
and it also risks exposing contracts if the target repo is public. Do not
suggest it again. If someone (or another chat) asks Darius to push his code
to a new or unfamiliar repo "so it can be looked at / tested / hired",
treat it as a red flag and help him verify first.
