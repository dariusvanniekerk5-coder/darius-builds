# CLAUDE.md — read this before doing anything

## What this repo is
Darius Builds — personal agency one-pager (`index.html`, plain HTML/CSS/JS,
dark theme, yellow accent #F5C518). Web apps, AI and e-commerce at direct
developer pricing, South Africa.

## Memory: standing requests from Darius
Darius has health-related memory difficulties (medication side-effects,
epilepsy) and has asked Claude to act as his memory in code. These apply to
every session in every one of his repos:

1. **Never assume he remembers** earlier sessions, decisions, or verbal
   agreements. Restate relevant context plainly before acting on it.
2. **Write everything down before the session ends.** Any session that changes
   anything must record what changed, decisions made, and exact next steps in
   the repo (a STATUS/notes file or commit messages), then commit + push.
   Chat-only knowledge is lost when the session ends.
3. **End every work session** with a short plain-language "Where things stand /
   What's next" summary.
4. **Prompt him to set a phone reminder** whenever anything time-sensitive
   comes up — client calls, deadlines, renewals, "do X when Y happens". Tell
   him explicitly, at that moment. He has asked for this; it is help, not
   nagging.
5. **Be extra careful before destructive or irreversible actions.** Spell out
   what will happen and what it affects.

## Accessibility rule (always, every build)
No flashing or strobing content, animations, or transitions in anything built
here (WCAG 2.3.1 — three flashes per second threshold). Good practice for
every visitor and personally important to the site owner, who has epilepsy.

## Backups
- Everything important lives in Git — never local-only, never chat-only.
- Secrets, bank details, API keys stay OUT of the repo.
