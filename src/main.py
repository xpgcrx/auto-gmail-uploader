import logging
import traceback
import re
from datetime import datetime
from typing import Any

from src.config import AppConfig
from src.gmail_client import GmailClient
from src.drive_client import DriveClient
from src.converter import EmailConverter
from src.notifier import DiscordNotifier
from dotenv import load_dotenv

# Logger configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables (from .env if it exists)
load_dotenv()

def main(event: Any = None, context: Any = None) -> str:
    """
    Main entry point for the application.
    Compatible with Cloud Functions and local execution.
    
    :param event: Cloud Functions trigger event (unused)
    :param context: Cloud Functions execution context (unused)
    :return: Execution status string
    """
    processed_files = []
    notifier = None

    try:
        # 1. Load configuration (configs/newsletters.yaml)
        config = AppConfig()
        
        # 2. Initialize clients
        # Credentials are automatically loaded from Secret Manager (Prod) or .env (Local)
        gmail_client = GmailClient()
        drive_client = DriveClient()
        notifier = DiscordNotifier()

        # 3. Process each newsletter target
        for newsletter in config.newsletters:
            logger.info(f"Processing newsletter: {newsletter['name']} (Query: {newsletter['query']})")
            
            # Search for matching emails in Gmail
            messages = gmail_client.search_messages(newsletter['query'])
            logger.info(f"Found {len(messages)} candidate messages.")

            # Process only the latest 1 message to prevent duplicates and keep it lightweight
            for msg_meta in messages[:1]:
                msg_id = msg_meta['id']
                
                # Fetch email details (Subject, HTML body, Date)
                details = gmail_client.get_message_details(msg_id)
                
                # Generate filename (e.g., 20260301_Subject.md)
                date_str = details['date'].strftime('%Y%m%d')
                
                # Sanitize filename by removing invalid characters
                clean_subject = re.sub(r'[\\/:*?"<>|]', '', details['subject']).strip()
                filename = f"{date_str}_{clean_subject}.md"
                
                # Check for existing file in Google Drive to ensure idempotency
                if drive_client.file_exists(filename, newsletter['folder_id']):
                    logger.info(f"Skip: {filename} already exists in Drive.")
                    continue
                
                # Convert HTML body to Markdown format
                # Handles line break adjustments and footer truncation
                markdown_content = EmailConverter.html_to_markdown(
                    details['html_content'],
                    subject=details['subject'],
                    date=details['date'],
                    footer_starts_with=newsletter.get('footer_starts_with')
                )
                
                # Upload to designated folder in Google Drive
                file_id = drive_client.upload_markdown(
                    filename,
                    markdown_content,
                    newsletter['folder_id']
                )
                
                logger.info(f"Uploaded: {filename} (ID: {file_id})")
                processed_files.append(filename)

        # 4. Notify results via Discord (on success)
        notifier.send_success(processed_files)
        return "Success"

    except Exception as e:
        # Error handling: Log traceback and notify via Discord
        error_msg = str(e)
        detail = traceback.format_exc()
        logger.error(f"Error during execution: {error_msg}\n{detail}")
        
        if notifier:
            try:
                notifier.send_error(error_msg, detail)
            except Exception as notify_err:
                logger.error(f"Failed to send error notification to Discord: {notify_err}")
        
        # Rethrow exception for Cloud Functions retry/monitoring
        raise e

if __name__ == "__main__":
    # Local execution for testing
    main()
