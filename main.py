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
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
from src.url_parser import URLFileParser
from src.feed_reader import FeedReader
from src.ai_analyzer import AIAnalyzer

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

def save_to_markdown(content: str, output_dir: str) -> str:
    """Save content to a markdown file with timestamp"""
    # Create timestamp for filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(output_dir, f'ai_news_summary_{timestamp}.md')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write(content)
    
    return output_file

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    logger = setup_logging()
    
    # Configuration
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sources_file = os.path.join(current_dir, 'news_sources.txt')
    output_dir = os.path.join(current_dir, 'summaries')
    
    try:
        logger.info("Starting AI Newspipe")
        
        # Verify OpenAI API key is available
        if not os.getenv('OPENAI_API_KEY'):
            logger.error("OpenAI API key not found in .env file")
            raise ValueError("Please add OPENAI_API_KEY to your .env file")
        
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
            logger.warning("No entries from today found!")
            return
        
        # Show entry count and size estimate
        entries_json = json.dumps(entries)
        json_size_kb = len(entries_json)/1024
        json_size_tokens = len(entries_json)/4  # Rough estimate of tokens (4 chars per token)
        
        logger.info(f"Prepared payload summary:")
        logger.info(f"Number of entries: {len(entries)}")
        logger.info(f"Payload size: {json_size_kb:.1f}KB")
        logger.info(f"Estimated tokens: {json_size_tokens:.0f}")
        
        if json_size_tokens > 6000:  # Conservative limit for GPT-4
            logger.warning("Payload might still be too large for API!")
            logger.warning("Consider further reducing entry count or description length")
        
        # Analyze and process feeds
        logger.info("Analyzing feeds with AI...")
        analyzer = AIAnalyzer(verbose=True)
        markdown_content = analyzer.process_feeds(entries)
        
        # Save to markdown
        logger.info("Saving processed content...")
        output_file = save_to_markdown(markdown_content, output_dir)
        logger.info(f"Saved to: {output_file}")
        
        logger.info("Process completed successfully!")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()