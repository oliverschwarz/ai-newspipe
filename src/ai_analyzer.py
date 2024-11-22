"""
AI Analyzer

Sends content to OpenAI to summarize and returns the response.

Author: Oliver Schwarz
Version: 1.0
Contributor: claude.ai
License: MIT
"""
# src/ai_analyzer.py
import json
import logging
from typing import List, Dict
from openai import OpenAI
import os
from datetime import datetime
from dotenv import load_dotenv

class AIAnalyzer:
    """Component for analyzing news feeds using OpenAI API."""
    
    def __init__(self, api_key: str = None, verbose: bool = False):
        """
        Initialize AIAnalyzer.
        
        Args:
            api_key (str): OpenAI API key. If None, will look for OPENAI_API_KEY in .env file
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
        
        # Load .env file and setup OpenAI client
        load_dotenv()  # This will load the .env file
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key must be provided in .env file with OPENAI_API_KEY=your-key")
        
        if self.verbose:
            self.logger.info("Successfully loaded API key from .env file")
            
        self.client = OpenAI(api_key=self.api_key)

    def _create_analysis_prompt(self, entries: List[Dict]) -> str:
        """Create the prompt for OpenAI with the entries in JSON format."""
        
        # Convert entries to JSON string
        entries_json = json.dumps(entries, indent=2)
        
        prompt = f"""You are an AI news curator specializing in artificial intelligence, machine learning, and LLM news.
        
Task: Analyze these RSS feed entries and create a comprehensive summary in markdown format.

Requirements:
1. Focus on AI, ML, and LLM-related news only
2. For each relevant article:
   - Highlight key technological advancements
   - Note any significant business or industry implications
   - Identify potential societal impacts
3. Group related stories together
4. Use clear markdown formatting
5. Include a summary section at the top

Format the output as a proper markdown document with:
- A main title with date
- A brief executive summary
- Grouped categories of news
- Individual entries with titles, links, and your analysis
- Clear separation between sections

Here are the feed entries in JSON format:

{entries_json}

Please analyze these entries and provide your response in complete markdown format, ready for direct saving to a file."""

        return prompt

    def analyze_feeds(self, entries: List[Dict]) -> str:
        """
        Analyze feed entries using OpenAI API.
        
        Args:
            entries (List[Dict]): List of feed entries to analyze
            
        Returns:
            str: Markdown-formatted analysis
        """
        if self.verbose:
            self.logger.info(f"Analyzing {len(entries)} feed entries")
        
        try:
            prompt = self._create_analysis_prompt(entries)
            
            if self.verbose:
                self.logger.info("Sending request to OpenAI")
            
            response = self.client.chat.completions.create(
                model="gpt-4",  # Using GPT-4 for better analysis
                messages=[
                    {"role": "system", "content": "You are an AI news curator specializing in artificial intelligence and machine learning news analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,  # Balance between creativity and consistency
                max_tokens=4000  # Adjust based on your needs
            )
            
            markdown_content = response.choices[0].message.content
            
            if self.verbose:
                self.logger.info("Successfully received and processed OpenAI response")
            
            return markdown_content
            
        except Exception as e:
            if self.verbose:
                self.logger.error(f"Error during AI analysis: {str(e)}")
            raise

    def process_feeds(self, entries: List[Dict]) -> str:
        """
        Main method to process feed entries into a markdown summary.
        
        Args:
            entries (List[Dict]): List of feed entries to process
            
        Returns:
            str: Final markdown content
        """
        if self.verbose:
            self.logger.info("Starting feed processing")
        
        try:
            # Analyze feeds and get markdown content
            markdown_content = self.analyze_feeds(entries)
            
            if self.verbose:
                self.logger.info("Feed processing completed successfully")
            
            return markdown_content
            
        except Exception as e:
            if self.verbose:
                self.logger.error(f"Error in feed processing: {str(e)}")
            raise