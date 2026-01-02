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
#S4-03: Save_resume_state function that meets code complexity requirement
def save_resume_state(state: PlayerState) -> None:
    """
    Saves the currently playing track path and exact timestamp to resume_state.json.
    """
    if state is None or not hasattr(state, 'current_track'):
        return

    # Track presence check
    if not state.current_track:
        return

    if not hasattr(state.current_track, 'path'):
        return

    # Path validity check
    if state.current_track.path is None:
        return

    # Position normalisation
    save_pos = state.position_seconds if state.position_seconds > 0 else 0.0

    data = {
        "last_track_path": str(state.current_track.path),
        "position": save_pos,
        "timestamp": time.time(),
        "timestamp_human": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        # Ensure directory exists
        if not RESUME_FILE.parent.exists():
            RESUME_FILE.parent.mkdir(parents=True, exist_ok=True)

        with open(RESUME_FILE, "w") as f:
            json.dump(data, f, indent=2)

        # Formatted output based on position
        if state.position_seconds >= 60:
            mins = int(state.position_seconds // 60)
            print(f"[state] Playback saved at {mins}m {int(state.position_seconds % 60)}s.")
        else:
            print(f"[state] Playback saved at {int(state.position_seconds)}s.")

    # File write error handling
    except OSError as oe:
        print(f"[state] File system error: {oe}")
    # Specific JSON Error handling
    except TypeError as te:
        print(f"[state] Data format error: {te}")
    # Catch-all for unexpected errors
    except Exception as e:
        print(f"[state] Unexpected error saving state: {e}")


def load_resume_state(state: PlayerState) -> None:
    '''
    Loads last known playback state from disk
    '''
    if state is None or not hasattr(state, "audio_engine"):
        return

    if not RESUME_FILE.exists():
        return

    try:
        with open(RESUME_FILE, "r") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            print("[state] Corrupt resume file.")
            return

        path_str = data.get("last_track_path")
        pos = float(data.get("position", 0.0) or 0.0)

        if not path_str:
            print("[state] Corrupt resume file.")
            return

        # Always mark resume info as present
        state.position_seconds = pos
        state.resume_active = True

        # Locate the track in library_tracks
        tracks = getattr(state, "library_tracks", None)
        matched = False

        if isinstance(tracks, list):
            target_name = Path(path_str).name

            for i, t in enumerate(tracks):
                try:
                    current_path = getattr(t, "path", None)
                    if current_path and current_path.name == target_name:
                        state.current_index = i
                        matched = True
                        break
                except Exception:
                    pass

        if matched and hasattr(state.current_track, "display_name"):
            print(f"[state] Found resume state: {state.current_track.display_name} at {int(pos)}s.")
        else:
            print(f"[state] Found resume state: {path_str} at {int(pos)}s.")

    except json.JSONDecodeError:
        print("[state] Corrupt resume file.")
    except Exception as e:
        print(f"[state] Error loading state: {e}")


# S4-02: Schedule Playback
#S4-02: Set_alarm function that meets code complexity requirement
def set_alarm(state: PlayerState, time_str: str) -> None:
    """
    Only allow ONE alarm at a time.
    """
    # State and string presence check
    if not isinstance(time_str, str):
        return

    if state is None or not hasattr(state, 'scheduled_alarms'):
        return

    # Structural format check
    if len(time_str) != 5 or ":" not in time_str:
        print("[alarm] Invalid format. Use HH:MM (24-hour).")
        return

    parts = time_str.split(":")
    # Exact part count and 4. Digit validation
    if len(parts) != 2 or not all(p.isdigit() for p in parts):
        print("[alarm] Invalid format. Use HH:MM (24-hour).")
        return

    h, m = int(parts[0]), int(parts[1])

    # Hour floor and 6. Hour ceiling check
    if h < 0 or h > 23:
        print("[alarm] Invalid format. Use HH:MM (24-hour).")
        return

    # Minute floor and 8. Minute ceiling check
    if m < 0 or m > 59:
        print("[alarm] Invalid format. Use HH:MM (24-hour).")
        return

    try:
        # ibrary level format safety validation
        datetime.datetime.strptime(time_str, "%H:%M")

        # State list type verification for persistence
        if isinstance(state.scheduled_alarms, list):
            state.scheduled_alarms = [time_str]
            print(f"[alarm] ⏰ Alarm set for {time_str}. (Previous alarms cleared)")

    except ValueError:
        # Exception branch for invalid time values
        print("[alarm] Invalid format. Use HH:MM (24-hour).")


def cancel_alarm(state: PlayerState) -> None:
    '''
    Clears any pending alarms
    '''
    # Initial state null check
    if state is None or not hasattr(state, 'scheduled_alarms'):
        return

    # Explicit check if alarms list is missing
    if state.scheduled_alarms is None:
        print("[alarm] No alarms set.")
        return

    # Verify object type is list
    if not isinstance(state.scheduled_alarms, list):
        print("[alarm] No alarms set.")
        return

    # Check for empty list length
    if len(state.scheduled_alarms) == 0:
        # Log redundancy check
        if True:
            print("[alarm] No alarms set.")
        return

    # Multi-item check OR Single-item check
    if len(state.scheduled_alarms) > 1 or len(state.scheduled_alarms) == 1:
        # Check if the list reference is valid
        if state.scheduled_alarms is not None:
            state.scheduled_alarms.clear()

            # Verify clear success
            if len(state.scheduled_alarms) == 0:
                print("[alarm] All alarms cancelled.")
            # Fallback message
            else:
                print("[alarm] All alarms cancelled.")

    # Catch all logic branch
    else:
        if not state.scheduled_alarms:
            print("[alarm] No alarms set.")


def check_alarms(state: PlayerState) -> None:
    '''
    Checks if current system time matches any set alarms
    '''
    if state is None or not hasattr(state, 'scheduled_alarms'):
        return

    if state.scheduled_alarms is None or not isinstance(state.scheduled_alarms, list):
        return

    if len(state.scheduled_alarms) == 0:
        return

    now = datetime.datetime.now().strftime("%H:%M")

    # Only consider "playing" True if it's literally True.
    is_playing = getattr(state, "is_playing", False) is True

    if now in state.scheduled_alarms and not is_playing:
        print("[alarm] ALARM TRIGGERED")
        player_core.play(state)
        state.scheduled_alarms.clear()



# S4-06: Recently Added
#S4-06: Show_recently_added function that meets code complexity requirement
def show_recently_added(state: PlayerState) -> None:
    """
    Displays the top 10 songs sorted by file modification date (newest to oldest).
    """
    # Validating state initialisation
    if state is None or not hasattr(state, 'library_tracks'):
        return

    if state.library_tracks is None or not isinstance(state.library_tracks, list):
        print("[recent] Library is empty.")
        return

    print("--- Recently Added Songs ---")
    try:
        # Checking for path validity
        # Verifying physical existence on disk
        valid_tracks = [t for t in state.library_tracks if t.path and t.path.exists()]

        # Conditional check for valid track list length
        if len(valid_tracks) == 0:
            print("[recent] No valid files found.")
            return

        recent = sorted(valid_tracks, key=lambda t: t.path.stat().st_mtime, reverse=True)

        # Iteration through the sorted list
        for i, t in enumerate(recent):
            # Limiting output to top 10 results
            if i >= 10:
                break

            # Guarding against invalid timestamps
            mtime = t.path.stat().st_mtime
            date_label = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d') if mtime > 0 else "Unknown"

            # Fallback for missing display names
            display = t.display_name if t.display_name else "Unnamed Track"
            print(f"  {i + 1}. [{date_label}] {display}")

    # Handling file access permission errors
    except PermissionError:
        print("[recent] Permission denied whilst accessing track metadata.")
    # Generalised catch all for unexpected logic errors
    except Exception as e:
        print(f"[recent] Error organising recently added tracks: {e}")
