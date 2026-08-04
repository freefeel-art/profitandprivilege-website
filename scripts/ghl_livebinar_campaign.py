"""OLSP Livebinar email campaign via Hostinger SMTP.

Sends in daily batches of 50. Tracks sent, bounced, and unsubscribed in
runtime/email-campaign-state.json. Every link carries UTM parameters for
conversion attribution.

Usage:
    python scripts/ghl_livebinar_campaign.py [--batch-size 50] [--dry-run]
"""

import os, json, smtplib, time
from datetime import datetime, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from app.core.projects import active_project_runtime_directory
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = "smtp.hostinger.com"
SMTP_PORT = 587
FROM_EMAIL = os.getenv("GHL_ADMIN_EMAIL", "info@profitandprivilege.com")
FROM_NAME = "Profit & Privilege"
SMTP_PASSWORD = os.getenv("GHL_SMTP_PASSWORD", "")

GHL_TOKEN = os.getenv("GHL_TOKEN", "")
LOC_ID = "GSInZxexJyODz5tKWVuH"
BASE = "https://services.leadconnectorhq.com"

STATE_FILE = active_project_runtime_directory() / "email-campaign-state.json"

SUBJECT = "The shortcut most OLSP beginners skip (Tue/Thu/Sat)"

UTM_SOURCE = "email"
UTM_MEDIUM = "livebinar"
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

      <p>You signed up to learn more about OLSP Academy. Here's something most people skip:</p>

      <p><strong style="color:#F3F4F6">The live coaching sessions.</strong></p>

      <p>Three times a week — Tuesday, Thursday, and Saturday — someone walks you through exactly what to do. It's not a sales pitch. It's real training, live coaching, and a community of builders learning alongside you.</p>

      <div style="background:#374151;border-left:4px solid #B8862B;padding:16px 20px;margin:20px 0;border-radius:0 8px 8px 0">
        <p style="margin:0;color:#F3F4F6"><strong style="color:#FBBF24">This is the shortcut.</strong><br>Most people spend years trying to figure it out alone. A small group shows up to the livebinar instead.</p>
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
      <p style="font-size:14px;color:#F3F4F6;margin:0 0 12px 0">Ready to start earning right now?</p>
      <a href="{MEGA_LINK_URL}?olsp={OLSP_ID}&utm_source={UTM_SOURCE}&utm_medium={UTM_MEDIUM}&utm_campaign={UTM_CAMPAIGN}"
         style="display:inline-block;background:#1D2433;color:#22C55E;padding:12px 28px;border:1px solid #22C55E;border-radius:8px;text-decoration:none;font-weight:600;font-size:14px">
        Start with the $7 Mega Link →
      </a>
    </td>
  </tr>

  <tr>
    <td style="background:#111827;padding:24px 36px 24px 36px;font-size:12px;color:#6B7280;line-height:1.6;text-align:center">
      <p style="margin:0 0 8px 0">Profit &amp; Privilege — Evidence-based OLSP Academy review</p>
      <p style="margin:0 0 8px 0">
        <a href="https://profitandprivilege.com" style="color:#9CA3AF;text-decoration:underline">ProfitAndPrivilege.com</a>
        &nbsp;·&nbsp;
        <span style="color:#6B7280">Independent research since 2025</span>
      </p>
      <p style="margin:0">
        You received this because you signed up for OLSP Academy information.
        <a href="mailto:info@profitandprivilege.com?subject=Unsubscribe&body=Please remove me from OLSP Academy updates." style="color:#9CA3AF;text-decoration:underline">Unsubscribe</a>
      </p>
    </td>
  </tr>

</table>

</td></tr>
</table>

</body>
</html>"""


def send_email(to_email: str) -> tuple[bool, str]:
    """Send one email. Returns (success, status_reason)."""
    if not SMTP_PASSWORD:
        return False, "no_smtp_password"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = SUBJECT
    msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"] = to_email
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


def fetch_contacts() -> list[dict]:
    headers = {
        "Authorization": f"Bearer {GHL_TOKEN}",
        "Accept": "application/json",
        "Version": "2021-07-28",
    }
    contacts = []
    next_url = f"{BASE}/contacts/?locationId={LOC_ID}&limit=100"
    while next_url:
        r = requests.get(next_url, headers=headers, timeout=15)
        if not r.ok:
            break
        data = r.json()
        for c in data.get("contacts", []):
            tags = c.get("tags", [])
            if "olsp_lead" in tags and "no_email" not in tags and c.get("email"):
                contacts.append({"id": c["id"], "email": c["email"]})
        next_url = data.get("meta", {}).get("nextPageUrl")
        if next_url and not next_url.startswith("http"):
            next_url = f"{BASE}{next_url}"
        time.sleep(0.2)
    return contacts


def load_state() -> dict:
    if STATE_FILE.is_file():
        return json.loads(STATE_FILE.read_text())
    return {
        "sent": [],
        "bounced": [],
        "last_index": 0,
        "total": 0,
        "batches": 0,
        "last_batch_at": None,
        "last_batch_size": 0,
    }


def save_state(state: dict):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


if __name__ == "__main__":
    import sys
    batch_size = 50
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

    print("Fetching olsp_lead contacts...")
    contacts = fetch_contacts()
    print(f"Found {len(contacts)} contacts with email\n")

    state = load_state()
    state["total"] = len(contacts)

    # ── Data integrity: detect and document the last_index / sent mismatch ──
    sent_count_total = len(state["sent"])
    if state["last_index"] > sent_count_total:
        gap = state["last_index"] - sent_count_total
        print(f"⚠  DATA ANOMALY: last_index={state['last_index']} but sent has {sent_count_total} entries")
        print(f"   {gap} contacts at indices {sent_count_total}–{state['last_index']-1} may have been sent but not recorded.")
        print(f"   Keeping last_index={state['last_index']} — will not resend potentially-duplicate contacts.")
        state["anomaly_last_index_gap"] = gap
        state["anomaly_note"] = f"On {_now_iso()}: last_index ahead of sent by {gap}. Conservative: skip these contacts."
    else:
        state.pop("anomaly_last_index_gap", None)
        state.pop("anomaly_note", None)

    already_sent = set(state["sent"])
    start = state["last_index"]

    remaining = [c for c in contacts[start:] if c["email"] not in already_sent]
    batch = remaining[:batch_size]

    if not batch:
        print("All contacts have been sent. Campaign complete.")
        sys.exit(0)

    print(f"Batch {state['batches'] + 1}: sending {len(batch)} emails (index {start}+)")
    if dry_run:
        print("DRY RUN — would send to:")
        for c in batch:
            print(f"  {c['email']}")
        print(f"\nTotal remaining after this batch: {len(remaining) - len(batch)}")
        sys.exit(0)

    sent_count = 0
    bounced_count = 0
    rate_hit = False
    for contact in batch:
        success, reason = send_email(contact["email"])
        if success:
            state["sent"].append(contact["email"])
            sent_count += 1
            print(f"  OK {sent_count}/{len(batch)}: {contact['email']}")
        elif reason.startswith("bounced"):
            state["bounced"].append(contact["email"])
            bounced_count += 1
            print(f"  BOUNCE: {contact['email']} — {reason}")
        elif reason.startswith("rate_limited"):
            print(f"  RATE: {contact['email']} — hostinger rate limit hit, stopping batch")
            rate_hit = True
            break
        else:
            print(f"  FAIL: {contact['email']} — {reason}")
        time.sleep(0.5)

    # Advance only past actually processed contacts — rate-limited contacts retry next run
    processed = sent_count + bounced_count
    state["last_index"] = start + (processed if rate_hit else len(batch))
    state["batches"] += 1
    state["last_batch_at"] = _now_iso()
    state["last_batch_size"] = processed
    save_state(state)

    print(f"\nBatch complete: {sent_count}/{processed} sent, {bounced_count} bounced"
          f"{' — rate limit hit, retry remaining next run' if rate_hit else ''}")
    print(f"Total sent: {len(state['sent'])}/{len(contacts)}")
    print(f"Total bounced: {len(state.get('bounced', []))}")
    print(f"State saved to {STATE_FILE}")
