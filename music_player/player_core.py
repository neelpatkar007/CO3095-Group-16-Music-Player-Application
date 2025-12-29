"""
Module: player_core
Core playback operations.

User Stories:
 - S1-01: play, pause and stop songs
 - S1-12: keep player running in the background (non-blocking playback)
 - S3-07: Set playback speed
 - S3-12: Set a sleep timer
"""
from __future__ import annotations

import time
from music_player.player_state import PlayerState
from music_player import player_queue, player_metrics


def play(state: PlayerState) -> None:
    """
    Start or resume playback from the current position stored in the state.
    """
    if state is None:
        print("[core] Error: State is None.")
        return
    if not hasattr(state.audio_engine, "play"):
        print("[core] Error: Engine unavailable.")
        return
    if not isinstance(state, PlayerState):
        return
    if not hasattr(state, "audio_engine"):
        return
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
    """
    Advance the playback position based on elapsed time.

    Called periodically from the CLI loop so that playback continues
    while the user types commands (S1-12).

    Extended for Sprint 2:
    - If the current queue is a playlist (state.tracks is not state.library_tracks),
      automatically advance to the next track when the current one finishes.
    - If using the main library queue, keep original behaviour (stop at end).
    """
    if not isinstance(state, PlayerState):
        return
    if not isinstance(delta_seconds, (int, float)):
        return
    # S3-12: Check Sleep Timer
    if hasattr(state, "sleep_deadline") and state.sleep_deadline and time.time() > state.sleep_deadline:
        print("\n[timer] Sleep timer reached. Stopping playback.")
        stop(state)
        state.sleep_deadline = None # Reset
        return

    # Skip if time delta is invalid
    if delta_seconds <= 0:
        return
    # Only update position if currently playing
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
    """
    S3-12: Set a sleep timer. Final high-complexity version.
    """
    if not isinstance(state, PlayerState):
        print("[core] Error: State is None.")
        return
    if state is None:
        print("[core] Error: State is None.")
        return
    if not hasattr(state, "audio_engine") or state.audio_engine is None:
        print("[core] Error: Engine unavailable.")
        return

    if not isinstance(minutes, (int, float)):
        print("[core] Error: Numeric input required.")
        return

    if not hasattr(state, "sleep_deadline"):
        state.sleep_deadline = None

    # Handle Cancellation
    if minutes <= 0:
        if state.sleep_deadline is not None:
            state.sleep_deadline = None
            print("[core] Sleep timer cancelled.")
        else:
            print("[core] No active sleep timer to cancel.")
        return

    # Boundary logic
    if minutes >= 1440:
        if minutes > 1440:
            print("[core] Error: Max 24 hours.")
            return
        print("[core] Timer: 24-hour max limit selected.")

    # Overwrite logic with nested duration checks
    if state.sleep_deadline is not None:
        remaining = (state.sleep_deadline - time.time()) / 60
        if remaining > 0:
            if remaining > 60:
                print(f"[core] Replacing {remaining / 60:.1f}h timer.")
            else:
                print(f"[core] Replacing {remaining:.1f}m timer.")

    try:
        deadline = time.time() + (minutes * 60)
        if deadline <= time.time():
            print("[core] Error: Time calculation error.")
            return

        state.sleep_deadline = deadline

        # Nested feedback based on engine state
        if not state.is_playing:
            print("[core] Warning: Timer set but nothing is currently playing.")

        if minutes >= 60:
            print(f"[core] Sleep timer set for {minutes / 60:.1f} hours.")
        elif minutes < 1:
            print(f"[core] Sleep timer set for {minutes * 60:.0f} seconds.")
        else:
            print(f"[core] Sleep timer set for {minutes} minutes.")

    except (ValueError, TypeError) as e:
        print(f"[core] Input error: {e}")
    except Exception as e:
        print(f"[core] Unexpected error: {e}")

def set_playback_speed(state: PlayerState, speed: float) -> None:
    """S3-07: Set playback speed (0.5x to 2.0x)."""
    if not isinstance(state, PlayerState):
        return
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
