"""This Into That - Personal URL/file conversion utilities

FastAPI application for web-based converters.
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from converters.spotify_to_apple import convert_playlist

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
async def index(request: Request):
    """Main landing page with converter form."""
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/convert/spotify-to-apple")
async def convert_spotify(request: Request, spotify_url: str = Form(...)):
    """Process Spotify playlist URL and return conversion results."""
    try:
        # Convert playlist using real integration
        result = convert_playlist(spotify_url)

        # Format results for template
        results = {
            "playlist_name": result.playlist_name,
            "total_tracks": result.total_tracks,
            "matched": [
                {
                    "name": track.name,
                    "artist": ", ".join(track.artists),
                    "apple_url": match.apple_music_url
                }
                for track, match in result.matched
            ],
            "unmatched": [
                {
                    "name": track.name,
                    "artist": ", ".join(track.artists)
                }
                for track in result.unmatched
            ],
            "match_rate": result.match_rate,
            "spotify_url": spotify_url
        }

        return templates.TemplateResponse(
            "results.html",
            {"request": request, "results": results}
        )

    except ValueError as e:
        # Handle invalid URL or scraping errors
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": str(e)}
        )


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "service": "this-into-that"}
