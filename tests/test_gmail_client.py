import pytest
from unittest.mock import MagicMock, patch
from src.gmail_client import GmailClient
from google.oauth2.credentials import Credentials

@pytest.fixture
def mock_credentials():
    return MagicMock(spec=Credentials)

@pytest.fixture
def gmail_client(mock_credentials):
    with patch('src.gmail_client.build') as mock_build:
        client = GmailClient(credentials=mock_credentials)
        return client, mock_build.return_value

def test_search_messages(gmail_client):
    """Test the message search functionality."""
    client, mock_service = gmail_client
    mock_list = mock_service.users().messages().list
    mock_list.return_value.execute.return_value = {
        'messages': [{'id': '123'}, {'id': '456'}]
    }

    results = client.search_messages("query")
    
    assert len(results) == 2
    assert results[0]['id'] == '123'
    mock_list.assert_called_with(userId='me', q="query")

def test_get_message_details(gmail_client):
    """Test the retrieval of message details."""
    client, mock_service = gmail_client
    mock_get = mock_service.users().messages().get
    mock_get.return_value.execute.return_value = {
        'id': '123',
        'payload': {
            'headers': [
                {'name': 'Subject', 'value': 'Test Subject'},
                {'name': 'Date', 'value': 'Mon, 28 Feb 2026 10:00:00 +0900'}
            ],
            'body': {
                'data': 'PGgxPkhlbGxvPC9oMT4=' # <h1>Hello</h1> in base64
            }
        }
    }

    details = client.get_message_details("123")
    
    assert details['id'] == '123'
    assert details['subject'] == 'Test Subject'
    assert "<h1>Hello</h1>" in details['html_content']
    assert details['date'].year == 2026
