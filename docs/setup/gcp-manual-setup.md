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
