import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow

# Required scopes (Gmail read-only, Drive file creation)
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/drive.file'
]

def main() -> None:
    """Run a local server to authenticate the user and retrieve a refresh token."""
    client_secret_file = 'client_secret.json'
    
    if not os.path.exists(client_secret_file):
        print(f"Error: '{client_secret_file}' not found.")
        print("Please rename your downloaded JSON to 'client_secret.json' and place it in the project root.")
        return

    # Start authentication flow for a desktop application
    flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
    creds = flow.run_local_server(port=0)

    # Display the result
    print("\n--- Authentication Successful! ---")
    print(f"Refresh Token: {creds.refresh_token}")
    print("\n--- Important Note ---")
    print("This Refresh Token is needed for Cloud Functions to access your Gmail.")
    print("Keep it safe and do NOT commit it to Git.")

if __name__ == '__main__':
    main()
