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
    if state is None:
        return
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

#S4-01: Load_settings function that meets code complexity requirement
def load_settings(state: PlayerState) -> None:
    """
    Loads config from disk and applies it to the PlayerState and AudioEngine.
    """
    if not CONFIG_FILE.exists():
        return
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)

            # Volume Validation
            # Check type AND range to prevent crashing the audio engine with bad values
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

            # Shuffle and Loop
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

            # Playback Speed
            # Speed must be a float between 0.5 and 2.0
            speed = data.get("speed", 1.0)
            if isinstance(speed, (float, int)):
                if 0.5 <= speed <= 2.0:
                    state.playback_speed = float(speed)
                else:
                    print(f"[config] Warning: Speed {speed} out of bounds. Resetting to 1.0.")
                    state.playback_speed = 1.0
            else:
                state.playback_speed = 1.0

            # Custom Tags
            tags = data.get("tags", {})
            if isinstance(tags, dict):
                state.song_tags = tags
            else:
                print("[config] Warning: Corrupted tags data. Resetting.")
                state.song_tags = {}

            # Total Play Time
            t_time = data.get("total_time", 0.0)
            if isinstance(t_time, (float, int)):
                if t_time >= 0:
                    state.total_play_time = float(t_time)
                else:
                    state.total_play_time = 0.0
            else:
                state.total_play_time = 0.0

            # Apply loaded volume to actual audio engine
            state.audio_engine.set_volume(state.volume)
            print("[config] Settings loaded.")
    except Exception as e:
        print(f"[config] Error loading settings: {e}")

# S4-05: Tags
#S4-05: Add_tag function that meets code complexity requirement
def add_tag(state: PlayerState, index_str: str, tag: str) -> None:
    """
    Adds a custom tag to a specific song by index.
    """
    if state is None:
        print("[tags] Error: State is None.")
        return
    try:
        if index_str is None:
            raise ValueError
        idx = int(index_str) - 1

    except (ValueError, TypeError):
        print("[tags] Error: Invalid number format.")
        return

    # Verify status integrity before proceeding
    if not hasattr(state, "song_tags") or not isinstance(state.song_tags, dict):
        print("[tags] Error: Tag data is unavailable/corrupted.")
        return
    if not hasattr(state, "library_tracks") or not isinstance(state.library_tracks, list):
        print("[tags] Error: Library tracks missing/corrupted.")
        return

    # Check the boundaries
    if idx < 0 or idx >= len(state.library_tracks):
        print("[tags] Error: Song index out of range.")
        return
    track = state.library_tracks[idx]
    if track is None:
        return

    # Use path as the unique key for storage
    path_str = str(track.path)

    if tag is None:
        print("[tags] Error: Tag cannot be empty.")
        return

    # Clean tag - remove whitespace and leading #
    clean_tag = tag.strip().lstrip("#")

    # Validation Rules
    # Max length is 15 characters
    if len(clean_tag) > 15:
        print("[tags] Error: Tag is too long (max 15 chars).")
        return
    # Only allow A-Z, 0-9, and _
    valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
    for char in clean_tag:
        if char not in valid_chars:
            print(f"[tags] Error: Invalid character '{char}'. Use A-Z, 0-9, _ only.")
            return

    # Max 5 tags per song
    current_tags = state.song_tags.get(path_str, [])
    if len(current_tags) >= 5:
        print(f"[tags] Error: Song '{track.title}' has reached the limit of 5 tags.")
        return

    # Initialise list if songs has no tags yet
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
    if state is None:
        print("[tags] Error: State is None.")
        return
    if not hasattr(state, "song_tags") or not isinstance(state.song_tags, dict):
        print("[tags] Error: Tag data is unavailable/corrupted.")
        return
    if not hasattr(state, "library_tracks") or not isinstance(state.library_tracks, list):
        print("[tags] Error: Library tracks missing/corrupted.")
        return
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
    if state is None:
        print("[tags] Error: State is None.")
        return
    if not hasattr(state, "song_tags") or not isinstance(state.song_tags, dict):
        print("[tags] Error: Tag data is unavailable/corrupted.")
        return
    if not hasattr(state, "library_tracks") or not isinstance(state.library_tracks, list):
        print("[tags] Error: Library tracks missing/corrupted.")
        return
    if tag is None:
        print("[tags] Error: Tag cannot be empty.")
        return
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
#S4-08: View_stats function that meets code complexity requirement
def view_stats(state: PlayerState) -> None:
    """
    Calculates and displays:
    Total listening time (Hours/Minutes).
    Total number of songs played.
    Top 3 most played artists.
    """
    if state is None:
        print("[stats] Error: State is None.")
        return

    # Data Integrity Checks
    if not isinstance(getattr(state, "play_counts", None), dict):
        print("[stats] Error: Play count data is corrupted.")
        return
    if not state.play_counts:
        print("[stats] No play history yet.")
        return
    if not isinstance(getattr(state, "library_tracks", None), list) or not state.library_tracks:
        print("[stats] Error: Library tracks are missing.")
        return
    if not isinstance(getattr(state, "total_play_time", None), (int, float)):
        print("[stats] Error: Total play time is corrupted.")
        return

    # Calculate total listening time
    total_sec = int(state.total_play_time)
    hours = total_sec // 3600
    mins = (total_sec % 3600) // 60

    # Calculate total songs played
    valid_counts = [c for c in state.play_counts.values() if isinstance(c, (int, float))]
    total_played = sum(valid_counts)

    print("--- Playback Statistics ---")
    print(f"Total Listening Time: {hours}h {mins}m")
    print(f"Total Songs Played: {total_played}")

    # Artist Aggregation
    # Map file paths to artists to aggregate play counts by artist
    artist_counts = {}
    for path_str, count in state.play_counts.items():
        if not isinstance(count, (int, float)):
            continue

        # Find track object to get real artist name
        for t in state.library_tracks:
            if str(t.path) == path_str:
                art = t.artist or "Unknown"
                artist_counts[art] = artist_counts.get(art, 0) + count
                break

    print("\nTop Artists:")
    if not artist_counts:
        print("  (No data yet)")

    # Sort and get top 3
    top_3 = sorted(artist_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    for art, count in top_3:
        print(f"  {art}: {count} plays")