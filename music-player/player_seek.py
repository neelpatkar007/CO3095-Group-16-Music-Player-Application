"""
Module: player_seek
User Stories:
 - S1-05: see the song progress and total time
 - S1-06: progress bar and jump to a specific time
 - S1-08: rewind or fast-forward by five seconds
"""

from time_utils import format_mm_ss, parse_timecode
from player_state import PlayerState


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


def nudge(state: PlayerState, offset_seconds: float) -> None:
    """
    Move current position by +5 or -5 seconds (S1-08).

    Will be clamped to track bounds.
    """
    pass
