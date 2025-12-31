"""
Module: player_queue
User Story:
 - S1-02: skip to the next or previous song.
 - S3-01: Shuffle
 - S3-02: Loop
 - S3-03: History tracking
 - S3-04: Add/Remove from queue
 - S3-05: Play Next
 - S3-06: Clear Queue
"""

import random
from music_player.player_state import PlayerState
from music_player.library import Track

def _get_tracks_safe(state: PlayerState) -> list:
    """
    Helper to safely retrieve tracks as a list.
    """
    raw_tracks = getattr(state, "tracks", None)

    if raw_tracks is None:
        return []

    if isinstance(raw_tracks, list):
        return raw_tracks

    try:
        return list(raw_tracks)
    except Exception:
        return []

def next_track(state: PlayerState) -> None:
    '''
    Advance to the next track in the playlist.
    Automatically handles Shuffle selection and History logging.
    '''
    if state is None or isinstance(state, (str, int, float, bool)):
        print("[queue] Error: State is invalid.")
        return

    tracks = _get_tracks_safe(state)

    if not tracks:
        print("[queue] No tracks available.")
        return

    # Safe access to current_track
    curr = getattr(state, "current_track", None)
    if curr:
        if not hasattr(state, "history") or state.history is None:
            state.history = []
        state.history.append(curr)

    n = len(tracks)
    if n == 0:
        print("[queue] Library empty.")
        return

    # Normalise current index
    old = getattr(state, "current_index", 0)
    if old is None: old = 0
    if not isinstance(old, int): old = 0

    if old < 0:
        old = 0
    elif old >= n:
        old = n - 1

    # S3-02: Loop One Logic
    loop_mode = getattr(state, "loop_mode", "off")
    shuffle_active = getattr(state, "shuffle_active", False)

    if loop_mode == "one":
        new = old
        wrapped = False
        changed = False
    elif shuffle_active and n > 1:
        # S3-01: Shuffle logic with duplicate avoidance
        if n == 2:
            new = 1 if old == 0 else 0
        else:
            new = old
            attempts = 0
            while new == old and attempts < 15:
                new = random.randint(0, n - 1)
                attempts += 1
        wrapped = False
        changed = new != old
    else:
        # Normal sequential logic + S3-02: Loop All/Off
        cand = old + 1
        if cand >= n:
            if loop_mode == "all":
                new = 0
                wrapped = True
            else:
                print("[queue] End of playlist.")
                state.is_playing = False
                return # Stop at end
        else:
            new = cand
            wrapped = False
        changed = new != old

    # Update state and track
    state.current_index = new
    state.position_seconds = 0.0 # Reset position

    # Safe track retrieval
    track = None
    if 0 <= new < len(tracks):
        track = tracks[new]

    if track is None:
        print("[queue] Selected track missing.")
        return

    # Safe Display Name
    display_name = getattr(track, "display_name", "Unknown Track")

    # Handle playback
    if getattr(state, "is_playing", False):
        try:
            # Stop current playing track before starting new one
            engine = getattr(state, "audio_engine", None)
            try:
                busy = False
                if hasattr(engine, "is_busy"):
                    busy = engine.is_busy()
            except Exception:
                busy = False
            if busy and hasattr(engine, "stop"):
                try:
                    engine.stop()
                except Exception:
                    pass

            # Start playback of new track from beginning
            try:
                # Validate path existence
                if hasattr(track, "path") and engine:
                    engine.play(track.path, start_pos=0.0)
            except Exception as e:
                try:
                    if engine: engine.stop()
                except Exception:
                    pass
                try:
                    if hasattr(track, "path") and engine:
                        engine.play(track.path, start_pos=0.0)
                except Exception:
                    print(f"[queue] ERROR starting playback: {e}")
                    state.is_playing = False
                    state.is_paused = False
                    return
            state.is_playing = True
            state.is_paused = False

            if loop_mode == "one":
                print(f"[queue] Looping: {display_name}")
            elif shuffle_active:
                print(f"[queue] Shuffled to: {display_name}")
            elif wrapped:
                print(f"[queue] Wrapped to next: {display_name}")
            elif changed:
                print(f"[queue] Next: {display_name}")
            else:
                print(f"[queue] Restarted: {display_name}")
        except Exception as e:
            print(f"[queue] Playback failed: {e}")
            state.is_playing = False
            state.is_paused = False

    # Handle Playback Paused
    elif getattr(state, "is_paused", False):
        try:
            if hasattr(state, "audio_engine") and hasattr(state.audio_engine, "stop"):
                state.audio_engine.stop()
        except:
            pass

        state.is_paused = False
        state.is_playing = False
        state.position_seconds = 0.0

        if shuffle_active:
             print(f"[queue] Shuffled to (ready): {display_name}")
        elif wrapped:
            print(f"[queue] Wrapped to next (ready): {display_name}")
        elif changed:
            print(f"[queue] Selected next (ready): {display_name}")
        else:
            print(f"[queue] Selected (ready): {display_name}")

    else:
        # Update messages for stopped state
        if shuffle_active:
            print(f"[queue] Shuffled to: {display_name}")
        elif wrapped:
            print(f"[queue] Wrapped to next: {display_name}")
        elif changed:
            print(f"[queue] Selected next: {display_name}")
        else:
            print(f"[queue] Selected: {display_name}")

def previous_track(state: PlayerState) -> None:
    '''
    Moves playback index to the previous track in the playlist.
    If Shuffle is active, it uses the history stack to go back correctly.
    '''
    if state is None or isinstance(state, (str, int, float, bool)):
        return

    tracks = _get_tracks_safe(state)
    if not tracks:
        print("[queue] No tracks available.")
        return

    n = len(tracks)
    if n == 0:
        print("[queue] Library empty.")
        return

    old = getattr(state, "current_index", 0)
    if old is None: old = 0
    if not isinstance(old, int): old = 0

    loop_mode = getattr(state, "loop_mode", "off")
    shuffle_active = getattr(state, "shuffle_active", False)

    # S3-02: Loop-Aware Previous Logic
    if loop_mode == "one":
        new = old  # Stay on current track
        wrapped = False
    elif shuffle_active and hasattr(state, "history") and state.history and len(state.history) > 0:
        last_track = state.history.pop() # Retrieve the last played song

        new_idx = None
        for i, t in enumerate(tracks):
            if t == last_track:
                new_idx = i
                break

        if new_idx is not None:
            new = new_idx
        else:
            new = old - 1 if old > 0 else n - 1
        wrapped = False
    else:
        # Normal sequential logic
        cand = old - 1
        if cand < 0:
            if loop_mode == "all":
                new = n - 1
                wrapped = True
            else:
                print("[queue] Beginning of playlist.")
                new = 0 # Stay at first track
                wrapped = False
        else:
            new = cand
            wrapped = False

    # Check for change
    changed = new != old

    # Update State and Track
    state.current_index = new
    state.position_seconds = 0.0 # Reset playback position

    track = None
    if 0 <= new < len(tracks):
        track = tracks[new]

    if track is None:
        print("[queue] Selected track missing.")
        return

    display_name = getattr(track, "display_name", "Unknown Track")

    # Handle Playback Playing
    if getattr(state, "is_playing", False):
        try:
            # Stop current playing track before starting new one
            engine = getattr(state, "audio_engine", None)
            try:
                busy = False
                if hasattr(engine, "is_busy"):
                    busy = engine.is_busy()
            except Exception:
                busy = False
            if busy and hasattr(engine, "stop"):
                try:
                    engine.stop()
                except Exception:
                    pass

            # Start playback of new track from beginning
            try:
                if hasattr(track, "path") and engine:
                    engine.play(track.path, start_pos=0.0)
            except Exception as e:
                try:
                    if engine: engine.stop()
                except Exception:
                    pass
                try:
                    if hasattr(track, "path") and engine:
                        engine.play(track.path, start_pos=0.0)
                except Exception:
                    print(f"[queue] ERROR starting playback: {e}")
                    state.is_playing = False
                    state.is_paused = False
                    return
            state.is_playing = True
            state.is_paused = False

            # Print appropriate message
            if shuffle_active:
                print(f"[queue] Back to shuffled: {display_name}")
            elif wrapped:
                print(f"[queue] Wrapped to prev: {display_name}")
            elif changed:
                print(f"[queue] Previous: {display_name}")
            else:
                print(f"[queue] Restarted: {display_name}")
        except Exception as e:
            print(f"[queue] Playback failed: {e}")
            state.is_playing = False
            state.is_paused = False

    # Handle Playback Paused
    elif getattr(state, "is_paused", False):
        try:
            if hasattr(state, "audio_engine") and hasattr(state.audio_engine, "stop"):
                state.audio_engine.stop()
        except:
            pass

        state.is_paused = False
        state.is_playing = False
        state.position_seconds = 0.0

        # Update messages for paused state
        if wrapped:
            print(f"[queue] Wrapped to prev (ready): {display_name}")
        elif changed:
            print(f"[queue] Selected prev (ready): {display_name}")
        else:
            print(f"[queue] Selected (ready): {display_name}")

    else:
        # Update messages for stopped state
        if wrapped:
            print(f"[queue] Wrapped to prev: {display_name}")
        elif changed:
            print(f"[queue] Selected prev: {display_name}")
        else:
            print(f"[queue] Selected: {display_name}")

def toggle_shuffle(state: PlayerState) -> None:
    """
    S3-01: Toggle shuffle mode.
    """
    if state is None or isinstance(state, (str, int, float, bool)):
        print("[queue] Error: State is null."); return

    if not hasattr(state, "tracks"):
        print("[queue] Error: Tracks attribute missing."); return

    tracks = _get_tracks_safe(state)
    n = len(tracks)

    if n == 0:
        print("[queue] Note: Shuffle enabled on empty queue.")

    current = getattr(state, "shuffle_active", False)
    state.shuffle_active = not current

    if state.shuffle_active:
        msg = "[queue] Shuffle: ON"
        if n == 1:
            msg += " (Limited effect: 1 song)"
        print(msg)

        current_index = getattr(state, "current_index", 0)
        if current_index is None: current_index = 0
        if not isinstance(current_index, int): current_index = 0

        if current_index >= n and n > 0:
            state.current_index = 0
            print("[queue] Reset index to 0.")
    else:
        print("[queue] Shuffle: OFF")
        loop_mode = getattr(state, "loop_mode", "off")
        if loop_mode == "one":
            print("[queue] (Loop One remains active)")


def set_loop_mode(state: PlayerState, mode: str) -> None:
    """S3-02: Set loop to 'off', 'one', or 'all'."""
    if state is None or isinstance(state, (str, int, float, bool)):
        return

    if not isinstance(mode, str):
        return

    mode_lower = mode.lower()
    is_valid = False
    if mode_lower == "off":
        is_valid = True
    elif mode_lower == "one":
        is_valid = True
    elif mode_lower == "all":
        is_valid = True

    if not is_valid:
        print("[queue] Invalid loop mode. Use: off, one, all")
        return

    current_mode = getattr(state, "loop_mode", None)
    if current_mode == mode_lower:
        print(f"[queue] Loop mode: {mode_lower}")
        return

    try:
        state.loop_mode = mode_lower
    except AttributeError:
        pass

    try:
        if hasattr(state, "loop_mode") and state.loop_mode is not None:
            if len(state.loop_mode) > 0:
                print(f"[queue] Loop mode: {mode_lower}")
    except (AttributeError, TypeError):
        pass

def _find_track(state: PlayerState, query: str) -> Track | None:
    """Helper Function: Find track by Index or Name."""
    try:
        query = query.strip()
        if query.isdigit():
            idx = int(query) - 1
            if hasattr(state, "library_tracks") and isinstance(state.library_tracks, list):
                if 0 <= idx < len(state.library_tracks):
                    return state.library_tracks[idx]
        query_lower = query.lower()

        if hasattr(state, "library_tracks") and isinstance(state.library_tracks, list):
            for t in state.library_tracks:
                if not hasattr(t, "display_name"):
                    continue
                if query_lower in t.display_name.lower():
                    return t
    except Exception:
        return None
    return None

def add_to_queue(state: PlayerState, query: str) -> None:
    """
    S3-04: Add songs to the end of the current queue (Decoupled).
    """
    if state is None or isinstance(state, (str, int, float, bool)):
        print("[queue] Error: State is None.")
        return

    if not query or not isinstance(query, str):
        print("[queue] Usage: /q.add <index|name>")
        return

    if not hasattr(state, "library_tracks") or not state.library_tracks:
        print("[queue] Error: Library is empty or missing.")
        return

    # Use safe retrieval logic for initial check
    if not hasattr(state, "tracks") or state.tracks is None:
        try:
            state.tracks = []
        except AttributeError:
            return
    elif not isinstance(state.tracks, list):
        # Forced conversion if possible, or reset
        try:
            state.tracks = list(state.tracks)
        except:
            state.tracks = []

    found = _find_track(state, query)

    if not found:
        print(f"[queue] Song '{query}' not found in Library.")
        return

    if not hasattr(found, "display_name") or not found.display_name:
        print("[queue] Error: Track data corrupted.")
        return

    _ensure_queue_decoupled(state)

    try:
        if isinstance(state.tracks, list):
            state.tracks.append(found)
    except Exception as e:
        print(f"[queue] Error appending to queue: {e}")
        return

    print(f"[queue] Added '{found.display_name}' to queue.")

    if len(state.tracks) > 500:
        print("[queue] Warning: Queue is getting very long.")


def play_next(state: PlayerState, query: str) -> None:
    """
    S3-05: Queue a specific song to play next (Decoupled).
    """
    if state is None or isinstance(state, (str, int, float, bool)):
        print("[queue] Error: State is None.")
        return

    if not query or not isinstance(query, str):
        print("[queue] Usage: /playnext <index|name>")
        return

    # Strict list requirement for insertion
    if not hasattr(state, "tracks") or not isinstance(state.tracks, list):
        print("[queue] Error: Queue corrupted.")
        try:
            state.tracks = []
        except AttributeError:
            return

    found = _find_track(state, query)

    if not found:
        print(f"[queue] Song '{query}' not found in Library.")
        return

    _ensure_queue_decoupled(state)

    tracks = state.tracks
    current_len = len(tracks)
    current_index = getattr(state, "current_index", 0)
    if current_index is None: current_index = 0
    if not isinstance(current_index, int): current_index = 0

    insert_idx = current_index + 1

    if insert_idx < 0:
        insert_idx = 0
    elif insert_idx > current_len:
        insert_idx = current_len

    try:
        tracks.insert(insert_idx, found)
    except Exception as e:
        print(f"[queue] Insertion failed: {e}")
        return

    if tracks[insert_idx] != found:
        print("[queue] Error: Track did not insert correctly.")
        return

    print(f"[queue] Queued next: '{found.display_name}'.")


def remove_from_queue(state: PlayerState, query: str) -> None:
    """
    S3-04: Remove a song from the queue by Index or Name.
    """
    if state is None or isinstance(state, (str, int, float, bool)): return

    # Use safe retrieval, but we need the actual reference to remove from it
    if not hasattr(state, "tracks") or not isinstance(state.tracks, list):
        print("[queue] Queue is empty.")
        return

    tracks = state.tracks
    if not tracks:
        print("[queue] Queue is empty.")
        return

    if not query or not isinstance(query, str):
        print("[queue] Usage: /q.remove <index|name>")
        return

    _ensure_queue_decoupled(state)

    if query.isdigit():
        try:
            idx = int(query) - 1
            if 0 <= idx < len(tracks):
                removed = tracks.pop(idx)

                current_index = getattr(state, "current_index", 0)
                if current_index is None: current_index = 0

                if idx < current_index:
                    state.current_index = current_index - 1

                name = getattr(removed, "display_name", "Unknown")
                print(f"[queue] Removed '{name}' from queue.")
                return
            else:
                print("[queue] Index out of range.")
                return
        except ValueError:
            print("[queue] Error parsing index.")
            return

    query_lower = query.lower()

    for i, t in enumerate(tracks):
        if t is None: continue
        if not hasattr(t, "display_name"): continue

        if query_lower in t.display_name.lower():
            removed = tracks.pop(i)

            current_index = getattr(state, "current_index", 0)
            if current_index is None: current_index = 0

            if i < current_index:
                state.current_index = current_index - 1

            print(f"[queue] Removed '{removed.display_name}' from queue.")
            return

    print(f"[queue] '{query}' not found in current queue.")

def clear_queue(state: PlayerState) -> None:
    """
    S3-06: Clear the queue (keep playing current song).
    """
    if state is None or isinstance(state, (str, int, float, bool)):
        print("[queue] Error: State is None.")
        return

    # Use safe retrieval for reading, but check type for modification
    tracks_ref = getattr(state, "tracks", None)

    if tracks_ref is None:
        print("[queue] Queue is already missing.")
        try:
            state.tracks = []
        except AttributeError:
            pass
        return

    if not isinstance(tracks_ref, list):
        try:
            state.tracks = list(tracks_ref)
            tracks_ref = state.tracks
        except:
            print("[queue] Queue corrupted (invalid type).")
            state.tracks = []
            return

    if not tracks_ref:
        print("[queue] Queue is already empty.")
        return

    _ensure_queue_decoupled(state)

    current = None
    current_index = getattr(state, "current_index", 0)
    if current_index is None: current_index = 0
    if not isinstance(current_index, int): current_index = 0

    if 0 <= current_index < len(tracks_ref):
        current = tracks_ref[current_index]

    if current:
        if not hasattr(current, "display_name"):
            print("[queue] Warning: Current track data seems corrupted.")

        state.tracks = [current]
        state.current_index = 0
        print("[queue] Queue cleared (current song retained).")
    else:
        state.tracks = []
        state.current_index = 0
        print("[queue] Queue completely cleared.")

    # Re-check len
    if len(state.tracks) > 1:
        print("[queue] Error: Queue failed to clear.")

    if not getattr(state, "is_playing", False) and not getattr(state, "is_paused", False):
        print("[queue] (Player is stopped)")

def show_queue(state: PlayerState) -> None:
    if state is None or isinstance(state, (str, int, float, bool)):
        return

    print("[queue] --- History ---")
    history = getattr(state, "history", [])
    if not history:
        print("  (Empty)")
    else:
        for t in history[-5:]:
            if hasattr(t, "display_name"):
                print(f"  [Played] {t.display_name}")

    print("\n[queue] --- Up Next ---")

    tracks = _get_tracks_safe(state)

    if not tracks:
        print("  (Empty)")

    current_idx = getattr(state, "current_index", 0)
    if current_idx is None: current_idx = 0
    if not isinstance(current_idx, int): current_idx = 0

    if current_idx >= len(tracks):
        print("  (End of queue)")
        return

    for i in range(current_idx, len(tracks)):
        track = tracks[i]
        marker = " "

        if i == current_idx:
            if getattr(state, "is_playing", False):
                marker = "▶"
            elif getattr(state, "is_paused", False):
                marker = "‖"
            else:
                marker = "•"

        d_name = getattr(track, "display_name", "Unknown")
        print(f"  {marker} {i + 1}. {d_name}")

    if getattr(state, "shuffle_active", False):
        print("\n  (Note: Shuffle is ON, playing order is randomized)")

def _ensure_queue_decoupled(state: PlayerState) -> None:
    """
    Helper Function:
    Create a copy of the current library/playlist so that all changes
    made to a queue are only to the temp copy queue and not the real playlist.
    """
    if state.tracks is state.library_tracks:
        state.tracks = list(state.library_tracks)
        return

    for pl in state.playlists:
        if state.tracks is pl.tracks:
            state.tracks = list(pl.tracks)
            return