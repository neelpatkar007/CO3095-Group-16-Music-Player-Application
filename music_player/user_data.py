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
    # Collect all playlists
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

def _save_profiles(state: PlayerState):
    """Persist all profiles to JSON."""
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
    serialized = _serialize_current_state(state)
    if serialized:
        state.profiles[state.active_profile] = serialized
        _save_profiles(state)

def _apply_profile_data(state: PlayerState, data: dict):
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

        for path_str in p_dict.get("tracks", []):
            for t in state.library_tracks:
                if str(t.path) == path_str:
                    new_pl.tracks.append(t)
                    break
        restored_pl.append(new_pl)

    state.playlists = restored_pl


# S4-07: User Profiles

def load_profiles_index(state: PlayerState) -> None:
    """Loads profile metadata on startup."""
    if not PROFILE_FILE.exists():
        _save_profiles(state)
        return

    try:
        with open(PROFILE_FILE, "r") as f:
            data = json.load(f)
            state.active_profile = data.get("active", "default")
            state.profiles = data.get("profiles", {})
            print(f"[profile] Profiles loaded. Active: '{state.active_profile}'")

            # Apply the active profile data
            if state.active_profile in state.profiles:
                _apply_profile_data(state, state.profiles[state.active_profile])
            else:
                # If active is default but empty then save state
                if state.active_profile == "default":
                    _save_current_to_profile(state)

    except Exception as e:
        print(f"[profile] Error loading profiles: {e}")

def create_profile(state: PlayerState, name: str) -> None:
    if not name:
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
    print("--- User Profiles ---")
    all_profiles = set(state.profiles.keys())
    all_profiles.add("default")

    for name in sorted(all_profiles):
        marker = " (Active)" if state.active_profile == name else ""
        print(f"  - {name}{marker}")

def show_current_profile(state: PlayerState) -> None:
    print(f"[profile] Current Profile: {state.active_profile}")


# S4-09: Advanced Search

def advanced_search(state: PlayerState, query_str: str) -> None:
    if not query_str:
        print("[search] Usage: /advanced.search <query>")
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
            print(f"  {i+1}. {t.display_name} ({time_utils.format_mm_ss(t.duration_seconds)})")

# S4-12: Rate Songs

def rate_song(state: PlayerState, rating_str: str) -> None:
    track = state.current_track
    if not track:
        print("[rate] No song playing.")
        return

    try:
        val = int(rating_str)
        if not (1 <= val <= 5): raise ValueError
    except ValueError:
        print("[rate] Rating must be a whole number 1-5.")
        return

    path_str = str(track.path)
    state.song_ratings[path_str] = val
    print(f"[rate] Rated '{track.title}' {val}/5 stars.")
    # Auto-save
    _save_current_to_profile(state)

def view_rated(state: PlayerState) -> None:
    if not state.song_ratings:
        print("[rate] No songs rated yet.")
        return

    print("--- Rated Songs ---")
    sorted_paths = sorted(state.song_ratings.items(), key=lambda x: x[1], reverse=True)

    for path_str, rating in sorted_paths:
        name = "Unknown File"
        for t in state.library_tracks:
            if str(t.path) == path_str:
                name = t.display_name
                break
        print(f"  {'★' * rating} ({rating}) - {name}")