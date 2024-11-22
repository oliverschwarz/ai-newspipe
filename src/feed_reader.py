"""
Feed reader class

Supposed to fetch content from multiple rss feeds and
return their structured content.

Author: Oliver Schwarz
Version: 1.0
Contributor: claude.ai
License: MIT
"""
class FeedReader:
    def __init__(self, feed_urls):
        self.feed_urls = feed_urls