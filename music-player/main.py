import time
import player_seek

from audio_backend import AudioEngine
from library import discover_tracks
from player_state import PlayerState
import player_core
import player_queue
import player_help
import player_ui
import player_audio


def handle_command(state: PlayerState, command: str) -> bool:
    cmd = command.strip().lower()

    if cmd in ("/quit", "/exit", "q"):
        return False

    parts = cmd.split()
    base = parts[0] if parts else ""
    arg = parts[1] if len(parts) > 1 else ""

    if base == "/play":
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
    if cmd == "/play":
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
    # S1-08 rewind/fast-forward
    elif cmd == "/rw":
        player_seek.nudge(state, -5.0)
    elif cmd == "/ff":
        player_seek.nudge(state, 5.0)
    elif cmd.startswith("/seek"):
        parts = command.split()
        if len(parts) < 2:
            print("[main] Usage: /seek <mm:ss or seconds>")
        else:
            player_seek.seek_to(state, parts[1])
    # S1-11
    elif cmd.startswith("/help"):
        parts = cmd.split(maxsplit=1)
        topic = parts[1] if len(parts) == 2 else None
        player_help.print_help(topic)
    elif base == "/volume" or base == "/vol":
        player_audio.change_volume(state, arg)
    else:
        print("Unknown command. Try /help")

    return True


def main() -> None:
    audio_engine = AudioEngine()
    tracks = discover_tracks()
    state = PlayerState(tracks=tracks, audio_engine=audio_engine)

    print("Music Player – Sprint 1 Backbone")
    print("Commands: /play, /pause, /stop, /next, /prev, /info, /progress, /bar, /list, /volume <val>, /seek, /rw, /ff, /list, /help, /quit")

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

    state.audio_engine.stop()

if __name__ == "__main__":
    main()