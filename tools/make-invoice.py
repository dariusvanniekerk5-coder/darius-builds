#!/usr/bin/env python3
"""
VNK Digital invoice generator.

WHY THIS IS COMMITTED
---------------------
The generated invoice PDFs for `-003`, `-004` and `-005` lived only in a session
scratchpad and were lost when the container was recycled, along with the script
that made them. Rebuilding the layout from scratch each time is wasted work and
invites inconsistency between invoices sent to the same client. The service-terms
generator was committed for exactly this reason; so is this.

🔴 WHAT IS NOT COMMITTED, AND MUST NEVER BE
-------------------------------------------
  * The banking details. BANK below ships with «PLACEHOLDERS». Paste the real bank
    details in, generate, then DO NOT commit the edit. Standing rule:
    bank details, secrets and API keys stay out of this repo.
  * The generated PDF, which contains those details once filled in.
  * Darius's ID number and residential address. They appear on the bank's
    proof of account and are deliberately absent here — a client needs to pay
    him, not identify him.

Add `INV-*.pdf` to .gitignore rather than relying on memory. (Done.)

USAGE
-----
  1. Copy this file somewhere outside the repo, or edit in place and revert.
  2. Fill in CONFIG and the real BANK values.
  3. pip install weasyprint    (not in the base image)
  4. python3 make-invoice.py
  5. Check it is ONE page before sending.

LAYOUT RULES LEARNED THE HARD WAY
---------------------------------
  * No VAT line — removed on Darius's instruction, 18 Aug 2026. If VNK Digital
    registers for VAT this has to come back.
  * Do NOT put `page-break-inside: avoid` on tall sections. That produced a
    484-character orphan page on the service-terms PDF. Headings use
    `page-break-after: avoid` instead.
  * State a reduced rate ON the invoice. Furbabies' R300 sits below the
    published R500 Basic Care floor; if that is not restated every month it
    quietly becomes the assumed baseline, which is how the rate became
    contentious in the first place.

INVOICE NUMBERS ARE SEQUENTIAL BY ISSUE DATE, NOT RESERVED PER CLIENT.
The live ledger is the invoice table in VNK-DIGITAL.md. Check it before
choosing a number.
"""
from weasyprint import HTML

# ─────────────────────────── CONFIG ───────────────────────────
INVOICE_NO   = "INV-VNK-2026-008"
ISSUE_DATE   = "18 September 2026"
DUE_DATE     = "25 September 2026"
DUE_NOTE     = "Payable by 25 September 2026."

CLIENT_NAME  = "Furbabies"
CLIENT_ATTN  = "Attn: Donovan Visagie"
CLIENT_EXTRA = ""          # registered name / reg no., if a formal invoice is wanted

LINES = [
    # (description, period, amount in Rand)
    ("Website care plan — Furbabies", "25 September – 24 October 2026", 300.00),
]

REDUCED_RATE_NOTE = (
    "The R300 monthly rate is a reduced rate, below VNK Digital&rsquo;s published "
    "Basic Care price of R500 per month. It is held as agreed and is not the "
    "standard rate."
)

# ⚠️ PASTE BANKING DETAILS HERE BEFORE GENERATING. Never commit them.
BANK = {
    "Bank":           "«BANK»",
    "Account name":   "«ACCOUNT NAME»",
    "Account number": "«ACCOUNT NUMBER»",
    "Account type":   "«ACCOUNT TYPE»",
    "Branch code":    "«BRANCH CODE»",
    "Reference":      INVOICE_NO,
}

OUT = "%s.pdf" % INVOICE_NO   # written to the current directory — do NOT commit it
# ──────────────────────────────────────────────────────────────

def rands(v):
    return "R%s" % format(v, ",.2f").replace(",", " ")

total = sum(a for _, _, a in LINES)

rows = "".join(
    "<tr><td><strong>%s</strong><br><span class='per'>%s</span></td>"
    "<td class='amt'>%s</td></tr>" % (d, p, rands(a))
    for d, p, a in LINES
)

bank_rows = "".join(
    "<tr><td class='k'>%s</td><td class='v'>%s</td></tr>" % (k, v)
    for k, v in BANK.items()
)

html = """
<style>
  @page { size: A4; margin: 18mm 16mm 16mm 16mm; }
  body { font-family: "DejaVu Sans", Arial, sans-serif; color: #1f2937;
         font-size: 10.5pt; line-height: 1.5; }
  h1 { font-size: 20pt; margin: 0 0 2mm; color: #0f172a; letter-spacing: -0.3px;
       page-break-after: avoid; }
  h2 { font-size: 11pt; margin: 8mm 0 2mm; color: #0f172a;
       text-transform: uppercase; letter-spacing: 0.6px;
       page-break-after: avoid; }
  .head { display: flex; justify-content: space-between; align-items: flex-start;
          border-bottom: 2px solid #0f172a; padding-bottom: 4mm; }
  .brand { font-size: 15pt; font-weight: 700; color: #0f172a; }
  .brand span { display: block; font-size: 9pt; font-weight: 400; color: #6b7280;
                letter-spacing: 1px; text-transform: uppercase; margin-top: 1mm; }
  .meta { text-align: right; font-size: 9.5pt; color: #4b5563; }
  .meta strong { color: #0f172a; }
  table { width: 100%%; border-collapse: collapse; }
  .items td { padding: 3.5mm 0; border-bottom: 1px solid #e5e7eb;
              vertical-align: top; }
  .per { color: #6b7280; font-size: 9.5pt; }
  .amt { text-align: right; white-space: nowrap; font-variant-numeric: tabular-nums; }
  .total td { padding-top: 4mm; font-size: 13pt; font-weight: 700; color: #0f172a;
              border-top: 2px solid #0f172a; }
  .bank td { padding: 1.6mm 0; }
  .bank .k { color: #6b7280; width: 38%%; }
  .bank .v { font-weight: 600; }
  .note { background: #f8fafc; border-left: 3px solid #cbd5e1;
          padding: 3mm 4mm; font-size: 9.5pt; color: #374151; margin-top: 3mm; }
  .foot { margin-top: 10mm; padding-top: 3mm; border-top: 1px solid #e5e7eb;
          font-size: 8.5pt; color: #6b7280; }
</style>

<div class="head">
  <div class="brand">VNK Digital<span>Web design &amp; development</span></div>
  <div class="meta">
    <strong>%(no)s</strong><br>
    Issued %(issued)s<br>
    Due %(due)s
  </div>
</div>

<h1>Invoice</h1>

<h2>Billed to</h2>
<p style="margin:0">
  <strong>%(client)s</strong><br>%(attn)s%(extra)s
</p>

<h2>Detail</h2>
<table class="items">%(rows)s
  <tr class="total"><td>Amount due</td><td class="amt">%(total)s</td></tr>
</table>

<p class="note">%(duenote)s %(reduced)s</p>

<h2>Payment</h2>
<table class="bank">%(bank)s</table>

<h2>Scope</h2>
<p style="margin:0">
  The monthly care fee covers hosting, uptime monitoring, SSL, backups,
  security and dependency updates, keeping the payment, database, storage and
  email services running, bug fixes, and small text and image changes.
  New pages, new features, integrations and redesigns are quoted separately
  before any work starts. Third-party running costs &mdash; domain renewal,
  email sending credit, payment gateway fees and app store accounts &mdash; are
  billed to the client directly, and VNK Digital manages them as part of the fee.
</p>

<div class="foot">
  VNK Digital &middot; Johannesburg &middot; darius@vnkdigital.co.za &middot;
  vnkdigital.co.za
</div>
""" % {
    "no": INVOICE_NO,
    "issued": ISSUE_DATE,
    "due": DUE_DATE,
    "client": CLIENT_NAME,
    "attn": CLIENT_ATTN,
    "extra": ("<br>" + CLIENT_EXTRA) if CLIENT_EXTRA else "",
    "rows": rows,
    "total": rands(total),
    "duenote": DUE_NOTE,
    "reduced": REDUCED_RATE_NOTE,
    "bank": bank_rows,
}

HTML(string=html).write_pdf(OUT)
print("wrote", OUT)
