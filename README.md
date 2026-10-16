# Sauna Gus Alert ❄️🔥

Emails you when a new **Gus** event is posted in the Vinterbad Bryggen calendar.

A GitHub Action runs [`check_events.py`](check_events.py) about every 5 minutes. It reads the
calendar API, keeps events with activityId `Activity2518853345471384032`, and emails any it hasn't
seen before. Seen events are stored in `seen_events.json`, which the bot commits back to the repo.

## Setup

Add these repository secrets (Settings → Secrets and variables → Actions):

- `API_URL`: `https://www.vinterbadbryggen.com/api/activity/event/days`
- `SMTP_USER`: Gmail address that sends the alerts
- `SMTP_PASSWORD`: Gmail app password for that account
- `EMAIL_TO`: recipients, comma-separated (sent as BCC)

## Test

Actions → *Watch for new Gus events* → **Run workflow**, then tick **Send test email**.
