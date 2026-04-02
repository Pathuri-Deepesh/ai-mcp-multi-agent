# MCP Agent - LangChain Multi-Server Integration

A sophisticated Python framework demonstrating the integration of multiple **Model Context Protocol (MCP)** servers with **LangChain** agents. This project showcases how to build intelligent AI agents that can orchestrate and execute tools from multiple specialized servers, including real-world API integrations.

## 🌟 Features

- **Multi-Server MCP Integration**: Seamlessly connect multiple MCP servers (math, weather, and web search) to a single agent
- **Real API Integrations**: 
  - OpenWeatherMap for live weather data
  - Official DuckDuckGo MCP server for web search and news articles
- **LangChain Agent Framework**: Intelligent agent orchestration using Claude AI (Haiku model)
- **Error Handling & Logging**: Comprehensive error handling with structured logging throughout
- **Type Safety**: Full type hints for better code quality and IDE support
- **Async/Await Support**: Non-blocking asynchronous operations for better performance
- **Interactive REPL**: Command-line interface for testing queries interactively
- **Production-Ready Code**: Follows best practices with docstrings, validation, and error recovery
- **Official Servers**: Uses maintained community/official MCP servers where available

## 📋 What is MCP (Model Context Protocol)?

MCP is a protocol that standardizes how applications provide context to language models. It allows you to:
- Define tools and resources that AI models can access
- Create specialized servers that expose specific functionalities
- Integrate multiple servers with a single agent interface

Learn more: [MCP Documentation](https://github.com/anthropics/model-context-protocol)

## 🧠 What is LangChain?

LangChain is a framework for building applications with large language models. It provides:
- Agent orchestration for multi-step reasoning
- Tool integration and calling
- Memory and context management
- Integration with various LLM providers

## 🏗️ Project Architecture

### Available MCP Servers

#### Math Server (`mathserver.py`)
Custom MCP server providing basic arithmetic operations with validation and error handling:
- **add(a, b)**: Add two numbers
- **subtract(a, b)**: Subtract two numbers
- **multiply(a, b)**: Multiply two numbers
- **divide(a, b)**: Divide two numbers (with zero-division protection)

#### Weather Server (`weather.py`)
Custom MCP server providing real-time weather information via OpenWeatherMap API:
- **get_weather(location)**: Get current weather for a given location
- Returns: Temperature, humidity, wind speed, and weather conditions
- Live API integration with error handling for network failures

#### Official DuckDuckGo Search Server
Official community-maintained MCP server for web search and news (installed via `uvx`):
- **search(query)**: Search the web for information
  - Returns: Title, description, and URL for each result
  - Use case: Finding tutorials, documentation, general information
- **search_news(query)**: Search for recent news articles
  - Returns: Headline, source, date, and URL for each article
  - Use case: Finding latest news, trends, current events
- **Features**:
  - Official, community-maintained server
  - No API key required
  - Automatic updates via uvx
  - Real-time web scraping for fresh results

### Interactive Client (`interactive_client.py`)
Main entry point providing a REPL-style command-line interface for testing:
- Interactive query entry
- Help command to list available tools
- Tools command to show categorized tools (Math, Weather, Search)
- Clear command to reset context
- Exit command to quit the program
- Real-time tool responses with formatted output

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher
- pip or uv package manager
- ANTHROPIC_API_KEY (from [Anthropic Console](https://console.anthropic.com))
- OPENWEATHER_API_KEY (optional, from [OpenWeatherMap](https://openweathermap.org/api))
- uvx (for running the official DuckDuckGo MCP server)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Pathuri-Deepesh/ai-mcp-multi-agent.git
   cd ai-mcp-multi-agent
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or with uv:
   ```bash
   uv pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY and OPENWEATHER_API_KEY
   ```

### Running the Project

#### Interactive REPL (Recommended)
Use the interactive client for real-time queries:

```bash
python interactive_client.py
```

Then try these commands:
```
You: what is the weather in New York?
You: search for machine learning frameworks
You: find recent technology news
You: python async programming tutorials
You: tools
You: help
You: exit
```

### Example Output

**Interactive Client:**
```
═══════════════════════════════════════════════════════════
🤖  INTERACTIVE MCP AGENT
═══════════════════════════════════════════════════════════

This agent has access to multiple tools:
  📐 MATH TOOLS: add, subtract, multiply, divide
  🌤️  WEATHER: get weather for any location

Just ask questions naturally, e.g.:
  'What is 5 + 3?'
  'What is the weather in London?'
  'Calculate (100 + 50) * 2'

Type 'help' for commands, 'exit' to quit
═══════════════════════════════════════════════════════════

You: What is the weather in London?

⏳ Processing your query...

Agent: The current weather in London is 15°C with scattered clouds. 
Humidity is 72% and wind speed is 8 km/h.

You: search for python async programming

⏳ Processing your query...

Agent: Search Results for 'python async programming' (5 results):

1. Python Async/Await Tutorial
   📝 Learn how to write non-blocking code in Python...
   🔗 https://example.com/async-tutorial

2. Advanced Python Asyncio Patterns
   📝 Master concurrent programming with asyncio...
   🔗 https://example.com/asyncio-patterns

You: tools

────────────────────────────────────────────────────────────
AVAILABLE TOOLS (8 total):
────────────────────────────────────────────────────────────

📐 Math Tools:
   • add: Add two numbers
   • subtract: Subtract two numbers
   • multiply: Multiply two numbers
   • divide: Divide two numbers

🌤️  Weather Tools:
   • get_weather: Get current weather for a given location

🔍 Search Tools:
   • search: Search the web for information
   • search_news: Search for recent news articles

────────────────────────────────────────────────────────────

You: exit
```

## 📁 Project Structure

```
ai-mcp-multi-agent/
├── mathserver.py              # Math operations MCP server (custom)
├── weather.py                 # Weather information MCP server (custom, OpenWeatherMap API)
├── interactive_client.py       # Interactive REPL client (main entry point)
├── main.py                    # Example helper file
├── README.md                  # This file
├── requirements.txt           # Python dependencies with versions
├── pyproject.toml             # Project configuration
├── .python-version            # Python version specification (3.12)
├── .gitignore                 # Git ignore rules
├── .env.example               # Environment template (copy to .env)
└── tests/                     # Unit tests
    ├── test_math_server.py    # 45+ math operation tests
    └── test_weather_server.py # 30+ async weather tests
```

**Note**: 
- `search_server.py` has been removed in favor of the official `duckduckgo-mcp-server`
- `client.py` has been removed in favor of `interactive_client.py`

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Required
ANTHROPIC_API_KEY=your-anthropic-api-key

# Optional (required for real weather data)
OPENWEATHER_API_KEY=your-openweathermap-api-key

# Optional
LOG_LEVEL=INFO
AGENT_MODEL=claude-haiku-4-5-20251001
```

### Dependency Versions

All dependencies in `requirements.txt` are pinned to ensure consistency:

| Package | Version | Purpose |
|---------|---------|---------|
| langchain | >=1.2.13 | AI framework |
| langchain-anthropic | >=1.4.0 | Claude integration |
| langchain-mcp-adapters | >=0.2.2 | MCP protocol support |
| langgraph | >=1.1.3 | Graph-based agent orchestration |
| mcp | >=1.26.0 | MCP server/client |
| python-dotenv | >=1.0.0 | Environment management |
| requests | >=2.31.0 | HTTP client for APIs |
| pytest | >=7.4.0 | Testing framework |
| pytest-asyncio | >=0.21.0 | Async test support |

## 🧪 Testing

### Running Tests

```bash
# Install test dependencies (included in requirements.txt)
pip install pytest pytest-asyncio

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_math_server.py

# Run with coverage
pytest --cov=. tests/
```

### Test Coverage

- ✅ Math operations (add, subtract, multiply, divide) - 45+ tests
- ✅ Error handling (division by zero, invalid inputs) - 10+ tests
- ✅ Type validation - 15+ tests
- ✅ Weather server responses with async operations - 30+ tests
- ✅ API error handling (401, 404, 500, timeouts) - 10+ tests
- ✅ Weather data formatting and parsing - 5+ tests
- ⏳ Search integration tests (available via official server)

## 🔄 Development Workflow

### Adding a New Tool

1. **Create a new MCP server** (e.g., `calculator_server.py`)
   ```python
   from mcp.server.fastmcp import FastMCP
   
   mcp = FastMCP("Calculator")
   
   @mcp.tool()
   def advanced_calculation(expr: str) -> float:
       """Advanced math expression calculator"""
       # Implementation here
       pass
   ```

2. **Update the client** to include the new server in `interactive_client.py`:
   ```python
   client = MultiServerMCPClient({
       "math": {...},
       "weather": {...},
       "search": {...},
       "calculator": {  # New server
           "command": "python",
           "args": ["calculator_server.py"],
           "transport": "stdio"
       }
   })
   ```

3. **Test the integration** with your agent

### Using the Search Tools

The search tools are integrated via the official DuckDuckGo MCP server. Simply ask natural language questions and the agent automatically uses the search tools:

```python
# Examples in interactive client:
"Find information about machine learning"
"What are the latest technology news articles?"
"Search for python programming tutorials"
"Show me recent AI breakthroughs"
```

The agent will automatically choose to use the search tools when appropriate.

### Real API Integration

The project uses real API integrations:

**Weather API (OpenWeatherMap):**
- Live weather data for any location
- Sign up at https://openweathermap.org/api
- Add API key to `.env` as `OPENWEATHER_API_KEY`
- Supports current weather, forecasts, and historical data

**Search API (DuckDuckGo):**
- Official MCP server (maintained by community)
- No API key required - uses free web scraping
- Supports general web search and news search
- Installed and managed via uvx

## 📊 Performance Considerations

- **Async Operations**: All MCP server calls are asynchronous for better concurrency
- **Error Recovery**: Graceful handling of server failures with detailed logging
- **Model Selection**: Uses Claude Haiku (fast and cost-effective) instead of larger models
- **Tool Caching**: Available tools are cached after initial load to improve performance
- **Connection Pooling**: Reuses connections to minimize overhead
- **Official Servers**: Leverages maintained community servers for stability

## 🐛 Troubleshooting

### Common Issues

**Issue: `ANTHROPIC_API_KEY not set`**
```bash
# Solution: Create .env file with your API key
echo "ANTHROPIC_API_KEY=your-key-here" > .env
```

**Issue: `ModuleNotFoundError: No module named 'langchain'`**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue: Search returns rate limit error or no results**
This is expected behavior with DuckDuckGo's free API. Solutions:
- Wait a few minutes for rate limits to reset
- Try rephrasing your search query
- Use more specific search terms
- Check that you have internet connectivity

**Issue: Math server fails to start**
```bash
# Check Python version
python --version  # Should be 3.12+

# Check if mathserver.py is in the correct path
ls -la mathserver.py
```

**Issue: Weather API returns 401 (Unauthorized)**
```
# Solution: Check that OPENWEATHER_API_KEY is set correctly
cat .env | grep OPENWEATHER_API_KEY

# If not set, add it to .env:
OPENWEATHER_API_KEY=your-actual-api-key
```

**Issue: Agent times out**
- Increase timeout in client configuration
- Check internet connection for API calls
- Review server logs for specific errors
- Reduce the complexity of queries

## 📚 Learning Resources

- [Model Context Protocol Spec](https://github.com/anthropics/model-context-protocol)
- [LangChain Documentation](https://python.langchain.com/)
- [Claude API Reference](https://docs.anthropic.com/claude/reference)
- [Async Python Best Practices](https://docs.python.org/3/library/asyncio.html)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [DuckDuckGo MCP Server](https://github.com/anthropics/mcp-servers)

## 🚦 Roadmap

- [x] Real weather API integration (OpenWeatherMap)
- [x] Web search integration (official DuckDuckGo MCP server)
- [x] News search functionality
- [x] Unit and integration tests (75+ tests)
- [x] Interactive REPL client
- [x] Official server integration (DuckDuckGo)
- [ ] GitHub Actions CI/CD pipeline
- [ ] Docker containerization
- [ ] Web API wrapper (FastAPI)
- [ ] Advanced query caching
- [ ] Performance benchmarks
- [ ] Additional MCP servers (database, file system, etc.)

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Code Standards

- Follow PEP 8 style guide
- Add docstrings to all functions and modules
- Include type hints for all parameters and returns
- Add error handling with meaningful messages
- Write tests for new functionality
- Test with `pytest` before submitting PR

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Created as a demonstration of advanced MCP and LangChain integration patterns with real-world API integrations using official and custom servers.

## 🙏 Acknowledgments

- [Anthropic](https://anthropic.com) for Claude and MCP
- [LangChain](https://www.langchain.com/) team for the excellent framework
- [OpenWeatherMap](https://openweathermap.org/) for weather API
- [DuckDuckGo](https://duckduckgo.com/) for search services and official MCP server
- The open-source community for inspiration and tools

---

**Questions or Issues?** Open a GitHub issue or check the troubleshooting section above.

**Repository**: https://github.com/Pathuri-Deepesh/ai-mcp-multi-agent
