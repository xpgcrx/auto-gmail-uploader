from src.converter import EmailConverter
from datetime import datetime

def test_html_to_markdown_basic():
    """Test basic HTML to Markdown conversion."""
    html = "<h1>Heading</h1><p>Text <b>Bold</b> and <a href='https://example.com'>Link</a>.</p>"
    expected_md = "# Heading\n\nText **Bold** and [Link](https://example.com)."
    result = EmailConverter.html_to_markdown(html)
    assert expected_md in result

def test_html_to_markdown_with_header():
    """Test if subject and date are included in the header."""
    html = "<p>Content</p>"
    subject = "Test Subject"
    now = datetime.now()
    result = EmailConverter.html_to_markdown(html, subject=subject, date=now)
    
    assert f"# {subject}" in result
    assert f"Date: {now.strftime('%Y-%m-%d %H:%M:%S')}" in result
    assert "---" in result
    assert "Content" in result

def test_html_to_markdown_script_removal():
    """Test that unnecessary script tags are removed."""
    html = "<p>Visible</p><script>alert('hidden');</script>"
    result = EmailConverter.html_to_markdown(html)
    assert "Visible" in result
    assert "alert" not in result
