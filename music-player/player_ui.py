"""
Module: player_ui
User Stories:
 - S1-03: see current song title, artist and duration
 - S1-05: see song progress and total time
 - S1-06: see a progress bar
 - S1-10: indicator showing which song is playing in a list
"""
from __future__ import annotations

from player_state import PlayerState
from player_seek import get_progress
from time_utils import format_mm_ss


def print_now_playing(state: PlayerState) -> None:
    """
    Print the current song title, artist and duration (S1-03).

    Backbone: Signature and docstring only.
    """
    pass


def print_progress(state: PlayerState) -> None:
    pos, total = get_progress(state)
    print(f"[ui] Progress: {format_mm_ss(pos)}/{format_mm_ss(total)}")


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
