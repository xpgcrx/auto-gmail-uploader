import os
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2.credentials import Credentials
from typing import Optional

class DriveClient:
    """Handles interactions with the Google Drive API."""

    def __init__(self, credentials: Optional[Credentials] = None) -> None:
        """
        Initialize the Google Drive API client.
        :param credentials: Credentials object. Generates from env vars if not provided.
        """
        if credentials is None:
            credentials = self._get_credentials_from_env()
        
        self.service = build('drive', 'v3', credentials=credentials)

    def _get_credentials_from_env(self) -> Credentials:
        """Generate OAuth 2.0 credentials from environment variables."""
        client_id = os.environ.get("GCP_CLIENT_ID")
        client_secret = os.environ.get("GCP_CLIENT_SECRET")
        refresh_token = os.environ.get("GCP_REFRESH_TOKEN")

        if not all([client_id, client_secret, refresh_token]):
            raise ValueError("Required environment variables are not set.")

        return Credentials(
            token=None,
            refresh_token=refresh_token,
            client_id=client_id,
            client_secret=client_secret,
            token_uri="https://oauth2.googleapis.com/token"
        )

    def upload_markdown(self, filename: str, content: str, folder_id: str) -> str:
        """
        Upload a Markdown string as a file to Google Drive.
        
        :param filename: Desired name of the file in Drive.
        :param content: Markdown text content.
        :param folder_id: ID of the destination folder.
        :return: ID of the created file.
        """
        file_metadata = {
            'name': filename,
            'parents': [folder_id],
            'mimeType': 'text/markdown'
        }
        
        # Convert string to binary stream for upload
        media = MediaIoBaseUpload(
            io.BytesIO(content.encode('utf-8')),
            mimetype='text/markdown',
            resumable=True
        )

        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        return file.get('id', '')

    def file_exists(self, filename: str, folder_id: str) -> bool:
        """
        Check if a file with the same name already exists in the folder.
        
        :param filename: Filename to check.
        :param folder_id: Destination folder ID.
        :return: True if file exists, False otherwise.
        """
        # Query: matching name, matching parent, and not in trash
        query = f"name = '{filename}' and '{folder_id}' in parents and trashed = false"
        results = self.service.files().list(q=query, fields="files(id, name)").execute()
        return len(results.get('files', [])) > 0
