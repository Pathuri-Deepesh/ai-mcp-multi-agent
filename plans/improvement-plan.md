# LangChain MCP Agents - Project Improvement Plan

## Objective
Transform the project from a 5/10 rating to a 10/10 production-ready project

## Phase 1: Foundation Setup

### Step 1: Rename Project Folder
- Current: `dummy-project`
- New: `langchain-mcp-agents`
- This will be done via file system operations

### Step 2: Update Project Configuration

#### Update `pyproject.toml`
- Change name from "dummy-project" to "langchain-mcp-agents"
- Add comprehensive description
- Update Python requirement from 3.14 to 3.12 (more stable)
- Ensure all dependencies are listed with version constraints

#### Update `.python-version`
- Change from `3.14` to `3.12`

#### Update `requirements.txt`
- Add version pinning for all dependencies:
  - langchain>=1.2.13
  - langchain-anthropic>=1.4.0
  - langchain-mcp-adapters>=0.2.2
  - langgraph>=1.1.3
  - mcp>=1.26.0
  - python-dotenv>=1.0.0
  - pytest>=7.0.0 (for testing)

---

## Phase 2: Project Structure

### Step 3: Reorganize Files into Logical Directories

Current structure:
```
dummy-project/
├── weather.py
├── mathserver.py
├── client.py
├── main.py
└── ...
```

Target structure:
```
langchain-mcp-agents/
├── servers/
│   ├── __init__.py
│   ├── math_server.py (renamed from mathserver.py)
│   └── weather_server.py (renamed from weather.py)
├── client/
│   ├── __init__.py
│   ├── mcp_client.py (renamed from client.py)
│   └── agent_runner.py (new - extracted from main async logic)
├── tests/
│   ├── __init__.py
│   ├── test_math_server.py
│   └── test_weather_server.py
├── config/
│   ├── __init__.py
│   └── settings.py (new - centralized configuration)
├── .env.example (new - template for .env)
├── .gitignore (new)
├── README.md (new - comprehensive)
├── pyproject.toml (updated)
├── requirements.txt (updated)
├── .python-version (updated)
└── uv.lock
```

---

## Phase 3: Code Quality Improvements

### Step 4: Create .gitignore
Exclude:
- `.env` (never commit secrets)
- `__pycache__/`
- `*.pyc`
- `.venv/`
- `.pytest_cache/`
- `.coverage`
- `dist/`
- `build/`
- `.vscode/` (optional)
- `*.egg-info/`
- `.DS_Store`

### Step 5: Add Error Handling & Validation

#### In `client.py`:
- Wrap `agent.ainvoke()` calls with try-except blocks
- Add logging for debugging
- Handle API timeouts and network errors
- Add input validation for user queries

#### In `weather.py`:
- Add error handling for API calls
- Validate location parameter

#### In `mathserver.py`:
- Already has divide-by-zero check (good!)
- Add input validation for parameter types

### Step 6: Add Comprehensive Documentation

#### Create README.md
Include:
- Project overview
- What is MCP and LangChain
- Features
- Installation instructions
- Environment setup (.env.example)
- Usage examples (how to run the agent)
- Project structure explanation
- Contributing guidelines
- License

#### Add Module Docstrings
- Each Python file starts with module-level docstring
- Each function has proper docstring with Args, Returns, Raises

---

## Phase 4: Testing & Integration

### Step 7: Create Unit Tests

#### `tests/test_math_server.py`:
```python
- test_add()
- test_subtract()
- test_multiply()
- test_divide()
- test_divide_by_zero()
```

#### `tests/test_weather_server.py`:
```python
- test_get_weather() - mock the response
- test_invalid_location_handling()
```

### Step 8: Replace Hardcoded Values

#### Weather Server
- Replace hardcoded response with actual API call
- Use OpenWeatherMap API or similar
- Store API key in .env
- Add proper error handling for API failures

---

## Phase 5: Documentation & Deployment

### Step 9: Create Configuration Module
- Centralize settings in `config/settings.py`
- Use environment variables
- Create `.env.example` template

### Step 10: Create Comprehensive README.md
- Clear project description
- Setup instructions
- Usage examples
- Architecture diagram (optional)
- Troubleshooting guide

---

## Phase 6: GitHub Setup

### Step 11: Create GitHub Repository
1. Go to github.com
2. Click "New Repository"
3. Name: `langchain-mcp-agents`
4. Add description: "Multi-server AI agent using LangChain and MCP (Model Context Protocol) for executing math operations and weather queries"
5. Choose Public (for visibility)
6. Add topics: `langchain`, `mcp`, `ai-agents`, `python`

### Step 12: Initialize Git & Push

```bash
# In the renamed folder
git init
git add .
git commit -m "Initial commit: Multi-server MCP agent with LangChain integration"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/langchain-mcp-agents.git
git push -u origin main
```

### Step 13: Configure GitHub Repository
- Add comprehensive repository description
- Add topics for discoverability
- Enable GitHub Actions (optional CI/CD)
- Add license (MIT or Apache 2.0 recommended)

---

## Quality Improvements Summary

| Aspect | Current | Improved |
|--------|---------|----------|
| **Documentation** | None | Comprehensive README + docstrings |
| **Structure** | Flat (files at root) | Organized (servers/, client/, tests/) |
| **Error Handling** | Minimal | Proper try-catch and validation |
| **Testing** | None | Unit tests for core functions |
| **Configuration** | Hardcoded/scattered | Centralized in config/ |
| **Secrets Management** | .env in repo | .gitignore + .env.example |
| **Code Quality** | Basic | Professional standards |
| **Dependencies** | Loose versions | Pinned versions |
| **Python Version** | 3.14 (bleeding edge) | 3.12 (stable) |

---

## Execution Order (Step by Step)

1. ✅ Create this plan
2. ⏳ Rename folder to `langchain-mcp-agents`
3. ⏳ Update `.python-version` to 3.12
4. ⏳ Create `.gitignore`
5. ⏳ Create directory structure (servers/, client/, tests/, config/)
6. ⏳ Move and rename files to new directories
7. ⏳ Update `pyproject.toml`
8. ⏳ Update `requirements.txt` with version pinning
9. ⏳ Add error handling to all modules
10. ⏳ Add comprehensive docstrings
11. ⏳ Create `config/settings.py` and `.env.example`
12. ⏳ Create comprehensive `README.md`
13. ⏳ Create unit tests
14. ⏳ Test that everything works
15. ⏳ Initialize git and push to GitHub
16. ⏳ Configure GitHub repository

---

## Expected Outcome
A professional, well-documented, tested, and production-ready Python project that demonstrates:
- Advanced async/await patterns
- MCP server integration
- LangChain AI agent orchestration
- Professional project structure
- Comprehensive testing
- Production-grade error handling
