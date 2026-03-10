# Google Cloud Manual Setup Guide (Phase 0)

This document explains the one-time manual steps required to set up the project on Google Cloud.

---

## Step 1: Project Creation and Billing

1.  Log in to the **Google Cloud Console** ([console.cloud.google.com](https://console.cloud.google.com/)).
2.  Click the project selection dropdown at the top and select "**New Project**".
3.  **Project Name**: `auto-gmail-uploader` (or any name you prefer) and click "Create".
4.  After creation, go to the "**Billing**" menu and ensure a valid billing account is linked to the project.
    - _Note: While usage is expected to stay within the Free Tier, a billing account is required for Cloud Functions and other services._

## Step 2: Enabling Required APIs

Search for the following APIs and click "**Enable**" for each:

1.  **Gmail API**
2.  **Google Drive API**
3.  **Secret Manager API**
4.  **Cloud Functions API**
5.  **Cloud Build API**
6.  **Cloud Run Admin API**
7.  **Cloud Scheduler API**
8.  **Cloud Logging API**

## Step 3: Configuring the OAuth Consent Screen

Configure the consent screen required to access personal Gmail data.

1.  Go to "**APIs & Services**" > "**OAuth consent screen**".
2.  **User Type**: Select "**External**" and click "Create".
3.  **App Information**:
    - **App name**: `Gmail to Drive Uploader`
    - **User support email**: Your Gmail address
    - **Developer contact info**: Your Gmail address
4.  Click "Save and Continue" through the scopes section.
5.  In the "**Test users**" section, click "**ADD USERS**" and enter **your own Gmail address** (where you receive the newsletters).
    - _Important: Skipping this will result in errors during authentication._
6.  Click "Save and Continue" and then "Back to Dashboard".
7.  **Crucial Step to Prevent Expiry**: On the OAuth consent screen dashboard, under "Publishing status", click "**PUBLISH APP**" to change the status from "Testing" to "In production".
    - _Note: If left in "Testing", your refresh token will expire every 7 days, causing `invalid_grant` errors. Since this is an internal/personal tool, you do not need to go through Google's app verification process._

## Step 4: Creating OAuth 2.0 Credentials

Generate the credentials (keys) needed for the application to access Gmail.

1.  Go to the "**Credentials**" menu.
2.  Click "**+ CREATE CREDENTIALS**" > "**OAuth client ID**".
3.  **Application type**: Select "**Desktop app**".
4.  **Name**: `Uploader Local Key` (or any name).
5.  Click "Create".
6.  In the dialog, click "**DOWNLOAD JSON**".
7.  Rename the downloaded file to `client_secret.json` and store it safely in the project root.
    - _Note: NEVER commit this file to Git._

---

## Next Steps

Once these steps are complete, proceed with Phase 1 (Environment Setup).
After that, you will run a script to obtain a "Refresh Token" using this `client_secret.json` to be stored in Secret Manager.

---

## Troubleshooting

### Error: `invalid_grant: Token has been expired or revoked.`

This error occurs if your Google API refresh token has expired. This typically happens if the OAuth consent screen was left in "Testing" mode (which limits token validity to 7 days).

**How to fix:**
1. **Publish the App**: In the Google Cloud Console, go to **APIs & Services** > **OAuth consent screen** and click **PUBLISH APP** to change the status to "In production".
2. **Re-authenticate locally**: Run the following command and authenticate in your browser to get a new token:
   ```bash
   uv run python scripts/get_refresh_token.py
   ```
3. **Update `.env`**: Copy the new "Refresh Token" output and update the `GCP_REFRESH_TOKEN` value in your `.env` file.
4. **Update Secret Manager**: Run the script to push the new token to Google Cloud Secret Manager:
   ```bash
   uv run python scripts/update_secrets.py
   ```
