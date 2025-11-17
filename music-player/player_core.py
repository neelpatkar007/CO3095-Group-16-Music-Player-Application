"""
Module: player_core
Core playback operations.

User Stories:
 - S1-01: play, pause and stop songs
 - S1-12: keep player running in the background (non-blocking playback)
"""
from __future__ import annotations
from player_state import PlayerState


def play(state: PlayerState) -> None:
    """
    Start or resume playback from the current position.

    S1-01: user can start/resume a song.
    S1-12: this must not block the CLI; background updating will be
           handled via update_playback in the main loop.
    """
    track = state.current_track
    if track is None:
        print("[core] No tracks loaded.")
        return

    # Already playing
    if state.is_playing and not state.is_paused:
        print("[core] Already playing.")
        return

    # Resume from pause
    if state.is_paused:
        state.audio_engine.resume()
        state.is_playing = True
        state.is_paused = False
        print(f"[core] Resumed: {track.display_name}")
        return

    # Fresh play
    state.audio_engine.play(track.path, start_pos=state.position_seconds)
    state.is_playing = True
    state.is_paused = False
    print(f"[core] Playing: {track.display_name}")


def pause(state: PlayerState) -> None:
    """
    Pause playback without resetting position.

    S1-01.
    """
    if not state.is_playing or state.is_paused:
        print("[core] Nothing to pause.")
        return

    state.audio_engine.pause()
    state.is_playing = False
    state.is_paused = True
    print("[core] Paused.")


def stop(state: PlayerState) -> None:
    """
    Stop playback and reset position to 0.

    S1-01.
    """
    if not state.is_playing and not state.is_paused:
        print("[core] Nothing is playing.")
        return

    state.audio_engine.stop()
    state.is_playing = False
    state.is_paused = False
    state.position_seconds = 0.0
    print("[core] Stopped.")


def update_playback(state: PlayerState, delta_seconds: float) -> None:
    """
    Advance the playback position based on elapsed time.

    Called periodically from the CLI loop so that playback continues
    while the user types commands (S1-12).

    """
    if delta_seconds <= 0:
        return
    if not state.is_playing or state.is_paused:
        return

    state.position_seconds += delta_seconds

    track = state.current_track
    if track and track.duration_seconds is not None:
        if state.position_seconds >= track.duration_seconds:
            # End of track reached – stop.
            state.position_seconds = track.duration_seconds
            state.is_playing = False
            state.audio_engine.stop()
            print("[core] Track finished.")
