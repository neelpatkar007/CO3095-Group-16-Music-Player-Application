import time
from audio_backend import AudioEngine
from library import discover_tracks
from player_state import PlayerState
import player_core
import player_queue
import player_help
import player_ui
import player_seek
import player_audio
import player_shortcuts


def handle_command(state: PlayerState, command: str) -> bool:
    """
    Simple command dispatcher backbone.
    Returns False if the application should quit.
    """
    raw = command.strip()
    
    # S1-07 keyboard shortcuts (single letters)
    if len(raw) == 1 and raw.lower() in {"p", "s", "m"}:
        player_shortcuts.handle_keypress(state, raw)
        return True

    cmd = raw.lower()
    parts = cmd.split()
    base = parts[0] if parts else ""
    arg = parts[1] if len(parts) > 1 else ""

    if cmd in ("/quit", "/exit", "q"):
        return False
    
    # Standard Controls
    if cmd == "/play":
        player_core.play(state)
    elif cmd == "/pause":
        player_core.pause(state)
    elif cmd == "/stop":
        player_core.stop(state)
    elif cmd == "/next":
        player_queue.next_track(state)
    elif cmd == "/prev":
        player_queue.previous_track(state)
    
    # UI / Info
    elif cmd == "/info":
        player_ui.print_now_playing(state)
    elif cmd == "/progress":
        player_ui.print_progress(state)
    elif cmd == "/bar":
        player_ui.print_progress_bar(state)
    elif cmd == "/list":
        player_ui.print_playlist_with_indicator(state)
    elif cmd == "/list":
        player_ui.print_playlist_with_indicator(state)
    
    # Seek / RW / FF (S1-08)
    elif base == "/rw":
        player_seek.nudge(state, -5.0)
    elif base == "/ff":
        player_seek.nudge(state, 5.0)
    elif base == "/seek":
        if not arg:
            print("[main] Usage: /seek <mm:ss or seconds>")
        else:
            player_seek.seek_to(state, arg)
            
    # Volume & Mute (S1-04 & S1-09)
    elif base == "/volume" or base == "/vol":
        player_audio.change_volume(state, arg)
    elif base == "/mute":
        player_audio.handle_mute_command(state, "/mute")
    elif base == "/unmute":
        player_audio.handle_mute_command(state, "/unmute")

    # Help
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
    print("Commands: /play, /pause, /stop, /next, /prev, /info, /progress, /bar, /list, /seek, /volume <val>, /mute, /unmute, /rw, /ff, /help, /quit")

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