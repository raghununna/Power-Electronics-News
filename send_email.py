#!/usr/bin/env python3
"""
Email today's digest to your Gmail inbox.
Used by the GitHub Actions workflow. Configured via repository secrets:

    GMAIL_USER      your Gmail address, e.g. john.smith@gmail.com
    GMAIL_APP_PASS  16-character Gmail "App Password" (no spaces needed)
    DIGEST_TO       (optional) other recipient; default: GMAIL_USER

If the secrets are not set, this script exits quietly (workflow stays green).
"""

import datetime as dt
import os
import re
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIGEST = os.path.join(BASE_DIR, "digests", "latest.html")

USER = os.environ.get("GMAIL_USER", "").strip()
PASS = os.environ.get("GMAIL_APP_PASS", "").strip()
TO = os.environ.get("DIGEST_TO", "").strip() or USER


def main():
    if not USER or not PASS:
        print("Email skipped: GMAIL_USER / GMAIL_APP_PASS secrets not set.")
        print("Add them under Settings -> Secrets and variables -> Actions.")
        return 0
    if not os.path.exists(DIGEST):
        print("No digest found - nothing to send.")
        return 0

    with open(DIGEST, encoding="utf-8") as f:
        html = f.read()

    today = dt.date.today().strftime("%d %b %Y")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"\u26a1 Power & EV Daily Digest \u2014 {today}"
    msg["From"] = USER
    msg["To"] = TO

    # plain-text fallback (titles + links) for mail clients that block HTML
    lines = []
    for m in re.finditer(r"<h3><a href=\"([^\"]+)\"[^>]*>(.*?)</a></h3>", html):
        title = re.sub(r"<[^>]+>", "", m.group(2))
        lines.append(f"- {title}\n  {m.group(1)}")
    text = "Power & EV Daily Digest " + today + "\n\n" + "\n\n".join(lines or ["(open the HTML view)]"])

    msg.attach(MIMEText(text, "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=60) as srv:
        srv.starttls()
        srv.login(USER, PASS)
        srv.send_message(msg)
    print(f"Digest emailed to {TO} ✓")
    return 0


if __name__ == "__main__":
    sys.exit(main())
