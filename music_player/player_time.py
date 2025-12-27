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
from music_player import player_core

RESUME_FILE = Path("resume_state.json")

# S4-03: Resume State
def save_resume_state(state: PlayerState) -> None:
    """
    Saves the currently playing track path and exact timestamp to resume_state.json.
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

    try:
        # 3. Decision: Is it actually a file?
        if not RESUME_FILE.is_file():
            return

        with open(RESUME_FILE, "r") as f:
            data = json.load(f)

        # 4. Decision: Validate dictionary structure
        if not isinstance(data, dict):
            return

        path_str = data.get("last_track_path")
        pos = data.get("position", 0.0)

        # 5. Decision: Ensure path exists and track list is not empty
        if not path_str or not state.tracks:
            return

        match_found = False
        for idx, t in enumerate(state.tracks):  # 6. Decision: Loop
            # 7. Decision: String comparison for path
            if str(t.path) == path_str:
                state.current_index = idx
                state.position_seconds = pos if pos > 0 else 0.0  # 8. Decision: Ternary
                state.resume_active = True
                match_found = True
                print(f"[state] Resume available: '{t.title}' at {int(pos)}s.")
                break

        # 9. Decision: Check if no match was found in library
        if not match_found:
            print("[state] Saved track no longer found in library.")

    # 10. Decision: JSON decode error handling
    except json.JSONDecodeError:
        print("[state] Corrupt resume file.")
    except Exception as e:
        print(f"[state] Error loading state: {e}")


# --- S4-02: Schedule Playback ---

def set_alarm(state: PlayerState, time_str: str) -> None:
    """Only allow ONE alarm at a time."""
    # 1. Decision: State and string presence check
    if state is None or time_str is None:
        return

    # 2. Decision: Structural format check
    if len(time_str) != 5 or ":" not in time_str:
        print("[alarm] Invalid format. Use HH:MM (24-hour).")
        return

    parts = time_str.split(":")
    # 3. Decision: Exact part count and 4. Digit validation
    if len(parts) != 2 or not all(p.isdigit() for p in parts):
        print("[alarm] Invalid format. Use HH:MM (24-hour).")
        return

    h, m = int(parts[0]), int(parts[1])

    # 5. Decision: Hour floor and 6. Hour ceiling check
    if h < 0 or h > 23:
        print("[alarm] Invalid format. Use HH:MM (24-hour).")
        return

    # 7. Decision: Minute floor and 8. Minute ceiling check
    if m < 0 or m > 59:
        print("[alarm] Invalid format. Use HH:MM (24-hour).")
        return

    try:
        # 9. Decision: Library level format safety validation
        datetime.datetime.strptime(time_str, "%H:%M")

        # 10. Decision: State list type verification for persistence
        if isinstance(state.scheduled_alarms, list):
            state.scheduled_alarms = [time_str]
            print(f"[alarm] ⏰ Alarm set for {time_str}. (Previous alarms cleared)")

    except ValueError:
        # 11. Decision: Exception branch for invalid time values
        print("[alarm] Invalid format. Use HH:MM (24-hour).")

def cancel_alarm(state: PlayerState) -> None:
    # 1. Decision: State null check
    if state is None:
        return

    # 2. Decision: Attribute existence check
    if not hasattr(state, 'scheduled_alarms'):
        return

    # 3. Decision: Explicit None check OR 4. Type verification
    if state.scheduled_alarms is None or not isinstance(state.scheduled_alarms, list):
        print("[alarm] No alarms set.")
        return

    # 5. Decision: Check if list is empty
    if len(state.scheduled_alarms) == 0:
        print("[alarm] No alarms set.")
    else:
        # 6. Decision: Final safety check before clearing
        if state.scheduled_alarms is not None:
            state.scheduled_alarms.clear()
            print("[alarm] All alarms cancelled.")


def check_alarms(state: PlayerState) -> None:
    if not state.scheduled_alarms:
        return

    now = datetime.datetime.now().strftime("%H:%M")
    if now in state.scheduled_alarms:
        if not state.is_playing:
            print(f"\n[alarm] ⏰ It's {now}! Starting playback.")
            player_core.play(state)
            state.scheduled_alarms.remove(now)

# S4-06: Recently Added

def show_recently_added(state: PlayerState) -> None:
    """
    Displays the top 10 songs sorted by file modification date (newest to oldest).
    """
    pass