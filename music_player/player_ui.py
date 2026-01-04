"""
Module: player_ui
User Stories:
 - S1-03: see current song title, artist and duration
 - S1-05: see song progress and total time
 - S1-06: see a progress bar
 - S1-10: indicator showing which song is playing in a list
"""
from __future__ import annotations

from typing import Any

from music_player.player_state import PlayerState
from music_player.player_seek import render_progress_bar, get_progress
from music_player.time_utils import format_mm_ss
from music_player.library import Track


def _ensure_player_state(state: Any, context: str) -> PlayerState | None:
    """
    Internal helper - validate that `state` is a PlayerState object.
    Protects against unexpected inputs and provides clear warnings if a
    module attempts to pass something else - invalid data
    """
    if not isinstance(state, PlayerState):
        print(f"[ui] Invalid player state for {context}.")
        return None
    return state

#S1-05: Print_now_playing function that meets code complexity requirement
def print_now_playing(state: PlayerState) -> None:
    """
    Print the current title, artist, track status and total duration.
    """
    state = _ensure_player_state(state, "now_playing")
    if state is None:
        return

    track = state.current_track

    if track is None:
        print("[ui] No track selected.")
        return

    if not isinstance(track, Track):
        print("[ui] Error: Track data corrupted.")
        return

    if not hasattr(track, "display_name"):
        print("[ui] Error: Track metadata missing.")
        return

    if not hasattr(track, "duration_seconds"):
        duration = 0.0
    else:
        duration = track.duration_seconds

    if duration is None:
        duration = 0.0

    if duration < 0:
        duration = 0.0

    duration_str = format_mm_ss(duration)
    status = "Stopped"

    if state.is_playing:
        if state.is_paused:
            status = "Paused"
        else:
            status = "Playing"

    elif state.is_paused:
        status = "Paused"

    print(f"[ui] {status}: {track.display_name} [{duration_str}]")


def print_progress(state: PlayerState) -> None:
    """
    Prints the current position and the total time numerically (S1-05).
    """
    state = _ensure_player_state(state, "progress")
    if state is None:
        return

    # Get current position and total duration from the seek module
    pos, total = get_progress(state)

    # Format values before printing
    # Example output: [ui] Progress: 01:19/03:24
    print(f"[ui] Progress: {format_mm_ss(pos)}/{format_mm_ss(total)}")


def print_progress_bar(state: PlayerState) -> None:
    """
    Prints a textual progress bar for the current track (S1-06).
    """
    state = _ensure_player_state(state, "progress_bar")
    if state is None:
        return

    # Delegate complex rendering logic to player_seek module
    bar = render_progress_bar(state)

    # Example output: [ui] ███████░░░░░░░  47%
    print(f"[ui] {bar}")

#S1-10: Print_playlist_with_indicator function that meets code complexity requirement
def print_playlist_with_indicator(state: PlayerState) -> None:
    """
    Prints the entire track list with a symbol indicating  currently
    active track (S1-10).
    """
    state = _ensure_player_state(state, "playlist")
    if state is None:
        return

    tracks = state.library_tracks

    if not isinstance(tracks, list) or not all(
            isinstance(t, Track) for t in tracks
    ):
        print("[ui] Warning: Library is in an invalid state.")
        return

    if not tracks:
        print("[ui] Warning: Library is empty.")
        return

    # Metadata warning
    if any(not t.display_name for t in tracks):
        print("[ui] Warning: Some tracks have missing titles.")

    # Single-track warning
    if len(tracks) == 1:
        print("[ui] Note: Only one track in the library.")

    # Iterate and print Master Library
    for idx, track in enumerate(tracks):
        # Check if this specific track object is the one currently playing
        current = state.current_track

        if current and track == current:
            # Determine indicator marker based on playback status
            if state.is_playing:
                marker = "▶"  # Playing Indicator
            elif state.is_paused:
                marker = "‖"  # Paused Indicator
            else:
                marker = "•"  # Stopped Indicator
        else:
            marker = " "  # No Indicator

        print(f"{marker} {idx + 1:02d}: {track.display_name}")