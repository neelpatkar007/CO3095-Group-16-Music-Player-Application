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
import time  # Added for S3-12
from music_player.player_state import PlayerState


def play(state: PlayerState) -> None:
    """
    Start or resume playback from the current position stored in the state.

    S1-01: user can start/resume a song.
    S1-12: this must not block the CLI; background updating will be
           handled via update_playback in the main loop.
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
    state.audio_engine.play(track.path, start_pos=state.position_seconds)
    state.is_playing = True
    state.is_paused = False
    print(f"[core] Playing: {track.display_name}")


def pause(state: PlayerState) -> None:
    """
    Pause playback without resetting position.

    S1-01.
    """
    # Nothing to pause if not playing or already paused
    if not state.is_playing or state.is_paused:
        print("[core] Nothing to pause.")
        return

    state.audio_engine.pause()
    state.is_playing = False
    state.is_paused = True
    print("[core] Paused.")


def stop(state: PlayerState) -> None:
    """
    Stop playback and reset position to 0 (start of track).

    S1-01.
    """
    # Nothing to stop if not playing or paused
    if not state.is_playing and not state.is_paused:
        print("[core] Nothing is playing.")
        return

    state.audio_engine.stop()
    state.is_playing = False
    state.is_paused = False
    state.position_seconds = 0.0 # Reset position to start of track
    print("[core] Stopped.")


def update_playback(state: PlayerState, delta_seconds: float) -> None:
    """
    Advance the playback position based on elapsed time.

    Called periodically from the CLI loop so that playback continues
    while the user types commands (S1-12).

    Extended for Sprint 2:
    - If the current queue is a playlist (state.tracks is not state.library_tracks),
      automatically advance to the next track when the current one finishes.
    - If using the main library queue, keep original behaviour (stop at end).
    """
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
    # Advance position
    state.position_seconds += delta_seconds
    # Check if track duration is known and if we have passed it
    track = state.current_track
    if track and track.duration_seconds is not None:
        if state.position_seconds >= track.duration_seconds:
            # End of track reached – stop.
            state.position_seconds = track.duration_seconds

            # Decide whether to auto-advance or stop
            is_playlist_queue = hasattr(state, "library_tracks") and (
                state.tracks is not state.library_tracks
            )

            if is_playlist_queue:
                # Auto-advance within playlist queue
                from music_player import player_queue

                # Reset position and move to next track; next_track()
                # will keep state.is_playing True and start the engine.
                state.position_seconds = 0.0
                player_queue.next_track(state)
            else:
                # Original behaviour for main library queue: just stop.
                state.is_playing = False
                state.audio_engine.stop()
                print("[core] Track finished.")


def set_sleep_timer(state: PlayerState, minutes: float) -> None:
    """
    S3-12: Set a sleep timer. After the specified number of minutes,
    playback will stop automatically.
    """
    if state is None:
        print("[core] Error: State is None.")
        return

    # Branch: Verify audio engine availability
    if not hasattr(state, "audio_engine") or state.audio_engine is None:
        print("[core] Error: Audio engine not initialized. Cannot set timer.")
        return

    if not isinstance(minutes, (int, float)):
        print("[core] Error: Minutes must be a number.")
        return

    if not hasattr(state, "sleep_deadline"):
        state.sleep_deadline = None

    if minutes <= 0:
        if state.sleep_deadline is not None:
            state.sleep_deadline = None
            print("[core] Sleep timer cancelled.")
        else:
            print("[core] No active sleep timer to cancel.")
        return

    if minutes > 1440:
        print("[core] Error: Timer cannot exceed 24 hours (1440 min).")
        return

    if state.sleep_deadline is not None:
        remaining = state.sleep_deadline - time.time()
        if remaining > 0:
            print(f"[core] Overwriting existing timer ({remaining / 60:.1f} min remaining).")

    try:
        deadline = time.time() + (minutes * 60)
        if deadline < time.time():
            print("[core] Error: Calculation failed (Time travel?).")
            return

        state.sleep_deadline = deadline
        if minutes >= 60:
            hrs = minutes / 60
            print(f"[core] Sleep timer set for {hrs:.1f} hours.")
        else:
            print(f"[core] Sleep timer set for {minutes} minutes.")

    except Exception as e:
        print(f"[core] Error setting timer: {e}")

def set_playback_speed(state: PlayerState, speed: float) -> None:
    """S3-07: Set playback speed (0.5x to 2.0x)."""