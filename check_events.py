"""Poll the activity calendar API and email when a new event appears
for the watched activityId.

Environment variables:
  API_URL        URL of the calendar JSON endpoint (required unless --file)
  ACTIVITY_ID    activityId to follow
  SMTP_HOST      e.g. smtp.gmail.com
  SMTP_PORT      e.g. 465
  SMTP_USER      login for the SMTP server (also used as sender)
  SMTP_PASSWORD  app password for the SMTP server
  EMAIL_TO       where to send the notification

Usage:
  python check_events.py                # fetch API_URL
  python check_events.py --file x.json  # read a local file (testing)
  python check_events.py --dry-run      # print the email instead of sending
"""

import argparse
import json
import os
import smtplib
import sys
import urllib.request
from email.message import EmailMessage
from pathlib import Path

STATE_FILE = Path(__file__).with_name("seen_events.json")
DEFAULT_ACTIVITY_ID = "Activity2518853345471384032"


def load_calendar(args):
    if args.file:
        return json.loads(Path(args.file).read_text(encoding="utf-8"))
    url = os.environ["API_URL"]
    req = urllib.request.Request(url, headers={"User-Agent": "event-watcher/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def matching_events(calendar, activity_id):
    for day in calendar:
        for slot in day.get("slots", []):
            if slot.get("activityId") == activity_id:
                yield slot


def build_email(events):
    msg = EmailMessage()
    count = len(events)
    msg["Subject"] = (
        f"New event: {events[0]['name']} {events[0]['startTime'][:16].replace('T', ' ')}"
        if count == 1
        else f"{count} new events"
    )
    msg["From"] = os.environ.get("SMTP_USER", "event-watcher@localhost")
    # Recipients go in Bcc so they can't see each other's addresses.
    msg["To"] = msg["From"]
    msg["Bcc"] = os.environ.get("EMAIL_TO", "")

    text_lines, html_parts = [], []
    for e in events:
        when = f"{e['startTime'][:16].replace('T', ' ')} - {e['endTime'][11:16]}"
        hosts = ", ".join(r["displayName"] for r in e.get("responsible", []))
        spots = f"{e['booked']}/{e['maxAttendees']} booked, waiting list {e['waitingList']}"
        text_lines += [e["name"], f"  {when}", f"  Hosts: {hosts}", f"  {spots}", ""]
        html_parts.append(
            f"<h2>{e['name']}</h2>"
            f"<p><b>{when}</b><br>Hosts: {hosts}<br>{spots}</p>"
            f"{e.get('description', '')}<hr>"
        )

    msg.set_content("\n".join(text_lines))
    msg.add_alternative("".join(html_parts), subtype="html")
    return msg


def send_email(msg):
    host = os.environ["SMTP_HOST"]
    port = int(os.environ.get("SMTP_PORT", "465"))
    with smtplib.SMTP_SSL(host, port) as smtp:
        smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
        smtp.send_message(msg)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    activity_id = os.environ.get("ACTIVITY_ID") or DEFAULT_ACTIVITY_ID
    events = list(matching_events(load_calendar(args), activity_id))

    first_run = not STATE_FILE.exists()
    seen = set() if first_run else set(json.loads(STATE_FILE.read_text()))
    new = [e for e in events if e["entityId"] not in seen]

    if first_run:
        # Don't email everything that already exists; just start tracking.
        print(f"First run: recording {len(new)} existing event(s), no email sent.")
    elif new:
        msg = build_email(new)
        if args.dry_run:
            print(msg.get_body(("plain",)).get_content())
        else:
            send_email(msg)
        print(f"Notified about {len(new)} new event(s).")
    else:
        print("No new events.")

    STATE_FILE.write_text(json.dumps(sorted(seen | {e["entityId"] for e in events}), indent=2) + "\n")


if __name__ == "__main__":
    sys.exit(main())
