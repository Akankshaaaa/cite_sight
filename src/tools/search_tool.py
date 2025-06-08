import requests
from typing import List, Dict
import time
from urllib.parse import quote_plus, urlparse, urljoin
from src.config.config import MAX_SEARCH_RESULTS, MAX_RETRIES, TIMEOUT, USER_AGENT

class SearchTool:
    def __init__(self):
        self.headers = {
            'User-Agent': USER_AGENT
        }

    def _fix_url(self, url: str) -> str:
        """Fix URL by adding scheme if missing"""
        if url.startswith('//'):
            return f'https:{url}'
        if not url.startswith(('http://', 'https://')):
            return f'https://{url}'
        return url

    def search(self, query: str) -> List[Dict]:
        """
        Perform a web search using DuckDuckGo and return results
        
        Args:
            query (str): Search query
            
        Returns:
            List[Dict]: List of search results with title, link, and snippet
        """
        for attempt in range(MAX_RETRIES):
            try:
                # DuckDuckGo's search API endpoint
                encoded_query = quote_plus(query)
                url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
                
                response = requests.get(
                    url,
                    headers=self.headers,
                    timeout=TIMEOUT
                )
                
                response.raise_for_status()
                
                # Use BeautifulSoup to parse the HTML response
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract search results
                results = soup.find_all('div', class_='result')
                formatted_results = []
                
                for result in results[:MAX_SEARCH_RESULTS]:
                    title_elem = result.find('a', class_='result__a')
                    snippet_elem = result.find('a', class_='result__snippet')
                    
                    if title_elem and snippet_elem:
                        link = title_elem.get('href', '')
                        # Extract the actual URL from DuckDuckGo's redirect URL
                        if 'uddg=' in link:
                            link = requests.utils.unquote(link.split('uddg=')[1].split('&')[0])
                        
                        # Fix the URL scheme
                        link = self._fix_url(link)
                        
                        formatted_results.append({
                            'title': title_elem.get_text(strip=True),
                            'link': link,
                            'snippet': snippet_elem.get_text(strip=True)
                        })
                
                return formatted_results
                
            except Exception as e:
                if attempt == MAX_RETRIES - 1:
                    raise Exception(f"Failed to perform search after {MAX_RETRIES} attempts: {str(e)}")
                time.sleep(2 ** attempt)  # Exponential backoff
                
        return [] 