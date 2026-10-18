# Sauna Gus Alert ❄️🔥

Emails you when a new **Gus** event is posted in the calendar.

## Setup

Add these repository secrets (Settings → Secrets and variables → Actions):

- `API_URL`: `api for the saunas`
- `SMTP_USER`: Gmail address that sends the alerts
- `SMTP_PASSWORD`: Gmail app password for that account
- `EMAIL_TO`: recipients, comma-separated (sent as BCC)
- `NTFY_TOPIC` (optional): an [ntfy](https://ntfy.sh) topic name for phone push notifications.
  Subscribe to the same topic in the ntfy app.

## Schedule

GitHub's own `schedule` is unreliable (often hours apart), so [cron-job.org](https://cron-job.org)
starts the workflow every 5 minutes through the GitHub API (`workflow_dispatch`). It uses a
fine-grained token with **Actions: Read and write** on this repo only.

- Token expires **16 January 2027**. Regenerate it and update the cron-job.org header before then.
- 401 in cron-job.org means the token expired or is wrong.

## Test

Actions → *Watch for new Gus events* → **Run workflow**, then tick **Send test email**.
