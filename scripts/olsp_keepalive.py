"""OLSP session keepalive — run periodically to prevent session expiry.

Usage:
    python scripts/olsp_keepalive.py          # check and refresh
    python scripts/olsp_keepalive.py --cron   # cron-friendly, one line output

Schedule: every 4-6 hours via cron or systemd timer.
    crontab: 0 */6 * * * cd /path/to/hermes && .venv/bin/python scripts/olsp_keepalive.py --cron
"""

import sys
import asyncio
from app.providers.olsp_dashboard import _health_check


async def main():
    ok = await _health_check()
    if "--cron" in sys.argv:
        print(f"OK: {ok}" if ok else "EXPIRED")
    else:
        print("Session active" if ok else "SESSION EXPIRED — run: python -m app.providers.olsp_dashboard init")
    return 0 if ok else 3


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
