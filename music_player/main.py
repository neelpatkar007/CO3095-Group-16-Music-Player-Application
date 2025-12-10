import time

from music_player.audio_backend import AudioEngine
from music_player.library import discover_tracks
from music_player.player_state import PlayerState

# Import all modules that handle specific commands
from music_player import (
    player_core,            # Handles core playback logic
    player_queue,           # Handles playlist navigation
    player_help,            # Handles displaying the help messages
    player_ui,              # Handles UI (visual output)
    player_seek,            # Handles seeking within tracks
    player_audio,           # Handles volume and mute controls
    player_shortcuts,       # Handles keyboard shortcuts (single-key commands)
)


def handle_command(state: PlayerState, command: str) -> bool:
    """
    Simple command dispatcher backbone.
    Parses user input and calls appropriate handlers.
    Returns False if the application should quit.
    """
    raw = command.strip()
    
    # S1-07 keyboard shortcuts (single letters)
    # Check for single-letter keyboard shortcuts (p, s, m)
    if len(raw) == 1 and raw.lower() in {"p", "s", "m"}:
        player_shortcuts.handle_keypress(state, raw)
        return True

    # Normalise the command for easier parsing
    cmd = raw.lower()
    parts = cmd.split()
    base = parts[0] if parts else "" # Base command (/play)
    arg = parts[1] if len(parts) > 1 else "" # Argument (volume level 30, or seek time)

    # Quit command
    if cmd in ("/quit", "/exit", "q"):
        return False
    
    # Standard Playback Controls (player_core.py and player_queue.py)
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
    
    # UI / Info Commands (player_ui.py)
    elif cmd == "/info":
        player_ui.print_now_playing(state)
    elif cmd == "/progress":
        player_ui.print_progress(state)
    elif cmd == "/bar":
        player_ui.print_progress_bar(state)
    elif cmd == "/list":
        player_ui.print_playlist_with_indicator(state)

    
    # Seek / RW / FF (S1-08) (player_seek.py)
    elif base == "/rw":
        # Rewind 5 seconds
        player_seek.nudge(state, -5.0)
    elif base == "/ff":
        # Fast-forward 5 seconds
        player_seek.nudge(state, 5.0)
    elif base == "/seek":
        if not arg:
            print("[main] Usage: /seek <mm:ss or seconds>")
        else:
            # Seek to a specified time
            player_seek.seek_to(state, arg)
            
    # Volume & Mute (S1-04 & S1-09) (player_audio.py)
    elif base == "/volume" or base == "/vol":
        # Change volume to specified level (/volume 30 or /volume 75)
        player_audio.change_volume(state, arg)
    elif base == "/mute":
        player_audio.handle_mute_command(state, "/mute")
    elif base == "/unmute":
        player_audio.handle_mute_command(state, "/unmute")

    # Help Commands (player_help.py)
    elif base.startswith("/help"):
        topic = parts[1] if len(parts) == 2 else None
        player_help.print_help(topic)

    # Unknown command
    else:
        print("Unknown command. Try /help")

    return True


def main() -> None:
    '''
    Main execution loop for the music player application.
    Initialises components, discovers tracks, and enters the command loop.
    '''
    # Initialise audio engine and discover tracks
    audio_engine = AudioEngine()
    tracks = discover_tracks()
    # Initialise player state with discovered tracks and audio engine
    state = PlayerState(tracks=tracks, audio_engine=audio_engine)

    # Startup display welcome message and available commands summary
    print("Music Player – Sprint 1 Backbone")
    print("Commands: /play, /pause, /stop, /next, /prev, /info, /progress, /bar, /list, /seek, /volume <val>, /mute, /unmute, /rw, /ff, /help, /quit")

    last_time = time.time() # For tracking delta time


    while True:
        # Calculate elapsed time since last loop iteration
        now = time.time()
        delta = now - last_time
        last_time = now

        # Update playback position based on elapsed time
        player_core.update_playback(state, delta)

        # Get user command input
        try:
            command = input("> ")
        except (EOFError, KeyboardInterrupt):
            # Exit on Ctrl+C or Ctrl+D commands
            break
        # Handle the command and check if we should quit
        if not handle_command(state, command):
            break

    # Cleanup on exit
    state.audio_engine.stop() # Ensure audio is stopped on exit of app


if __name__ == "__main__":
    main()