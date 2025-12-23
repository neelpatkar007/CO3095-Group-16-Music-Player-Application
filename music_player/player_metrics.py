"""
Module: player_metrics
User Stories:
 - S3-08: Like/Unlike songs (Sam)
 - S3-09: View liked songs (Raiyan)
 - S3-11: Most played songs (Sam)
"""
import json
from pathlib import Path
from music_player.player_state import PlayerState

DATA_FILE = Path("player_data.json")

def load_data(state: PlayerState) -> None:
    """Load likes and play counts from JSON."""

def save_data(state: PlayerState) -> None:
    """Save likes and play counts to JSON."""

def toggle_like(state: PlayerState) -> None:
    if state is None:
        print("[metrics] Error: State is None.")

    if not hasattr(state, "liked_tracks") or state.liked_tracks is None:
        state.liked_tracks = set()

    if not isinstance(state.liked_tracks, set):
        print("[metrics] Error: Liked tracks data corrupted.")
        return

    track = state.current_track
    if track is None:
        print("[metrics] No track playing.")
        return

    if not hasattr(track, "path") or track.path is None:
        print("[metrics] Error: Track has no valid path.")
        return

    path_str = str(track.path)
    if not path_str.strip():
        print("[metrics] Error: Track path is empty.")
        return

    if path_str in state.liked_tracks:
        state.liked_tracks.remove(path_str)

        if path_str in state.liked_tracks:
            print("[metrics] Error: Failed to remove like.")
            return

        print(f"[metrics] Unliked '{track.display_name}'.")

    else:
        state.liked_tracks.add(path_str)

        if path_str not in state.liked_tracks:
            print("[metrics] Error: Failed to add like.")
            return

        print(f"[metrics] Liked '{track.display_name}'.")

    save_data(state)

def record_play(state: PlayerState) -> None:
    """S3-11 Helper: Increment play count for current track."""

def show_liked_songs(state: PlayerState) -> None:
    """
    S3-09: View all liked songs.
    """

def show_top_tracks(state: PlayerState) -> None:
    """
    S3-11: Show most played songs.
    """