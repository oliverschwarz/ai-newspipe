"""
Testing the full integration of the application

Author: Oliver Schwarz
Version: 1.0
Contributor: claude.ai
License: MIT
"""
# tests/test_integration.py
import pytest
from unittest.mock import patch, MagicMock
import json
from src.url_parser import URLFileParser
from src.feed_reader import FeedReader
from src.ai_analyzer import AIAnalyzer
import time

@pytest.fixture
def mock_feed_data():
    """Create mock feed data with today's entry"""
    today = time.localtime()
    return {
        'feed': {
            'title': 'Test Feed'
        },
        'entries': [
            {
                'title': 'Today AI News',
                'description': 'Test description',
                'published': 'Today',
                'published_parsed': today,
                'link': 'http://example.com/today'
            }
        ]
    }

@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response"""
    class MockMessage:
        def __init__(self, content):
            self.content = content
    
    class MockChoice:
        def __init__(self, message):
            self.message = message
    
    class MockResponse:
        def __init__(self, content):
            self.choices = [MockChoice(MockMessage(content))]
    
    return MockResponse("# AI News Summary\n\nTest summary")

def test_full_pipeline(tmp_path, mock_feed_data, mock_openai_response):
    """Test the complete pipeline with all components"""
    # Setup test files
    source_file = tmp_path / "news_sources.txt"
    source_file.write_text("https://example.com/feed")
    
    # Mock OpenAI
    with patch('openai.OpenAI') as mock_openai:
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_openai_response
        mock_openai.return_value = mock_client
        
        # Mock feedparser
        with patch('feedparser.parse') as mock_parse:
            mock_parse.return_value = mock_feed_data
            
            # Setup components
            url_parser = URLFileParser(str(source_file), verbose=True)
            urls = url_parser.parse()
            
            feed_reader = FeedReader(urls, verbose=True)
            entries = feed_reader.fetch_feeds()
            
            # Verify feed processing
            assert len(entries) == 1
            assert entries[0]['title'] == 'Today AI News'
            assert len(entries[0]['description']) <= 200
            
            # Test API processing
            analyzer = AIAnalyzer(verbose=True)
            result = analyzer.process_feeds(entries)
            
            # Verify final output
            assert result.startswith("# AI News Summary")
            
            # Verify payload size
            entries_json = json.dumps(entries)
            assert len(entries_json)/1024 < 100  # Should be well under 100KB

def test_pipeline_with_no_today_entries(tmp_path, mock_openai_response):
    """Test pipeline behavior when no today's entries are found"""
    source_file = tmp_path / "news_sources.txt"
    source_file.write_text("https://example.com/feed")
    
    old_feed_data = {
        'feed': {'title': 'Test Feed'},
        'entries': [{
            'title': 'Old News',
            'description': 'Old description',
            'published': 'Old',
            'published_parsed': time.struct_time((2023, 1, 1, 12, 0, 0, 0, 1, -1)),
            'link': 'http://example.com/old'
        }]
    }
    
    with patch('feedparser.parse') as mock_parse:
        mock_parse.return_value = old_feed_data
        
        url_parser = URLFileParser(str(source_file), verbose=True)
        urls = url_parser.parse()
        
        feed_reader = FeedReader(urls, verbose=True)
        entries = feed_reader.fetch_feeds()
        
        assert len(entries) == 0