"""
Sprint 4 Module: User Data & Discovery
Stories:
 - S4-07: User Profiles
 - S4-09: Advanced Search
 - S4-12: Rate Songs
"""
from music_player.player_state import PlayerState


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
    """
    Performs specific field searches on the library for artist and duration (artist:<name> and duration<=<>><seconds>.
    """
    pass


# S4-12: Song Ratings

def rate_song(state: PlayerState, rating_str: str) -> None:
    track = state.current_track
    if not track:
        print("[rate] No song playing.")
        return

    if not rating_str or not rating_str.strip():
        print("[rate] Error: Please provide a rating (e.g., /rate 5).")
        return

    clean_str = rating_str.strip()
    if "." in clean_str:
        print("[rate] Error: Decimals are not supported. Use whole numbers.")
        return

    if not clean_str.lstrip("-").isdigit():
        print("[rate] Error: Input must be a number.")
        return

    try:
        val = int(clean_str)
        if not (1 <= val <= 5): raise ValueError
    except ValueError:
        print("[rate] Rating must be a whole number 1-5.")
        return

    path_str = str(track.path)
    if path_str in state.song_ratings:
        old_rating = state.song_ratings[path_str]
        if old_rating == val:
            print(f"[rate] Song is already rated {val}/5. No change made.")
            return
        print(f"[rate] Updated rating from {old_rating} to {val}/5.")

    else:
        if val == 5:
            print(f"[rate] Rated '{track.title}' 5/5 stars! (A favourite!!)")
        else:
            print(f"[rate] Rated '{track.title}' {val}/5 stars.")

    state.song_ratings[path_str] = val
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