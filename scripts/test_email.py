"""Send a single test email to the Owner for approval.

Usage: python scripts/test_email.py
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = "smtp.hostinger.com"
SMTP_PORT = 587
FROM_EMAIL = "info@profitandprivilege.com"
FROM_NAME = "Profit & Privilege"
SMTP_PASSWORD = os.getenv("GHL_SMTP_PASSWORD", "")
TO_EMAIL = "info@profitandprivilege.com"

SUBJECT = "Is OLSP Academy an MLM? — Honest answer, no hype"

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0;padding:0;background:#111827;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif">

<table width="100%" cellpadding="0" cellspacing="0" style="background:#111827;padding:40px 20px">
<tr><td align="center">

<table width="580" cellpadding="0" cellspacing="0" style="max-width:580px;background:#1F2937;border-radius:12px;overflow:hidden">

  <!-- header -->
  <tr>
    <td style="padding:40px 36px 24px 36px;text-align:center">
      <span style="font-weight:700;font-size:20px;color:#FFFFFF">Profit &amp; Privilege</span>
      <div style="width:40px;height:3px;background:#B8862B;margin:16px auto 0 auto;border-radius:2px"></div>
    </td>
  </tr>

  <!-- body -->
  <tr>
    <td style="padding:0 36px 8px 36px;font-size:15px;line-height:1.6;color:#D1D5DB">

      <p>You asked about OLSP Academy. Here's what we found — no fluff, no affiliate hype.</p>

      <p>We spent weeks cross-referencing FTC regulatory guidance, multiple independent reviews, vendor documentation, and community discussions. The question everyone asks: <strong>is it an MLM?</strong></p>

      <div style="background:#374151;border-left:4px solid #B8862B;padding:16px 20px;margin:20px 0;border-radius:0 8px 8px 0">
        <p style="margin:0;color:#F3F4F6"><strong>The short answer:</strong><br>Technically no — OLSP does not meet the FTC's legal definition of an illegal pyramid scheme. <strong style="color:#FBBF24">Practically, it shares meaningful MLM characteristics.</strong> The evidence is on the table. The decision is yours.</p>
      </div>

      <p>What's inside the review:</p>
      <ul style="color:#9CA3AF;padding-left:20px;margin:12px 0 24px 0">
        <li style="margin-bottom:6px">FTC criteria — how OLSP scores against every factor</li>
        <li style="margin-bottom:6px">Commission structure — what members actually promote</li>
        <li style="margin-bottom:6px">Pricing tiers — from free to VIP, what's real</li>
        <li style="margin-bottom:6px">Community trust — Reddit, Trustpilot, Quora sentiment</li>
        <li style="margin-bottom:6px">Your decision framework — 3 questions to ask yourself</li>
      </ul>

    </td>
  </tr>

  <!-- CTA primary -->
  <tr>
    <td align="center" style="padding:12px 36px 20px 36px">
      <a href="https://olsp.profitandprivilege.com/is-olsp-academy-an-mlm/"
         style="display:inline-block;background:#B8862B;color:#FFFFFF;padding:16px 36px;border-radius:8px;text-decoration:none;font-weight:600;font-size:16px">
        Read the full investigation →
      </a>
    </td>
  </tr>

  <!-- divider -->
  <tr><td style="padding:4px 36px 0 36px"><hr style="border:none;border-top:1px solid #374151;margin:0"></td></tr>

  <!-- CTA secondary -->
  <tr>
    <td style="padding:20px 36px 32px 36px;text-align:center">
      <p style="font-size:14px;color:#F3F4F6;margin:0 0 12px 0">Ready to try it yourself?</p>
      <a href="https://offers.olspsystem.com/get_megalink?olsp=1006001"
         style="display:inline-block;background:#1D2433;color:#22C55E;padding:12px 28px;border:1px solid #22C55E;border-radius:8px;text-decoration:none;font-weight:600;font-size:14px">
        Start with the $7 Mega Link →
      </a>
    </td>
  </tr>

  <!-- footer -->
  <tr>
    <td style="background:#111827;padding:24px 36px 24px 36px;font-size:12px;color:#6B7280;line-height:1.6;text-align:center">
      <p style="margin:0 0 8px 0">Profit &amp; Privilege — Evidence-based online business reviews</p>
      <p style="margin:0 0 8px 0">
        <a href="https://profitandprivilege.com" style="color:#9CA3AF;text-decoration:underline">ProfitAndPrivilege.com</a>
        &nbsp;·&nbsp;
        <span style="color:#6B7280">Independent research since 2025</span>
      </p>
      <p style="margin:0">
        You received this because you signed up for OLSP Academy information.
        Not the right fit? Simply ignore this — you won't receive another.
      </p>
    </td>
  </tr>

</table>

</td></tr>
</table>

</body>
</html>"""

PLAIN = """Is OLSP Academy an MLM? — Honest answer, no hype

You asked about OLSP Academy. Here's what we found — no fluff, no affiliate hype.

THE SHORT ANSWER:
Technically no — OLSP does not meet the FTC's legal definition of an illegal pyramid scheme. Practically, it shares meaningful MLM characteristics.

What's in the full review:
- FTC criteria — how OLSP scores against every factor
- Commission structure — what members actually promote
- Pricing tiers — from free to VIP, what's real
- Community trust — Reddit, Trustpilot, Quora sentiment
- Your decision framework — 3 questions to ask yourself

Read the full investigation:
https://olsp.profitandprivilege.com/is-olsp-academy-an-mlm/

Ready to try it yourself?
Start with the $7 Mega Link: https://offers.olspsystem.com/get_megalink?olsp=1006001

Profit & Privilege — Evidence-based online business reviews
ProfitAndPrivilege.com — Independent research since 2025

You received this because you signed up for OLSP Academy information.
Not the right fit? No hard feelings — you won't hear from us again.
"""


def send_test():
    if not SMTP_PASSWORD:
        print("GHL_SMTP_PASSWORD not set in .env")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = SUBJECT
    msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"] = TO_EMAIL
    msg.attach(MIMEText(PLAIN, "plain"))
    msg.attach(MIMEText(HTML, "html"))

    print(f"To:      {TO_EMAIL}")
    print(f"From:    {FROM_EMAIL}")
    print(f"Subject: {SUBJECT}")
    print()

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as server:
            server.starttls()
            server.login(FROM_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        print("TEST EMAIL SENT")
    except Exception as e:
        print(f"FAILED: {e}")


if __name__ == "__main__":
    send_test()
