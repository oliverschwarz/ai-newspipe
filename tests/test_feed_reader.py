"""
Testing the feed reader implementation

Author: Oliver Schwarz
Version: 1.0
Contributor: claude.ai
License: MIT
"""
import pytest
from src.feed_reader import FeedReader, InvalidURLError

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

def test_feed_reader_invalid_url_format():
    """Test that invalid URL formats raise an error"""
    invalid_urls = [
        "not_a_url",
        "http:/missing-slashes",
        "ftp://wrong-protocol.com",
        "",
        None
    ]
    
    for url in invalid_urls:
        with pytest.raises(InvalidURLError):
            FeedReader([url])

def test_feed_reader_valid_url_formats():
    """Test that valid URL formats are accepted"""
    valid_urls = [
        "https://example.com/feed",
        "http://example.com/rss",
        "https://example.com/feed.xml",
        "http://example.com/rss?format=xml"
    ]
    
    reader = FeedReader(valid_urls)
    assert reader.feed_urls == valid_urls