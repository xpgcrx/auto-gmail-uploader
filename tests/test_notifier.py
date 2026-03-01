import pytest
import json
from unittest.mock import MagicMock, patch
from src.notifier import DiscordNotifier

@pytest.fixture
def notifier():
    return DiscordNotifier(webhook_url="https://fake-webhook.com")

def test_send_success(notifier):
    """Test successful notification delivery."""
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        
        notifier.send_success(["test1.md", "test2.md"])
        
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        payload = json.loads(kwargs['data'])
        assert "✅ Gmail Uploader" in payload['content']
        assert "Uploaded 2 emails" in payload['content']
        assert "test1.md" in payload['content']

def test_send_error(notifier):
    """Test error notification delivery."""
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        
        notifier.send_error("Auth failed", "Invalid token")
        
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        payload = json.loads(kwargs['data'])
        assert "❌ **Gmail Uploader" in payload['content']
        assert "Auth failed" in payload['content']
        assert "Invalid token" in payload['content']
