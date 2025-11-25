"""
Module: player_shortcuts
User Story:
 - S1-07: keyboard shortcuts for play, pause, stop and mute.
"""

from player_state import PlayerState
import player_core

def handle_keypress(state: PlayerState, key: str) -> None:
    """
    Interpret a keyboard key and trigger the corresponding action
    (play/pause/stop/mute) (S1-07).
    """
    key = key.lower()
    if key == "p":
        if state.is_playing:
            player_core.pause(state)
        else:
            player_core.play(state)
    elif key == "s":
        player_core.stop(state)
    elif key == "m":
        state.is_muted = not state.is_muted
        state.audio_engine.set_muted(state.is_muted)
        print(f"[shortcut] mute -> {state.is_muted}")
    else:
        print(f"[shortcut] No action bound to key '{key}'.")