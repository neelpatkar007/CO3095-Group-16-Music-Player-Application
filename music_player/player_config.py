"""
Sprint 4 Module: Configuration & Insights
Stories:
 - S4-01: Remember Settings
 - S4-05: Custom Tags
 - S4-08: Playback Stats
"""
import json
from pathlib import Path
from music_player.player_state import PlayerState

CONFIG_FILE = Path("player_config.json")

# S4-01: Remember Settings

def save_settings(state: PlayerState) -> None:
    """
    Saves persistent config (Volume, Shuffle, Loop, Speed, Total Time)
    to player_config.json.
    """
    data = {
        "volume": state.volume,
        "shuffle": state.shuffle_active,
        "loop": state.loop_mode,
        "speed": state.playback_speed,
        "tags": state.song_tags,
        "total_time": state.total_play_time
    }
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=2)
        print("[config] Settings saved.")
    except Exception as e:
        print(f"[config] Error saving settings: {e}")

def load_settings(state: PlayerState) -> None:
    """
    Loads config from disk and applies it to the PlayerState and AudioEngine.
    """
    if not CONFIG_FILE.exists():
        return
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            state.volume = data.get("volume", 100)
            state.shuffle_active = data.get("shuffle", False)
            state.loop_mode = data.get("loop", "off")
            state.playback_speed = data.get("speed", 1.0)
            state.song_tags = data.get("tags", {})
            state.total_play_time = data.get("total_time", 0.0)

            state.audio_engine.set_volume(state.volume)
            print("[config] Settings loaded.")
    except Exception as e:
        print(f"[config] Error loading settings: {e}")

# S4-05: Tags

def add_tag(state: PlayerState, index_str: str, tag: str) -> None:
    """
    Adds a custom tag to a specific song by index.
    """
    pass

def list_all_tags(state: PlayerState) -> None:
    """
    Prints all tags currently existing in the library.
    """
    pass

def filter_by_tag(state: PlayerState, tag: str) -> None:
    """
    Creates a temporary playlist queue containing only songs with the specified tag.
    """
    pass

# S4-08: Playback Statistics

def view_stats(state: PlayerState) -> None:
    """
    Calculates and displays:
    Total listening time (Hours/Minutes).
    Total number of songs played.
    Top 3 most played artists.
    """
    pass