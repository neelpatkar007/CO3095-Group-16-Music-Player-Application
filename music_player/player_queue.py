"""
Module: player_queue
User Story:
 - S1-02: skip to the next or previous song.
"""

# python
from music_player.player_state import PlayerState

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
    single = n == 1
    if single:
        new = 0
    else:
        cand = old + 1
        if cand >= n:
            new = 0
        else:
            new = cand
    wrapped = new == 0 and old != 0
    changed = new != old
    state.current_index = new
    state.position_seconds = 0.0
    track = state.current_track
    if track is None:
        print("[queue] Selected track missing.")
        return
    if state.is_playing:
        try:
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
            if wrapped:
                print(f"[queue] Wrapped to next: {track.display_name}")
            elif changed:
                print(f"[queue] Next: {track.display_name}")
            else:
                print(f"[queue] Restarted: {track.display_name}")
        except Exception as e:
            print(f"[queue] Playback failed: {e}")
            state.is_playing = False
            state.is_paused = False
    elif state.is_paused:
        if wrapped:
            print(f"[queue] Wrapped to next (paused): {track.display_name}")
        elif changed:
            print(f"[queue] Selected next (paused): {track.display_name}")
        else:
            print(f"[queue] Selected (paused): {track.display_name}")
    else:
        if wrapped:
            print(f"[queue] Wrapped to next: {track.display_name}")
        elif changed:
            print(f"[queue] Selected next: {track.display_name}")
        else:
            print(f"[queue] Selected: {track.display_name}")

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
    single = n == 1
    if single:
        new = 0
    else:
        cand = old - 1
        if cand < 0:
            new = n - 1
        else:
            new = cand
    wrapped = new == n - 1 and old == 0
    changed = new != old
    state.current_index = new
    state.position_seconds = 0.0
    track = state.current_track
    if track is None:
        print("[queue] Selected track missing.")
        return
    if state.is_playing:
        try:
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
    elif state.is_paused:
        if wrapped:
            print(f"[queue] Wrapped to prev (paused): {track.display_name}")
        elif changed:
            print(f"[queue] Selected prev (paused): {track.display_name}")
        else:
            print(f"[queue] Selected (paused): {track.display_name}")
    else:
        if wrapped:
            print(f"[queue] Wrapped to prev: {track.display_name}")
        elif changed:
            print(f"[queue] Selected prev: {track.display_name}")
        else:
            print(f"[queue] Selected: {track.display_name}")
