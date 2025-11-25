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
    k = key.lower()

    if k == "p":
        # if and else for toggle play/pause
        if state.is_playing:
            player_core.pause(state)
        else:
            player_core.play(state)
        print("[shortcut] p → play/pause")

    elif k == "s":
        player_core.stop(state)
        print("[shortcut] s → stop")

    elif k == "m":
        state.is_muted = not getattr(state, "is_muted", False)
        state.audio_engine.set_mute(state.is_muted)
        print(f"[shortcut] m → mute={state.is_muted}")
