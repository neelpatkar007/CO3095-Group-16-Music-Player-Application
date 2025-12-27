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

# Helpers

def _serialize_current_state(state: PlayerState) -> dict:
    pl_data = []
    for pl in state.playlists:
        pl_data.append({
            "name": pl.name,
            "tracks": [str(t.path) for t in pl.tracks]
        })
        return {
            "liked": list(state.liked_tracks),
            "ratings": state.song_ratings,
            "playlists": pl_data
        }

def _apply_profile_data(state: PlayerState, data: dict):
    state.liked_tracks = set(data.get("liked", []))
    state.song_ratings = data.get("ratings", {})

    restored_pl = []
    for p_dict in data.get("playlists", []):
        pl_name = p_dict.get("name", "Unknown")
        new_pl = Playlist(pl_name)

        for path_str in p_dict.get("tracks", []):
            for t in state.library_tracks:
                if str(t.path) == path_str:
                    new_pl.tracks.append(t)
                    break
        restored_pl.append(new_pl)

    state.playlists = restored_pl


def _save_profiles(state: PlayerState):
    """Helper: Persists the entire profiles index to profiles.json."""
    pass


def _save_current_to_profile(state: PlayerState):
    """Helper: Snapshots current active state into the profiles dictionary."""
    pass


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
    print("--- User Profiles ---")
    all_profiles = set(state.profiles.keys())
    all_profiles.add("default")

    for name in sorted(all_profiles):
        marker = " (Active)" if state.active_profile == name else ""
        print(f"  - {name}{marker}")

def show_current_profile(state: PlayerState) -> None:
    print(f"[profile] Current Profile: {state.active_profile}")


def create_profile(state: PlayerState, name: str) -> None:
    if not name:
        print("[profile] Error: Name cannot be empty.")
        return

    if name == "default":
        print("[profile] 'default' is reserved.")
        return

    if len(name) < 3:
        print("[profile] Error: Name must be at least 3 characters.")
        return

    if len(name) > 15:
        print("[profile] Error: Name must be under 15 characters.")
        return

    if name[0].isdigit():
        print("[profile] Error: Name cannot start with a number.")
        return

    if " " in name:
        print("[profile] Error: Names cannot contain spaces.")
        return

    if len(state.profiles) >= 8:
        print("[profile] Error: Maximum number of profiles (8) reached.")
        return

    if name in state.profiles:
        print(f"[profile] Profile '{name}' already exists.")
        return

    state.profiles[name] = {
        "liked": [],
        "ratings": {},
        "playlists": []
    }
    print(f"[profile] Created profile '{name}'.")
    _save_profiles(state)


def switch_profile(state: PlayerState, name: str) -> None:
    if name not in state.profiles and name != "default":
        print(f"[profile] Profile '{name}' does not exist.")
        return

    if name == state.active_profile:
        print(f"[profile] Already on '{name}'.")
        return


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