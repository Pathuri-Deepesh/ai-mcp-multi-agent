# MCP Agent - LangChain Multi-Server Integration

A sophisticated Python framework demonstrating the integration of multiple **Model Context Protocol (MCP)** servers with **LangChain** agents. This project showcases how to build intelligent AI agents that can orchestrate and execute tools from multiple specialized servers.

## 🌟 Features

- **Multi-Server MCP Integration**: Seamlessly connect multiple MCP servers (math and weather) to a single agent
- **LangChain Agent Framework**: Intelligent agent orchestration using Claude AI (Haiku model)
- **Error Handling & Logging**: Comprehensive error handling with structured logging throughout
- **Type Safety**: Full type hints for better code quality and IDE support
- **Async/Await Support**: Non-blocking asynchronous operations for better performance
- **Production-Ready Code**: Follows best practices with docstrings, validation, and error recovery

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
Provides basic arithmetic operations:
- **add(a, b)**: Add two numbers
- **subtract(a, b)**: Subtract two numbers
- **multiply(a, b)**: Multiply two numbers
- **divide(a, b)**: Divide two numbers (with zero-division protection)

#### Weather Server (`weather.py`)
Provides weather information (currently mock data):
- **get_weather(location)**: Get weather for a given location
- *Future enhancement*: Integrate with real weather API (OpenWeatherMap, WeatherAPI)

### Client Agent (`client.py`)
Orchestrates both servers using a LangChain agent powered by Claude Haiku to:
- Execute complex calculations with step-by-step reasoning
- Query weather information
- Intelligently choose which tools to use for each query

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher
- pip or uv package manager
- ANTHROPIC_API_KEY (from [Anthropic Console](https://console.anthropic.com))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/dummy-project.git
   cd dummy-project
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
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

### Running the Project

**Start the agent and execute sample queries:**

```bash
python client.py
```

This will:
1. Initialize connections to the math and weather servers
2. Create a LangChain agent powered by Claude Haiku
3. Execute a complex math calculation: `(5 + 3) + (12 / 3) - (2 * 4)`
4. Execute a weather query: `What is the weather in New York?`
5. Display the agent's reasoning and responses

### Example Output

```
Math response: Let me break down this calculation step by step:
1. Addition: (5 + 3) = 8
2. Division: (12 / 3) = 4
3. First subtraction: 8 + 4 = 12
4. Multiplication: (2 * 4) = 8
5. Final subtraction: 12 - 8 = 4

Weather response: The current weather in New York is Cold and windy.
```

## 📁 Project Structure

```
dummy-project/
├── mathserver.py              # Math operations MCP server
├── weather.py                 # Weather information MCP server
├── client.py                  # LangChain agent client orchestrator
├── main.py                    # Example main entry point
├── README.md                  # This file
├── requirements.txt           # Python dependencies with versions
├── pyproject.toml             # Project configuration
├── .python-version            # Python version specification (3.12)
├── .gitignore                 # Git ignore rules
├── .env.example               # Environment template (copy to .env)
├── plans/
│   └── improvement-plan.md    # Detailed improvement roadmap
└── tests/                     # Unit tests (future)
    ├── test_math_server.py
    └── test_weather_server.py
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Required
ANTHROPIC_API_KEY=your-api-key-here

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

## 🧪 Testing

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_math_server.py
```

### Test Coverage

- ✅ Math operations (add, subtract, multiply, divide)
- ✅ Error handling (division by zero, invalid inputs)
- ✅ Type validation
- ✅ Weather server responses
- ⏳ Integration tests (coming soon)

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

2. **Update the client** to include the new server:
   ```python
   client = MultiServerMCPClient({
       "math": {...},
       "weather": {...},
       "calculator": {  # New server
           "command": "python",
           "args": ["calculator_server.py"],
           "transport": "stdio"
       }
   })
   ```

3. **Test the integration** with your agent

### Enhancing the Weather Server

Replace the mock weather data with a real API:

```python
import requests

async def get_weather(location: str) -> str:
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return f"Weather in {location}: {data['weather'][0]['description']}"
```

## 📊 Performance Considerations

- **Async Operations**: All MCP server calls are asynchronous for better concurrency
- **Error Recovery**: Graceful handling of server failures with detailed logging
- **Model Selection**: Uses Claude Haiku (fast and cost-effective) instead of larger models
- **Tool Caching**: Available tools are cached after initial load to improve performance

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

**Issue: Math server fails to start**
```bash
# Check Python version
python --version  # Should be 3.12+

# Check if mathserver.py is in the correct path
ls -la mathserver.py
```

**Issue: Agent times out**
- Increase timeout in client configuration
- Check internet connection for weather API calls
- Review server logs for specific errors

## 📚 Learning Resources

- [Model Context Protocol Spec](https://github.com/anthropics/model-context-protocol)
- [LangChain Documentation](https://python.langchain.com/)
- [Claude API Reference](https://docs.anthropic.com/claude/reference)
- [Async Python Best Practices](https://docs.python.org/3/library/asyncio.html)

## 🚦 Roadmap

- [ ] Real weather API integration (OpenWeatherMap or WeatherAPI)
- [ ] Unit and integration tests
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

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Created as a demonstration of advanced MCP and LangChain integration patterns.

## 🙏 Acknowledgments

- [Anthropic](https://anthropic.com) for Claude and MCP
- [LangChain](https://www.langchain.com/) team for the excellent framework
- The open-source community for inspiration and tools

---

**Questions or Issues?** Open a GitHub issue or check the troubleshooting section above.
