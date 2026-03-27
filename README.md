# Atlas Skills

Custom [OpenClaw](https://openclaw.ai) skills for Atlas AI assistant.

## 📚 Available Skills

| Skill | Description |
|-------|-------------|
| [git-helper](./git-helper/) | Common git operations wrapper |
| [n8n-automation](./n8n-automation/) | n8n workflow design with retries, logging, and review queues |
| [meta-ads-api](./meta-ads-api/) | Meta (Facebook) Ads API integration |
| [ga4-analytics-toolkit](./ga4-analytics-toolkit/) | Google Analytics 4 + Search Console integration |

## 🔄 Auto-Sync Setup

This repo is the **source of truth** for all skills. Changes sync automatically to GitHub.

### How It Works

1. Skills live in both places:
   - **Local:** `%APPDATA%\npm\node_modules\openclaw\skills\`
   - **GitHub:** `C:\Users\larry\atlas-skills\`

2. When installing new skills, I now:
   - Install to local OpenClaw directory
   - Copy to `atlas-skills` repo
   - Auto-commit and push to GitHub

### Manual Sync

To sync any changes manually:

```powershell
.\sync-skills.ps1
```

To add a custom commit message:

```powershell
.\sync-skills.ps1 -Message "Added new Facebook Ads workflow"
```

## 📂 Repo Structure

```
atlas-skills/
├── git-helper/              # Git operations wrapper
├── n8n-automation/          # n8n workflow design
│   └── assets/
│       └── runbook-template.md
├── meta-ads-api/            # Meta/Facebook Ads API
├── ga4-analytics-toolkit/   # GA4 + Search Console
│   └── references/
│       └── api-reference.md
├── Buckalew-CRM-Automation/ # CRM workflow backups
├── sync-skills.ps1          # Auto-sync script
└── README.md
```

## 🤝 Contributing

Found a bug or want to improve a skill? Open an issue or PR!

## 📄 License

Private use only. These skills are custom builds for Larry Buckalew's personal use.
