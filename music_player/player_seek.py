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
    '''
    Generates a visual progress bar for the current track.
    '''
    pos, total = get_progress(state)

    # Cannot render progress bar if total duration is unknown or invalid
    if total is None or not isinstance(total, (int, float)) or total <= 0:
        return "[Time null]"
    if not isinstance(pos, (int, float)):
        pos = 0.0
    # Calculate fill ratio
    ratio = max(0.0,min(1.0,pos/total))

    # Calculate character counts for filled and empty parts
    filledCount = int(ratio * width)
    emptyCount = width - filledCount

    # Build the progress bar string
    bar = ("█" * filledCount) + ("░"  * emptyCount)
    percentage = int(ratio * 100)

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
    '''
    Seek to a specific time in the track.
    Can accept a number or a timecode string (mm:ss).
    '''
    if state is None:
        return
    try:
        track = state.current_track
    except (AttributeError, TypeError):
        print("[seek] Error accessing track state.")
        return

    # Validate that a track is loaded
    if not isinstance(track, Track):
        print("[seek] No track loaded.")
        return

    # Determine if it's already a number
    if isinstance(text_or_seconds, (int, float)):
        new_pos = float(text_or_seconds)
    else:
        # Use timeutils to parse the timecode string
        new_pos = parse_timecode(str(text_or_seconds))

    # Bound check
    if track.duration_seconds is not None and isinstance(track.duration_seconds, (int, float)):
        # Ensure new position is within track duration
        new_pos = max(0.0, min(new_pos, track.duration_seconds))

    # Audio seek
    state.position_seconds = new_pos

    # Tell audio engine backend to jump to new position
    if hasattr(state, 'audio_engine') and hasattr(state.audio_engine, 'seek'):
        state.audio_engine.seek(new_pos)