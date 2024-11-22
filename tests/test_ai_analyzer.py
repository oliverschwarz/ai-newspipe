"""
Testing AI Analyzer

Sending the code to the OpenAI GPT API using MagicMock

Author: Oliver Schwarz
Version: 1.0
Contributor: claude.ai
License: MIT
"""
# tests/test_ai_analyzer.py
import pytest
from unittest.mock import patch, MagicMock
from src.ai_analyzer import AIAnalyzer
import json
import os

@pytest.fixture
def sample_entries():
    """Sample entries for testing"""
    return [
        {
            'title': 'AI News',
            'description': 'Test description',
            'published': '2024-11-22',
            'link': 'http://example.com',
            'feed_title': 'Test Feed'
        }
    ]

@pytest.fixture
def mock_openai_response():
    """Create a mock OpenAI API response"""
    class MockChoice:
        def __init__(self):
            self.message = MagicMock()
            self.message.content = "# AI News Summary\n\nTest summary"

    class MockResponse:
        def __init__(self):
            self.choices = [MockChoice()]

    return MockResponse()

def test_ai_analyzer_initialization():
    """Test AIAnalyzer initialization with environment variables"""
    with patch.dict(os.environ, {'OPENAI_API_KEY': 'dummy-key'}):
        analyzer = AIAnalyzer(verbose=True)
        assert analyzer.api_key == 'dummy-key'

def test_create_analysis_prompt(sample_entries):
    """Test the creation of the analysis prompt"""
    with patch.dict(os.environ, {'OPENAI_API_KEY': 'dummy-key'}):
        analyzer = AIAnalyzer()
        prompt = analyzer._create_analysis_prompt(sample_entries)
        
        # Verify prompt content
        assert 'AI News' in prompt
        assert 'Test Feed' in prompt
        assert 'markdown format' in prompt.lower()
        
        # Verify JSON structure in prompt
        assert json.dumps(sample_entries) in prompt

@patch('openai.OpenAI')
def test_analyze_feeds(mock_openai_class, sample_entries, mock_openai_response):
    """Test the feed analysis process"""
    # Setup mock OpenAI client
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_openai_response
    mock_openai_class.return_value = mock_client

    with patch.dict(os.environ, {'OPENAI_API_KEY': 'dummy-key'}):
        analyzer = AIAnalyzer(verbose=True)
        result = analyzer.analyze_feeds(sample_entries)
        
        # Verify API call
        mock_client.chat.completions.create.assert_called_once()
        
        # Verify result
        assert result.startswith("# AI News Summary")
        assert "Test summary" in result

@patch('openai.OpenAI')
def test_process_feeds(mock_openai_class, sample_entries, mock_openai_response):
    """Test the complete feed processing pipeline"""
    # Setup mock OpenAI client
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_openai_response
    mock_openai_class.return_value = mock_client

    with patch.dict(os.environ, {'OPENAI_API_KEY': 'dummy-key'}):
        analyzer = AIAnalyzer(verbose=True)
        result = analyzer.process_feeds(sample_entries)
        
        assert isinstance(result, str)
        assert result.startswith("# AI News Summary")

@patch('openai.OpenAI')
def test_api_error_handling(mock_openai_class, sample_entries):
    """Test handling of API errors"""
    # Setup mock OpenAI client to raise an exception
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("API Error")
    mock_openai_class.return_value = mock_client

    with patch.dict(os.environ, {'OPENAI_API_KEY': 'dummy-key'}):
        analyzer = AIAnalyzer(verbose=True)
        
        with pytest.raises(Exception) as exc_info:
            analyzer.process_feeds(sample_entries)
        
        assert "API Error" in str(exc_info.value)

def test_missing_api_key():
    """Test handling of missing API key"""
    with patch.dict(os.environ, {}, clear=True):  # Remove all env variables
        with pytest.raises(ValueError) as exc_info:
            AIAnalyzer(verbose=True)
        
        assert "API key" in str(exc_info.value)