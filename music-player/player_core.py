"""
Module: player_core
Core playback operations.

User Stories:
 - S1-01: play, pause and stop songs
 - S1-12: keep player running in the background (non-blocking playback)
"""

from player_state import PlayerState


def play(state: PlayerState) -> None:
    """
    Start or resume playback from the current position.

    S1-01: user can start/resume a song.
    S1-12: this must not block the CLI; background updating will be
           handled via update_playback in the main loop.
    """
    pass


def pause(state: PlayerState) -> None:
    """
    Pause playback without resetting position.

    S1-01.
    """
    pass


def stop(state: PlayerState) -> None:
    """
    Stop playback and reset position to 0.

    S1-01.
    """
    pass


def update_playback(state: PlayerState, delta_seconds: float) -> None:
    """
    Advance the playback position based on elapsed time.

    Called periodically from the CLI loop so that playback continues
    while the user types commands (S1-12).

    """
    pass
