"""
Test the url parsing component
Should check the component that fetches URLs line-by-line from a file.

Author: Oliver Schwarz
Version: 1.0
Contributor: claude.ai
License: MIT
"""
import pytest
import os
from src.url_parser import URLFileParser

# Need to define sample_feed_data fixture or import it
@pytest.fixture
def sample_feed_data():
    """Mock feed data for testing"""
    return {
        'feed': {
            'title': 'Test Feed'
        },
        'entries': [
            {
                'title': 'AI News',
                'description': 'Test Description',
                'published': 'Mon, 22 Nov 2024 12:00:00 GMT',
                'link': 'https://example.com/article1',
            }
        ],
        'status': 200
    }

def test_parse_invalid_urls(tmp_path):
    """Test parsing of invalid URLs"""
    # Create test source file with invalid URLs
    source_file = tmp_path / "invalid_sources.txt"
    source_file.write_text("not_a_url\nhttp://invalid")
    
    # Setup components
    url_parser = URLFileParser(str(source_file), verbose=True)
    
    # Should not include invalid URLs
    urls = url_parser.parse()
    assert len(urls) == 0  # Should pass as the URLs are invalid

def test_url_parser_validation(tmp_path):
    """Test URL validation in parser"""
    source_file = tmp_path / "test_sources.txt"
    source_file.write_text("""
not_a_url
http://missing-slashes
https://valid.com/feed
http://another-valid.com/rss
ftp://wrong-protocol.com
    """.strip())
    
    parser = URLFileParser(str(source_file), verbose=True)
    urls = parser.parse()
    
    # Should only include the two valid URLs
    assert len(urls) == 2
    assert "https://valid.com/feed" in urls
    assert "http://another-valid.com/rss" in urls

def test_parse_empty_file(tmp_path):
    """Test parsing an empty file"""
    source_file = tmp_path / "empty.txt"
    source_file.write_text("")
    
    parser = URLFileParser(str(source_file), verbose=True)
    urls = parser.parse()
    assert len(urls) == 0

def test_parse_commented_urls(tmp_path):
    """Test that commented lines are ignored"""
    source_file = tmp_path / "commented.txt"
    source_file.write_text("""
# This is a comment
https://valid.com/feed
# Another comment
http://another-valid.com/rss
    """.strip())
    
    parser = URLFileParser(str(source_file), verbose=True)
    urls = parser.parse()
    assert len(urls) == 2