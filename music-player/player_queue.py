"""
Module: player_queue
User Story:
 - S1-02: skip to the next or previous song.
"""

# python
from player_state import PlayerState

def next_track(state: PlayerState) -> None:
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
    new = (old + 1) % n
    state.current_index = new
    state.position_seconds = 0.0
    track = state.current_track
    if track is None:
        print("[queue] Selected track missing.")
        return
    if state.is_playing:
        try:
            state.audio_engine.play(track.path, start_pos=0.0)
            state.is_playing = True
            state.is_paused = False
            print(f"[queue] Next: {track.display_name}")
        except Exception as e:
            print(f"[queue] Playback failed: {e}")
    elif state.is_paused:
        print(f"[queue] Selected next (paused): {track.display_name}")
    else:
        print(f"[queue] Selected next: {track.display_name}")

def previous_track(state: PlayerState) -> None:
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
    new = (old - 1) % n
    state.current_index = new
    state.position_seconds = 0.0
    track = state.current_track
    if track is None:
        print("[queue] Selected track missing.")
        return
    if state.is_playing:
        try:
            state.audio_engine.play(track.path, start_pos=0.0)
            state.is_playing = True
            state.is_paused = False
            print(f"[queue] Previous: {track.display_name}")
        except Exception as e:
            print(f"[queue] Playback failed: {e}")
    elif state.is_paused:
        print(f"[queue] Selected prev (paused): {track.display_name}")
    else:
        print(f"[queue] Selected prev: {track.display_name}")
