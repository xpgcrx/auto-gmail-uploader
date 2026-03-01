import re
from markdownify import markdownify as md
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Optional

class EmailConverter:
    """Handles the transformation of email HTML into sanitized Markdown."""

    @staticmethod
    def html_to_markdown(
        html_content: str, 
        subject: Optional[str] = None, 
        date: Optional[datetime] = None,
        footer_starts_with: Optional[str] = None
    ) -> str:
        """
        Convert HTML to Markdown, with layout adjustments and footer removal.
        
        :param html_content: Source HTML string.
        :param subject: Email subject (used for Markdown header).
        :param date: Delivery date (used for Markdown header).
        :param footer_starts_with: Keyword to identify the start of the footer to be removed.
        :return: Converted Markdown string.
        """
        # 1. Pre-process with BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Remove style and script tags which are irrelevant for Markdown
        for style in soup(["style", "script"]):
            style.decompose()

        # 2. Adjust line breaks
        # Explicitly append newlines to structural tags (div, p, br, etc.) 
        # to prevent text from merging into a single line during conversion.
        for tag in soup.find_all(['div', 'p', 'br', 'tr', 'li']):
            tag.append('\n')

        # 3. Convert HTML to Markdown
        # Strip complex layout tags (tables, centers) to prioritize plain text structure.
        markdown_text = md(
            str(soup), 
            heading_style="ATX",
            strip=['table', 'thead', 'tbody', 'tr', 'td', 'center']
        )

        # 4. Text Cleanup
        # Sanitize white spaces and limit consecutive newlines to a maximum of two.
        markdown_text = re.sub(r' +', ' ', markdown_text)
        markdown_text = re.sub(r'\n{3,}', '\n\n', markdown_text).strip()

        # 5. Footer Removal based on specific keywords
        if footer_starts_with:
            lines = markdown_text.split('\n')
            final_lines = []
            footer_removed = False
            for line in lines:
                if footer_starts_with in line:
                    footer_removed = True
                    break
                final_lines.append(line)
            
            markdown_text = '\n'.join(final_lines).strip()
            # Insert a clear message if content was truncated
            if footer_removed:
                markdown_text += "\n\n--- [Footer Truncated] ---"

        # 6. Add Header Information (Subject and Date)
        header = ""
        if subject:
            header += f"# {subject}\n\n"
        if date:
            header += f"Date: {date.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        if header:
            header += "---\n\n"

        return header + markdown_text
