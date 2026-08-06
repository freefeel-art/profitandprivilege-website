"""Owner network reconnection campaign via Hostinger SMTP.

Sends to contacts from the Owner's downloaded Google Contacts exports.
Personal tone — these are known contacts, not cold leads.

Usage:
    python scripts/owner_network_campaign.py [--batch-size 30] [--dry-run]
"""

import os, json, smtplib, time
from datetime import datetime, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from app.core.projects import active_project_runtime_directory
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = "smtp.hostinger.com"
SMTP_PORT = 587
FROM_EMAIL = "info@profitandprivilege.com"
FROM_NAME = "Profit & Privilege"
SMTP_PASSWORD = os.getenv("GHL_SMTP_PASSWORD", "")

STATE_FILE = active_project_runtime_directory() / "owner-network-campaign-state.json"
CONTACTS_FILE = active_project_runtime_directory() / "downloaded-contacts.json"

SUBJECT = "The shortcut most OLSP beginners skip (live Tue/Thu/Sat)"

UTM_SOURCE = "email"
UTM_MEDIUM = "owner_network"
UTM_CAMPAIGN = "olsp_launch"
OLSP_ID = "1006001"

LIVEBINAR_URL = "https://olspacademy.com/c/livebinar"
MEGA_LINK_URL = "https://offers.olspsystem.com/get_megalink"

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0;padding:0;background:#111827;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif">

<table width="100%" cellpadding="0" cellspacing="0" style="background:#111827;padding:40px 20px">
<tr><td align="center">

<table width="580" cellpadding="0" cellspacing="0" style="max-width:580px;background:#1F2937;border-radius:12px;overflow:hidden">

  <tr>
    <td style="padding:40px 36px 24px 36px;text-align:center">
      <span style="font-weight:700;font-size:20px;color:#FFFFFF">Profit &amp; Privilege</span>
      <div style="width:40px;height:3px;background:#B8862B;margin:16px auto 0 auto;border-radius:2px"></div>
    </td>
  </tr>

  <tr>
    <td style="padding:0 36px 8px 36px;font-size:15px;line-height:1.6;color:#D1D5DB">

      <p>Here's something most people skip when trying to earn online:</p>

      <p><strong style="color:#F3F4F6">The live coaching sessions.</strong></p>

      <p>Three times a week — Tuesday, Thursday, and Saturday — someone walks you through exactly what to do. It's not a sales pitch. It's real training, live coaching, and a community of builders learning alongside you.</p>

      <p>No complicated funnels. No monthly fees to start. Just a tracking link you share, and someone shows you how — live.</p>

      <div style="background:#374151;border-left:4px solid #B8862B;padding:16px 20px;margin:20px 0;border-radius:0 8px 8px 0">
        <p style="margin:0;color:#F3F4F6"><strong style="color:#FBBF24">This is the shortcut.</strong><br>Most people spend years trying to figure it out alone. A small group shows up instead.</p>
      </div>

    </td>
  </tr>

  <tr>
    <td align="center" style="padding:12px 36px 20px 36px">
      <a href="{LIVEBINAR_URL}?utm_source={UTM_SOURCE}&utm_medium={UTM_MEDIUM}&utm_campaign={UTM_CAMPAIGN}"
         style="display:inline-block;background:#B8862B;color:#FFFFFF;padding:16px 36px;border-radius:8px;text-decoration:none;font-weight:600;font-size:16px">
        Join the next livebinar →
      </a>
    </td>
  </tr>

  <tr><td style="padding:4px 36px 0 36px"><hr style="border:none;border-top:1px solid #374151;margin:0"></td></tr>

  <tr>
    <td style="padding:20px 36px 32px 36px;text-align:center">
      <p style="font-size:14px;color:#F3F4F6;margin:0 0 12px 0">Ready to see what it's all about right now?</p>
      <a href="{MEGA_LINK_URL}?olsp={OLSP_ID}&utm_source={UTM_SOURCE}&utm_medium={UTM_MEDIUM}&utm_campaign={UTM_CAMPAIGN}"
         style="display:inline-block;background:#1D2433;color:#22C55E;padding:12px 28px;border:1px solid #22C55E;border-radius:8px;text-decoration:none;font-weight:600;font-size:14px">
        Start with the $7 Mega Link →
      </a>
    </td>
  </tr>

  <tr>
    <td style="background:#111827;padding:24px 36px 24px 36px;font-size:12px;color:#6B7280;line-height:1.6;text-align:center">
      <p style="margin:0 0 8px 0">Profit &amp; Privilege — Evidence-based online business reviews</p>
      <p style="margin:0 0 8px 0">
        <a href="https://profitandprivilege.com" style="color:#9CA3AF;text-decoration:underline">ProfitAndPrivilege.com</a>
        &nbsp;·&nbsp;
        <span style="color:#6B7280">Independent research since 2025</span>
      </p>
      <p style="margin:0">Not interested? No hard feelings — you won't hear from us again.</p>
      <p style="margin:4px 0 0 0">
        <a href="mailto:info@profitandprivilege.com?subject=Unsubscribe&body=Please remove me from the OLSP update list." style="color:#64748B">Unsubscribe</a>
      </p>
    </td>
  </tr>

</table>

</td></tr>
</table>

</body>
</html>"""

PLAIN = f"""The shortcut most OLSP beginners skip (live Tue/Thu/Sat)

Here's something most people skip when trying to earn online: the live coaching sessions.

Three times a week someone walks you through exactly what to do. Not a sales pitch — real training, live coaching, and a community alongside you.

Join the next livebinar: {LIVEBINAR_URL}?utm_source={UTM_SOURCE}&utm_medium={UTM_MEDIUM}&utm_campaign={UTM_CAMPAIGN}

Ready to start right now?
$7 Mega Link: {MEGA_LINK_URL}?olsp={OLSP_ID}&utm_source={UTM_SOURCE}&utm_medium={UTM_MEDIUM}&utm_campaign={UTM_CAMPAIGN}

Not interested? No hard feelings.
Unsubscribe: reply to this email with \"unsubscribe\"
— Profit & Privilege"""


def load_state():
    if STATE_FILE.is_file():
        return json.loads(STATE_FILE.read_text())
    return {"sent": [], "bounced": [], "last_index": 0, "batches": 0, "last_batch_at": None}


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = _now_iso()
    STATE_FILE.write_text(json.dumps(state, indent=2))


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def send_email(to_email):
    """Send one email. Returns (success, status_reason)."""
    if not SMTP_PASSWORD:
        return False, "no password"
    msg = MIMEMultipart("alternative")
    msg["Subject"] = SUBJECT
    msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"] = to_email
    msg.attach(MIMEText(PLAIN, "plain"))
    msg.attach(MIMEText(HTML, "html"))
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as server:
            server.starttls()
            server.login(FROM_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        return True, "sent"
    except Exception as e:
        err = str(e).lower()
        if any(kw in err for kw in ("bounce", "does not exist", "invalid", "unknown user",
                                      "mailbox", "not found", "undelivered", "5.1.1", "5.5.0",
                                      "550", "553", "554")):
            return False, f"bounced: {e}"
        if any(kw in err for kw in ("ratelimit", "rate limit", "too many", "4.7.1", "try again")):
            return False, f"rate_limited: {e}"
        return False, f"failed: {e}"


RATE_LIMIT_WAIT = 900  # 15 minutes
RATE_LIMIT_KEYWORDS = ("ratelimit", "rate limit", "too many", "try again later", "4.7.1")


if __name__ == "__main__":
    import sys

    batch_size = 10
    dry_run = False

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--batch-size" and i + 1 < len(args):
            batch_size = int(args[i + 1]); i += 2
        elif args[i] == "--dry-run":
            dry_run = True; i += 1
        else:
            i += 1

    if not SMTP_PASSWORD:
        print("GHL_SMTP_PASSWORD not set in .env")
        sys.exit(1)

    if not CONTACTS_FILE.is_file():
        print("No downloaded contacts found. Run download first.")
        sys.exit(1)

    data = json.loads(CONTACTS_FILE.read_text())
    contacts = data.get("emails", [])
    print(f"Total new contacts: {len(contacts)}")

    state = load_state()

    if dry_run:
        already_sent = set(state["sent"])
        remaining = [c for c in contacts if c not in already_sent]
        print(f"Already sent: {len(already_sent)}, Remaining: {len(remaining)}")
        print(f"DRY RUN — next 5: {remaining[:5]}")
        sys.exit(0)

    rate_limited = False
    total_sent = len(state["sent"])
    total_bounced = len(state.get("bounced", []))
    consecutive_fails = 0

    while True:
        already_sent = set(state["sent"])
        already_bounced = set(state.get("bounced", []))
        remaining = [c for c in contacts if c not in already_sent and c not in already_bounced]

        if not remaining:
            print(f"\nCampaign complete. {total_sent}/{len(contacts)} sent, {total_bounced} bounced.")
            break

        if rate_limited:
            print(f"Rate limit — waiting {RATE_LIMIT_WAIT}s...")
            time.sleep(RATE_LIMIT_WAIT)
            rate_limited = False

        batch = remaining[:batch_size]
        batch_num = state["batches"] + 1
        print(f"\nBatch {batch_num}: {len(batch)} emails ({total_sent} sent, {total_bounced} bounced, {len(remaining) - len(batch)} after this)")

        sent_this_batch = 0
        bounced_this_batch = 0
        for email in batch:
            ok, reason = send_email(email)
            if ok:
                state["sent"].append(email)
                sent_this_batch += 1
                total_sent += 1
                consecutive_fails = 0
                print(f"  OK {sent_this_batch}/{len(batch)}: {email}")
            elif reason.startswith("bounced"):
                state.setdefault("bounced", []).append(email)
                bounced_this_batch += 1
                total_bounced += 1
                consecutive_fails += 1
                print(f"  BOUNCE: {email}")
            elif reason.startswith("rate_limited"):
                consecutive_fails += 1
                print(f"  RATE: {email} — {reason}")
                rate_limited = True
                break
            else:
                consecutive_fails += 1
                print(f"  FAIL: {email} — {reason}")
            time.sleep(1.5)

        if sent_this_batch > 0 or bounced_this_batch > 0:
            state["last_index"] = state["last_index"] + sent_this_batch + bounced_this_batch
            state["batches"] += 1
            state["last_batch_at"] = _now_iso()
            state["last_batch_size"] = len(batch)
            save_state(state)

        if consecutive_fails > 5 and not rate_limited:
            print(f"Too many consecutive failures ({consecutive_fails}) — stopping.")
            break

    state["last_batch_at"] = _now_iso()
    save_state(state)
    print(f"\nFinal: {total_sent} sent, {total_bounced} bounced, {len(contacts) - total_sent - total_bounced} remaining")
