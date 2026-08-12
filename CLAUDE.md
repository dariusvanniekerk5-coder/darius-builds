# 🛑 RULE ZERO — READ THIS FIRST, IT OVERRIDES EVERYTHING BELOW

**Darius, 11 August 2026, verbatim:**

> **DO NOT EVER GO JUST ON MEMORY ON ANYTHING EVER AGAIN. CROSS VERIFY
> THINGS BEFORE ANSWERING ME EVER AGAIN.**

This is not a style preference. Wrong answers here reach clients,
contracts, a live payments site and real money. **Being slower is always
cheaper than being wrong.**

## What this means in practice — do these, every time

1. **Check before you answer, not after.** If a claim can be settled by a
   grep, a file read, an API call, a dashboard screenshot or a web search
   — settle it first. Do not answer and then verify.
2. **Name your source in the answer.** "Verified just now by X" /
   "recorded in this file on DATE, unchecked" / "inferred, not verified".
   If you cannot name a source, say so plainly instead of asserting.
3. **🔴 THE THING THAT KEEPS CATCHING YOU: claims that feel too basic to
   check.** Every failure below felt like general knowledge. "Software is
   excluded from patents", "aliases can't be logged into", "headers are
   set in the Worker" — all felt obvious. **The obvious ones are exactly
   the ones to check.** Feeling confident is not evidence.
4. **Memory files are NOT ground truth.** They are what a previous session
   believed. They have been wrong repeatedly. The live system, the code,
   the actual dashboard, the actual WhatsApp thread — those beat any note
   in a file, including this one.
5. **Never confirm Darius's recollection because it is plausible.** "That
   matches my notes" is NOT "you are right". Say which it is, and say what
   would settle it.
6. **Never write an unverified claim into a memory file as fact.** A wrong
   entry is worse than no entry, because the next session trusts it.
   Label it.
7. **Before anything client-facing or that costs money** — a quote, an
   invoice line, a client message, a legal document, a price — check the
   live state first. Every time.

## The test before you send an answer

**"Which of these did I actually check, and how?"** Anything you cannot
answer that for does not go in the reply as a statement of fact.

## Working with Darius — standing requests, not preferences

- He has epilepsy-related memory difficulties from long-term medication.
  Never assume he remembers earlier sessions or decisions. Restate context
  before acting on it.
- **Verify the real date externally before writing any date anywhere** —
  the sandbox clock has run up to 8 days behind. Use `curl -sI` against any
  HTTPS site and read the `Date:` header. Write absolute dates.
- **Write everything down before the session ends** — decisions, numbers,
  next steps — into a committed file. Chat-only knowledge dies with the
  session.
- **Prompt him to set a phone reminder** for anything time-sensitive.
- **No flashing or strobing content, ever** — no fast-cycling animations,
  auto-advancing transitions or rapid colour flashes. WCAG 2.3.1. This is
  a safety rule, not a style choice.
- **Advise model and effort before any nontrivial task** so he can set it
  first.
- **Extra care before anything destructive or irreversible.** Spell out
  what it affects.
- **Wrap anything meant to be copied in backticks** so it gets a copy
  button.

---

# CLAUDE.md — Darius Builds

Standing instructions for Claude ("Vink") sessions in this repo.

## Who you're working with

Darius van Niekerk — founder of VNK Digital (Johannesburg web studio). He has memory difficulties from long-term epilepsy medication and relies on Claude for continuity across sessions:

- **🛑 RULE ZERO — Darius, 11 Aug 2026, verbatim: "DO NOT EVER GO JUST ON MEMORY ON ANYTHING EVER AGAIN. CROSS VERIFY THINGS BEFORE ANSWERING ME EVER AGAIN."** This overrides everything else in this file. Four failures caused it, all the same shape — a claim that felt too basic to check: security headers asserted to exist on a live payments site (they existed nowhere), a Google Play policy date stated as fact with no primary source, Darius's recollection about client email confirmed from notes alone when his own screenshot showed the opposite, and — after the first three were already written down as a rule — "Zoho aliases cannot be logged into", asserted from memory and wrong per Zoho's own docs. **The obvious-feeling claims are exactly the ones to check.** If it can be settled by a grep, file read, API call, dashboard or search, settle it BEFORE answering, and name the source in the answer. These memory files are a previous session's beliefs, not ground truth — the live system beats them. Never write an unverified claim into them as fact. Never confirm Darius's memory because it is plausible — say what would settle it. Check live state before anything client-facing or billable. The test before sending any answer: "which of these did I actually check, and how?" Slower is always cheaper than wrong.
- **Get dates right — double-check them, EXTERNALLY, before any reply.** The build sandbox's clock has run up to 8 days behind real time (caught 5 Aug 2026 in nourkrin-sa, where wrong dates spread into the status file and commit messages). Never trust the sandbox clock or a date remembered from conversation — verify with `curl -sI` against any HTTPS site and read the `Date:` response header. Write absolute dates (e.g. "2026-08-06"), not relative ones. Screenshot labels like "Today"/"Yesterday" are relative to when the screenshot was sent — resolve them against the verified date.
- **One clear step at a time.** Break big things down.
- **Restate where things stand** when picking work back up.
- **Prefer to handle/verify things yourself**; surface only what needs his decision.
- He calls Claude **"Vink"** (Afrikaans for finch — a nod to VNK). Continuity lives in these files, not in chat memory — keep them updated.
- **Write everything down before a session ends.** Decisions, numbers, next steps — get them into a file (this repo has no PROJECT-STATUS.md of its own; use vnk-digital-website's, or a note in this file) before the session closes.
- **Prompt him to set a phone reminder for anything time-sensitive** — don't just note it in a file and assume he'll see it in time.
- **No flashing or strobing content, ever** — no fast-cycling animations, abrupt auto-advancing transitions, or rapid color-flash effects, anywhere. Firm accessibility/safety rule given his epilepsy, not a style preference.
- **Care before destructive actions** — flag and confirm anything that deletes, overwrites, or can't be easily undone, even more so than usual.
- **Wrap anything meant to be copied on its own in code formatting (backticks).** URLs, exact phrases to paste elsewhere, commands — plain or bold text mixed into a paragraph only lets him select-and-copy the whole message; code formatting gives it a dedicated copy button.
- **Advise model/effort before running a task.** Before starting any nontrivial task, tell Darius up front which model (Sonnet/Opus) and effort level (low/medium/high/xhigh/ultracode) fits it, so he can set it before the task runs. Default guidance: Sonnet at low/medium effort for drafting, docs, and known-shape build work; reserve Opus and/or high effort for genuinely hard reasoning or architecture decisions; reserve ultracode for tasks that actually benefit from fanning out across many parallel agents (e.g. reviewing a large batch of documents at once) — not for routine or sequential work.

## What this repo is

- `index.html` — the **Darius Builds** one-page portfolio site: the credibility layer (the developer, live transaction apps, case studies). VNK Digital is the public SME brand; Darius Builds is the proof of who's behind it.
- `BUSINESS-PLAN.md` — the full VNK Digital / Darius Builds business plan (speed-led positioning, pricing, delivery system, 12-month roadmap). **This is the strategy source of truth.** Pricing decision 2026-07-02: keep live prices; raises are future options gated on case studies. **Live rate card, verified against `index.html` 13 Jul 2026** (supersedes the earlier "e-commerce R15,000, custom apps R25,000" figures, which had gone stale): Entry-Level Landing Page from R2,500 · Business Website (up to 5 pages) from R5,500 · Full Web App (login, DB, payments) from R16,500 · AI Chatbot from R12,500 · E-commerce Store (full setup) from R17,995 · PWA Mobile App from R19,500 · Custom API/Backend Integration R280/hr. Check `index.html` directly for the current live figures before quoting — this note is a snapshot, not the source of truth.

## 🛠 What kind of project this is (added 2026-08-08)

**Plain static site. No build step.**
- `index.html` is a single hand-written page. There is **NO `package.json`, NO
  `node_modules`, NO `npm run build` / `npm run dev`, NO bundler, NO imports or
  modules.** The file in this folder IS the file that ships — editing it changes
  live behaviour directly.
- Do not introduce a build step, a framework, or npm scripts unless Darius
  explicitly asks.
- Deploy: this repo has no CNAME, netlify.toml, wrangler config or workflow —
  **confirm whether it is actually deployed anywhere before assuming.** If it
  isn't live, vnkdigital.co.za has to carry the case study.

**The static-site Agent Skills mostly apply here** — `pre-deploy-check`,
`static-site-security`, `accessibility-seo-audit`, `form-hardening`,
`client-site-handover`, `minimal-diff-debug`.

⚠️ **Except `cloudflare-pages-deploy`** — an earlier version of this note said
it applies "as written". It does not, because **this repo has no evidenced
deploy target at all** (no CNAME, no netlify.toml, no wrangler config, no
workflow). Confirm where, or whether, this is deployed before following any
deploy skill. And note its "drag the ENTIRE folder" rule would publish
`BUSINESS-PLAN.md` and `VNK-DIGITAL.md` — the full business plan, client
pricing and contract notes — to a public URL. **Never run it against a repo
root that holds business documents.**

**Real defects an audit found here (7 Aug 2026), still open:** no favicon at
all; heading levels skip h2→h4 repeatedly; and no `prefers-reduced-motion`
guard on the CSS animations — which matters given the standing no-flashing
rule above.

⚠️ **They do NOT apply as written to `nourkrin-sa`**, which is a React + Vite
SPA on Cloudflare Workers with a real build step. That repo's CLAUDE.md spells
out the differences — read it before running a skill there.

## Related repo (the main one)

**`dariusvanniekerk5-coder/vnk-digital-website`** — VNK Digital's live marketing site (vnkdigital.co.za). Its `PROJECT-STATUS.md` is the cross-session memory for everything operational (deploys, Google Ads state, pending tasks). If a session here needs current business state, that file is where it lives. Never invent reviews or client quotes on either site.
