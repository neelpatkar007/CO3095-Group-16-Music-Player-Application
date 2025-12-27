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


PROFILE_FILE = Path("profiles.json")


# S4-07: User Profiles

def load_profiles_index(state: PlayerState) -> None:
    if not PROFILE_FILE.exists():
        _save_profiles(state)
        return

    try:
        with open(PROFILE_FILE, "r") as f:
            data = json.load(f)
            state.active_profile = data.get("active", "default")
            state.profiles = data.get("profiles", {})
            print(f"[profile] Loaded profiles. Active: '{state.active_profile}'")

            # Apply the active profile data
            if state.active_profile in state.profiles:
                _apply_profile_data(state, state.profiles[state.active_profile])
            else:
                # If active is default but empty then save state
                if state.active_profile == "default":
                    _save_current_to_profile(state)

    except Exception as e:
        print(f"[profile] Error loading profiles: {e}")


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
    """
    Performs specific field searches on the library for artist and duration (artist:<name> and duration<=<>><seconds>.
    """
    pass


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