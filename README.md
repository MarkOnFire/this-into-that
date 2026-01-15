# This Into That

**Personal internet toolbox for URL and file conversion utilities**

"Converts This Into That" - a collection of web-based converters for common internet format transformations.

## Current Converters

### Spotify → Apple Music
Convert Spotify playlist URLs to Apple Music search links for easy playlist recreation.

**Status**: In development

## Quick Start

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
uv pip install -e ".[dev]"

# Run development server
uvicorn app:app --reload

# Open browser to http://localhost:8000
```

## Architecture

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: Jinja2 templates
- **APIs**: spotifyscraper, iTunes Search API
- **Server**: Uvicorn ASGI

## Planned Converters

Future conversion utilities under consideration:

- **YouTube Playlist → Apple Music** - Convert YouTube music playlists to Apple Music searches
- **Twitter List → RSS Feed** - Generate RSS feeds from Twitter lists
- **Markdown → Styled PDF** - Convert markdown documents to professionally formatted PDFs
- **Instagram Links → Embeddable Format** - Transform Instagram URLs for better embedding
- **Google Maps → Apple Maps** - Convert location links between mapping services
- **Spotify → YouTube Music** - Cross-platform music playlist conversion

## Project Structure

```
this-into-that/
├── app.py                 # FastAPI application
├── converters/            # Converter modules
│   └── spotify_to_apple.py
├── templates/             # Jinja2 HTML templates
├── static/                # CSS, JavaScript, images
├── tests/                 # Test suite
└── planning/              # Project planning and tracking
```

## Development

### Running Tests

```bash
pytest

# With coverage
pytest --cov=converters --cov-report=html
```

### Code Quality

```bash
# Format
black .

# Lint
ruff check .
```

### Adding a New Converter

1. Create converter module in `converters/`
2. Implement `convert()` function with standard return type
3. Add routes to `app.py`
4. Create UI template
5. Write tests
6. Update this README

See `AGENTS.md` for detailed development guidelines.

## Contributing

This is a personal project, but the patterns and converters may be useful references. All converters are self-contained modules with standard interfaces.

## License

Personal use only. Individual converter modules may use different open source libraries - see their respective licenses.

## Co-Authors

This repository is developed collaboratively with AI assistance. Contributors are tracked via git commits:

| Agent | Role | Recent Commits |
|-------|------|----------------|
| **The Fixer** | Repository setup and infrastructure | [View commits](https://github.com/user/repo/commits?author=the-fixer) |

To see agent-specific contributions:
```bash
# View all commits by agent
git log --grep="Agent: Main Assistant"

# View agent distribution
git log --oneline | grep -o '\[Agent: [^]]*\]' | sort | uniq -c
```

See [workspace conventions](../the-lodge/conventions/COMMIT_CONVENTIONS.md) for details.
