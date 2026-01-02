"""
Module: player_seek
User Stories:
 - S1-05: see the song progress and total time
 - S1-06: progress bar and jump to a specific time
 - S1-08: rewind or fast-forward by five seconds
"""
from __future__ import annotations # Importing annotations

from music_player.player_state import PlayerState
from music_player.time_utils import parse_timecode, format_mm_ss # Utility functions for time formatting
from music_player.library import Track

def get_progress(state: PlayerState) -> tuple[float, float | None]:
    '''
    Retrieve current position and total duration of the track.
    '''
    try:
        track = state.current_track
    except (AttributeError, TypeError):
        return 0.0, None

    if not isinstance(track, Track):
        pos = getattr(state, 'position_seconds', 0.0)
        return (pos if isinstance(pos, (int, float)) else 0.0), None

    return state.position_seconds, track.duration_seconds

def render_progress_bar(state: PlayerState, width: int = 15) -> str:
    """
    Generates a progress bar represents current progress for the track as a % visualised.
    Example   output: ██████░░░░░░░ 40%
    """
    if state is None:
        return "[ui error]"

    if not isinstance(width, int):
        return "[ui error]"

    if width <= 0:
        return "[ui error]"

    pos, total = get_progress(state)

    if total is None:
        return "[Time null]"

    if not isinstance(total, (int, float)):
        return "[Time error]"

    if total <= 0:
        return "[Time zero]"

    if pos is None:
        pos = 0.0

    if not isinstance(pos, (int, float)):
        pos = 0.0

    if pos < 0:
        pos = 0.0

    ratio = pos / total
    final_ratio = min(1.0, max(0.0, ratio))

    filledCount = int(final_ratio * width)
    emptyCount = width - filledCount

    bar = ("█" * filledCount) + ("░" * emptyCount)
    percentage = int(final_ratio * 100)

    return f"{bar} {percentage:3d}%"

# Function to nudge the current position by an offset in seconds
def nudge(state: PlayerState, offset_seconds: float) -> None:
    '''
    Move forward/backward by offset seconds.
    Use for /ff and /rw commands.
    '''
    if state is None:
        return

    current_pos = getattr(state, 'position_seconds', 0.0)
    if not isinstance(current_pos, (int, float)):
        current_pos = 0.0

    # Calculate new position
    new_pos = current_pos + offset_seconds

    # Seek to the new position
    seek_to(state, new_pos)

# Function to seek to a specific time in the track
def seek_to(state: PlayerState, text_or_seconds) -> None:
    """
    Seek to a specific time in the track.
    """
    if state is None:
        return
    try:
        track = state.current_track
    except (AttributeError, TypeError):
        print("[seek] Error accessing track state.")
        return

    if not isinstance(track, Track):
        print("[seek] No track loaded.")
        return

    if not hasattr(track, "duration_seconds"):
        return

    duration = track.duration_seconds
    if duration is None:
        duration = 0.0

    new_pos = 0.0

    if isinstance(text_or_seconds, (int, float)):
        new_pos = float(text_or_seconds)
    elif isinstance(text_or_seconds, str):
        new_pos = parse_timecode(text_or_seconds)

    if hasattr(state, "audio_engine"):
        if hasattr(state.audio_engine, "seek"):
            final_pos = max(0.0, min(new_pos, duration))

            state.position_seconds = final_pos
            state.audio_engine.seek(final_pos)