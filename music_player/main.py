import os
import warnings

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
warnings.filterwarnings("ignore", category=UserWarning, message=".*pkg_resources.*")

import threading
import time

from music_player.audio_backend import AudioEngine
from music_player.library import discover_tracks
from music_player.player_state import PlayerState

from music_player import (
    player_core,
    player_queue,
    player_help,
    player_ui,
    player_seek,
    player_audio,
    player_shortcuts,
)

# Sprint 2 modules
from music_player import (
    playlists_basic,
    playlists_edit,
    playlists_advanced,
    library_search_scan,
)

# Sprint 3 module
from music_player import (
    player_metrics
)

# Sprint 4 module
from music_player import (
    user_data,
    player_time,
    player_io,
    player_config
)

def _playback_worker(state: PlayerState, stop_event: threading.Event) -> None:
    """
    Background loop that periodically advances playback time.
    """
    last = time.time()
    while not stop_event.is_set():
        now = time.time()
        delta = now - last
        last = now

        if state.is_playing and not state.is_paused:
            player_core.update_playback(state, delta)
            state.total_play_time += delta

        # S4-02: Check for scheduled alarms every 10 seconds
        if int(now) % 10 == 0:
            player_time.check_alarms(state)

        # Sleep a little so we don't spin too fast
        time.sleep(0.1)

def handle_command(state: PlayerState, command: str) -> bool:
    """
    Parses user input and calls appropriate handlers.
    Returns False if the application should quit.
    """
    raw = command.strip()
    if not raw:
        return True

    # S1-07 keyboard shortcuts (single letters)
    # Check for single-letter keyboard shortcuts (p, s, m)
    if len(raw) == 1 and raw.lower() in {"p", "s", "m"}:
        player_shortcuts.handle_keypress(state, raw)
        return True

    # Split keeping original case for arguments but lowercasing the base command
    # Normalise the command for easier parsing
    parts = raw.split()
    base = parts[0].lower() if parts else "" # Base command (/play)
    args = parts[1:] # Argument (volume level 30, or seek time)

    if base in ("/quit", "/exit", "q"):
        player_metrics.save_data(state)
        return False

    # SPRINT 1 COMMANDS

    # Standard Playback Controls
    if base == "/play":
        # S4-03: Resume Logic (Apply seek if first play)
        if state.resume_active and state.current_track:
            print(f"[resume] Seeking to saved position: {int(state.position_seconds)}s...")
            player_core.play(state)
            if state.position_seconds > 0:
                player_seek.seek_to(state, str(state.position_seconds))
            state.resume_active = False  # Consumed
        else:
            player_core.play(state)
    elif base == "/pause":
        player_core.pause(state)
    elif base == "/stop":
        player_core.stop(state)
    elif base == "/next":
        player_queue.next_track(state)
    elif base == "/prev":
        player_queue.previous_track(state)

    # UI / Info (player_ui.py)
    elif base == "/info":
        player_ui.print_now_playing(state)
    elif base == "/progress":
        player_ui.print_progress(state)
    elif base == "/bar":
        player_ui.print_progress_bar(state)
    elif base == "/list":
        player_ui.print_playlist_with_indicator(state)

    # Seek / RW / FF (S1-08) (player_seek.py)
    elif base == "/rw":
        # Rewind 5 seconds
        player_seek.nudge(state, -5.0)
    elif base == "/ff":
        # Fast-forward 5 seconds
        player_seek.nudge(state, 5.0)
    elif base == "/seek":
        if not args:
            print("[main] Usage: /seek <mm:ss or seconds>")
        else:
            # Seek to a specified time
            player_seek.seek_to(state, " ".join(args))

    # Volume & Mute (S1-04 & S1-09) (player_audio.py)
    elif base in {"/volume", "/vol"}:
        val = args[0] if args else ""
        # Change volume to specified level (/volume 30 or /volume 75)
        player_audio.change_volume(state, val)
    elif base == "/mute":
        player_audio.handle_mute_command(state, "/mute")
    elif base == "/unmute":
        player_audio.handle_mute_command(state, "/unmute")

    # Help Commands (player_help.py)
    elif base.startswith("/help"):
        topic = args[0] if len(args) == 1 else None
        player_help.print_help(topic)

    # SPRINT 2 COMMANDS:
    # Playlists basic (S2-01, S2-05, S2-06, S2-10)
    elif base == "/pl.new":
        name = " ".join(args) if args else ""
        playlists_basic.create_playlist(state, name)
    elif base == "/pl.rename":
        if len(args) < 2:
            print("[main] Usage: /pl.rename <old> <new>")
        else:
            old, new = args[0], " ".join(args[1:])
            playlists_basic.rename_playlist(state, old, new)
    elif base == "/pl.del":
        if not args:
            print("[main] Usage: /pl.del <name|index>")
        else:
            playlists_basic.delete_playlist(state, args[0])
    elif base == "/pl.list":
        playlists_basic.list_playlists(state)
    elif base == "/pl.open":
        if not args:
            print("[main] Usage: /pl.open <name|index>")
        else:
            playlists_basic.open_playlist(state, args[0])
    elif base == "/pl.show":
        playlists_basic.show_current_playlist(state)
    elif base == "/pl.play":
        # /pl.play           -> play active playlist
        # /pl.play MyMix    -> play named/indexed playlist
        if args:
            playlists_basic.play_playlist(state, args[0])
        else:
            playlists_basic.play_active_playlist(state)
    elif base == "/pl.close":
            playlists_basic.close_playlist(state)

    # Playlist edit (S2-02, S2-07, S2-08)
    elif base == "/pl.add":
        if len(args) < 2:
            print("[main] Usage: /pl.add <playlist> <library-index>")
        else:
            playlists_edit.add_track_from_library(state, args[0], args[1])
    elif base == "/pl.remove":
        if len(args) < 2:
            print("[main] Usage: /pl.remove <playlist> <playlist-index>")
        else:
            playlists_edit.remove_track_from_playlist(state, args[0], args[1])
    elif base == "/pl.move":
        if len(args) < 3:
            print("[main] Usage: /pl.move <playlist> <from> <to>")
        else:
            playlists_edit.move_track_within_playlist(state, args[0], args[1], args[2])

    # Playlist advanced (S2-11, S2-12)
    elif base == "/pl.merge":
        if len(args) < 2:
            print("[main] Usage: /pl.merge <target> <source> [dedupe|all]")
        else:
            target, source = args[0], args[1]
            dedupe = True
            if len(args) >= 2 and args[2].lower() in {"all", "keepdups"}:
                dedupe = False
            playlists_advanced.merge_playlists(state, target, source, dedupe=dedupe)
    elif base == "/scan":
        library_search_scan.rescan_for_new_tracks(state)
    elif base == "/pl.copy":
        if len(args) < 2:
            print("[main] Usage: /pl.copy <source> <new-name>")
        else:
            source, new_name = args[0], " ".join(args[1:])
            playlists_advanced.copy_playlist(state, source, new_name)

    # Library search & views (S2-03, S2-04, S2-09)
    elif base == "/search":
        q = " ".join(args) if args else ""
        library_search_scan.search_library(state, q)
    elif base == "/songs":
        library_search_scan.view_songs_table(state)
    elif base == "/artists":
        library_search_scan.view_artists_table(state)
    elif base == "/albums":
        library_search_scan.view_albums_table(state)
    elif base == "/scan":
        library_search_scan.rescan_for_new_tracks(state)

    # SPRINT 3 COMMANDS

    # S3-01: Shuffle (Sunny)
    elif base == "/shuffle":
        player_queue.toggle_shuffle(state)

    # S3-02: Loop
    elif base == "/loop":
        if not args:
            print("[main] Usage: /loop <off|one|all>")
        else:
            player_queue.set_loop_mode(state, args[0])

    # S3-03: View Queue/History
    elif base == "/queue":
        player_queue.show_queue(state)

    # S3-04: Add to Queue
    elif base == "/q.add":
        player_queue.add_to_queue(state, " ".join(args))
    # S3-04: Remove from Queue
    elif base == "/q.remove":
        player_queue.remove_from_queue(state, " ".join(args))
    # S3-05: Play Next
    elif base == "/playnext":
        player_queue.play_next(state, " ".join(args))
    # S3-06: Clear Queue
    elif base == "/q.clear":
        player_queue.clear_queue(state)
    # S3-07: Playback Speed
    elif base == "/speed":
        try:
            player_core.set_playback_speed(state, float(args[0]))
        except (IndexError, ValueError):
            print("Usage: /speed <0.5 - 2.0>")
    # S3-08: Like a song
    elif base == "/like":
        player_metrics.toggle_like(state)

    # S3-09: View Liked
    elif base == "/likes":
        player_metrics.show_liked_songs(state)
    # S3-10: Sort Playlist
    elif base == "/pl.sort":
        if len(args) < 2:
            print("Usage: /pl.sort <playlist> <artist|title|duration>")
        else:
            playlists_basic.sort_playlist(state, args[0], args[1])

    elif base == "/top":
        player_metrics.show_top_tracks(state)

    # S3-12: Sleep Timer
    elif base == "/sleep":
        try:
            player_core.set_sleep_timer(state, float(args[0]))
        except (IndexError, ValueError):
            print("Usage: /sleep <minutes>")

    # Sprint 4 Commands
    # S4-04: Import Songs
    elif base == "/import":
        player_io.import_song(state, " ".join(args))
    # S4-05: Add, List & Filter Tag
    elif base == "/tag.add":
        if len(args) < 2:
            print("Usage: /tag.add <song-index> <tag>")
        else:
            player_config.add_tag(state, args[0], args[1])
    elif base == "/tags":
        player_config.list_all_tags(state)
    elif base == "/tag.filter":
        if not args:
            print("[tags] Usage: /tag.play <tag_name>")
        else:
            player_config.filter_by_tag(state, args[0])

    # S4-02: Schedule Playback
    elif base == "/schedule":
        player_time.set_alarm(state, args[0] if args else "")
    elif base == "/schedule.cancel":
        player_time.cancel_alarm(state)

    # S4-06: Recently Added
    elif base == "/recent":
        player_time.show_recently_added(state)

   # S4-08: Playback Statistics
    elif base == "/stats":
        player_config.view_stats(state)

    # S4-11: Update Metadata
    elif base == "/edit":
        if len(args) >= 3:
            player_io.update_metadata(state, args[0], args[1], " ".join(args[2:]))
        else:
            print("Usage: /edit <index> <title|artist> <value>")
    elif base == "/pl.export":
        player_io.export_playlist(state, args[0], args[1] if len(args) > 1 else "") if args else print(
            "Usage: /pl.export <playlist>")

    #S4-07: User Profile Switch
    elif base == "/profile.new":
        user_data.create_profile(state, args[0] if args else "")
    elif base == "/profile.switch":
        user_data.switch_profile(state, args[0] if args else "")
    elif base == "/profiles":
        user_data.list_profiles(state)
    elif base == "/profile":
        user_data.show_current_profile(state)

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

    # S4-01: Load previous state from JSON file
    player_config.load_settings(state)

    # Load previously held metric data from start up (the JSON file)
    player_metrics.load_data(state)

    # S4-03: Load resume state from previous session
    player_time.load_resume_state(state)

    # Startup display welcome message and available commands summary
    print("Music Player – Sprint 4")
    print(
        "Core: /play /pause /stop /next /prev /seek /rw /ff /volume /mute /unmute "
        "/info /progress /bar /list /help /quit /speed /sleep"
    )
    print(
        "Queue: /queue /q.add /q.remove /playnext /q.clear /shuffle /loop"
    )
    print(
        "Playlists: /pl.new /pl.rename /pl.del /pl.list /pl.open /pl.show "
        "/pl.play /pl.close /pl.add /pl.remove /pl.move /pl.merge /pl.copy /pl.sort"
    )
    print("Library & Stats: /search /songs /artists /albums /scan /like /likes /top")
    print("Scheduling: /schedule HH:MM, /schedule.cancel, /recent")

    # start background playback thread
    stop_event = threading.Event()
    playback_thread = threading.Thread(
        target=_playback_worker,
        args=(state, stop_event),
        daemon=True,
    )
    playback_thread.start()
    # Get user command input
    try:
        while True:
            try:
                command = input("> ")
            except (EOFError, KeyboardInterrupt):
                # Exit on Ctrl+C or Ctrl+D commands
                break
            # Handle the command and check if we should quit
            if not handle_command(state, command):
                break
    finally:
        # S4-03: Save Resume State BEFORE stopping
        player_time.save_resume_state(state)
        # Stop background playback loop
        stop_event.set()
        playback_thread.join(timeout=1.0)
        # S4-01: Save settings to JSON file
        player_config.save_settings(state)

        # Ensure audio is stopped
        state.audio_engine.stop()


if __name__ == "__main__":
    main()