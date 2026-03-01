import os
import requests
import json
from typing import Optional

class DiscordNotifier:
    """Handles sending notifications via Discord Webhook."""

    def __init__(self, webhook_url: Optional[str] = None) -> None:
        """
        Initialize the notification client.
        :param webhook_url: Discord Webhook URL. Loaded from environment variable if not provided.
        """
        if webhook_url is None:
            webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
        
        if not webhook_url:
            raise ValueError("Environment variable DISCORD_WEBHOOK_URL is not set.")
        
        self.webhook_url = webhook_url

    def send_success(self, processed_items: list[str]) -> None:
        """
        Send a notification for successful execution.
        :param processed_items: List of filenames successfully processed.
        """
        count = len(processed_items)
        if count == 0:
            content = "✅ Gmail Uploader: No new emails to process."
        else:
            items_str = "\n".join([f"- {item}" for item in processed_items])
            content = f"✅ Gmail Uploader: Uploaded {count} emails.\n\n**Processed Files:**\n{items_str}"

        self._post_message(content)

    def send_error(self, error_msg: str, detail: Optional[str] = None) -> None:
        """
        Send a detailed notification for execution errors.
        :param error_msg: Summary of the error.
        :param detail: Detailed information such as stack traces.
        """
        content = f"❌ **Gmail Uploader: Execution Error**\n\n**Summary:** {error_msg}"
        if detail:
            # Truncate details to fit within Discord's 2000 character limit per message
            content += f"\n\n**Details:**\n```\n{detail[:1500]}\n```"

        self._post_message(content)

    def _post_message(self, content: str) -> None:
        """Internal method to send HTTP POST request to Discord."""
        payload = {"content": content}
        response = requests.post(
            self.webhook_url,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
