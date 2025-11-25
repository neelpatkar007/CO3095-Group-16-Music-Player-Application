"""
Module: player_ui
User Stories:
 - S1-03: see current song title, artist and duration
 - S1-05: see song progress and total time
 - S1-06: see a progress bar
 - S1-10: indicator showing which song is playing in a list
"""

from player_state import PlayerState


def print_now_playing(state: PlayerState) -> None:
    """
    Print the current song title, artist and duration (S1-03).

    Backbone: Signature and docstring only.
    """
    pass


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
    Print the track list with an indicator showing the currently
    active track (S1-10).
    """
    if not state.tracks:
        print("[ui] Warning: Library is empty.")
        return

    # Clamp current_index to a valid range
    if state.current_index < 0:
        state.current_index = 0
    elif state.current_index >= len(state.tracks):
        state.current_index = len(state.tracks) - 1

    # Metadata warning
    if any(not t.display_name for t in state.tracks):
        print("[ui] Warning: Some tracks have missing titles.")

    # Single-track warning
    if len(state.tracks) == 1:
        print("[ui] Note: Only one track in the library.")

    for idx, track in enumerate(state.tracks):
        # Determine marker for the active track
        if idx == state.current_index:
            if state.is_playing:
                marker = "▶"
            elif state.is_paused:
                marker = "‖"
            else:
                marker = "•"
        else:
            marker = " "

        print(f"{marker} {idx + 1:02d}: {track.display_name}")