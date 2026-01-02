from typing import Optional


def print_help(command: Optional[str] = None) -> None:
    '''
    Displays help information for the music player commands.
    Provides detailed instructions for specific command
    If not given a command, shows the full list of commands.
    '''

    # If they just type /help, give them the full run-down
    if command is None or command.strip() == "":
        print("--- Music Player: Help Menu ---")

        # The essential playback stuff
        print("Playback:   /play, /pause, /stop, /next, /prev, /seek, /rw, /ff")
        print("Volume:     /volume, /mute, /unmute")

        # Playlist tools from Sprint 2
        print("Playlists:  /pl.new, /pl.rename, /pl.del, /pl.list, /pl.open, /pl.show,")
        print("            /pl.play, /pl.close, /pl.add, /pl.remove, /pl.move,")
        print("            /pl.merge, /pl.copy, /pl.sort, /pl.export")

        # Queue and more advanced bits from Sprint 3
        print("Queue:      /queue, /q.add, /q.remove, /playnext, /q.clear, /shuffle, /loop")
        print("Advanced:   /speed, /sleep, /like, /likes, /top, /rate, /rated, /stats")

        # Library, Tags, and Profile management from Sprint 4
        print("Library:    /search, /songs, /artists, /albums, /scan, /recent, /import, /edit, /advanced.search")
        print("Tags:       /tag.add, /tags, /tag.filter")
        print("Profiles:   /profile, /profiles, /profile.new, /profile.switch")
        print("System:     /schedule, /schedule.cancel, /info, /progress, /bar, /quit")

        print("\nKeyboard Shortcuts: 'p' (toggle), 's' (stop), 'm' (mute)")
        print("\nTip: Need details? Try '/help schedule' or '/help profile'.")
        return

    # Input Normalisation
    # Clean up the input so both /play and play work fine
    # Strip whitespace and lowercase for case-insensitivity matching
    topic = command.strip().lower()
    if topic.startswith("/"):
        topic = topic[1:]

    # BASIC PLAYBACK COMMANDS
    if topic == "play":
        print("\n[Help] /play")
        print("Starts the music. If a session was saved, it picks up from where you left off.")
    elif topic == "pause":
        print("\n[Help] /pause")
        print("Pauses the audio. Use /play to keep going.")
    elif topic == "stop":
        print("\n[Help] /stop")
        print("Stops the audio and winds the song back to the start (00:00).")
    elif topic == "next":
        print("\n[Help] /next")
        print("Skips to the next track in the queue or playlist.")
    elif topic == "prev":
        print("\n[Help] /prev")
        print("Goes back to the previous track.")
    elif topic == "seek":
        print("\n[Help] /seek <time>")
        print("Jump to a specific time. Use seconds (90) or mm:ss (1:30).")
    elif topic == "rw":
        print("\n[Help] /rw")
        print("Rewind: jumps back 5 seconds.")
    elif topic == "ff":
        print("\n[Help] /ff")
        print("Fast-forward: jumps ahead 5 seconds.")

    # VOLUME CONTROLS
    elif topic in ["volume", "vol"]:
        print("\n[Help] /volume <0-100>")
        print("Adjust the loudness. e.g. /volume 25 for a bit of background music.")
    elif topic == "mute":
        print("\n[Help] /mute")
        print("Silences the sound without stopping the track.")
    elif topic == "unmute":
        print("\n[Help] /unmute")
        print("Turns the sound back on to the previous level.")

    # QUEUE & ADVANCED (Sprint 3)
    elif topic == "shuffle":
        print("\n[Help] /shuffle")
        print("Toggles random playback mode.")
    elif topic == "loop":
        print("\n[Help] /loop <off|one|all>")
        print("Set repeat mode. 'one' repeats the current track, 'all' repeats the whole list.")
    elif topic == "queue":
        print("\n[Help] /queue")
        print("Shows recently played songs and what's coming up next.")
    elif topic == "q.add":
        print("\n[Help] /q.add <index|name>")
        print("Adds a song from the library to the end of the queue.")
    elif topic == "q.remove":
        print("\n[Help] /q.remove <index|name>")
        print("Removes a specific song from the queue.")
    elif topic == "playnext":
        print("\n[Help] /playnext <index|name>")
        print("Pops a song right after the current one.")
    elif topic == "q.clear":
        print("\n[Help] /q.clear")
        print("Clears everything from the upcoming queue.")
    elif topic == "speed":
        print("\n[Help] /speed <0.5-2.0>")
        print("Changes playback speed. 1.0 is the normal speed.")
    elif topic == "sleep":
        print("\n[Help] /sleep <minutes>")
        print("Sets a timer to stop the music automatically.")

    # METRICS & RATINGS (Sprint 3 & 4)
    elif topic == "like":
        print("\n[Help] /like")
        print("Toggles the 'Liked' status for the current song.")
    elif topic == "likes":
        print("\n[Help] /likes")
        print("Lists all the songs you've liked.")
    elif topic == "top":
        print("\n[Help] /top")
        print("Shows your most-played tracks.")
    elif topic == "rate":
        print("\n[Help] /rate <rating>")
        print("Rate the current song. Use /rated to see all your scores.")
    elif topic == "rated":
        print("\n[Help] /rated")
        print("Check all the songs you have rated.")
    elif topic == "stats":
        print("\n[Help] /stats")
        print("Shows your listening stats and playback data.")

    # PLAYLIST MANAGEMENT
    elif topic == "pl.new":
        print("\n[Help] /pl.new <name>")
        print("Creates a brand new, empty playlist.")
    elif topic == "pl.rename":
        print("\n[Help] /pl.rename <target> <new_name>")
        print("Change the name of a playlist.")
    elif topic == "pl.del":
        print("\n[Help] /pl.del <name|index>")
        print("Deletes a playlist permanently.")
    elif topic == "pl.list":
        print("\n[Help] /pl.list")
        print("Shows all the playlists you've made.")
    elif topic == "pl.open":
        print("\n[Help] /pl.open <name|index>")
        print("Opens up a playlist so you can view or edit it.")
    elif topic == "pl.show":
        print("\n[Help] /pl.show")
        print("Lists all the tracks in the playlist you've currently got open.")
    elif topic == "pl.play":
        print("\n[Help] /pl.play [name|index]")
        print("Starts playing a playlist.")
    elif topic == "pl.close":
        print("\n[Help] /pl.close")
        print("Closes the playlist view.")
    elif topic == "pl.export":
        print("\n[Help] /pl.export <playlist>")
        print("Saves the playlist to a file.")
    elif topic == "pl.sort":
        print("\n[Help] /pl.sort <playlist> <artist|title|duration>")
        print("Sorts a playlist out based on your choice.")

    # PLAYLIST EDITING
    elif topic == "pl.add":
        print("\n[Help] /pl.add <playlist> <library-index>")
        print("Adds a song from the main library to a playlist.")
    elif topic == "pl.remove":
        print("\n[Help] /pl.remove <playlist> <index>")
        print("Removes a track from a playlist.")
    elif topic == "pl.move":
        print("\n[Help] /pl.move <playlist> <from> <to>")
        print("Moves a track to a different spot in the playlist.")
    elif topic == "pl.merge":
        print("\n[Help] /pl.merge <target> <source> [dedupe|all]")
        print("Squashes two playlists together.")
    elif topic == "pl.copy":
        print("\n[Help] /pl.copy <source> <new_name>")
        print("Makes a copy of an existing playlist.")

    # LIBRARY & TAGS
    elif topic == "search":
        print("\n[Help] /search <text> or /advanced.search <query>")
        print("Search for songs by title, artist, or tags.")
    elif topic == "songs":
        print("\n[Help] /songs")
        print("See your whole music library.")
    elif topic == "artists":
        print("\n[Help] /artists")
        print("View the library grouped by Artist.")
    elif topic == "albums":
        print("\n[Help] /albums")
        print("View the library grouped by Album/Folder.")
    elif topic == "scan":
        print("\n[Help] /scan")
        print("Scans the folder to look for any new files.")
    elif topic == "recent":
        print("\n[Help] /recent")
        print("Shows what was recently added to the library.")
    elif topic == "import":
        print("\n[Help] /import <file>")
        print("Import a new song file into the library.")
    elif topic == "edit":
        print("\n[Help] /edit <index> <title|artist> <value>")
        print("Fix the info (metadata) for a specific track.")
    elif topic == "tag.add":
        print("\n[Help] /tag.add <song-index> <tag>")
        print("Stick a custom tag on a song.")
    elif topic == "tags":
        print("\n[Help] /tags")
        print("Lists all the tags you've created.")
    elif topic == "tag.filter":
        print("\n[Help] /tag.filter <tag>")
        print("Filter the library to show only tracks with that tag.")

    # PROFILES & SCHEDULING
    elif topic == "profile":
        print("\n[Help] /profile")
        print("Check which profile is currently active.")
    elif topic == "profiles":
        print("\n[Help] /profiles")
        print("Lists every user profile.")
    elif topic == "profile.new":
        print("\n[Help] /profile.new <name>")
        print("Creates a new profile.")
    elif topic == "profile.switch":
        print("\n[Help] /profile.switch <name>")
        print("Switch over to a different profile.")
    elif topic == "schedule":
        print("\n[Help] /schedule <HH:MM>")
        print("Set the music to start playing at a specific time.")
    elif topic == "schedule.cancel":
        print("\n[Help] /schedule.cancel")
        print("Turns off any active playback alarms.")

    # UI & SYSTEM
    elif topic == "info":
        print("\n[Help] /info")
        print("Shows info about the song currently playing.")
    elif topic == "progress":
        print("\n[Help] /progress")
        print("Shows how far through the track you are.")
    elif topic == "bar":
        print("\n[Help] /bar")
        print("Displays a visual progress bar.")
    elif topic == "list":
        print("\n[Help] /list")
        print("Shows the queue with an indicator for what's playing.")
    elif topic in ["quit", "exit", "q"]:
        print("\n[Help] /quit")
        print("Saves your data and shuts down the app.")
    else:
        # Fallback for when they type something that doesn't exist
        print(f"I couldn't find a command named '/{topic}'.")
        print("Try '/help' to see the full list.")