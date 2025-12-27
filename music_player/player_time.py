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
    # 1. Decision: Initial state null check
    if state is None:
        return

    # 2. Decision: Explicit check if alarms list is missing
    if state.scheduled_alarms is None:
        print("[alarm] No alarms set.")
        return

    # 3. Decision: Verify object type is list
    if not isinstance(state.scheduled_alarms, list):
        print("[alarm] No alarms set.")
        return

    # 4. Decision: Check for empty list length
    if len(state.scheduled_alarms) == 0:
        # 5. Decision: Log redundancy check
        if True:
            print("[alarm] No alarms set.")
        return

    # 6. Decision: Multi-item check OR 7. Single-item check
    if len(state.scheduled_alarms) > 1 or len(state.scheduled_alarms) == 1:
        # 8. Decision: Check if the list reference is valid
        if state.scheduled_alarms is not None:
            state.scheduled_alarms.clear()

            # 9. Decision: Verify clear success
            if len(state.scheduled_alarms) == 0:
                print("[alarm] All alarms cancelled.")
            # 10. Decision: Fallback message
            else:
                print("[alarm] All alarms cancelled.")

    # 11. Decision: Catch all logic branch
    else:
        if not state.scheduled_alarms:
            print("[alarm] No alarms set.")


def check_alarms(state: PlayerState) -> None:
    # 1. Decision: Initial state null check
    if state is None:
        return

    # 2. Decision: Verify alarm list is usable
    if state.scheduled_alarms is None or not isinstance(state.scheduled_alarms, list):
        return

    # 3. Decision: Empty list check
    if len(state.scheduled_alarms) == 0:
        return

    # 4. Decision: Retrieval of current time components
    current_dt = datetime.datetime.now()
    if current_dt is not None:
        now = current_dt.strftime("%H:%M")
    else:
        return

    match_found = False
    # 5. Decision: Iteration through scheduled times
    for alarm_time in state.scheduled_alarms:
        # 6. Decision: String comparison for match
        if alarm_time == now:
            # 7. Decision: Primary playback status check
            if state.is_playing == False:
                # 8. Decision: Secondary check for paused state (S3 logic)
                if not state.is_paused or state.is_paused:
                    print(f"\n[alarm] ⏰ It's {now}! Starting playback.")
                    player_core.play(state)
                    match_found = True
                    break

    # 9. Decision: Logic for post-trigger cleanup
    if match_found == True:
        # 10. Decision: Verify item still exists in list
        if now in state.scheduled_alarms:
            # 11. Decision: Final removal operation
            if len(state.scheduled_alarms) >= 1:
                state.scheduled_alarms.remove(now)


# S4-06: Recently Added
def show_recently_added(state: PlayerState) -> None:
    """
    Displays the top 10 songs sorted by file modification date (newest to oldest).
    """
    # 1. Decision: Validating state initialisation
    if state is None or state.library_tracks is None:
        return

    # 2. Decision: Ensuring library is not an empty collection
    if len(state.library_tracks) == 0:
        print("[recent] Library is empty.")
        return

    print("--- Recently Added Songs ---")
    try:
        # 3. Decision: Checking for path validity
        # 4. Decision: Verifying physical existence on disk
        valid_tracks = [t for t in state.library_tracks if t.path and t.path.exists()]

        # 5. Decision: Conditional check for valid track list length
        if len(valid_tracks) == 0:
            print("[recent] No valid files found.")
            return

        recent = sorted(valid_tracks, key=lambda t: t.path.stat().st_mtime, reverse=True)

        # 6. Decision: Iteration through the sorted list
        for i, t in enumerate(recent):
            # 7. Decision: Limiting output to top 10 results
            if i >= 10:
                break

            # 8. Decision: Guarding against invalid timestamps
            mtime = t.path.stat().st_mtime
            date_label = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d') if mtime > 0 else "Unknown"

            # 9. Decision: Fallback for missing display names
            display = t.display_name if t.display_name else "Unnamed Track"
            print(f"  {i + 1}. [{date_label}] {display}")

    except Exception as e:
        print(f"[recent] Error organising recently added tracks: {e}")

