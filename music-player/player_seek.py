"""
Module: player_seek
User Stories:
 - S1-05: see the song progress and total time
 - S1-06: progress bar and jump to a specific time
 - S1-08: rewind or fast-forward by five seconds
"""
from player_state import PlayerState


def get_progress(state: PlayerState) -> tuple[float, float | None]:
    track = state.current_track
    total = track.duration_seconds if track else None
    return state.position_seconds, total


def render_progress_bar(state: PlayerState) -> str:
    """
    Return textual progress bar for current track (S1-06).

    Example final format: '████░░ 40%'.
    """
    return ""


def seek_to(state: PlayerState, timecode: str) -> None:
    """
    Seek to a specific time given as 'mm:ss' or total seconds.

    S1-06: will clamp to valid range and preserve play/pause state.
    """
    pass


def nudge(state: PlayerState, offset_seconds: float) -> None:
    """
    Move current position by +5 or -5 seconds (S1-08).

    Will be clamped to track bounds.
    """
    pass
