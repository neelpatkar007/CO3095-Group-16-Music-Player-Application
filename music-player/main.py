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
    cmd = command.strip().lower()

    if cmd in ("/quit", "/exit", "q"):
        return False

    parts = cmd.split()
    base = parts[0] if parts else ""
    arg = parts[1] if len(parts) > 1 else ""

    if base == "/play":
        player_core.play(state)
    elif base == "/pause":
        player_core.pause(state)
    elif base == "/stop":
        player_core.stop(state)
    elif base == "/next":
        player_queue.next_track(state)
    elif base == "/prev":
        player_queue.previous_track(state)
    elif base == "/info":
        player_ui.print_now_playing(state)
    elif base == "/progress":
        player_ui.print_progress(state)
    elif base == "/bar":
        player_ui.print_progress_bar(state)
    elif base == "/list":
        player_ui.print_playlist_with_indicator(state)
    elif base.startswith("/help"):
        topic = parts[1] if len(parts) == 2 else None
        player_help.print_help(topic)
    else:
        print("Unknown command. Try /help")

    return True


def main() -> None:
    audio_engine = AudioEngine()
    tracks = discover_tracks()
    state = PlayerState(tracks=tracks, audio_engine=audio_engine)

    print("Music Player – Sprint 1 Backbone")
    print("Commands: /play, /pause, /stop, /next, /prev, /info, /progress, /bar, /list, /volume <val>, /help, /quit")

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

