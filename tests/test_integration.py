"""
Testing the full integration of the application

Author: Oliver Schwarz
Version: 1.0
Contributor: claude.ai
License: MIT
"""
# tests/test_integration.py
import pytest
from unittest.mock import patch
from src.url_parser import URLFileParser
from src.feed_reader import FeedReader

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

def test_full_pipeline(tmp_path, sample_feed_data):
    """Test the complete pipeline from file parsing to feed fetching"""
    # Create test source file
    source_file = tmp_path / "news_sources.txt"
    source_file.write_text("https://example.com/feed1\nhttps://example.com/feed2")
    
    # Setup components
    url_parser = URLFileParser(str(source_file), verbose=True)
    urls = url_parser.parse()
    
    # Mock feedparser.parse to return the same sample data for each URL
    with patch('feedparser.parse') as mock_parse:
        mock_parse.return_value = sample_feed_data
        reader = FeedReader(urls, verbose=True)
        entries = reader.fetch_feeds()
        
        # Verify results
        assert len(entries) == 2  # Two entries (one per feed)
        for entry in entries:
            assert entry['feed_title'] == 'Test Feed'
            assert entry['title'] == 'AI News'
            assert entry['description'] == 'Test Description'
            assert entry['published'] == 'Mon, 22 Nov 2024 12:00:00 GMT'
            assert entry['link'] == 'https://example.com/article1'
            assert entry['feed_url'] in ['https://example.com/feed1', 'https://example.com/feed2']

def test_full_pipeline_with_empty_file(tmp_path, sample_feed_data):
    """Test pipeline with empty source file"""
    # Create empty test source file
    source_file = tmp_path / "empty_sources.txt"
    source_file.write_text("")
    
    # Setup components
    url_parser = URLFileParser(str(source_file), verbose=True)
    urls = url_parser.parse()
    reader = FeedReader(urls, verbose=True)
    entries = reader.fetch_feeds()
    
    # Verify results
    assert len(entries) == 0  # Should have no entries

def test_full_pipeline_with_invalid_urls(tmp_path, sample_feed_data):
    """Test pipeline with invalid URLs in source file"""
    # Create test source file with invalid URLs
    source_file = tmp_path / "invalid_sources.txt"
    source_file.write_text("not_a_url\nhttp://invalid")
    
    # Setup components
    url_parser = URLFileParser(str(source_file), verbose=True)
    
    # Should not raise an error, but should have no valid URLs
    urls = url_parser.parse()
    assert len(urls) == 0  # Will fail if URL validation isn't strict enough