"""
Main python

Prepares logging, fetches rss urls, fetch content.

Author: Oliver Schwarz
Version: 1.0
Contributor: claude.ai
License: MIT
"""
# main.py
import os
import logging
from datetime import datetime
from src.url_parser import URLFileParser
from src.feed_reader import FeedReader

def setup_logging():
    """Setup logging configuration"""
    logger = logging.getLogger('ai_newspipe')
    logger.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger

def save_entries_to_markdown(entries, output_dir):
    """Save feed entries to a markdown file with timestamp"""
    # Create timestamp for filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(output_dir, f'ai_news_summary_{timestamp}.md')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    with open(output_file, 'w') as f:
        # Write header
        f.write(f"# AI News Summary\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Group entries by feed
        feeds = {}
        for entry in entries:
            feed_title = entry['feed_title']
            if feed_title not in feeds:
                feeds[feed_title] = []
            feeds[feed_title].append(entry)
        
        # Write entries grouped by feed
        for feed_title, feed_entries in feeds.items():
            f.write(f"## {feed_title}\n\n")
            
            for entry in feed_entries:
                f.write(f"### [{entry['title']}]({entry['link']})\n\n")
                f.write(f"*Published: {entry['published']}*\n\n")
                f.write(f"{entry['description']}\n\n")
                f.write("---\n\n")
    
    return output_file

def main():
    logger = setup_logging()
    
    # Configuration
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sources_file = os.path.join(current_dir, 'news_sources.txt')
    output_dir = os.path.join(current_dir, 'summaries')
    
    try:
        logger.info("Starting AI Newspipe")
        
        # Parse URLs
        logger.info(f"Reading URLs from {sources_file}")
        url_parser = URLFileParser(sources_file, verbose=True)
        urls = url_parser.parse()
        
        if not urls:
            logger.warning("No valid URLs found!")
            return
        
        # Fetch feeds
        logger.info("Fetching feeds...")
        feed_reader = FeedReader(urls, verbose=True)
        entries = feed_reader.fetch_feeds()
        
        if not entries:
            logger.warning("No entries found!")
            return
        
        # Save to markdown
        logger.info(f"Saving {len(entries)} entries...")
        output_file = save_entries_to_markdown(entries, output_dir)
        logger.info(f"Saved to: {output_file}")
        
        logger.info("Process completed successfully!")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()