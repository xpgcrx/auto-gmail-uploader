import pytest
from unittest.mock import MagicMock, patch
from src.drive_client import DriveClient
from google.oauth2.credentials import Credentials

@pytest.fixture
def mock_credentials():
    return MagicMock(spec=Credentials)

@pytest.fixture
def drive_client(mock_credentials):
    with patch('src.drive_client.build') as mock_build:
        client = DriveClient(credentials=mock_credentials)
        return client, mock_build.return_value

def test_file_exists_true(drive_client):
    """Test when a file exists in the folder."""
    client, mock_service = drive_client
    mock_list = mock_service.files().list
    mock_list.return_value.execute.return_value = {
        'files': [{'id': '123', 'name': 'test.md'}]
    }

    exists = client.file_exists("test.md", "folder_id")
    
    assert exists is True
    mock_list.assert_called_with(
        q="name = 'test.md' and 'folder_id' in parents and trashed = false",
        fields="files(id, name)"
    )

def test_file_exists_false(drive_client):
    """Test when a file does not exist in the folder."""
    client, mock_service = drive_client
    mock_list = mock_service.files().list
    mock_list.return_value.execute.return_value = {'files': []}

    exists = client.file_exists("absent.md", "folder_id")
    
    assert exists is False

def test_upload_markdown(drive_client):
    """Test the file upload functionality."""
    client, mock_service = drive_client
    mock_create = mock_service.files().create
    mock_create.return_value.execute.return_value = {'id': 'new_file_id'}

    file_id = client.upload_markdown("test.md", "# Content", "folder_id")
    
    assert file_id == 'new_file_id'
    mock_create.assert_called_once()
    # Validate a part of the call arguments (body)
    args, kwargs = mock_create.call_args
    assert kwargs['body']['name'] == 'test.md'
    assert kwargs['body']['parents'] == ['folder_id']
