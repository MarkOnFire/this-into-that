# AGENTS.md

This file provides guidance to AI coding agents working in this repository.

## Repository Purpose

**This Into That** is a personal internet toolbox for URL and file conversion utilities. It provides web-based converters for common "this into that" transformations.

**Current converters:**
- Spotify playlist → Apple Music links (in development)

**Future converters:**
- YouTube playlist → Apple Music search
- Twitter list → RSS feed
- Markdown → styled PDF
- And other common internet format conversions

## Architecture Overview

### Technology Stack
- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: Jinja2 templates with minimal JavaScript
- **Deployment**: Uvicorn ASGI server

### Project Structure

```
this-into-that/
├── app.py                 # FastAPI application with route definitions
├── converters/            # Converter modules (one per conversion type)
│   ├── __init__.py
│   └── spotify_to_apple.py  # Spotify → Apple Music converter
├── templates/             # Jinja2 HTML templates
│   └── index.html         # Main conversion interface
├── static/                # CSS, JavaScript, images
│   ├── css/
│   └── js/
└── planning/              # Task planning and progress tracking
```

### Design Principles

1. **Modular converters**: Each converter is a self-contained module with a standard interface
2. **Simple UI**: Clean, functional web interface focused on the conversion task
3. **API-first**: Converters expose both web UI and JSON API endpoints
4. **Error handling**: Clear error messages for invalid input or API failures

## Development Commands

### Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies (using uv or pip)
uv pip install -e ".[dev]"
# OR
pip install -e ".[dev]"
```

### Run Development Server

```bash
# Activate virtual environment
source venv/bin/activate

# Run with auto-reload
uvicorn app:app --reload --port 8000

# Server runs at: http://localhost:8000
```

### Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=converters --cov-report=html
```

### Code Quality

```bash
# Format code
black .

# Lint code
ruff check .
```

## Coding Conventions

### Python Style
- Follow PEP 8 with 100-character line length
- Use type hints for function signatures
- Use async/await for I/O operations (HTTP requests, file operations)
- Prefer descriptive variable names over abbreviations

### Converter Module Structure

Each converter module should follow this pattern:

```python
"""Converter: Source → Target

Brief description of what this converter does.
"""

from typing import Optional
from dataclasses import dataclass

@dataclass
class ConversionResult:
    """Standard result format for all converters."""
    success: bool
    output: dict | str
    error: Optional[str] = None
    metadata: Optional[dict] = None

async def convert(input_data: str) -> ConversionResult:
    """Main conversion function.

    Args:
        input_data: The source data to convert (URL, text, etc.)

    Returns:
        ConversionResult with output or error message
    """
    # Implementation
    pass
```

### FastAPI Route Conventions

```python
# Web UI endpoints
@app.get("/")
async def index():
    """Main conversion interface."""
    pass

@app.get("/converters/{converter_name}")
async def converter_ui(converter_name: str):
    """Specific converter UI."""
    pass

# API endpoints
@app.post("/api/convert/{converter_name}")
async def convert_api(converter_name: str, data: dict):
    """JSON API for conversions."""
    pass
```

## Testing Guidelines

### Test Structure
- Place tests in `tests/` directory
- One test file per converter: `tests/test_spotify_to_apple.py`
- Use pytest fixtures for common setup

### What to Test
1. **Converter logic**: Valid input produces expected output
2. **Error handling**: Invalid input produces clear error messages
3. **API integration**: External APIs are called correctly (use mocking)
4. **Edge cases**: Empty input, malformed URLs, API failures

### Example Test

```python
import pytest
from converters.spotify_to_apple import convert

@pytest.mark.asyncio
async def test_spotify_playlist_conversion():
    result = await convert("https://open.spotify.com/playlist/...")
    assert result.success
    assert "tracks" in result.output
```

## Commit Conventions

This project follows workspace-wide commit conventions.

**See**: `/Users/mriechers/Developer/the-lodge/conventions/COMMIT_CONVENTIONS.md`

**Quick reference**: All AI-generated commits must include `[Agent: <name>]` after the subject line.

Example:
```
feat: Add Spotify to Apple Music converter

[Agent: Main Assistant]

Implements basic playlist conversion using spotifyscraper and iTunes API.
```

## Important Paths

- `/Users/mriechers/Developer/the-lodge/knowledge/spotify/` - Spotify API documentation
- `/Users/mriechers/Developer/the-lodge/knowledge/apple-music/` - Apple Music documentation
- `planning/README.md` - Current project status and planning
- `planning/backlog.md` - Ongoing maintenance items
- `planning/progress.md` - Session-by-session progress log

## Common Workflows

### Adding a New Converter

1. **Create converter module**: `converters/new_converter.py`
   - Implement `convert()` function with `ConversionResult` return type
   - Add comprehensive docstrings
   - Handle errors gracefully

2. **Add API route**: In `app.py`
   ```python
   @app.post("/api/convert/new-converter")
   async def new_converter_api(data: dict):
       from converters.new_converter import convert
       result = await convert(data["input"])
       return result
   ```

3. **Create UI template**: `templates/new_converter.html`
   - Input form for source data
   - Output display area
   - Error message handling

4. **Write tests**: `tests/test_new_converter.py`
   - Test valid conversions
   - Test error cases
   - Mock external APIs

5. **Update documentation**: Add converter to README.md and this file

### Debugging API Integration Issues

1. **Enable request logging**: Set environment variable
   ```bash
   export LOG_LEVEL=DEBUG
   ```

2. **Test API endpoints directly**: Use httpx or curl
   ```bash
   curl -X POST http://localhost:8000/api/convert/spotify-to-apple \
     -H "Content-Type: application/json" \
     -d '{"input": "https://open.spotify.com/playlist/..."}'
   ```

3. **Check external API responses**: Add logging in converter module
   ```python
   response = await client.get(url)
   logger.debug(f"API response: {response.status_code} {response.text}")
   ```

### Planning Folder Usage

- **Read `planning/README.md` first** - Understand current project state
- **Check `planning/backlog.md`** - Pick maintenance items
- **Update `planning/progress.md`** - Log work completed each session
- **For major features**: Create sprint in `planning/sprints/current/`

See: `/Users/mriechers/Developer/the-lodge/conventions/PLANNING_CONVENTIONS.md`

## External References

### Workspace Conventions
All conventions are stored in the-lodge repository:
- Agent cooperation: `~/Developer/the-lodge/conventions/AGENT_COOPERATION.md`
- Planning structure: `~/Developer/the-lodge/conventions/PLANNING_CONVENTIONS.md`
- Commit format: `~/Developer/the-lodge/conventions/COMMIT_CONVENTIONS.md`
- Secrets management: `~/Developer/the-lodge/conventions/SECRETS_MANAGEMENT.md`

### Knowledge Base
Documentation for APIs and services used in converters:
- `~/Developer/the-lodge/knowledge/spotify/` - Spotify API docs
- `~/Developer/the-lodge/knowledge/apple-music/` - Apple Music docs
- `~/Developer/the-lodge/knowledge/youtube/` - YouTube API docs (future)
