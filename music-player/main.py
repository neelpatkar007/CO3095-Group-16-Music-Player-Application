"""
Main entry point – Sprint 1 backbone.

Responsibilities:
 - Load tracks from the /songs folder.
 - Create PlayerState and AudioEngine.
 - Run a simple CLI loop.
 - Periodically call update_playback so playback continues while the user types commands (S1-12).
"""

import time

from audio_backend import AudioEngine
from library import discover_tracks
from player_state import PlayerState
import player_core
import player_queue
import player_help
import player_ui


def handle_command(state: PlayerState, command: str) -> bool:
    """
    Simple command dispatcher backbone.

    Returns False if the application should quit.
    """
    raw = command.strip()
    # S1-07 keyboard shortcuts (single letters)
    if len(raw) == 1 and raw.lower() in {"p", "s", "m"}:
        import player_shortcuts
        player_shortcuts.handle_keypress(state, raw)
        return True
    cmd = raw.lower()

    if cmd in ("/quit", "/exit", "q"):
        return False

    # S1-01 commands (backbone only)
    if cmd == "/play":
        player_core.play(state)
    elif cmd == "/pause":
        player_core.pause(state)
    elif cmd == "/stop":
        player_core.stop(state)
    # S1-02
    elif cmd == "/next":
        player_queue.next_track(state)
    elif cmd == "/prev":
        player_queue.previous_track(state)
    # S1-03, S1-05, S1-06, S1-10
    elif cmd == "/info":
        player_ui.print_now_playing(state)
    elif cmd == "/progress":
        player_ui.print_progress(state)
    elif cmd == "/bar":
        player_ui.print_progress_bar(state)
    elif cmd == "/list":
        player_ui.print_playlist_with_indicator(state)
    # S1-11
    elif cmd.startswith("/help"):
        parts = cmd.split(maxsplit=1)
        topic = parts[1] if len(parts) == 2 else None
        player_help.print_help(topic)
    else:
        print("Unknown command. Try /help")

    return True


def main() -> None:
    """
    Initialise library, state and run the main command loop.

    Playback is updated every loop iteration so that audio continues
    while commands are processed (S1-12).
    """
    audio_engine = AudioEngine()
    tracks = discover_tracks()
    state = PlayerState(tracks=tracks, audio_engine=audio_engine)

    print("Music Player – Sprint 1 Backbone")
    print("Commands: /play, /pause, /stop, /next, /prev, /info, /progress, /bar, /list, /help, /quit")

    last_time = time.time()

    while True:
        now = time.time()
        delta = now - last_time
        last_time = now
        player_core.update_playback(state, delta)

        try:
            command = input("> ")
        except (EOFError, KeyboardInterrupt):
            break

        if not handle_command(state, command):
            break


if __name__ == "__main__":
    main()
