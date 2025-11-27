"""
Module: player_seek
User Stories:
 - S1-05: see the song progress and total time
 - S1-06: progress bar and jump to a specific time
 - S1-08: rewind or fast-forward by five seconds
"""
from __future__ import annotations # Importing annotations

from time_utils import format_mm_ss, parse_timecode
from player_state import PlayerState
from time_utils import parse_timecode, format_mm_ss # Import time utilities


def get_progress(state: PlayerState) -> tuple[float, float | None]:

    track = state.current_track
    total = track.duration_seconds if track else None
    return state.position_seconds, total


def render_progress_bar(state: PlayerState, width: int = 15) -> str:


    pos, total = get_progress(state)
    if total is None or total <= 0 :
        return "[Time null]"

    ratio = max(0.0,min(1.0,pos/total))
    filledCount = int(ratio * width)
    emptyCount = width - filledCount
    bar = ("█" * filledCount) + ("░"  * emptyCount)
    percentage = int(ratio * 100)
    return f"{bar} {percentage:3d}%"


def seek_to(state: PlayerState, timecode: str) -> None:

    track = state.current_track
    if not track:
        print("[seek] No track selected.")
        return

    try:
        target = parse_timecode(timecode)
    except ValueError:
        print("[seek] Invalid time format. Use mm:ss or seconds.")
        return

    max_duration = track.duration_seconds if track.duration_seconds is not None else float('inf')

    target = max(0.0, min(max_duration, target))

    state.position_seconds = target
    print(f"[seek] New position: {format_mm_ss(state.position_seconds)}")

    if state.is_playing:
        state.audio_engine.play(track.path, start_pos=state.position_seconds)

# Function to nudge the current position by an offset
def nudge(state: PlayerState, offset_seconds: float) -> None:
    # Move forward/backward by offset seconds.
    new_pos = state.position_seconds + offset
    seek_to(state, new_pos)

    
# Function to seek to a specific time in the track
def seek_to(state: PlayerState, text_or_seconds) -> None:
    track = state.current_track
    if track is None:
        print("[seek] No track loaded.")
        return

    # Determine if it's already a number
    if isinstance(text_or_seconds, (int, float)):
        new_pos = float(text_or_seconds)
    else:
        new_pos = parse_timecode(str(text_or_seconds))
    if track.duration_seconds is not None:
        new_pos = max(0.0, min(new_pos, track.duration_seconds))
    state.position_seconds = new_pos
    # Audio seek
    state.audio_engine.seek(new_pos)
    print(f"[seek] Jumped to {format_mm_ss(new_pos)}")
