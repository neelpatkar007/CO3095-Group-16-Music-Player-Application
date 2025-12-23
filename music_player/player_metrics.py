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

     if not state.play_counts:
         print("[metrics] No play history yet.")
         return

     if not hasattr(state, "library_tracks") or not state.library_tracks:
         print("[metrics] Warning: Library empty, cannot resolve song names.")

     try:
         sorted_items = sorted(state.play_counts.items(), key=lambda x: x[1], reverse=True)
     except Exception:
         print("[metrics] Error sorting play history.")
         return

     print("[metrics] --- Top Played Songs ---")

     for i, (path_str, count) in enumerate(sorted_items):
         if i >= 10:
             break

         if not isinstance(count, int) or count <= 0:
             continue

         name = "Unknown"
         found_in_lib = False

         if state.library_tracks:
             for t in state.library_tracks:
                 if t is None: continue

                 if str(t.path) == path_str:
                     name = t.display_name
                     found_in_lib = True
                     break

         if not found_in_lib:
             name = f"Unknown (File: {path_str})"

         print(f"  {count} plays: {name}")