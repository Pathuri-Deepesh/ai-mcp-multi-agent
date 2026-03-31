"""
Interactive MCP Agent Client - A REPL-style interface for multi-server AI agent.

Users can ask questions interactively in the command prompt. The agent:
1. Loads available tools from all MCP servers
2. Listens for user queries
3. Decides which tool to use for each query
4. Executes the appropriate tool
5. Returns results in natural language
6. Loops for the next question

Run: python interactive_client.py
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


def print_header():
    """Print welcome header with instructions."""
    print("\n" + "="*70)
    print("🤖  INTERACTIVE MCP AGENT")
    print("="*70)
    print("\nThis agent has access to multiple tools:")
    print("  📐 MATH TOOLS: add, subtract, multiply, divide")
    print("  🌤️  WEATHER: get weather for any location")
    print("\nJust ask questions naturally, e.g.:")
    print("  'What is 5 + 3?'")
    print("  'What is the weather in London?'")
    print("  'Calculate (100 + 50) * 2'")
    print("\nType 'help' for commands, 'exit' to quit")
    print("="*70 + "\n")


def print_help():
    """Print help information."""
    print("\n" + "-"*70)
    print("AVAILABLE COMMANDS:")
    print("-"*70)
    print("  help          - Show this help message")
    print("  tools         - Show available tools")
    print("  clear         - Clear screen")
    print("  exit / quit   - Exit the program")
    print("-"*70)
    print("EXAMPLES:")
    print("  > What is 5 + 3?")
    print("  > Calculate (12 / 3) + 5")
    print("  > What is the weather in Paris?")
    print("  > Get weather for New York")
    print("-"*70 + "\n")


def print_tools(tools):
    """Print available tools."""
    if not tools:
        print("\n❌ No tools available")
        return
    
    print("\n" + "-"*70)
    print(f"AVAILABLE TOOLS ({len(tools)} total):")
    print("-"*70)
    
    # Separate tools by category
    math_tools = []
    weather_tools = []
    other_tools = []
    
    for tool in tools:
        tool_name = tool.name.lower()
        if tool_name in ['add', 'subtract', 'multiply', 'divide']:
            math_tools.append(tool)
        elif 'weather' in tool_name:
            weather_tools.append(tool)
        else:
            other_tools.append(tool)
    
    if math_tools:
        print("\n📐 Math Tools:")
        for tool in math_tools:
            print(f"   • {tool.name}: {tool.description}")
    
    if weather_tools:
        print("\n🌤️  Weather Tools:")
        for tool in weather_tools:
            print(f"   • {tool.name}: {tool.description}")
    
    if other_tools:
        print("\n🔧 Other Tools:")
        for tool in other_tools:
            print(f"   • {tool.name}: {tool.description}")
    
    print("-"*70 + "\n")


def _extract_response_text(response_data: Dict[str, Any]) -> str:
    """
    Extract text content from an agent response.
    
    Args:
        response_data (Dict[str, Any]): The response dictionary from agent.ainvoke()
    
    Returns:
        str: The extracted text response
    
    Raises:
        ValueError: If response structure is unexpected
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
        
        return response_text
    except (KeyError, IndexError) as e:
        logger.error(f"Error extracting response: {str(e)}")
        raise ValueError(f"Invalid response structure: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error extracting response: {str(e)}")
        raise


async def initialize_agent():
    """
    Initialize MCP client and Claude agent.
    
    Returns:
        tuple: (agent, tools_list, MultiServerMCPClient)
    
    Raises:
        ValueError: If required environment variables are missing
        Exception: If unable to connect to MCP servers
    """
    try:
        # Validate required environment variables
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
        
        logger.info("Initializing MCP client with math, weather, and search servers...")
        
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
        
        return agent, tools, client
        
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error initializing agent: {str(e)}")
        raise


async def execute_query(agent, user_query: str) -> str:
    """
    Execute a user query using the agent.
    
    Args:
        agent: The LangChain agent
        user_query (str): The user's natural language query
    
    Returns:
        str: The agent's response
    
    Raises:
        Exception: If query execution fails
    """
    try:
        logger.info(f"Processing query: {user_query}")
        
        response = await agent.ainvoke({
            "messages": [{
                "role": "user",
                "content": user_query
            }]
        })
        
        response_text = _extract_response_text(response)
        logger.info("Query processed successfully")
        return response_text
        
    except Exception as e:
        logger.error(f"Query execution failed: {str(e)}")
        raise


async def main_interactive() -> None:
    """
    Main interactive REPL loop for the MCP agent.
    
    This function:
    1. Initializes the agent with available tools
    2. Shows welcome message and available tools
    3. Continuously prompts for user input
    4. Processes each query with the agent
    5. Displays results in natural language
    """
    agent = None
    tools = None
    client = None
    
    try:
        # Initialize agent
        print("\n⏳ Initializing agent... Please wait")
        agent, tools, client = await initialize_agent()
        
        print_header()
        print_tools(tools)
        
        # Interactive REPL loop
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                # Handle empty input
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() == 'exit' or user_input.lower() == 'quit':
                    print("\n👋 Goodbye!\n")
                    break
                
                elif user_input.lower() == 'help':
                    print_help()
                    continue
                
                elif user_input.lower() == 'tools':
                    print_tools(tools)
                    continue
                
                elif user_input.lower() == 'clear':
                    # Clear screen (works on Windows and Unix)
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print_header()
                    continue
                
                # Process user query
                print("\n⏳ Processing your query...\n")
                response = await execute_query(agent, user_input)
                print(f"Agent: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted by user. Goodbye!\n")
                break
            except Exception as e:
                logger.error(f"Error processing query: {str(e)}")
                print(f"\n❌ Error: {str(e)}\n")
                print("   Try rephrasing your question or type 'help' for assistance.\n")
    
    except ValueError as e:
        print(f"\n❌ Configuration Error: {str(e)}")
        print("\nPlease ensure:")
        print("  • ANTHROPIC_API_KEY is set in .env")
        print("  • OPENWEATHER_API_KEY is set in .env")
        print("  • mathserver.py and weather.py are in the same directory")
    
    except Exception as e:
        print(f"\n❌ Fatal Error: {str(e)}")
        logger.error(f"Fatal error: {str(e)}")


if __name__ == "__main__":
    try:
        asyncio.run(main_interactive())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        print(f"\n❌ Fatal Error: {str(e)}\n")
