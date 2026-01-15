"""This Into That - Personal URL/file conversion utilities

FastAPI application for web-based converters.
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI(
    title="This Into That",
    description="Personal internet toolbox for URL and file conversion utilities",
    version="0.1.0",
)

# Setup static files and templates
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def index():
    """Main landing page with available converters."""
    return HTMLResponse(
        content="""
        <!DOCTYPE html>
        <html>
        <head>
            <title>This Into That</title>
        </head>
        <body>
            <h1>This Into That</h1>
            <p>Personal internet toolbox for URL and file conversion utilities</p>
            <h2>Available Converters</h2>
            <ul>
                <li><a href="/converters/spotify-to-apple">Spotify → Apple Music</a> (Coming soon)</li>
            </ul>
        </body>
        </html>
        """,
        status_code=200,
    )


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "service": "this-into-that"}


# Converter routes will be added here
# Example:
# @app.get("/converters/spotify-to-apple")
# async def spotify_to_apple_ui():
#     """Spotify to Apple Music converter UI"""
#     pass
#
# @app.post("/api/convert/spotify-to-apple")
# async def spotify_to_apple_api(data: dict):
#     """Spotify to Apple Music converter API endpoint"""
#     pass
