"""
iTunes Search API matcher for finding Apple Music tracks.

Uses the free, public iTunes Search API (no authentication required) to search
the Apple Music catalog and return match information.

API Documentation: https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/
"""

import re
import time
from dataclasses import dataclass
from urllib.parse import quote_plus

import httpx


@dataclass
class AppleMusicMatch:
    """Result from iTunes Search API matching."""

    track_name: str
    artist_name: str
    album_name: str
    track_url: str  # https://music.apple.com/...
    apple_music_url: str  # music:// protocol URL for direct app opening
    preview_url: str | None
    confidence: float  # 0.0 - 1.0 match confidence


def normalize_for_search(text: str) -> str:
    """
    Normalize text for better search matching.

    Removes parentheticals like (Remastered), (Live), (feat. ...), etc.
    Lowercases and strips extra whitespace.

    Args:
        text: Text to normalize

    Returns:
        Normalized text suitable for search matching
    """
    # Remove parenthetical annotations
    text = re.sub(r"\([^)]*\)", "", text)
    # Remove brackets
    text = re.sub(r"\[[^\]]*\]", "", text)
    # Remove "feat." and "ft." annotations
    text = re.sub(r"\s+(?:feat\.|ft\.|featuring)\s+.*", "", text, flags=re.IGNORECASE)
    # Lowercase and strip whitespace
    text = text.lower().strip()
    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text)
    return text


def _calculate_confidence(
    query_artist: str, query_title: str, result_artist: str, result_title: str
) -> float:
    """
    Calculate match confidence score between query and result.

    Args:
        query_artist: Artist name from search query
        query_title: Track title from search query
        result_artist: Artist name from API result
        result_title: Track title from API result

    Returns:
        Confidence score from 0.0 to 1.0
    """
    # Normalize for comparison
    norm_query_artist = normalize_for_search(query_artist)
    norm_query_title = normalize_for_search(query_title)
    norm_result_artist = normalize_for_search(result_artist)
    norm_result_title = normalize_for_search(result_title)

    # Exact match
    if norm_query_artist == norm_result_artist and norm_query_title == norm_result_title:
        return 1.0

    # Artist exact, title close
    if norm_query_artist == norm_result_artist:
        # Check if one title contains the other
        if norm_query_title in norm_result_title or norm_result_title in norm_query_title:
            return 0.8
        # Check word overlap
        query_words = set(norm_query_title.split())
        result_words = set(norm_result_title.split())
        if query_words and result_words:
            overlap = len(query_words & result_words) / len(query_words | result_words)
            if overlap > 0.6:
                return 0.7
        return 0.5

    # Partial artist match, title match
    if norm_query_title == norm_result_title:
        if norm_query_artist in norm_result_artist or norm_result_artist in norm_query_artist:
            return 0.7
        return 0.5

    # Both partial matches
    artist_match = (
        norm_query_artist in norm_result_artist or norm_result_artist in norm_query_artist
    )
    title_match = norm_query_title in norm_result_title or norm_result_title in norm_query_title

    if artist_match and title_match:
        return 0.6

    # One or the other has partial match
    if artist_match or title_match:
        return 0.4

    return 0.2


def _convert_to_music_protocol(track_view_url: str) -> str:
    """
    Convert https://music.apple.com URL to music:// protocol URL.

    Args:
        track_view_url: HTTPS URL from iTunes API

    Returns:
        music:// protocol URL for direct app opening
    """
    return track_view_url.replace("https://music.apple.com", "music://music.apple.com")


def search_track(artist: str, title: str) -> AppleMusicMatch | None:
    """
    Search iTunes API for a track and return the best match.

    Rate limited to ~20 calls per minute (0.5s delay after each request).

    Args:
        artist: Artist name
        title: Track title

    Returns:
        AppleMusicMatch if found with confidence > 0.5, None if no good match

    Raises:
        httpx.HTTPError: If API request fails
    """
    # Build search query
    query = quote_plus(f"{artist} {title}")
    url = (
        f"https://itunes.apple.com/search"
        f"?term={query}"
        f"&media=music"
        f"&entity=musicTrack"
        f"&country=US"
        f"&limit=10"
    )

    try:
        # Make API request
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        data = response.json()

        # Check for results
        if data.get("resultCount", 0) == 0:
            return None

        # Find best match
        best_match = None
        best_confidence = 0.0

        for result in data.get("results", []):
            # Calculate confidence
            confidence = _calculate_confidence(
                artist,
                title,
                result.get("artistName", ""),
                result.get("trackName", ""),
            )

            # Track best match
            if confidence > best_confidence:
                best_confidence = confidence
                best_match = result

        # Return best match if confidence is high enough
        if best_match and best_confidence >= 0.5:
            track_url = best_match.get("trackViewUrl", "")
            return AppleMusicMatch(
                track_name=best_match.get("trackName", ""),
                artist_name=best_match.get("artistName", ""),
                album_name=best_match.get("collectionName", ""),
                track_url=track_url,
                apple_music_url=_convert_to_music_protocol(track_url),
                preview_url=best_match.get("previewUrl"),
                confidence=best_confidence,
            )

        return None

    finally:
        # Rate limiting: iTunes API is strict, need ~3 seconds between calls
        time.sleep(3.0)
