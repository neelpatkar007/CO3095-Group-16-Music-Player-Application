from __future__ import annotations

"""
Keyboard shortcut handling for play/pause/stop/mute (S1-07).
"""
# Try package-style imports first (for tests / Pynguin),
# fall back to flat-layout imports for running via `python main.py`.
try:  # pragma: no cover - import branching only
    from music_player.player_state import PlayerState
    from music_player import player_core, player_audio
except ImportError:  # pragma: no cover
    from player_state import PlayerState  # type: ignore
    import player_core  # type: ignore
    import player_audio  # type: ignore

def handle_keypress(state: PlayerState, key: str) -> None:
    """
    Interpret a keyboard key press (p, s, m) and trigger the corresponding action
    (play/pause/stop/mute) in the player core or audio module (S1-07).
    """
    if not key:
        return

    key = key.lower()

    # Play/Pause Toggle
    if key == "p":
        if not state.tracks:
            print("[shortcuts] Error: No tracks loaded.")
            return

        # Toggle play/pause based on current state. If playing, pause; if paused/stopped, play.
        if state.is_playing:
            player_core.pause(state)
        else:
            player_core.play(state)

    # Stop Playback
    elif key == "s":
        # Stop playback and reset position
        if state.is_playing:
            player_core.stop(state)

    # Mute Toggle
    elif key == "m":
        # Toggle mute via the player_audio module
        player_audio.toggle_mute(state)

    elif key == "+":
        if state.volume < 100:
            new_vol = state.volume + 10
            state.volume = 100 if new_vol > 100 else new_vol
            print(f"[shortcuts] Volume up: {state.volume}%")

    elif key == "-":
        if state.volume > 0:
            new_vol = state.volume - 10
            state.volume = 0 if new_vol < 0 else new_vol
            print(f"[shortcuts] Volume down: {state.volume}%")

    # Unrecognised Key
    else:
        print(f"[shortcuts] No action bound to key '{key}'")