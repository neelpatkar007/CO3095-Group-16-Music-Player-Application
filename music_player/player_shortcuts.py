"""
Module: player_shortcuts
User Story:
 - S1-07: keyboard shortcuts for play, pause, stop and mute.
"""
from music_player import player_core
from music_player.player_state import PlayerState

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
        import player_audio
        player_audio.toggle_mute(state)
    else:
        print(f"[shortcut] No action bound to key '{key}'.")