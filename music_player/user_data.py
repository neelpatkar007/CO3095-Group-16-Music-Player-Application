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
    if state is None or not hasattr(state, "playlists"):
        return {}

    pl_data = []
    # Collect all playlists
    if state.playlists:
        for pl in state.playlists:
            if pl:
                pl_data.append({
                    "name": getattr(pl, "name", "Unknown"),
                    "tracks": [str(t.path) for t in pl.tracks if hasattr(t, "path")]
                })

    return {
        "liked": list(getattr(state, "liked_tracks", [])),
        "ratings": getattr(state, "song_ratings", {}),
        "playlists": pl_data
    }

def _save_profiles(state: PlayerState):
    """Persist all profiles to JSON."""
    if state is None or not hasattr(state, "profiles") or not hasattr(state, "active_profile"):
        return

    try:
        data = {
            "active": state.active_profile,
            "profiles": state.profiles
        }
        with open(PROFILE_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"[profile] Error saving: {e}")

def _save_current_to_profile(state: PlayerState):
    """Snapshot current state variables into the profiles dict storage."""
    if state is None or not hasattr(state, "profiles") or not hasattr(state, "active_profile"):
        return

    serialized = _serialize_current_state(state)
    if serialized:
        state.profiles[state.active_profile] = serialized
        _save_profiles(state)

def _apply_profile_data(state: PlayerState, data: dict):
    if state is None:
        return

    if not data:
        state.liked_tracks = set()
        state.song_ratings = {}
        state.playlists = []
        return

    state.liked_tracks = set(data.get("liked", []))
    state.song_ratings = data.get("ratings", {})

    restored_pl = []
    for p_dict in data.get("playlists", []):
        pl_name = p_dict.get("name", "Unknown")
        new_pl = Playlist(pl_name)

        # Ensure library_tracks exists before iterating
        lib_tracks = getattr(state, "library_tracks", []) or []

        for path_str in p_dict.get("tracks", []):
            for t in lib_tracks:
                if t and hasattr(t, "path") and str(t.path) == path_str:
                    new_pl.tracks.append(t)
                    break
        restored_pl.append(new_pl)

    state.playlists = restored_pl


# S4-07: User Profiles

import json


def load_profiles_index(state: PlayerState) -> None:
    """
    Loads profile metadata on startup.
    """
    if state is None:
        return

    if not PROFILE_FILE.exists():
        _save_profiles(state)
        return

    try:
        with open(PROFILE_FILE, "r") as f:
            data = json.load(f)

            if not isinstance(data, dict):
                data = {}

            if "active" in data:
                state.active_profile = data["active"]
            else:
                state.active_profile = "default"

            if "profiles" in data:
                state.profiles = data["profiles"]
            else:
                state.profiles = {}

            print(f"[profile] Profiles loaded. Active: '{state.active_profile}'")

            if state.active_profile in state.profiles:
                profile_data = state.profiles[state.active_profile]

                if profile_data is not None:
                    _apply_profile_data(state, profile_data)
            else:
                if state.active_profile == "default":
                    if "default" not in state.profiles:
                        _save_current_to_profile(state)

    except json.JSONDecodeError:
        print("[profile] Error: Profile file contains invalid JSON.")
    except Exception as e:
        print(f"[profile] Error loading profiles: {e}")

def create_profile(state: PlayerState, name: str) -> None:
    if state is None or not hasattr(state, "profiles"):
        print("[profile] Error: Invalid state.")
        return

    if not name or not isinstance(name, str):
        print("[profile] Error: Name cannot be empty.")
        return
    if name == "default":
        print("[profile] 'default' is reserved.")
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
    if state is None or not hasattr(state, "profiles") or not hasattr(state, "active_profile"):
        print("[profile] Error: Invalid state.")
        return

    if name not in state.profiles and name != "default":
        print(f"[profile] Profile '{name}' does not exist.")
        return

    if name == state.active_profile:
        print(f"[profile] Already on '{name}'.")
        return

    # Save old profile state
    _save_current_to_profile(state)

    # Clear State
    state.liked_tracks = set()
    state.song_ratings = {}
    state.playlists = []

    # Load new profile state
    state.active_profile = name
    if name in state.profiles:
        _apply_profile_data(state, state.profiles[name])

    print(f"[profile] Switched to profile '{name}'.")
    _save_profiles(state)

def list_profiles(state: PlayerState) -> None:
    if state is None or not hasattr(state, "profiles") or not hasattr(state, "active_profile"):
        return

    print("--- User Profiles ---")
    all_profiles = set(state.profiles.keys())
    all_profiles.add("default")

    for name in sorted(all_profiles):
        marker = " (Active)" if state.active_profile == name else ""
        print(f"  - {name}{marker}")

def show_current_profile(state: PlayerState) -> None:
    if state is None or not hasattr(state, "active_profile"):
        print("[profile] Error: Invalid state.")
        return
    print(f"[profile] Current Profile: {state.active_profile}")


# S4-09: Advanced Search

def advanced_search(state: PlayerState, query_str: str) -> None:
    if state is None or not hasattr(state, "library_tracks"):
        print("[search] Error: Invalid state.")
        return

    if not query_str or not isinstance(query_str, str):
        print("[search] Usage: /advanced.search <query>")
        return

    tokens = query_str.split()
    results = state.library_tracks

    if results is None:
        results = []

    for token in tokens:
        if token.lower().startswith("artist:"):
            val = token.split(":", 1)[1].lower().replace("_", " ")
            results = [t for t in results if t and val in (getattr(t, 'artist', '') or "").lower()]

        elif token.lower().startswith("duration>"):
            val_str = token.split(">", 1)[1]
            limit = time_utils.parse_timecode(val_str)
            results = [t for t in results if t and (getattr(t, 'duration_seconds', 0) or 0) > limit]

        elif token.lower().startswith("duration<"):
            val_str = token.split("<", 1)[1]
            limit = time_utils.parse_timecode(val_str)
            results = [t for t in results if t and (getattr(t, 'duration_seconds', 0) or 0) < limit]

        else:
            val = token.lower()
            results = [
                t for t in results
                if t and (val in (getattr(t, 'title', '') or "").lower() or val in (getattr(t, 'artist', '') or "").lower())
            ]

    if not results:
        print("[search] No matches found.")
    else:
        print(f"[search] Found {len(results)} matches:")
        for i, t in enumerate(results[:10]):
            name = getattr(t, 'display_name', 'Unknown') or 'Unknown'
            dur = time_utils.format_mm_ss(getattr(t, 'duration_seconds', 0) or 0)
            print(f"  {i+1}. {name} ({dur})")

# S4-12: Rate Songs

def rate_song(state: PlayerState, rating_str: str) -> None:
    if state is None or not hasattr(state, "current_track"):
        print("[rate] No song playing.")
        return

    track = state.current_track
    if not track:
        print("[rate] No song playing.")
        return

    try:
        val = int(rating_str)
        if not (1 <= val <= 5): raise ValueError
    except (ValueError, TypeError):
        print("[rate] Rating must be a whole number 1-5.")
        return

    if not hasattr(track, "path") or not hasattr(state, "song_ratings"):
        return

    path_str = str(track.path)
    if state.song_ratings is None:
        state.song_ratings = {}

    state.song_ratings[path_str] = val

    title = getattr(track, 'title', 'Unknown') or 'Unknown'
    print(f"[rate] Rated '{title}' {val}/5 stars.")
    # Auto-save
    _save_current_to_profile(state)

def view_rated(state: PlayerState) -> None:
    if state is None or not hasattr(state, "song_ratings") or state.song_ratings is None:
        print("[rate] No songs rated yet.")
        return

    if not state.song_ratings:
        print("[rate] No songs rated yet.")
        return

    print("--- Rated Songs ---")
    try:
        sorted_paths = sorted(state.song_ratings.items(), key=lambda x: x[1], reverse=True)
    except Exception:
        print("[rate] Error sorting ratings.")
        return

    # Check for library existence
    lib_tracks = getattr(state, "library_tracks", []) or []

    for path_str, rating in sorted_paths:
        try:
            val = int(rating)
        except (ValueError, TypeError):
            continue

        name = "Unknown File"
        for t in lib_tracks:
            if t and hasattr(t, "path") and str(t.path) == path_str:
                name = getattr(t, "display_name", "Unknown")
                break
        print(f"  {'★' * val} ({val}) - {name}")