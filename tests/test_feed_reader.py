"""
Testing the feed reader implementation

Author: Oliver Schwarz
Version: 1.0
Contributor: claude.ai
License: MIT
"""
import pytest
from src.feed_reader import FeedReader

def test_feed_reader_initialization():
    """Test that FeedReader can be initialized with a list of URLs"""
    urls = ["https://example.com/feed"]
    reader = FeedReader(urls)
    assert reader.feed_urls == urls
    assert isinstance(reader.feed_urls, list)

def test_feed_reader_empty_urls():
    """Test that FeedReader can be initialized with empty URL list"""
    reader = FeedReader([])
    assert reader.feed_urls == []

# TODO: Come back with exception or log if a source can not be fetched (typically 403)

# src/feed_reader.py
class FeedReader:
    """
    Component for reading RSS feeds.
    """
    def __init__(self, feed_urls):
        """
        Initialize FeedReader with a list of RSS feed URLs.
        
        Args:
            feed_urls (list): List of URLs to RSS feeds
        """
        self.feed_urls = feed_urls