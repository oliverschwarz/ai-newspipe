"""
Testing the feed reader implementation

Author: Oliver Schwarz
Version: 1.0
Contributor: claude.ai
License: MIT
"""
import pytest
from unittest.mock import patch, MagicMock
import logging
from src.feed_reader import FeedReader, InvalidURLError

@pytest.fixture
def mock_feed_data():
    """Fixture providing mock RSS feed data"""
    return {
        'feed': {
            'title': 'Test Feed'
        },
        'entries': [
            {
                'title': 'Test Article',
                'description': 'Test Description',
                'published': 'Mon, 22 Nov 2024 12:00:00 GMT',
                'link': 'https://example.com/article1',
            }
        ]
    }

def test_fetch_feeds(mock_feed_data):
    """Test fetching feeds includes feed title"""
    urls = ["https://example.com/feed"]
    reader = FeedReader(urls)
    
    with patch('feedparser.parse') as mock_parse:
        mock_parse.return_value = mock_feed_data
        entries = reader.fetch_feeds()
        
        assert len(entries) == 1
        assert entries[0]['feed_title'] == 'Test Feed'
        assert set(entries[0].keys()) == {
            'title', 'description', 'published', 'link', 'feed_url', 'feed_title'
        }

def test_fetch_feeds_missing_attributes(caplog):
    """Test handling of feeds with missing attributes"""
    urls = ["https://example.com/feed"]
    reader = FeedReader(urls, verbose=True)
    
    minimal_feed = {
        'feed': {},
        'entries': [
            {
                'title': 'Test Article'
                # Missing other attributes
            }
        ]
    }
    
    with patch('feedparser.parse') as mock_parse:
        mock_parse.return_value = minimal_feed
        entries = reader.fetch_feeds()
        
        assert len(entries) == 1
        assert entries[0]['title'] == 'Test Article'
        assert entries[0]['description'] == ''
        assert entries[0]['feed_title'] == 'Unknown Feed'

def test_fetch_feeds_malformed_response(caplog):
    """Test handling of malformed feed responses"""
    urls = ["https://example.com/feed"]
    reader = FeedReader(urls, verbose=True)
    
    malformed_feed = {}  # Completely empty response
    
    with patch('feedparser.parse') as mock_parse:
        mock_parse.return_value = malformed_feed
        entries = reader.fetch_feeds()
        
        assert entries == []  # Should return empty list for malformed feed
        assert "Found 0 entries" in caplog.text

def test_fetch_feeds_none_response(caplog):
    """Test handling of None response"""
    urls = ["https://example.com/feed"]
    reader = FeedReader(urls, verbose=True)
    
    with patch('feedparser.parse') as mock_parse:
        mock_parse.return_value = None
        entries = reader.fetch_feeds()
        
        assert entries == []  # Should return empty list for None response