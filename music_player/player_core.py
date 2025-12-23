"""
Module: player_core
Core playback operations.

User Stories:
 - S1-01: play, pause and stop songs
 - S1-12: keep player running in the background (non-blocking playback)
 - S3-07: Set playback speed
 - S3-12: Set a sleep timer
"""
import time
from music_player.player_state import PlayerState
from music_player import player_queue, player_metrics


def play(state: PlayerState) -> None:
    """
    Start or resume playback from the current position stored in the state.
    """
    track = state.current_track
    if track is None:
        print("[core] No tracks loaded.")
        return

    # Check if audio is already playing
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

    # Fresh play from the current position
    state.audio_engine.play(track.path, start_pos=state.position_seconds, speed=state.playback_speed)
    state.is_playing = True
    state.is_paused = False
    print(f"[core] Playing: {track.display_name} ({state.playback_speed}x)")


def pause(state: PlayerState) -> None:
    """Pause playback without resetting position."""
    if not state.is_playing or state.is_paused:
        print("[core] Nothing to pause.")
        return

    state.audio_engine.pause()
    state.is_playing = False
    state.is_paused = True
    print("[core] Paused.")


def stop(state: PlayerState) -> None:
    """Stop playback and reset position to 0."""
    if not state.is_playing and not state.is_paused:
        print("[core] Nothing is playing.")
        return

    state.audio_engine.stop()
    state.is_playing = False
    state.is_paused = False
    state.position_seconds = 0.0
    print("[core] Stopped.")


def update_playback(state: PlayerState, delta_seconds: float) -> None:
    # Skip if not playing
    if not state.is_playing or state.is_paused:
        return

    # S3-07: Apply Playback Speed
    adjusted_delta = delta_seconds * state.playback_speed

    state.position_seconds += adjusted_delta

    track = state.current_track
    if track and track.duration_seconds is not None:
        if state.position_seconds >= track.duration_seconds:
            # Track Finished
            player_metrics.record_play(state)
            state.position_seconds = track.duration_seconds
            player_queue.next_track(state)


def set_sleep_timer(state: PlayerState, minutes: float) -> None:
    """S3-12: Set a sleep timer."""

def set_playback_speed(state: PlayerState, speed: float) -> None:
    """S3-07: Set playback speed (0.5x to 2.0x)."""
    if state is None: return
    if not isinstance(speed, (int, float)):
        print("[core] Error: Speed must be a number.")
        return
    if speed < 0.5 or speed > 2.0:
        print("[core] Speed must be between 0.5x and 2.0x.")
        return
    if hasattr(state, "playback_speed") and state.playback_speed == speed:
        print(f"[core] Speed is already {speed}x.")
        return

    state.playback_speed = speed
    print(f"[core] Playback speed set to {speed}x.")
    if state.is_playing:
        print("[core] Applying speed change...")
        state.is_playing = False
        play(state)
    elif state.is_paused:
        print("[core] New speed will apply when you resume playback.")