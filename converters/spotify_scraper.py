"""
Spotify playlist scraper using SpotifyScraper library.

Extracts track information from Spotify playlists without requiring authentication.
"""

from dataclasses import dataclass

from spotify_scraper import SpotifyClient, ExtractionError, NetworkError


@dataclass
class SpotifyTrack:
    """Represents a track from a Spotify playlist."""

    name: str
    artists: list[str]
    album: str | None
    duration_ms: int


def scrape_playlist(url: str) -> tuple[str, list[SpotifyTrack]]:
    """
    Scrape a Spotify playlist URL and return track information.

    Args:
        url: Spotify playlist URL (e.g., https://open.spotify.com/playlist/...)

    Returns:
        Tuple of (playlist_name, list of SpotifyTrack objects)

    Raises:
        ValueError: If URL is invalid, playlist not found, or playlist is empty/private

    Example:
        >>> name, tracks = scrape_playlist("https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M")
        >>> print(f"{name}: {len(tracks)} tracks")
        Today's Top Hits: 50 tracks
    """
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")

    if not url.startswith("https://open.spotify.com/playlist/"):
        raise ValueError(
            "Invalid Spotify playlist URL. Expected format: "
            "https://open.spotify.com/playlist/..."
        )

    client = SpotifyClient()
    try:
        # Fetch playlist data
        try:
            playlist_data = client.get_playlist_info(url)
        except ExtractionError as e:
            raise ValueError(f"Failed to extract playlist data: {e}") from e
        except NetworkError as e:
            raise ValueError(f"Network error while fetching playlist: {e}") from e
        except Exception as e:
            raise ValueError(f"Unexpected error fetching playlist: {e}") from e

        # Validate playlist data
        if not playlist_data:
            raise ValueError("Playlist not found or is private")

        playlist_name = playlist_data.get("name")
        if not playlist_name:
            raise ValueError("Playlist has no name (may be private or deleted)")

        tracks_data = playlist_data.get("tracks", [])
        if not tracks_data:
            raise ValueError("Playlist is empty or tracks are not accessible")

        # Convert to SpotifyTrack objects
        tracks = []
        for track_data in tracks_data:
            try:
                # Extract artist names
                artists_data = track_data.get("artists", [])
                artists = [artist.get("name", "Unknown") for artist in artists_data]
                if not artists:
                    artists = ["Unknown"]

                # Extract album name (may be None per library limitations)
                album_data = track_data.get("album", {})
                album_name = album_data.get("name") if album_data else None

                # Create track object
                track = SpotifyTrack(
                    name=track_data.get("name", "Unknown"),
                    artists=artists,
                    album=album_name,
                    duration_ms=track_data.get("duration_ms", 0),
                )
                tracks.append(track)

            except Exception as e:
                # Skip malformed tracks but continue processing
                # This ensures partial playlist data can still be returned
                continue

        if not tracks:
            raise ValueError("No valid tracks found in playlist")

        return playlist_name, tracks

    finally:
        # Always clean up the client
        client.close()
