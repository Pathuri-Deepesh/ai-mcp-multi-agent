"""
MCP Agent Client - A LangChain agent that orchestrates multiple MCP (Model Context Protocol) servers.

This module provides a client that connects to multiple MCP servers (math and weather) and uses
LangChain's agent framework to answer user queries by leveraging the tools provided by those servers.
"""

import asyncio
import os
import logging
from typing import Any, Dict

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def _extract_response_text(response_data: Dict[str, Any], response_type: str = "general") -> str:
    """
    Extract text content from an agent response.
    
    Args:
        response_data (Dict[str, Any]): The response dictionary from agent.ainvoke()
        response_type (str): Type of response for logging (e.g., "math", "weather")
    
    Returns:
        str: The extracted text response
    
    Raises:
        KeyError: If response structure is unexpected
        IndexError: If messages list is empty
    """
    try:
        last_message = response_data['messages'][-1]
        
        if isinstance(last_message.content, list):
            # If content is a list of dicts, extract text from the text type items
            response_text = '\n'.join([
                item['text'] for item in last_message.content 
                if isinstance(item, dict) and item.get('type') == 'text'
            ])
        else:
            response_text = last_message.content
        
        logger.info(f"{response_type.capitalize()} response extracted successfully")
        return response_text
    except (KeyError, IndexError) as e:
        logger.error(f"Error extracting {response_type} response: {str(e)}")
        raise ValueError(f"Invalid response structure for {response_type} query")
    except Exception as e:
        logger.error(f"Unexpected error extracting {response_type} response: {str(e)}")
        raise


async def main() -> None:
    """
    Main entry point for the MCP agent client.
    
    Sets up connections to multiple MCP servers (math and weather) and executes
    queries using a LangChain agent powered by Claude Haiku.
    
    Raises:
        ValueError: If required environment variables are missing
        Exception: If unable to connect to MCP servers or execute agent queries
    """
    try:
        # Validate required environment variables
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
        
        logger.info("Initializing MCP client with math and weather servers...")
        
        # Initialize multi-server MCP client
        client = MultiServerMCPClient(
            {
                "math": {
                    "command": "python",
                    "args": ["mathserver.py"],
                    "transport": "stdio"
                },
                "weather": {
                    "command": "python",
                    "args": ["weather.py"],
                    "transport": "stdio",
                },
                # Add this back to the client config:
                "search": {
                    "command": "python",
                    "args": ["search_server.py"],
                    "transport": "stdio",
                }

            }
        )
        
        # Set API key in environment
        os.environ["ANTHROPIC_API_KEY"] = api_key
        
        # Get available tools from both servers
        logger.info("Fetching available tools from MCP servers...")
        tools = await client.get_tools()
        logger.info(f"Successfully loaded {len(tools) if tools else 0} tools from MCP servers")
        
        # Initialize Claude Haiku model
        model = ChatAnthropic(model="claude-haiku-4-5-20251001", streaming=True)
        
        # Create agent with the tools
        agent = create_agent(model, tools)
        logger.info("Agent created successfully")
        
        # Execute math query
        logger.info("Executing math query...")
        try:
            math_response = await agent.ainvoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": "Calculate (5 + 3) + (12 / 3) - (2 * 4)? Provide a detailed step-by-step breakdown mentioning the operation name (Addition, Subtraction, Multiplication, Division) for each calculation. Format like: Addition: (5 + 3) = 8"
                        }
                    ]
                }
            )
            math_response_text = _extract_response_text(math_response, "math")
            print("Math response:", math_response_text)
        except Exception as e:
            logger.error(f"Math query failed: {str(e)}")
            print(f"Error executing math query: {str(e)}")
        
        # Execute weather query
        logger.info("Executing weather query...")
        try:
            weather_response = await agent.ainvoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": "What is the weather in Chennai?"
                        }
                    ]
                }
            )
            weather_response_text = _extract_response_text(weather_response, "weather")
            print("Weather response:", weather_response_text)
        except Exception as e:
            logger.error(f"Weather query failed: {str(e)}")
            print(f"Error executing weather query: {str(e)}")
        
        logger.info("Agent execution completed successfully")
        
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in main: {str(e)}")
        raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        raise
