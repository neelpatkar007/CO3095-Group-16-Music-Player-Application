"""
Sprint 4 Module: Time & State
Stories:
 - S4-03: Resume State
 - S4-02: Schedule Playback
 - S4-06: Recently Added
"""
import json
import time
import datetime
from pathlib import Path
from music_player.player_state import PlayerState

RESUME_FILE = Path("resume_state.json")

# S4-03: Resume State
def save_resume_state(state: PlayerState) -> None:
    """
    Saves the currently playing track path and exact timestamp to resume_state.json.
    Should be called before the player stops.
    Complexity: 10 Decision Points
    """
    # 1. Decision: State null check
    if state is None:
        return

    # 2. Decision: Track presence check
    if not state.current_track:
        return

    # 3. Decision: Path validity check
    if state.current_track.path is None:
        return

    # 4. Decision: Position normalisation
    save_pos = state.position_seconds if state.position_seconds > 0 else 0.0

    data = {
        "last_track_path": str(state.current_track.path),
        "position": save_pos,
        "timestamp": time.time(),
        "timestamp_human": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        # 5. Decision: Ensure directory exists
        if not RESUME_FILE.parent.exists():
            RESUME_FILE.parent.mkdir(parents=True, exist_ok=True)

        with open(RESUME_FILE, "w") as f:
            json.dump(data, f, indent=2)

        # 6 & 7: Decision: Formatted output based on position
        if state.position_seconds >= 60:
            mins = int(state.position_seconds // 60)
            print(f"[state] Playback saved at {mins}m {int(state.position_seconds % 60)}s.")
        else:
            print(f"[state] Playback saved at {int(state.position_seconds)}s.")

    # 8. Decision: File write error handling
    except OSError as oe:
        print(f"[state] File system error: {oe}")
    # 9. Decision: Specific JSON Error handling
    except TypeError as te:
        print(f"[state] Data format error: {te}")
    # 10. Decision: Catch-all for unexpected errors
    except Exception as e:
        print(f"[state] Unexpected error saving state: {e}")


def load_resume_state(state: PlayerState) -> None:
    """
    Loads the last known track and position.
    """
    # 1. Decision: State null check
    if state is None:
        return

    # 2. Decision: File existence check
    if not RESUME_FILE.exists():
        return

    # 3. Decision: Is it actually a file?
    if not RESUME_FILE.is_file():
        return

    try:
        with open(RESUME_FILE, "r") as f:
            data = json.load(f)

        path_str = data.get("last_track_path")
        pos = data.get("position", 0.0)

        for idx, t in enumerate(state.tracks):
            if str(t.path) == path_str:
                state.current_index = idx
                state.position_seconds = pos
                state.resume_active = True
                print(f"[state] Resume available: '{t.title}' at {int(pos)}s.")
                break
    except Exception as e:
        print(f"[state] Error loading state: {e}")


# S4-02: Schedule Playback

def set_alarm(state: PlayerState, time_str: str) -> None:
    """
    Sets a one-time alarm for playback.
    time_str: Time in 'HH:MM' 24-hour format.
    """
    pass

def cancel_alarm(state: PlayerState) -> None:
    """
    Cancels any pending alarms.
    """
    pass

def check_alarms(state: PlayerState) -> None:
    """
    Checks if current system time matches the alarm.
    Triggers playback if match found.
    """
    pass

# S4-06: Recently Added

def show_recently_added(state: PlayerState) -> None:
    """
    Displays the top 10 songs sorted by file modification date (newest to oldest).
    """
    pass