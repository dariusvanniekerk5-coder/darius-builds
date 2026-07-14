# CLAUDE.md — Darius Builds

Standing instructions for Claude ("Vink") sessions in this repo.

## Who you're working with

Darius van Niekerk — founder of VNK Digital (Johannesburg web studio). He has memory difficulties from long-term epilepsy medication and relies on Claude for continuity across sessions:

- **Get dates right — double-check them.** Verify "today" against the actual current date; write absolute dates (e.g. "2026-07-02"), not relative ones.
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

## Related repo (the main one)

**`dariusvanniekerk5-coder/vnk-digital-website`** — VNK Digital's live marketing site (vnkdigital.co.za). Its `PROJECT-STATUS.md` is the cross-session memory for everything operational (deploys, Google Ads state, pending tasks). If a session here needs current business state, that file is where it lives. Never invent reviews or client quotes on either site.
