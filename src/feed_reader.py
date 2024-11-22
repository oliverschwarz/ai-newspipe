"""
Feed reader class

Supposed to fetch content from multiple rss feeds and
return their structured content.

Author: Oliver Schwarz
Version: 1.0
Contributor: claude.ai
License: MIT
"""
import feedparser
import logging
from typing import List, Dict
from urllib.parse import urlparse

class InvalidURLError(Exception):
    """Raised when an invalid URL is provided"""
    pass

class FeedReader:
    """Component for reading RSS feeds."""
    
    def __init__(self, feed_urls: List[str], verbose: bool = False):
        """
        Initialize FeedReader with a list of RSS feed URLs.
        
        Args:
            feed_urls (List[str]): List of URLs to RSS feeds
            verbose (bool): Enable verbose logging
        """
        # Set up logging
        self.logger = logging.getLogger(__name__)
        self.verbose = verbose
        
        if verbose:
            console_handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            self.logger.setLevel(logging.INFO)
        
        self.feed_urls = []
        self._validate_urls(feed_urls)
    
    def _validate_urls(self, urls: List[str]) -> None:
        """Validate and store URLs."""
        if self.verbose:
            self.logger.info(f"Validating {len(urls)} URLs")
            
        for url in urls:
            if self._is_valid_url(url):
                self.feed_urls.append(url)
                if self.verbose:
                    self.logger.info(f"Valid URL added: {url}")
    
    def _is_valid_url(self, url: str) -> bool:
        """
        Validate URL format.
        
        Args:
            url (str): URL to validate
            
        Returns:
            bool: True if valid
            
        Raises:
            InvalidURLError: If URL is invalid
        """
        if not url or not isinstance(url, str):
            error_msg = "URL must be a non-empty string"
            if self.verbose:
                self.logger.error(error_msg)
            raise InvalidURLError(error_msg)
            
        try:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                raise InvalidURLError(f"Invalid URL format: {url}")
            if result.scheme not in ['http', 'https']:
                raise InvalidURLError(f"URL must use HTTP(S) protocol: {url}")
            return True
        except Exception as e:
            if self.verbose:
                self.logger.error(f"URL validation error: {str(e)}")
            raise InvalidURLError(f"Invalid URL: {url}. Error: {str(e)}")

    def fetch_feeds(self) -> List[Dict]:
        """
        Fetch and parse all RSS feeds.
        
        Returns:
            List[Dict]: List of feed entries with standardized structure
        """
        all_entries = []
        
        if self.verbose:
            self.logger.info(f"Starting to fetch {len(self.feed_urls)} feeds")
        
        for url in self.feed_urls:
            try:
                if self.verbose:
                    self.logger.info(f"Fetching feed: {url}")
                
                feed = feedparser.parse(url)
                
                # Defensive feed title extraction
                feed_title = 'Unknown Feed'
                if isinstance(feed, dict):
                    if 'feed' in feed and isinstance(feed['feed'], dict):
                        feed_title = feed['feed'].get('title', 'Unknown Feed')
                
                # Defensive entries extraction
                entries = []
                if isinstance(feed, dict):
                    entries = feed.get('entries', [])
                    if not isinstance(entries, list):
                        entries = []
                
                if self.verbose:
                    self.logger.info(f"Successfully fetched feed: {feed_title} ({url})")
                    self.logger.info(f"Found {len(entries)} entries")
                
                for entry in entries:
                    if not isinstance(entry, dict):
                        continue
                        
                    structured_entry = {
                        'title': entry.get('title', ''),
                        'description': entry.get('description', ''),
                        'published': entry.get('published', ''),
                        'link': entry.get('link', ''),
                        'feed_url': url,
                        'feed_title': feed_title
                    }
                    all_entries.append(structured_entry)
                    
                    if self.verbose:
                        self.logger.debug(f"Processed entry: {structured_entry['title']}")
                    
            except Exception as e:
                if self.verbose:
                    self.logger.error(f"Error fetching feed {url}: {str(e)}")
                continue
        
        if self.verbose:
            self.logger.info(f"Completed fetching all feeds. Total entries: {len(all_entries)}")
                
        return all_entries