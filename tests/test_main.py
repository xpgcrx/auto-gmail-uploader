import pytest
from unittest.mock import MagicMock, patch
from src.main import main
from datetime import datetime

@pytest.fixture
def mock_config():
    """Mock application configuration."""
    with patch('src.main.AppConfig') as mock:
        mock.return_value.newsletters = [
            {'name': 'TestNewsletter', 'query': 'label:test', 'folder_id': 'folder123'}
        ]
        yield mock

@pytest.fixture
def mock_clients():
    """Mock external service clients."""
    with patch('src.main.GmailClient') as mock_gmail, \
         patch('src.main.DriveClient') as mock_drive, \
         patch('src.main.DiscordNotifier') as mock_notifier:
        yield mock_gmail.return_value, mock_drive.return_value, mock_notifier.return_value

def test_main_flow_success(mock_config, mock_clients):
    """Test the successful end-to-end main flow with mocks."""
    mock_gmail, mock_drive, mock_notifier = mock_clients
    
    # Configure Gmail mock
    mock_gmail.search_messages.return_value = [{'id': 'msg1'}]
    mock_gmail.get_message_details.return_value = {
        'id': 'msg1',
        'subject': 'Hello',
        'html_content': '<h1>World</h1>',
        'date': datetime(2026, 2, 28)
    }
    
    # Configure Drive mock (file does not exist)
    mock_drive.file_exists.return_value = False
    mock_drive.upload_markdown.return_value = 'file_abc'
    
    # Execute main logic
    result = main()
    
    # Assertions
    assert result == "Success"
    mock_gmail.search_messages.assert_called_once_with('label:test')
    mock_drive.upload_markdown.assert_called_once()
    # Expect filename following the rule: yyyymmdd_Subject.md
    mock_notifier.send_success.assert_called_once_with(['20260228_Hello.md'])

def test_main_flow_duplicate_skip(mock_config, mock_clients):
    """Test that existing files are skipped during processing."""
    mock_gmail, mock_drive, mock_notifier = mock_clients
    
    mock_gmail.search_messages.return_value = [{'id': 'msg1'}]
    mock_gmail.get_message_details.return_value = {
        'id': 'msg1',
        'subject': 'Hello',
        'html_content': '<h1>World</h1>',
        'date': datetime(2026, 2, 28)
    }
    
    # Simulate existing file in Drive
    mock_drive.file_exists.return_value = True
    
    # Execute main logic
    main()
    
    # Verify that upload is skipped and notification is sent with an empty list
    mock_drive.upload_markdown.assert_not_called()
    mock_notifier.send_success.assert_called_with([])
