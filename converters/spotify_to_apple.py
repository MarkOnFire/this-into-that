"""
Integration layer for converting Spotify playlists to Apple Music.

Combines Spotify scraping and iTunes matching into a complete conversion pipeline.
"""

import logging
from dataclasses import dataclass

from converters.itunes_matcher import AppleMusicMatch, search_track
from converters.spotify_scraper import SpotifyTrack, scrape_playlist

# Setup logging
logger = logging.getLogger(__name__)


@dataclass
class ConversionResult:
    """Result of converting a Spotify playlist to Apple Music."""

    playlist_name: str
    total_tracks: int
    matched: list[tuple[SpotifyTrack, AppleMusicMatch]]
    unmatched: list[SpotifyTrack]
    match_rate: float  # Percentage 0-100


def convert_playlist(spotify_url: str, progress_callback=None) -> ConversionResult:
    """
    Convert a Spotify playlist to Apple Music matches.

    Args:
        spotify_url: Spotify playlist URL
        progress_callback: Optional callback(current, total) for progress updates

    Returns:
        ConversionResult with matched and unmatched tracks

    Raises:
        ValueError: If Spotify URL is invalid or playlist cannot be scraped
    """
    # Scrape Spotify playlist
    logger.info(f"Scraping Spotify playlist: {spotify_url}")
    playlist_name, tracks = scrape_playlist(spotify_url)
    logger.info(f"Found {len(tracks)} tracks in playlist '{playlist_name}'")

    # Process each track
    matched: list[tuple[SpotifyTrack, AppleMusicMatch]] = []
    unmatched: list[SpotifyTrack] = []
    total_tracks = len(tracks)

    for i, track in enumerate(tracks, start=1):
        # Call progress callback if provided
        if progress_callback:
            try:
                progress_callback(i, total_tracks)
            except Exception as e:
                logger.warning(f"Progress callback failed: {e}")

        # Use first artist for matching
        artist = track.artists[0] if track.artists else "Unknown"

        try:
            # Search for track in Apple Music
            match = search_track(artist, track.name)

            if match:
                matched.append((track, match))
                logger.debug(
                    f"Matched: {track.name} by {artist} "
                    f"(confidence: {match.confidence:.2f})"
                )
            else:
                unmatched.append(track)
                logger.debug(f"No match found: {track.name} by {artist}")

        except Exception as e:
            # Network errors or API issues - skip track and add to unmatched
            logger.error(f"Error matching track '{track.name}' by {artist}: {e}")
            unmatched.append(track)

    # Calculate match rate
    match_rate = (len(matched) / total_tracks * 100) if total_tracks > 0 else 0.0

    logger.info(
        f"Conversion complete: {len(matched)}/{total_tracks} tracks matched "
        f"({match_rate:.1f}%)"
    )

    return ConversionResult(
        playlist_name=playlist_name,
        total_tracks=total_tracks,
        matched=matched,
        unmatched=unmatched,
        match_rate=match_rate,
    )
