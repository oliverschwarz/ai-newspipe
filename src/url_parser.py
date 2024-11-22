"""
URL Parser
Fetches the RSS urls from a file named news_sources.txt line-by-line
and returns them in an object.

Author: Oliver Schwarz
Version: 1.0
Contributor: claude.ai
License: MIT
"""
# src/url_parser.py
import logging
from typing import List
import os
from urllib.parse import urlparse

class URLFileParser:
    """Component for parsing URLs from a text file."""
    
    def __init__(self, file_path: str, verbose: bool = False):
        """
        Initialize URLFileParser.
        
        Args:
            file_path (str): Path to the file containing URLs
            verbose (bool): Enable verbose logging
        """
        self.file_path = file_path
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

    def _is_valid_url(self, url: str) -> bool:
        """
        Validate if a URL is properly formatted.
        
        Args:
            url (str): URL to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not url or not isinstance(url, str):
            return False
            
        try:
            result = urlparse(url)
            # Check for scheme and netloc
            if not all([result.scheme, result.netloc]):
                return False
            # Check for valid protocol
            if result.scheme not in ['http', 'https']:
                return False
            # Check for proper domain format
            if '.' not in result.netloc or len(result.netloc.split('.')) < 2:
                return False
            # Check for suspicious or incomplete domains
            if result.netloc in ['invalid', 'example', 'localhost']:
                return False
            return True
        except Exception:
            return False

    def parse(self) -> List[str]:
        """
        Parse and validate URLs from the file.
        
        Returns:
            List[str]: List of valid URLs
            
        Raises:
            FileNotFoundError: If the source file doesn't exist
        """
        if not os.path.exists(self.file_path):
            if self.verbose:
                self.logger.error(f"File not found: {self.file_path}")
            raise FileNotFoundError(f"File not found: {self.file_path}")
            
        if self.verbose:
            self.logger.info(f"Reading URLs from file: {self.file_path}")
            
        valid_urls = []
        with open(self.file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    if self._is_valid_url(line):
                        valid_urls.append(line)
                        if self.verbose:
                            self.logger.debug(f"Valid URL found: {line}")
                    else:
                        if self.verbose:
                            self.logger.warning(f"Invalid URL found: {line}")
        
        if self.verbose:
            self.logger.info(f"Found {len(valid_urls)} valid URLs")
            
        return valid_urls