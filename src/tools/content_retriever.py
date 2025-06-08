import trafilatura
import requests
from typing import Optional, Dict
from src.config.config import USER_AGENT, TIMEOUT

class ContentRetriever:
    def __init__(self):
        self.headers = {
            'User-Agent': USER_AGENT
        }

    def fetch_content(self, url: str) -> Optional[Dict[str, str]]:
        """
        Fetch and extract content from a URL
        
        Args:
            url (str): URL to fetch content from
            
        Returns:
            Optional[Dict[str, str]]: Dictionary containing title and text content
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=TIMEOUT)
            response.raise_for_status()
            
            downloaded = trafilatura.fetch_url(url)
            
            if downloaded is None:
                return None
            
            # Extract the main content
            text = trafilatura.extract(downloaded)
            
            # Extract metadata
            metadata = trafilatura.extract_metadata(downloaded)
            title = metadata.title if metadata else ""
            
            if not text:
                return None
                
            return {
                "title": title,
                "content": text,
                "url": url
            }
            
        except Exception as e:
            print(f"Error fetching content from {url}: {str(e)}")
            return None 