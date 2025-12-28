"""
Sprint 4 Module: User Data & Discovery
Stories:
 - S4-07: User Profiles
 - S4-09: Advanced Search
 - S4-12: Rate Songs
"""
import json
from pathlib import Path
from music_player.player_state import PlayerState
from music_player import time_utils
from music_player.playlist_model import Playlist

PROFILE_FILE = Path("profiles.json")


# S4-07: User Profiles

def load_profiles_index(state: PlayerState) -> None:
    """
    Loads profile metadata on startup. Restores the active profile
    and its playlists/ratings/likes.
    """
    pass


def list_profiles(state: PlayerState) -> None:
    """
    Prints a list of all available user profiles.
    """
    pass


def show_current_profile(state: PlayerState) -> None:
    """
    Displays the name of the currently active profile.
    """
    pass


def create_profile(state: PlayerState, name: str) -> None:
    """
    Creates a new user profile with empty data and saves it.
    """
    pass


def switch_profile(state: PlayerState, name: str) -> None:
    """
    Switches the active user context.
    - Saves the current profile's state.
    - Clears current memory.
    - Loads the new profile's data.
    """
    pass


# Helpers

def _serialize_current_state(state: PlayerState) -> dict:
    """Helper: Converts Playlists to JSON dictionaries."""
    pass


def _apply_profile_data(state: PlayerState, data: dict):
    """Helper: Restores runtime objects from a dictionary."""
    pass


def _save_profiles(state: PlayerState):
    """Helper: Persists the entire profiles index to profiles.json."""
    pass


def _save_current_to_profile(state: PlayerState):
    """Helper: Snapshots current active state into the profiles dictionary."""
    pass


# S4-09: Advanced Search

def advanced_search(state: PlayerState, query_str: str) -> None:
    if not query_str:
        print("[search] Usage: /search <query>")
        return

    tokens = query_str.split()
    results = state.library_tracks

    for token in tokens:
        if token.lower().startswith("artist:"):
            val = token.split(":", 1)[1].lower().replace("_", " ")
            results = [t for t in results if val in (t.artist or "").lower()]

        elif token.lower().startswith("duration>"):
            val_str = token.split(">", 1)[1]
            limit = time_utils.parse_timecode(val_str)
            results = [t for t in results if (t.duration_seconds or 0) > limit]

        elif token.lower().startswith("duration<"):
            val_str = token.split("<", 1)[1]
            limit = time_utils.parse_timecode(val_str)
            results = [t for t in results if (t.duration_seconds or 0) < limit]

        else:
            val = token.lower()
            results = [t for t in results if val in t.title.lower() or val in (t.artist or "").lower()]

        if not results:
            print("[search] No matches found.")
        else:
            print(f"[search] Found {len(results)} matches:")
            for i, t in enumerate(results[:10]):
                print(f"  {i + 1}. {t.display_name} ({time_utils.format_mm_ss(t.duration_seconds)})")


# S4-12: Song Ratings

def rate_song(state: PlayerState, rating_str: str) -> None:
    """
    Assigns a rating (1-5) to the currently playing song.
    """
    pass


def view_rated(state: PlayerState) -> None:
    """
    Displays all rated songs sorted by rating (highest first).
    """
    pass