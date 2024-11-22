"""
Testing the feed reader implementation

Author: Oliver Schwarz
Version: 1.0
Contributor: claude.ai
License: MIT
"""
# tests/test_feed_reader.py
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.feed_reader import FeedReader
import time

@pytest.fixture
def mock_feed_data():
    """Fixture providing mock RSS feed data"""
    feed_info = MagicMock()
    feed_info.title = 'Test Feed'
    
    mock_data = MagicMock()
    mock_data.feed = feed_info
    mock_data.entries = [
        {
            'title': 'Test Article',
            'description': 'Test Description',
            'published': 'Mon, 22 Nov 2024 12:00:00 GMT',
            'link': 'https://example.com/article1',
        }
    ]
    return mock_data

@pytest.fixture
def mock_today_feed_data():
    """Fixture providing mock RSS feed data with today's date"""
    today = time.localtime()
    
    feed_info = MagicMock()
    feed_info.title = 'Test Feed'
    
    mock_data = MagicMock()
    mock_data.feed = feed_info
    mock_data.entries = [
        {
            'title': 'Today Article',
            'description': 'This is a test description that is definitely longer than 200 characters so we can verify that the truncation is working properly. We need to make sure it has more than 200 characters so lets add some more text here to make it longer and longer until we are sure it will be truncated properly.',
            'published': 'Today',
            'published_parsed': today,
            'link': 'https://example.com/today'
        }
    ]
    return mock_data

@pytest.fixture
def mock_mixed_dates_feed():
    """Fixture providing feed with both today's and old entries"""
    today = time.localtime()
    old_date = time.struct_time((2023, 1, 1, 12, 0, 0, 0, 1, -1))
    
    feed_info = MagicMock()
    feed_info.title = 'Test Feed'
    
    mock_data = MagicMock()
    mock_data.feed = feed_info
    mock_data.entries = [
        {
            'title': 'Today Article',
            'description': 'Today description',
            'published': 'Today',
            'published_parsed': today,
            'link': 'https://example.com/today'
        },
        {
            'title': 'Old Article',
            'description': 'Old description',
            'published': 'Old',
            'published_parsed': old_date,
            'link': 'https://example.com/old'
        }
    ]
    return mock_data

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
            'title', 'description', 'published', 'link', 'feed_title'
        }

def test_fetch_feeds_missing_attributes(caplog):
    """Test handling of feeds with missing attributes"""
    urls = ["https://example.com/feed"]
    reader = FeedReader(urls, verbose=True)
    
    feed_info = MagicMock()
    feed_info.title = 'Unknown Feed'
    
    minimal_feed = MagicMock()
    minimal_feed.feed = feed_info
    minimal_feed.entries = [
        {
            'title': 'Test Article'
            # Missing other attributes
        }
    ]
    
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
    
    feed_info = MagicMock()
    feed_info.title = 'Empty Feed'
    
    malformed_feed = MagicMock()
    malformed_feed.feed = feed_info
    malformed_feed.entries = []
    
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

def test_date_filtering(mock_mixed_dates_feed):
    """Test that only today's entries are included"""
    urls = ["https://example.com/feed"]
    
    with patch('feedparser.parse') as mock_parse:
        mock_parse.return_value = mock_mixed_dates_feed
        reader = FeedReader(urls, verbose=True)
        entries = reader.fetch_feeds()
        
        assert len(entries) == 1
        assert entries[0]['title'] == 'Today Article'

def test_description_truncation(mock_today_feed_data):
    """Test that descriptions are truncated to 200 characters"""
    urls = ["https://example.com/feed"]
    
    with patch('feedparser.parse') as mock_parse:
        mock_parse.return_value = mock_today_feed_data
        reader = FeedReader(urls, verbose=True)
        entries = reader.fetch_feeds()
        
        assert len(entries) == 1
        assert len(entries[0]['description']) == 200

def test_feed_processing_logs(mock_mixed_dates_feed, caplog):
    """Test logging of feed processing statistics"""
    urls = ["https://example.com/feed"]
    
    with patch('feedparser.parse') as mock_parse:
        mock_parse.return_value = mock_mixed_dates_feed
        reader = FeedReader(urls, verbose=True)
        entries = reader.fetch_feeds()
        
        log_text = caplog.text
        assert "Total entries across all feeds: 2" in log_text
        assert "Entries from today: 1" in log_text
        assert "Filtered out 1 older entries" in log_text