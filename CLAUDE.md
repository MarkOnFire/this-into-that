# CLAUDE.md

> **See [AGENTS.md](./AGENTS.md)** for complete project instructions.

This file provides Claude Code-specific guidance for working in this repository.

## Claude-Specific Notes

### Available MCP Servers

When working in this project, you have access to these globally-deployed MCP servers:

- **cli-agent**: Multi-LLM queries via `query_agent` and `code_review` tools
  - Also available as HTTP API at `http://localhost:3001`
  - Use for getting opinions from Gemini/Codex on architectural decisions
- **obsidian-vault**: Access and search Obsidian notes
  - Useful for referencing API documentation stored in the-lodge knowledge base
  - Search for Spotify, Apple Music, YouTube API docs
- **the-library**: Centralized knowledge base
  - Documentation for APIs and external services
  - Read documentation topics: spotify, apple-music, youtube
- **readwise**: Access Readwise highlights and documents
  - Search for relevant articles about web scraping, API integration
- **airtable**: Access AirTable bases (if project tracking is needed)

Configurations are deployed to:
- **Claude Desktop**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Claude Code CLI**: `~/.claude.json` (mcpServers key)

### Claude Code Features

- Use TodoWrite for complex multi-step tasks (e.g., building new converters)
- Use Task tool with specialized agents when appropriate
- Agent threads always have their cwd reset between bash calls - use absolute file paths

### Quick Start for Claude

```bash
# Setup environment
cd ~/Developer/this-into-that
python3 -m venv venv
source venv/bin/activate
uv pip install -e ".[dev]"

# Run development server
uvicorn app:app --reload

# Run tests
pytest
```

### Knowledge Base References

When working on converters, reference documentation in the-lodge:

**Spotify converter:**
- Use the-library MCP: `read_documentation topic="spotify"`
- Or read directly: `~/Developer/the-lodge/knowledge/spotify/`

**Apple Music converter:**
- Use the-library MCP: `read_documentation topic="apple-music"`
- Or read directly: `~/Developer/the-lodge/knowledge/apple-music/`

### Session Protocol

**Starting a session:**
1. Read `planning/README.md` - understand current state
2. Check `planning/backlog.md` - see maintenance items
3. Review `planning/progress.md` (last 2-3 entries) - recent context
4. Activate venv: `source venv/bin/activate`

**Ending a session:**
1. Commit changes with agent attribution
2. Update `planning/backlog.md` (check off completed items)
3. Append entry to `planning/progress.md`
4. Update `planning/README.md` - current state

### Important Workspace Conventions

- **Secrets in Keychain**: Use `~/Developer/the-lodge/scripts/keychain_secrets.py`
  - Never store API keys in .env files
  - See: `~/Developer/the-lodge/conventions/SECRETS_MANAGEMENT.md`

- **Planning structure**: This project follows the-lodge conventions
  - See: `~/Developer/the-lodge/conventions/PLANNING_CONVENTIONS.md`

- **Commit format**: Include agent attribution
  - See: `~/Developer/the-lodge/conventions/COMMIT_CONVENTIONS.md`

### Development Tips

- **API testing**: Use httpx in Python or curl for quick endpoint testing
- **Debugging**: Enable debug logging with `LOG_LEVEL=DEBUG uvicorn app:app --reload`
- **Frontend work**: Templates are in `templates/`, static assets in `static/`
- **New converters**: Follow the pattern in `converters/spotify_to_apple.py`

### Common Tasks

**Add a new converter:**
1. Create module in `converters/`
2. Implement `convert()` function with `ConversionResult` return type
3. Add routes to `app.py`
4. Create template in `templates/`
5. Write tests in `tests/`
6. Update README.md

**Debug API integration:**
1. Check external API documentation in the-library
2. Use the-library MCP to search for examples
3. Test API endpoints with curl/httpx before implementing
4. Mock external APIs in tests

**Refactor existing converter:**
1. Read current implementation
2. Write tests for current behavior (if missing)
3. Refactor incrementally
4. Ensure all tests pass
5. Update documentation

### Terminal Profile

This project uses standard Python development profile. No custom Terminal.app profile needed.

Standard shell configuration at `~/.zshrc` includes:
- Python virtual environment helpers
- Git aliases
- Claude Code shortcuts
