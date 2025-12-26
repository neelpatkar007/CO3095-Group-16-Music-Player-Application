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
    """
    # 1. Null check for state
    if state is None:
        return

    # 2. Check if a track is actually active
    if not state.current_track:
        return

    # 3. Validation check for track path
    if state.current_track.path is None:
        return

    data = {
        "last_track_path": str(state.current_track.path),
        "position": state.position_seconds,
        "timestamp": time.time(),
        "timestamp_human": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        with open(RESUME_FILE, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[state] Playback saved at {int(state.position_seconds)}s.")
    except Exception as e:
        print(f"[state] Error saving state: {e}")

def load_resume_state(state: PlayerState) -> None:
    """
    Loads the last known track and position.
    """
    if not RESUME_FILE.exists():
        return

    try:
        with open(RESUME_FILE, "r") as f:
            data = json.load(f)

        path_str = data.get("last_track_path")
        pos = data.get("position", 0.0)

        # Find the track index
        for idx, t in enumerate(state.tracks):
            if str(t.path) == path_str:
                state.current_index = idx
                state.position_seconds = pos
                state.resume_active = True # Signal for main.py
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