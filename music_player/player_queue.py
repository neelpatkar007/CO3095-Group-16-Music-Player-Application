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


def next_track(state: PlayerState) -> None:
    '''
    Advance to the next track in the playlist.
    Wrap around to the first track if at the end.
    Automatically starts playback if currently playing.
    '''
    if not state.tracks:
        print("[queue] No tracks available.")
        return
    n = len(state.tracks)
    if n == 0:
        print("[queue] Library empty.")
        return

    # Normalise current index
    old = state.current_index
    if old is None:
        old = 0
    # Checks to ensure index is in bounds
    if old < 0:
        old = 0
    if old >= n:
        old = n - 1

    # Determine new index
    single = n == 1
    if single:
        new = 0
    elif state.shuffle_active and n > 1:
        # S3-01: Shuffle logic from repo 123
        new = old
        while new == old:
            new = random.randint(0, n - 1)
    else:
        # Normal sequential logic
        cand = old + 1
        if cand >= n:
            new = 0
        else:
            new = cand

    # Check for wrap and change
    wrapped = new == 0 and old != 0 and not state.shuffle_active
    changed = new != old

    # Update state and track
    state.current_index = new
    state.position_seconds = 0.0 # Reset position
    track = state.current_track
    if track is None:
        print("[queue] Selected track missing.")
        return

    # Handle playback
    if state.is_playing:
        try:
            # Stop current playing track before starting new one
            engine = state.audio_engine
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
                engine.play(track.path, start_pos=0.0)
            except Exception as e:
                try:
                    engine.stop()
                except Exception:
                    pass
                try:
                    engine.play(track.path, start_pos=0.0)
                except Exception:
                    print(f"[queue] ERROR starting playback: {e}")
                    state.is_playing = False
                    state.is_paused = False
                    return
            state.is_playing = True
            state.is_paused = False

            if state.shuffle_active:
                print(f"[queue] Shuffled to: {track.display_name}")
            elif wrapped:
                print(f"[queue] Wrapped to next: {track.display_name}")
            elif changed:
                print(f"[queue] Next: {track.display_name}")
            else:
                print(f"[queue] Restarted: {track.display_name}")
        except Exception as e:
            print(f"[queue] Playback failed: {e}")
            state.is_playing = False
            state.is_paused = False

    # Handle Playback Paused or Stopped
    elif state.is_paused:
        if state.shuffle_active:
             print(f"[queue] Shuffled to (paused): {track.display_name}")
        elif wrapped:
            print(f"[queue] Wrapped to next (paused): {track.display_name}")
        elif changed:
            print(f"[queue] Selected next (paused): {track.display_name}")
        else:
            print(f"[queue] Selected (paused): {track.display_name}")
    else:
        # Update messages for stopped state
        if state.shuffle_active:
            print(f"[queue] Shuffled to: {track.display_name}")
        elif wrapped:
            print(f"[queue] Wrapped to next: {track.display_name}")
        elif changed:
            print(f"[queue] Selected next: {track.display_name}")
        else:
            print(f"[queue] Selected: {track.display_name}")

def previous_track(state: PlayerState) -> None:
    '''
    Moves playback index to the previous track in the playlist.
    Wrap around to the last track if at the beginning.
    Automatically starts playback if currently playing.
    '''
    if not state.tracks:
        print("[queue] No tracks available.")
        return
    n = len(state.tracks)
    if n == 0:
        print("[queue] Library empty.")
        return
    old = state.current_index
    if old is None:
        old = 0
    if old < 0:
        old = 0
    if old >= n:
        old = n - 1
    single = n == 1
    if single:
        new = 0
    else:
        cand = old - 1
        if cand < 0:
            new = n - 1
        else:
            new = cand

    # Check for wrap and change
    wrapped = new == n - 1 and old == 0
    changed = new != old

    # Update State and Track
    state.current_index = new
    state.position_seconds = 0.0 # Reset playback position

    track = state.current_track
    if track is None:
        print("[queue] Selected track missing.")
        return

    # Handle Playback Playing
    if state.is_playing:
        try:
            # Stop current playing track before starting new one
            engine = state.audio_engine
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

            # Start playback of new track from beginning with error handling
            try:
                engine.play(track.path, start_pos=0.0)
            except Exception as e:
                try:
                    engine.stop()
                except Exception:
                    pass
                try:
                    engine.play(track.path, start_pos=0.0)
                except Exception:
                    print(f"[queue] ERROR starting playback: {e}")
                    state.is_playing = False
                    state.is_paused = False
                    return
            state.is_playing = True
            state.is_paused = False

            # Print appropriate message
            if wrapped:
                print(f"[queue] Wrapped to prev: {track.display_name}")
            elif changed:
                print(f"[queue] Previous: {track.display_name}")
            else:
                print(f"[queue] Restarted: {track.display_name}")
        except Exception as e:
            print(f"[queue] Playback failed: {e}")
            state.is_playing = False
            state.is_paused = False

    # Handle Playback Paused or Stopped
    elif state.is_paused:
        # Update messages for paused state
        if wrapped:
            print(f"[queue] Wrapped to prev (paused): {track.display_name}")
        elif changed:
            print(f"[queue] Selected prev (paused): {track.display_name}")
        else:
            print(f"[queue] Selected (paused): {track.display_name}")
    else:
        # Update messages for stopped state
        if wrapped:
            print(f"[queue] Wrapped to prev: {track.display_name}")
        elif changed:
            print(f"[queue] Selected prev: {track.display_name}")
        else:
            print(f"[queue] Selected: {track.display_name}")

def toggle_shuffle(state: PlayerState) -> None:
    """S3-01: Toggle shuffle mode."""
    state.shuffle_active = not state.shuffle_active
    status = "ON" if state.shuffle_active else "OFF"
    print(f"[queue] Shuffle mode: {status}")

def set_loop_mode(state: PlayerState, mode: str) -> None:
    """S3-02: Set loop to 'off', 'one', or 'all'."""

def _find_track(state: PlayerState, query: str) -> Track | None:
    """Helper: Find track by Index (1-based) OR Name."""

def add_to_queue(state: PlayerState, query: str) -> None:
    """S3-04: Add songs to the end of the current queue (Decoupled)."""

def play_next(state: PlayerState, query: str) -> None:
    """S3-05: Queue a specific song to play next (Decoupled)."""

def remove_from_queue(state: PlayerState, query: str) -> None:
    """S3-04: Remove a song from the queue by Index or Name."""

def clear_queue(state: PlayerState) -> None:
    """S3-06: Clear the queue (keep playing current song)."""

def show_queue(state: PlayerState) -> None:
    """S3-03: View queue (starting from current track) and history."""

def _ensure_queue_decoupled(state: PlayerState) -> None:
    """
    Internal Helper:
    If the current play queue IS the main library or a playlist then
    create a copy of it before modifying so that temporary queue
    changes from editing the actual Library/Playlist.
    """