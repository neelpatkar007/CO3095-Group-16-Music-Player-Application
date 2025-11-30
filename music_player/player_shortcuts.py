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
    Interpret a keyboard key and trigger the corresponding action
    (play/pause/stop/mute) (S1-07).
    """
    key = key.lower()
    if key == "p":
        # Toggle play/pause based on current state
        if state.is_playing:
            player_core.pause(state)
        else:
            player_core.play(state)
    elif key == "s":
        # Stop playback
        player_core.stop(state)
    elif key == "m":
        # Toggle mute via the audio module
        player_audio.toggle_mute(state)
    else:
        print(f"[shortcuts] No action bound to key '{key}'")