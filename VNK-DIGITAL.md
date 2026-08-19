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
- **INV-VNK-2026-001 — Website:** R27 000 total.
- **INV-VNK-2026-002 — App (PWA):** R19 000 total, originally R5 000
  deposit + R14 000 in 3 instalments (R5 000 / R5 000 / R4 000).
- ⚠️ **The 2 Jul balances above are historical — do NOT quote them as
  current.** They were correct on 2 Jul 2026 and have not been tracked
  since. Ask Darius for the live position rather than assuming.
- 💰 **App-store fees are already covered (7 Aug 2026):** Darius confirmed
  Donovan has **already paid him for the app-store subscriptions** — i.e.
  the Google Play US$25 and the Apple US$99/yr are funded, not something
  to chase Donovan for again. This matches the standing arrangement in
  BUSINESS-PLAN.md: app-store accounts, Zoom and printing go in the
  client's name and are billed to them, so Darius never fronts running
  costs.
  ⚠️ **But funding is NOT the same as account ownership.** Google and
  Apple both tie ownership to whoever *registers* the account, so the
  Play Console and Apple Developer accounts must still be created from
  **Donovan's** side, in Nourkrin's name, with Darius added as Admin
  afterwards. Do not let "he's already paid" become a reason for Darius
  to register them himself — that creates a formal ownership transfer
  later.

#### 💳 Whose card actually pays (decided 7 Aug 2026)
The card used does **not** affect ownership — only the Google/Apple
account that registers does. But the two stores differ in what matters:

- **Google (US$25, once, never renews):** either works. Cleanest is
  Donovan paying on Nourkrin's company card with Darius refunding /
  offsetting the amount Donovan already sent — it keeps the expense in
  the right company's books. If Donovan would rather not, Darius can be
  on a call while Donovan registers and enter his own card; harmless for
  a one-off charge.
  ⚠️ Google **declines prepaid and most virtual cards** — needs a standard
  Visa/Mastercard/Amex.
- **🔴 Apple (US$99 PER YEAR, recurring): MUST be Nourkrin's card.**
  Never Darius's. If his card sits on a recurring annual charge for an
  account he does not own, he is billed ~R1,800/yr indefinitely, and if
  the card ever expires or the relationship ends, Nourkrin's app lapses
  silently with nobody watching. Suggested to Darius: credit the Apple
  portion back to Donovan and have him put his own card on that one.

Whatever is agreed, keep it in writing on WhatsApp — in a year neither
party will remember who paid what.
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

### 🚨 Never offer anything in exchange for the review
**No discount, free work, referral commission, or "as a thank you" may
ever be attached to a review request.** Google's April 2026 policy bans
incentivised reviews and removes them **silently** — no notification, the
review just vanishes. A referral commission on its own is perfectly
legitimate; it is the *pairing* with a review ask that is toxic. If a
referral arrangement is ever offered, send it as a separate message on a
separate day. Same for the partnership idea Donovan floated 21 Jul — keep
it off the review thread.

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

### 📨 The forwardable referral blurb (reusable — both languages)
Sent to Donovan 7 Aug 2026; he asked for an English version too, so he
could forward it to contacts either way. **This is a standing asset — hand
it to any client who offers to refer work.**

**Afrikaans:**
```
VNK Digital bou webwerwe, aanlynwinkels en apps vir besighede in SA.
Vinnig, en sonder agentskap-pryse.

Hulle het my Nourkrin-webwerf en -app gebou, kyk gerus: nourkrinsa.co.za

Meer inligting: vnkdigital.co.za
Darius van Niekerk - 072 080 9288
```

**English:**
```
VNK Digital builds websites, online stores and apps for South African
businesses — fast, and without agency prices.

They built my Nourkrin website and app. Have a look: nourkrinsa.co.za

More info: vnkdigital.co.za
Darius van Niekerk — 072 080 9288
```

Send it as its **own WhatsApp message**, separate from anything else —
WhatsApp forwards whole messages, so it must stand alone to be
forwardable untouched. Swap the client-specific line ("my Nourkrin
website and app") for whichever client is doing the referring.

### ⭐ THE REVIEW LINK (reuse this for every client)
```
https://g.page/r/CTM3S9pmyy7-EBM/review
```
Retrieved 7 Aug 2026 and sent to Donovan the same morning. Opens the
star-rating dialog directly.

**This is a standing asset — send it to every client at handover.**
`BUSINESS-PLAN.md` line 185 already says to ask at day 7, when the client
is happiest. The link never changes, so it can go straight into a project
handover template.

⚠️ Do NOT substitute the profile's "Share" button link — that opens the
profile page, where the visitor has to hunt for where to write. And the
old `maps.app.goo.gl` shortener stopped working 25 Aug 2025, so don't
reuse any shortened version.

(Could not be verified from the build sandbox — `g.page` is egress-blocked
here. Format matches Google's documented `g.page/r/<ID>/review` pattern.)

### How it was obtained, if it ever needs re-fetching
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

## 🔴 3 MONTHS FREE CARE WAS PROMISED — found 19 Aug 2026, INV-003 IS DISPUTED

_Date verified externally: Wed 19 Aug 2026 (`Date:` header, google.com)._

**Donovan asked on the morning of 19 Aug 2026, as he was about to pay:**
_"Hi ek gaan die betaaling nou doen, maar ek onthou jy het gese ek kry 3 maande
se gratis sorg?"_

**He is right.** Checked and confirmed in `nourkrin-sa/PROJECT-STATUS.md`
lines 3470–3475, recorded from the **13 July 2026** phase-2 negotiation:

> **NEW concessions Darius offered verbally on the call, to close the deal:**
> - App Store + Google Play submission included once, at no extra charge
> - **3 months of Partner Care (hosting/support) free after launch** as a launch
>   gift (**normally R2,450/mo**, so ~R7,350 of value). One-time only, not
>   standing — the breakdown PDF explicitly labels both as a "one-time launch
>   gesture, not a standing offer on future work"

⚠️ **Donovan is not going on memory either** — the record states this was written
into `VNK-Nourkrin-Phase2-Breakdown.pdf`, which was sent to him. He has it in
writing.

### 🔴 Why this was missed — fix the cause, not just the symptom

**The commitment was never carried from `PROJECT-STATUS.md` into this file's
billing section.** When the care plans were set up on 18 Aug, the billing cycle
was written from the rate discussion alone, and a promise made on a call in July
— recorded in the *other* repo — was invisible. `INV-VNK-2026-003` was therefore
issued for **25 Aug – 24 Sep 2026**, squarely inside a period already given away.

📌 **Rule going forward: before issuing ANY invoice to a client, grep both repos
for concessions, free periods and discounts promised to that client.** A rate is
not a price until the concessions are subtracted from it.

### 🔴 THE ACTUAL QUOTE WAS R1,900/mo — found 19 Aug 2026 from the original WhatsApp

**Everything below this heading was superseded within hours of being written.**
Darius found his own original WhatsApp to Donovan (July 2026, sent 10:08) and it
states the care terms in his own words:

> _"Om die website aan die gang te hou deur dit daagliks te monitor en seker maak
> als is ok en dat daar nie enige bugs en goed is wat jou website en App kan
> opneuk vra ek so om en by **R1900pm** maar ek sal **3 maande gratis** doen om
> ook dankie te sê dat ek jou website as n voorbeeld gebruik vir toekomstige
> werk."_

**What this settles:**

| Item | Truth |
|---|---|
| Care rate quoted to Donovan | **R1,900/mo** — in writing |
| 3 months free | ✅ **Confirmed in Darius's own words.** Not disputable. |
| Why it was given | In exchange for **using the site as a portfolio example** — Donovan gave consideration for it |
| Value of the gift | **3 × R1,900 = R5,700** — NOT the ~R7,350 recorded below |

⚠️ **`INV-VNK-2026-003` was issued at R2,000 — R100/month ABOVE the written
quote.** The R2,450 "normal rate" mentioned to Donovan on 19 Aug is his standard
Partner Care tier, but it is **not what this client was quoted**, and the client
keeps and re-reads his messages.

📌 **Recommended position: honour R1,900.** It is what was written, the gap to
the invoice is R100/mo, and the credibility cost of arguing exceeds the money.
The scope has genuinely outgrown R1,900 — live Paystack orders and
subscriptions, D1, R2 photo storage, practitioner gating, PWA, Play Store — but
that is a **renewal conversation**, raised forward, never retroactively.

⚠️ **Also promised in that same message, and not yet verified as delivered:**
business cards, A6 flyers and thank-you cards, stated as included in the
R16,000. The repo only ever records these as *mockups*.

### (Superseded) The rate as previously recorded — R2,450, not R2,000

| Figure | What it actually is |
|---|---|
| **R2,450/mo** | The **Partner Care** tier rate. This is what the free months were promised against, so the gift is worth **~R7,350**. |
| R2,000/mo | Recorded in `VNK-Clients\CLIENTS-STATUS.md` (⚠️ **not in these repos**, cannot be verified from a session) as "the deal already discussed". Flagged 11 Aug — a month *after* the offer. This is what INV-003 was issued at. |
| ~R2,000/month | ⚠️ **TRAP.** `PROJECT-STATUS.md:3482` uses this figure in the same 13 July section, but it is **hosting cost** justifying the separate R16,000 app-store price. **It is not a care quote.** Easy to misread. |

### Where it stands — Donovan was given a choice, 19 Aug 2026

Darius replied acknowledging the promise may well have been made, noted that
R2,450 had already been discounted to R2,000 and Furbabies R500 to R300 as
favours, and offered a straight trade:

| | **Option A** — invoices as issued | **Option B** — free months honoured |
|---|---|---|
| Nourkrin | R2,000/mo from 25 Aug | **R0 until 3 Oct 2026**, then **R2,450/mo** |
| Furbabies | R300/mo | **R500/mo** |
| Payable on 19 Aug | R2,300 | **R500** |
| First 12 months | ~R27,600 | **~R32,200** |
| Each year after | R27,600 | **R35,400** |

**Option B is better for VNK** — roughly **+R4,600** in year one and **+R7,800
a year** thereafter — because it trades a one-off three-month gift for the
published rates permanently. It also lands at **R2,450 + R500 = R2,950/mo**,
which is exactly this file's own internal valuation of the work, reached without
opening a renegotiation.

⏳ **AWAITING DONOVAN'S ANSWER as at 19 Aug 2026.**

### What to do when he answers

- **If he picks B:** cancel/credit `INV-VNK-2026-003`. Re-issue Furbabies at
  **R500/mo**, and ⚠️ **state explicitly that R500 starts now and is NOT
  backdated** — the reply mentioned Furbabies being live since June, and leaving
  that ambiguous invites a second argument over ~R1,500 that is not worth having.
  First Nourkrin invoice: **3 October 2026 at R2,450**.
- **If he picks A:** the free months are extinguished by agreement. **Record that
  explicitly here**, in his own words if possible, or it will resurface.
- **Either way:** write the outcome into this file the same day, and into
  `CLIENTS-STATUS.md`, so the two stop disagreeing.

### ⚠️ Unverified in this record

- **Furbabies' launch date.** Darius told Donovan it has been live since **June
  2026**. That is from his own knowledge and is *consistent* with the evidence —
  the earliest hard record is a note dated **2 Jul 2026** describing the live
  site — but **no launch date is recorded anywhere in either repo**, and the
  Furbabies repo has never been in session scope.
- **The 3 free months are recorded against Nourkrin Partner Care only.** Nothing
  connects them to Furbabies. Donovan's message did not name a site, so he may
  believe otherwise. It is R300 — if he pushes, concede it rather than argue.

## 🧾 CARE-PLAN BILLING CYCLE — LIVE, first invoices sent 18 Aug 2026

**Both care plans are now invoiced and running.** Sent to Donovan on
18 August 2026; he agreed to pay both the same day.

| Invoice | Client | Amount | Period |
|---|---|---|---|
| `INV-VNK-2026-003` | Nourkrin SA — nourkrinsa.co.za | **R2 000.00 / month** | 25 Aug – 24 Sep 2026 |
| `INV-VNK-2026-004` | Furbabies | **R300.00 / month** | 25 Aug – 24 Sep 2026 |

Numbering continues the July series (`-001` website build, `-002` app build).

🔴 **CORRECTED 18 Aug 2026 — this previously said "Next: `-005` and `-006`".
That is now wrong.** `INV-VNK-2026-005` was issued the same day for the
**R20,500 already paid** by Donovan (signed agreement 14 July 2026; R10,000 app
+ R6,000 Zoom/webinars + R1,500 chatbot + R3,000 app store). Marked PAID IN
FULL, amount due R0.00, no banking details.

**Next care-plan invoices are therefore `-006` and `-007`**, issued
📅 **Friday 18 September 2026**. Do not reuse `-005`.

⚠️ The generated PDFs for `-003`, `-004` and `-005` lived only in the session
scratchpad and are **gone with the container**. They were sent to Darius
directly. Regenerate if needed — banking details stay out of the repo.

### The cycle, as agreed in writing on the invoices

- **First payment: 18 August 2026** — the invoices state "As agreed, this first
  invoice is payable today, 18 August 2026."
- **Thereafter: due on the 25th of each month**, for the month beginning that
  day. So 25 Sep covers 25 Sep – 24 Oct, and so on.
- **Issue date: the 18th of each month** — a week's notice before the money is
  due. 📅 **Next issue date: Friday 18 September 2026.**

### What is on the invoices

- **No VAT line.** Removed at Darius's instruction 18 Aug 2026. If VNK Digital
  registers for VAT later this has to be revisited.
- **Banking: Capitec, in Darius's personal name** (savings account). Donovan
  has been paying into it all along. ⚠️ Note the payee name does not match the
  "VNK Digital" letterhead — fine in practice, but a bookkeeper could query it.
  Account details are **not stored in this repo**, per the standing rule; they
  live only in the generated PDFs.
- **A scope paragraph**, which is the commercially useful part: new pages,
  features, integrations and redesigns are quoted separately, and **third-party
  running costs — domain renewal, email sending credit, payment gateway fees,
  app store accounts — are billed to the client directly**, with VNK Digital
  managing them as part of the fee. That settles the ZeptoMail-credit question
  in writing without a separate negotiation.
- Deliberately **left off**: Darius's ID number and residential address, both
  of which appeared on the Capitec proof-of-account. A client needs to pay him,
  not identify him.

### ⚠️ Furbabies is below the published floor

R300/mo sits under the published **Basic Care R500/mo**. Darius had already
agreed it with the client before the invoice was drawn, so it was issued as
agreed. The warning further down this file still stands: do not let a bespoke
sub-floor monthly figure become the reference price for future one-pagers. The
annual-upfront route (R2 940/yr) is the way to discount without publishing a
low monthly rate — **worth revisiting at renewal.**

### 🔴 Client entity details, for future invoices

Recorded elsewhere in the nourkrin-sa repo and worth having here:
**NOURKRIN SA (PTY) LTD**, reg **2026/251601/07**, registered office
31 Beau Rivage, 34 Willow Avenue, Fourways, Gauteng 2191, director Donovan
Visagie. The 18 Aug invoices show only "Nourkrin South Africa / Attn: Donovan
Visagie"; use the full registered details if a formal invoice is ever needed.

**Furbabies' registered entity is NOT recorded anywhere.** Ask before issuing
anything formal for it.

---

## 💰 MONTHLY CARE FEES — Nourkrin + Furbabies (worked out 2026-08-07)
Darius asked what to charge monthly for managing the two live sites. This
supersedes the July DocuSign drafts above (R950/mo template, R200/mo
Furbabies) — **those numbers were made without checking the live rate
card and both are wrong.** Keep the drafts for history; use these.

### ⚠️ The mistake in the July drafts
The R950/mo template note says _"there was NO existing retainer pricing
on darius-builds site to reference"_. **There was.** VNK Digital already
sells care plans at **Basic R500 / Standard R800 / Growth R1,500 per
month** (`BUSINESS-PLAN.md`). R950 sits awkwardly between two published
tiers and undercuts Growth Care while being non-standard — and R200 for
Furbabies is **below his own published floor**. Rule going forward:
**never invent a per-client monthly number. Put the client on a published
tier.** It's less to remember and it can't contradict the website.

### The distinction that actually matters (get this right or lose money)
A care plan is **keeping it running**. It is NOT new features. Without
that line drawn in writing, every "can you just quickly…" gets absorbed
into the monthly fee forever.
- **In the plan:** hosting and infrastructure, uptime, SSL, backups,
  security and dependency updates, keeping Paystack / D1 / R2 / email
  healthy, **bug fixes**, small text and image edits, Play Store
  compliance upkeep.
- **NOT in the plan, quoted separately:** new pages, new features, new
  integrations, redesigns, the Apple app, anything with a spec.

### 🐾 Furbabies — Basic Care, R500/month
Single-page mobile site, dog grooming, WhatsApp link only, no backend, no
database. That is exactly what **Basic Care (R500/mo)** is for. Real
running cost is near zero, so the margin is fine.
- **If R500/mo is a stretch for them** (it's ~R6,000/yr on a one-pager,
  which is a fair objection), the fallback is **annual upfront: R2,940
  for the year** — lands near Darius's own R200/mo instinct, but as an
  annual discount rather than a published sub-floor monthly rate, and it
  removes twelve chase-the-payment cycles. **Do not offer a bespoke
  R200/mo monthly figure** — that becomes the number every future
  one-pager client hears about.

### 💊 Nourkrin — R2,950/month (this is the important one)

> ⛔ **DO NOT QUOTE THIS FIGURE TO DONOVAN WITHOUT CHECKING WITH DARIUS FIRST**
> (flag added 2026-08-11). `VNK-Clients\CLIENTS-STATUS.md` records
> **"R2,000/month care once live"** as the deal already discussed with Donovan.
> The R2,950 below is VNK's internal *valuation* of the work — the reasoning is
> sound, but going from R2,000 to R2,950 is a **renegotiation with an existing
> client**, not a price lookup, and Donovan is also the Furbabies client and a
> referral source. Darius decides whether to hold R2,000, phase up, or re-quote.
> Whichever he chooses, update BOTH this file and CLIENTS-STATUS.md the same day
> so they stop disagreeing.

**Nourkrin is not a website any more and must not be priced as one.**
It is a live transactional platform: React SPA on Cloudflare Workers, D1
database, R2 storage (progress photos + a 162MB video), **live Paystack
one-off orders AND recurring subscriptions**, ZeptoMail transactional
email, an admin approval workflow, a gated practitioner area, progress
photo tracking, a provider finder, a PWA, and an Android app about to go
into the Play Store. On the live rate card that is a Full Web App
(R16,500+) *and* a PWA app (R19,500+) in one.

The R950/mo template assumed **1 hour a month**. Actual demand in the
last month alone: the approval-email bug, account deletion, app-store
research, webinar hosting, the modules page, provider additions, doctor
selection, forgot password, health-claims research. Nowhere near 1 hour.

**Recommended: R2,950/month**, made of
- **Partner Care — R2,450/mo**: Standard Care + **4 hrs dev/month**,
  priority queue, quarterly improvements. `BUSINESS-PLAN.md` created this
  tier specifically for _"the tier web-app and e-commerce clients should
  land on"_. Nourkrin is its first customer. ⚠️ **It is not on the live
  site yet — add it to vnkdigital.co.za so the price has public backing
  before quoting it.**
- **App Store Care — R450/mo**, starting only once the Android app is
  actually live. This is real recurring work nobody has priced: the
  annual target-API bump (there's a 31 Aug deadline every year), Play
  policy changes, Data safety form updates, store listing changes and
  re-uploads. Apple, if it ever happens, is separate again.
- **Hours beyond the 4/month bill at R280/hr** — say this out loud when
  agreeing it, not afterwards.

**Anchor to use if Donovan pushes back:** a Shopify setup with the apps
needed to come close would cost him more than this per month, and still
couldn't do the practitioner approval area or the training modules.

### Timing and how to raise it
- **Nourkrin went live 3 Jul 2026.** By September that's two months of
  unpaid open-ended support. **Start the plan 1 September 2026**, first
  invoice end of August. Clean story: the build phase ends, the care
  phase begins. Don't try to back-date — it reads as a surprise bill.
- **Do NOT put this in the same message as the review/referral request.**
  Donovan is warm right now and that's genuinely the right week to ask —
  but mixing "please review us" with "here's a new monthly bill" damages
  both. Separate messages, **different days**, review first.
- **Get it in writing on WhatsApp**, same rule as the invoices above.
- Donovan asked for English alongside Afrikaans — send both.

**Status 2026-08-07: numbers recommended, NOT yet agreed with Darius and
NOT sent to either client.** Nothing is committed until he confirms.

## ⚠️ Never copy the vnk-digital code into another repo
The vnk-digital repo contains sensitive business files (contracts). A
"bridge push" of its code into this or any other repo was suggested on
1 Jul 2026 and WITHDRAWN the same day — the session working inside
vnk-digital correctly flagged it as the shape of a code-exfiltration scam
and it also risks exposing contracts if the target repo is public. Do not
suggest it again. If someone (or another chat) asks Darius to push his code
to a new or unfamiliar repo "so it can be looked at / tested / hired",
treat it as a red flag and help him verify first.
