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
    """
    S3-08: Like or unlike the current song.
    """

def record_play(state: PlayerState) -> None:
    track = state.current_track
    if not track: return
    path_str = str(track.path)
    state.play_counts[path_str] = state.play_counts.get(path_str, 0) + 1
    save_data(state)

def show_liked_songs(state: PlayerState) -> None:
    """
    S3-09: View all liked songs.
    """

def show_top_tracks(state: PlayerState) -> None:
     if state is None:
        print("[metrics] Error: State is None.")
        return

     if not hasattr(state, "play_counts") or state.play_counts is None:
         print("[metrics] No play history data available.")
         return

     if not isinstance(state.play_counts, dict):
         print("[metrics] Error: Play counts corrupted.")
         return