# Setup Instructions

This document provides a detailed guide on how to set up and deploy the **auto-gmail-uploader** project.

## 1. Google Cloud Manual Preparation

- Create a project and enable APIs (Gmail, Drive, Secret Manager, Cloud Functions, Cloud Run, Cloud Build).
- Configure the OAuth consent screen and add test users.
- Create OAuth 2.0 Client ID (Desktop App) and download `client_secret.json`.

Detailed steps for Google Cloud manual preparation can be found in [gcp-manual-setup.md](gcp-manual-setup.md).

## 2. Obtain Initial Token

```bash
# Place client_secret.json in the project root
uv run scripts/get_refresh_token.py
# Note down the displayed Refresh Token
```

## 3. Configure Environment Variables

Create a `.env` file and fill in the tokens.

```env
GCP_CLIENT_ID="..."
GCP_CLIENT_SECRET="..."
GCP_REFRESH_TOKEN="..."
DISCORD_WEBHOOK_URL="..."
```

## 4. Deploy Infrastructure (Terraform)

```bash
cd infra
# Create terraform.tfvars (with project_id, region)
terraform init
terraform apply
```

## 5. Synchronize Secrets

```bash
uv run scripts/update_secrets.py
```
