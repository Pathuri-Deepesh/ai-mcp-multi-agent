"""
SearchServer - A Model Context Protocol (MCP) server providing DuckDuckGo search.

This module provides web search tools using DuckDuckGo API without requiring any API keys.
Useful for finding information, current news, and general web search results.
"""

import logging
from mcp.server.fastmcp import FastMCP
from duckduckgo_search import DDGS
from typing import Optional

# Configure logging for debugging and monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the FastMCP server with a descriptive name
mcp = FastMCP("Search")


@mcp.tool()
def search(query: str, max_results: int = 5) -> str:
    """
    Search the web using DuckDuckGo search engine.
    
    Args:
        query (str): The search query/question to search for
        max_results (int): Maximum number of results to return (default: 5, max: 10)
    
    Returns:
        str: Formatted search results with title, description, and URL for each result
    
    Raises:
        ValueError: If query is empty or invalid
        Exception: If search service is unavailable
    
    Note:
        No API key required. Uses free DuckDuckGo search engine.
        Results are scraped in real-time.
    """
    try:
        # Validate input
        if not query or not isinstance(query, str):
            raise ValueError(f"Invalid query: expected non-empty string, got {type(query).__name__}")
        
        # Sanitize query
        query = query.strip()
        if not query:
            raise ValueError("Search query cannot be empty")
        
        # Limit max results to 10
        if max_results < 1 or max_results > 10:
            max_results = min(10, max(1, max_results))
        
        logger.info(f"Searching for: {query} (max results: {max_results})")
        
        try:
            # Perform DuckDuckGo search
            ddgs = DDGS()
            results = list(ddgs.text(query, max_results=max_results))
            
            if not results:
                logger.warning(f"No results found for query: {query}")
                return f"No search results found for '{query}'. Try rephrasing your search."
            
            # Format results
            formatted_results = f"Search Results for '{query}' ({len(results)} results):\n\n"
            
            for i, result in enumerate(results, 1):
                title = result.get("title", "N/A")
                description = result.get("body", "No description available")
                url = result.get("href", "N/A")
                
                formatted_results += f"{i}. {title}\n"
                formatted_results += f"   📝 {description[:150]}{'...' if len(description) > 150 else ''}\n"
                formatted_results += f"   🔗 {url}\n\n"
            
            logger.info(f"Successfully found {len(results)} results for: {query}")
            return formatted_results.strip()
        
        except Exception as e:
            logger.error(f"DuckDuckGo search error for query '{query}': {str(e)}")
            raise ValueError(f"Search service error: {str(e)}")
    
    except ValueError as e:
        logger.error(f"Validation error in search: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in search: {str(e)}")
        raise ValueError(f"Search failed: {str(e)}")


@mcp.tool()
def search_news(query: str, max_results: int = 3) -> str:
    """
    Search for news articles using DuckDuckGo news search.
    
    Args:
        query (str): The news search query/topic
        max_results (int): Maximum number of news articles to return (default: 3, max: 10)
    
    Returns:
        str: Formatted news results with headline, source, date, and URL
    
    Raises:
        ValueError: If query is empty or invalid
        Exception: If search service is unavailable
    
    Note:
        Returns recent news articles related to the search query.
        No API key required.
    """
    try:
        # Validate input
        if not query or not isinstance(query, str):
            raise ValueError(f"Invalid query: expected non-empty string, got {type(query).__name__}")
        
        # Sanitize query
        query = query.strip()
        if not query:
            raise ValueError("News search query cannot be empty")
        
        # Limit max results to 10
        if max_results < 1 or max_results > 10:
            max_results = min(10, max(1, max_results))
        
        logger.info(f"Searching news for: {query} (max results: {max_results})")
        
        try:
            # Perform DuckDuckGo news search
            ddgs = DDGS()
            results = list(ddgs.news(query, max_results=max_results))
            
            if not results:
                logger.warning(f"No news results found for query: {query}")
                return f"No news articles found for '{query}'. Try a different search term."
            
            # Format results
            formatted_results = f"News Results for '{query}' ({len(results)} articles):\n\n"
            
            for i, result in enumerate(results, 1):
                title = result.get("title", "N/A")
                source = result.get("source", "Unknown Source")
                date = result.get("date", "N/A")
                url = result.get("url", "N/A")
                description = result.get("body", "No description")
                
                formatted_results += f"{i}. {title}\n"
                formatted_results += f"   📰 Source: {source} | 📅 {date}\n"
                formatted_results += f"   📝 {description[:120]}{'...' if len(description) > 120 else ''}\n"
                formatted_results += f"   🔗 {url}\n\n"
            
            logger.info(f"Successfully found {len(results)} news articles for: {query}")
            return formatted_results.strip()
        
        except Exception as e:
            logger.error(f"DuckDuckGo news search error for query '{query}': {str(e)}")
            raise ValueError(f"News search service error: {str(e)}")
    
    except ValueError as e:
        logger.error(f"Validation error in news search: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in news search: {str(e)}")
        raise ValueError(f"News search failed: {str(e)}")


if __name__ == "__main__":
    logger.info("Starting SearchServer on stdio transport...")
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        logger.error(f"Error starting SearchServer: {str(e)}")
        raise
