# Sauna Gus Alert ❄️🔥

Emails you when a new **Gus** event is posted in the calendar.

## Setup

Add these repository secrets (Settings → Secrets and variables → Actions):

- `API_URL`: `api for the saunas`
- `SMTP_USER`: Gmail address that sends the alerts
- `SMTP_PASSWORD`: Gmail app password for that account
- `EMAIL_TO`: recipients, comma-separated (sent as BCC)

## Test

Actions → *Watch for new Gus events* → **Run workflow**, then tick **Send test email**.
