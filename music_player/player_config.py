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
            vol = data.get("volume", 100)
            if isinstance(vol, int):
                if 0 <= vol <= 100:
                    state.volume = vol
                else:
                    print(f"[config] Warning: Volume {vol} out of range. Resetting to 100.")
                    state.volume = 100
            else:
                print("[config] Warning: Invalid volume type. Resetting to 100.")
                state.volume = 100
            shuff = data.get("shuffle", False)
            if isinstance(shuff, bool):
                state.shuffle_active = shuff
            else:
                print("[config] Warning: Invalid shuffle type. Resetting to False.")
                state.shuffle_active = False
            loop = data.get("loop", "off")
            if isinstance(loop, str):
                if loop.lower() in ["off", "one", "all"]:
                    state.loop_mode = loop.lower()
                else:
                    print(f"[config] Warning: Unknown loop mode '{loop}'. Resetting to 'all'.")
                    state.loop_mode = "all"
            else:
                state.loop_mode = "off"
            speed = data.get("speed", 1.0)
            if isinstance(speed, (float, int)):
                if 0.5 <= speed <= 2.0:
                    state.playback_speed = float(speed)
                else:
                    print(f"[config] Warning: Speed {speed} out of bounds. Resetting to 1.0.")
                    state.playback_speed = 1.0
            else:
                state.playback_speed = 1.0
            tags = data.get("tags", {})
            if isinstance(tags, dict):
                state.song_tags = tags
            else:
                print("[config] Warning: Corrupted tags data. Resetting.")
                state.song_tags = {}
            t_time = data.get("total_time", 0.0)
            if isinstance(t_time, (float, int)):
                if t_time >= 0:
                    state.total_play_time = float(t_time)
                else:
                    state.total_play_time = 0.0
            else:
                state.total_play_time = 0.0
            state.audio_engine.set_volume(state.volume)
            print("[config] Settings loaded.")
    except Exception as e:
        print(f"[config] Error loading settings: {e}")

# S4-05: Tags

def add_tag(state: PlayerState, index_str: str, tag: str) -> None:
    """
    Adds a custom tag to a specific song by index.
    """
    try:
        idx = int(index_str) - 1
    except ValueError:
        print("[tags] Error: Invalid number format.")
        return
    if idx < 0 or idx >= len(state.library_tracks):
        print("[tags] Error: Song index out of range.")
        return
    track = state.library_tracks[idx]
    path_str = str(track.path)

    clean_tag = tag.strip().lstrip("#")

    if not clean_tag:
        print("[tags] Error: Tag cannot be empty.")
        return

    if len(clean_tag) > 15:
        print("[tags] Error: Tag is too long (max 15 chars).")
        return

    valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
    for char in clean_tag:
        if char not in valid_chars:
            print(f"[tags] Error: Invalid character '{char}'. Use A-Z, 0-9, _ only.")
            return

    current_tags = state.song_tags.get(path_str, [])
    if len(current_tags) >= 5:
        print(f"[tags] Error: Song '{track.title}' has reached the limit of 5 tags.")
        return

    if path_str not in state.song_tags:
        state.song_tags[path_str] = []

    tag = tag.strip().lstrip("#")
    if tag not in state.song_tags[path_str]:
        state.song_tags[path_str].append(tag)
        print(f"[tags] Added #{tag} to '{track.title}'.")
    else:
        print(f"[tags] Song already has tag #{tag}.")

def list_all_tags(state: PlayerState) -> None:
    """
    Prints all tags currently existing in the library.
    """
    unique_tags = set()
    for tags in state.song_tags.values():
        unique_tags.update(tags)

    if not unique_tags:
        print("[tags] No tags created yet.")
        return

    print("--- Custom Tags ---")
    for t in sorted(unique_tags):
        count = sum(1 for tags in state.song_tags.values() if t in tags)
        print(f"  #{t} ({count} songs)")

def filter_by_tag(state: PlayerState, tag: str) -> None:
    """
    Creates a temporary playlist queue containing only songs with the specified tag.
    """
    tag = tag.strip().lstrip("#")
    matches = []
    for path_str, tags in state.song_tags.items():
        if tag in tags:
            for t in state.library_tracks:
                if str(t.path) == path_str:
                    matches.append(t)
                    break
    if not matches:
        print(f"[tags] No songs found with #{tag}.")
        return
    print(f"[tags] Queue updated! Ready to play {len(matches)} songs tagged #{tag}:")
    for t in matches:
        print(f"  - {t.display_name}")

    # Update Queue Logic
    state.tracks = matches
    state.current_index = 0

# S4-08: Playback Statistics

def view_stats(state: PlayerState) -> None:
    """
    Calculates and displays:
    Total listening time (Hours/Minutes).
    Total number of songs played.
    Top 3 most played artists.
    """
    total_sec = int(state.total_play_time)
    hours = total_sec // 3600
    mins = (total_sec % 3600) // 60

    print("--- Playback Statistics ---")
    print(f"Total Listening Time: {hours}h {mins}m")
    print(f"Total Songs Played: {sum(state.play_counts.values())}")

    artist_counts = {}
    for path_str, count in state.play_counts.items():
        for t in state.library_tracks:
            if str(t.path) == path_str:
                art = t.artist or "Unknown"
                artist_counts[art] = artist_counts.get(art, 0) + count
                break

    print("\nTop Artists:")
    if not artist_counts:
        print("  (No data yet)")