from typing import Optional


def print_help(command: Optional[str] = None) -> None:
    '''
    A helpful guide for the user to navigate the player.
    Covers everything from basic playback to Sprint 3 advanced features.
    '''

    # If the user just types /help, show them the big picture
    # We check if the input is empty or missing to decide whether to show the full list
    if command is None or command.strip() == "":
        print("--- Music Player: Help Menu ---")

        # Grouping by functionality makes it easier for a human to scan
        # These are the basic bread-and-butter playback controls
        print("Playback:  /play, /pause, /stop, /next, /prev, /seek, /rw, /ff")
        print("Volume:    /volume, /mute, /unmute")

        # Sprint 2 Playlist features
        print("Playlists: /pl.new, /pl.rename, /pl.del, /pl.list, /pl.open, /pl.show,")
        print("           /pl.play, /pl.close, /pl.add, /pl.remove, /pl.move,")
        print("           /pl.merge, /pl.copy, /pl.sort")

        # Sprint 3 Queue and Advanced features
        print("Queue:     /queue, /q.add, /q.remove, /playnext, /q.clear, /shuffle, /loop")
        print("Advanced:  /speed, /sleep, /like, /likes, /top")

        # Sprint 2 Library features
        print("Library:   /search, /songs, /artists, /albums, /scan")

        print("Info/UI:   /list, /info, /progress, /bar, /quit")
        print("\nKeyboard Shortcuts: 'p' (toggle), 's' (stop), 'm' (mute)")
        print("\nTip: Need details? Try '/help shuffle' or '/help sleep'.")
        return

    # Normalize the topic so /play and play both work
    # We strip any whitespace and lowercase everything to make the matching more robust
    topic = command.strip().lower()
    if topic.startswith("/"):
        topic = topic[1:]

    # --- BASIC PLAYBACK ---
    if topic == "play":
        print("\n[Help] /play")
        print("Starts the music. If you were paused, it picks up right where you left off.")
    elif topic == "pause":
        print("\n[Help] /pause")
        print("Freeze-frames the audio. Use /play to keep going.")
    elif topic == "stop":
        print("\n[Help] /stop")
        print("Kills the audio and rewinds the song back to the 00:00 mark.")
    elif topic == "next":
        print("\n[Help] /next")
        print("Skips forward to the next track in your current queue or playlist.")
    elif topic == "prev":
        print("\n[Help] /prev")
        print("Jumps back to the previous track.")
    elif topic == "seek":
        print("\n[Help] /seek <time>")
        print("Jump to a specific spot. You can use seconds (90) or mm:ss (1:30).")
    elif topic == "rw":
        print("\n[Help] /rw")
        print("Quick rewind: jumps back 5 seconds.")
    elif topic == "ff":
        print("\n[Help] /ff")
        print("Quick forward: jumps ahead 5 seconds.")

    # --- VOLUME CONTROLS ---
    elif topic == "volume":
        print("\n[Help] /volume <0-100>")
        print("Adjust the loudness. Example: /volume 25 for quiet background music.")
    elif topic == "mute":
        print("\n[Help] /mute")
        print("Silence the output instantly without stopping the track.")
    elif topic == "unmute":
        print("\n[Help] /unmute")
        print("Brings the volume back to where it was before muting.")

    # --- SPRINT 3: QUEUE & ADVANCED ---
    elif topic == "shuffle":
        print("\n[Help] /shuffle")
        print("Toggles random playback. When ON, the next song is picked at random.")
    elif topic == "loop":
        print("\n[Help] /loop <off|one|all>")
        print("Set repeat mode. 'one' repeats the current track, 'all' repeats the whole list.")
    elif topic == "queue":
        print("\n[Help] /queue")
        print("Shows the last 5 played songs (history) and all upcoming songs.")
    elif topic == "q.add":
        print("\n[Help] /q.add <index|name>")
        print("Adds a song from the library to the end of the current playback queue.")
    elif topic == "q.remove":
        print("\n[Help] /q.remove <index|name>")
        print("Removes a specific song from the upcoming queue.")
    elif topic == "playnext":
        print("\n[Help] /playnext <index|name>")
        print("High-priority add: puts a song right after the current one.")
    elif topic == "q.clear":
        print("\n[Help] /q.clear")
        print("Wipes the entire upcoming queue but keeps the current song playing.")
    elif topic == "speed":
        print("\n[Help] /speed <0.5-2.0>")
        print("Changes the playback tempo. 1.0 is normal, 2.0 is double speed.")
    elif topic == "sleep":
        print("\n[Help] /sleep <minutes>")
        print("Sets a timer to stop playback automatically. Use 0 to cancel.")

    # --- SPRINT 3: METRICS & LIKES ---
    elif topic == "like":
        print("\n[Help] /like")
        print("Toggles 'Liked' status for the current track.")
    elif topic == "likes":
        print("\n[Help] /likes")
        print("Displays a list of all your bookmarked/liked tracks.")
    elif topic == "top":
        print("\n[Help] /top")
        print("Shows your most-played tracks based on listening history.")
    elif topic == "pl.sort":
        print("\n[Help] /pl.sort <playlist> <artist|title|duration>")
        print("Reorders a playlist alphabetically by artist/title or by song length.")

    # --- PLAYLIST MANAGEMENT (Sprint 2) ---
    elif topic == "pl.new":
        print("\n[Help] /pl.new <name>")
        print("Creates a fresh, empty playlist. Give it a name like 'Chill' or 'Gym'.")
    elif topic == "pl.rename":
        print("\n[Help] /pl.rename <target> <new_name>")
        print("Change a playlist's name. You can use the current name or its index number.")
    elif topic == "pl.del":
        print("\n[Help] /pl.del <name|index>")
        print("Permanently removes a playlist. Don't worry, the actual songs stay in your library.")
    elif topic == "pl.list":
        print("\n[Help] /pl.list")
        print("Shows all your playlists, how many songs they have, and their total runtime.")
    elif topic == "pl.open":
        print("\n[Help] /pl.open <name|index>")
        print("Peeks inside a playlist and prepares it for playback.")
    elif topic == "pl.show":
        print("\n[Help] /pl.show")
        print("Lists the tracks in the playlist you are currently working with.")
    elif topic == "pl.play":
        print("\n[Help] /pl.play [name|index]")
        print("Starts playing a playlist from song #1. If you don't specify one, it plays the 'open' one.")
    elif topic == "pl.close":
        print("\n[Help] /pl.close")
        print("Leaves the playlist view and goes back to your full music library.")

    # --- PLAYLIST EDITING (Sprint 2) ---
    elif topic == "pl.add":
        print("\n[Help] /pl.add <playlist> <library-index>")
        print("Picks a song from your main library and adds it to the end of a playlist.")
    elif topic == "pl.remove":
        print("\n[Help] /pl.remove <playlist> <index>")
        print("Removes a specific song from a playlist based on its position (number).")
    elif topic == "pl.move":
        print("\n[Help] /pl.move <playlist> <from> <to>")
        print("Reorder your tracks. Move song #5 to position #1, for example.")
    elif topic == "pl.merge":
        print("\n[Help] /pl.merge <target> <source> [dedupe|all]")
        print("Combines two playlists. Use 'dedupe' (default) to skip songs that are already in the target.")
    elif topic == "pl.copy":
        print("\n[Help] /pl.copy <source> <new_name>")
        print("Duplicates a playlist. Useful if you want to branch off a new version of a mix.")

    # --- LIBRARY SEARCH & VIEWS (Sprint 2) ---
    elif topic == "search":
        print("\n[Help] /search <text>")
        print("Look for songs by title, artist, or even the filename. It's case-insensitive.")
    elif topic == "songs":
        print("\n[Help] /songs")
        print("A clean, tabular view of every track you own.")
    elif topic == "artists":
        print("\n[Help] /artists")
        print("Groups your music by Artist, showing how much music you have for each.")
    elif topic == "albums":
        print("\n[Help] /albums")
        print("Groups music by folder name - an easy way to see your 'albums'.")
    elif topic == "scan":
        print("\n[Help] /scan")
        print("Checks your 'songs' folder for new files you've added since the app started.")

    # --- SYSTEM ---
    elif topic == "quit":
        print("\n[Help] /quit")
        print("Exits the app safely. See you next time!")
    else:
        # A gentle fallback in case they typo a command
        print(f"I couldn't find a command named '/{topic}'.")
        print("Try '/help' for any help.")