# Buckalew CRM Automation

CRM automation workflows for Buckalew Financial Services using GoHighLevel.

## 🚀 Workflows

| # | Workflow | File | Description |
|---|----------|------|-------------|
| 1 | New Lead Follow-Up | `01_new_lead_followup.py` | Auto-follow up with new leads (SMS + email + task) |
| 2 | Client Onboarding | `02_client_onboarding.py` | Welcome sequence for new clients |
| 3 | Appointment Reminders | `03_appointment_reminders.py` | 24h and 2h SMS/email reminders |
| 4 | Lead Scoring | `04_lead_scoring.py` | Auto-score leads based on engagement |
| 5 | Re-engagement | `05_reengagement.py` | Win back inactive leads (30+ days) |

## ⚙️ Setup

1. Set your GoHighLevel API key:
   ```
   set GHL_API_KEY=pit-fcb5ac96-c1fb-489a-bbdc-a6bea29e23ff
   ```

2. Set your Location ID:
   ```
   set GHL_LOCATION_ID=your_location_id_here
   ```

3. Run any workflow:
   ```
   python workflows/01_new_lead_followup.py
   ```

## 📅 Scheduling

Use OpenClaw cron or Windows Task Scheduler to run workflows automatically:
- **New Lead Check**: Every 30 minutes
- **Appointment Reminders**: Every hour
- **Lead Scoring**: Daily at 6 AM
- **Re-engagement**: Daily at 9 AM

## 🔧 GoHighLevel API

- Base URL: `https://services.leadconnectorhq.com`
- Auth: Bearer token
- Version: `2021-07-28`

## 📁 Project Structure

```
Buckalew-CRM-Automation/
├── README.md
├── .env                          # API keys
├── CRM_Automation_Setup_Guide.md # Detailed setup guide
└── workflows/
    ├── 01_new_lead_followup.py
    ├── 02_client_onboarding.py
    ├── 03_appointment_reminders.py
    ├── 04_lead_scoring.py
    └── 05_reengagement.py
```
