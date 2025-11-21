"""
Tavily search tool integration.
This demonstrates TOOL CALLING - one of the key MAT496 topics.
"""

from typing import List
from tavily import TavilyClient
from src.config import Config
from src.state import NewsArticle


class TavilySearchTool:
    """Wrapper for Tavily API to search for news articles."""
    
    def __init__(self):
        """Initialize the Tavily client."""
        self.client = TavilyClient(api_key=Config.TAVILY_API_KEY)
    
    def search_news(self, query: str, max_results: int = None) -> List[NewsArticle]:
        """
        Search for news articles using Tavily.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of NewsArticle objects
        """
        if max_results is None:
            max_results = Config.MAX_SEARCH_RESULTS
        
        try:
            # Perform search with Tavily
            response = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=max_results,
                include_domains=[],
                exclude_domains=[],
                topic="news"  # Focus on news content
            )
            
            # Convert results to NewsArticle objects
            articles = []
            for result in response.get("results", []):
                article = NewsArticle(
                    title=result.get("title", ""),
                    url=result.get("url", ""),
                    content=result.get("content", ""),
                    published_date=result.get("published_date"),
                    source=result.get("source")
                )
                articles.append(article)
            
            return articles
            
        except Exception as e:
            print(f"Error searching with Tavily: {e}")
            return []
    
    def get_context(self, query: str) -> str:
        """
        Get contextual information about a query.
        
        Args:
            query: Search query
            
        Returns:
            Contextual information as a string
        """
        try:
            response = self.client.get_search_context(
                query=query,
                search_depth="advanced",
                max_results=Config.MAX_SEARCH_RESULTS
            )
            return response
        except Exception as e:
            print(f"Error getting context from Tavily: {e}")
            return ""


# Singleton instance
tavily_search = TavilySearchTool()
