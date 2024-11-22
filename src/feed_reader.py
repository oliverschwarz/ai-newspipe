"""
Feed reader class

Supposed to fetch content from multiple rss feeds and
return their structured content.

Author: Oliver Schwarz
Version: 1.0
Contributor: claude.ai
License: MIT
"""
# src/feed_reader.py
import feedparser
import logging
from typing import List, Dict
from datetime import datetime

class FeedReader:
    """Component for reading RSS feeds."""
    
    def __init__(self, feed_urls: List[str], verbose: bool = False):
        """
        Initialize FeedReader.
        
        Args:
            feed_urls (List[str]): List of URLs to RSS feeds
            verbose (bool): Enable verbose logging
        """
        self.verbose = verbose
        self.logger = logging.getLogger(__name__)
        
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

    def _validate_urls(self, urls: List[str]):
        """Validate and store URLs."""
        if self.verbose:
            self.logger.info(f"Validating {len(urls)} URLs")
        
        self.feed_urls = urls

    def _is_from_today(self, entry) -> bool:
        """Check if entry is from today using feedparser's parsed date."""
        if not hasattr(entry, 'published_parsed') or not entry.published_parsed:
            return False
        
        try:
            entry_date = datetime(*entry.published_parsed[:3])  # Year, month, day
            today = datetime.now().date()
            return entry_date.date() == today
        except (TypeError, ValueError) as e:
            if self.verbose:
                self.logger.debug(f"Date parsing error: {str(e)}")
            return False

    def fetch_feeds(self) -> List[Dict]:
        """
        Fetch and parse RSS feeds, filtering for today's entries only.
        
        Returns:
            List[Dict]: List of feed entries with standardized structure
        """
        all_entries = []
        total_entries = 0
        today_entries = 0
        
        if self.verbose:
            self.logger.info(f"Starting to fetch {len(self.feed_urls)} feeds")
        
        for url in self.feed_urls:
            try:
                if self.verbose:
                    self.logger.info(f"Fetching feed: {url}")
                
                feed = feedparser.parse(url)
                feed_title = feed.feed.get('title', 'Unknown Feed')
                
                feed_total = len(feed.entries)
                total_entries += feed_total
                feed_today = 0
                
                if self.verbose:
                    self.logger.info(f"Found {feed_total} total entries in {feed_title}")
                
                for entry in feed.entries:
                    # Filter for today's entries
                    if not self._is_from_today(entry):
                        continue
                    
                    feed_today += 1
                    today_entries += 1
                    
                    structured_entry = {
                        'title': entry.get('title', ''),
                        'description': entry.get('description', '')[:200],  # Truncate to 200 chars
                        'published': entry.get('published', ''),
                        'link': entry.get('link', ''),
                        'feed_title': feed_title
                    }
                    all_entries.append(structured_entry)
                    
                    if self.verbose:
                        self.logger.debug(f"Added entry: {structured_entry['title']}")
                
                if self.verbose:
                    if feed_today == 0:
                        self.logger.warning(f"No entries from today found in {feed_title}")
                    else:
                        self.logger.info(f"Found {feed_today} entries from today in {feed_title}")
                    
            except Exception as e:
                if self.verbose:
                    self.logger.error(f"Error fetching feed {url}: {str(e)}")
                continue
        
        if self.verbose:
            self.logger.info(f"Feed processing summary:")
            self.logger.info(f"Total entries across all feeds: {total_entries}")
            self.logger.info(f"Entries from today: {today_entries}")
            self.logger.info(f"Filtered out {total_entries - today_entries} older entries")
                
        return all_entries