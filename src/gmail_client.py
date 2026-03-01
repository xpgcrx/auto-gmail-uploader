import os
import base64
import email.utils
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from typing import Any, Optional

class GmailClient:
    """Handles interactions with the Gmail API."""

    def __init__(self, credentials: Optional[Credentials] = None) -> None:
        """
        Initialize the Gmail API client.
        :param credentials: Credentials object. Generates from env vars if not provided.
        """
        if credentials is None:
            credentials = self._get_credentials_from_env()
        
        self.service = build('gmail', 'v1', credentials=credentials)

    def _get_credentials_from_env(self) -> Credentials:
        """Generate OAuth 2.0 credentials from environment variables."""
        client_id = os.environ.get("GCP_CLIENT_ID")
        client_secret = os.environ.get("GCP_CLIENT_SECRET")
        refresh_token = os.environ.get("GCP_REFRESH_TOKEN")

        if not all([client_id, client_secret, refresh_token]):
            raise ValueError("Required environment variables (GCP_CLIENT_ID, GCP_CLIENT_SECRET, GCP_REFRESH_TOKEN) are not set.")

        return Credentials(
            token=None,
            refresh_token=refresh_token,
            client_id=client_id,
            client_secret=client_secret,
            token_uri="https://oauth2.googleapis.com/token"
        )

    def search_messages(self, query: str) -> list[dict[str, str]]:
        """
        Search for Gmail messages matching the specified query.
        :param query: Search query (e.g., label:news)
        :return: List of message metadata containing IDs.
        """
        results = self.service.users().messages().list(userId='me', q=query).execute()
        return results.get('messages', [])

    def get_message_details(self, message_id: str) -> dict[str, Any]:
        """
        Retrieve detailed information (Subject, HTML body, Date) for a message ID.
        :param message_id: Gmail message ID.
        :return: Dictionary of extracted email data.
        """
        msg = self.service.users().messages().get(userId='me', id=message_id, format='full').execute()
        payload = msg['payload']
        headers = payload.get('headers', [])

        subject = ""
        date_str = ""
        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
            if header['name'] == 'Date':
                date_str = header['value']

        # Extract HTML content from message parts or directly from body
        html_content = ""
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/html':
                    data = part['body'].get('data')
                    if data:
                        html_content = base64.urlsafe_b64decode(data).decode('utf-8')
                        break
        else:
            data = payload.get('body', {}).get('data')
            if data:
                html_content = base64.urlsafe_b64decode(data).decode('utf-8')

        # Convert date string to Python datetime object
        dt = email.utils.parsedate_to_datetime(date_str) if date_str else datetime.now()

        return {
            'id': message_id,
            'subject': subject,
            'html_content': html_content,
            'date': dt
        }
