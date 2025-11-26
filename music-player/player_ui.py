"""
Module: player_ui
User Stories:
 - S1-03: see current song title, artist and duration
 - S1-05: see song progress and total time
 - S1-06: see a progress bar
 - S1-10: indicator showing which song is playing in a list
"""

from player_state import PlayerState
from time_utils import format_mm_ss


def print_now_playing(state: PlayerState) -> None:
    """
    Print the current song title, artist and duration (S1-03).
    """
    track = state.current_track
    if track is None:
        print("[ui] No track selected.")
        return

    duration_str = format_mm_ss(track.duration_seconds)

    if state.is_playing:
        status = "Playing"
    elif state.is_paused:
        status = "Paused"
    else:
        status = "Stopped"

    print(f"[ui] {status}: {track.display_name} [{duration_str}]")


def print_progress(state: PlayerState) -> None:
    """
    Print the current progress and total time of the song (S1-05).

    Will use functions from player_seek.
    """
    pass


def print_progress_bar(state: PlayerState) -> None:
    """
    Print a textual progress bar for the current track (S1-06).
    """
    pass


def print_playlist_with_indicator(state: PlayerState) -> None:
    """
    Print the track list with an indicator (e.g. '▶') showing which
    song is currently playing (S1-10).
    """
    pass
