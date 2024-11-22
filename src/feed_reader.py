"""
Feed reader class

Supposed to fetch content from multiple rss feeds and
return their structured content.

Author: Oliver Schwarz
Version: 1.0
Contributor: claude.ai
License: MIT
"""
from urllib.parse import urlparse
from typing import List

class InvalidURLError(Exception):
    """Raised when an invalid URL is provided"""
    pass

class FeedReader:
    """Component for reading RSS feeds."""
    
    def __init__(self, feed_urls: List[str]):
        """
        Initialize FeedReader with a list of RSS feed URLs.
        
        Args:
            feed_urls (List[str]): List of URLs to RSS feeds
            
        Raises:
            InvalidURLError: If any URL in the list is invalid
        """
        self.feed_urls = []
        for url in feed_urls:
            if self._is_valid_url(url):
                self.feed_urls.append(url)
    
    def _is_valid_url(self, url: str) -> bool:
        """
        Validate if the given URL is properly formatted.
        
        Args:
            url (str): URL to validate
            
        Returns:
            bool: True if valid, raises InvalidURLError if invalid
            
        Raises:
            InvalidURLError: If URL is invalid
        """
        if not url or not isinstance(url, str):
            raise InvalidURLError("URL must be a non-empty string")
            
        try:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                raise InvalidURLError(f"Invalid URL format: {url}")
            if result.scheme not in ['http', 'https']:
                raise InvalidURLError(f"URL must use HTTP(S) protocol: {url}")
            return True
        except Exception as e:
            raise InvalidURLError(f"Invalid URL: {url}. Error: {str(e)}")