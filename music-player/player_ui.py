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
    Print the track list with an indicator (e.g. '▶') showing which
    song is currently playing (S1-10).
    """
    if not state.tracks:
        print("[ui] Warning: Library is empty.")
        return
    # Clamp current_index to valid bounds
    if state.current_index < 0:
        state.current_index = 0
    if state.current_index >= len(state.tracks):
        state.current_index = len(state.tracks) - 1

    # Warning for tracks with missing metadata
    if any(not t.display_name for t in state.tracks):
        print("[ui] Warning: Some tracks have missing titles.")

    # Warning for if the playlist has only one track
    if len(state.tracks) == 1:
        print("[ui] Note: Only one track in the library.")

    for idx, track in enumerate(state.tracks):
        # Select indicator for the active track
        if idx == state.current_index and state.is_playing:
            marker = "▶"
        elif idx == state.current_index and state.is_paused:
            marker = "‖"
        elif idx == state.current_index:
            marker = "•"
        else:
            marker = " "
        # Print the track with its indicator
        print(f"{marker} {idx + 1:02d}: {track.display_name}")