from typing import Optional

def print_help(command: Optional[str] = None) -> None:
    if command is None or command.strip() == "":
        print("--- Help: Available Commands ---")
        print("Commands: /play, /pause, /stop, /next, /prev, /seek, /rw, /ff")
        print("          /list, /info, /progress, /bar")
        print("          /volume, /mute, /unmute, /quit")
        print("Shortcuts: 'p' (play/pause), 's' (stop), 'm' (mute)")
        print("\nTip: Type '/help <command>' for specific details (e.g. '/help play').")
        return

    topic = command.strip().lower()
    if topic.startswith("/"):
        topic = topic[1:]

    if topic == "play":
        print("\n[Help] /play")
        print("Usage: /play")
        print("Starts playback. If the player is paused, it resumes from the current position.")

    elif topic == "pause":
        print("\n[Help] /pause")
        print("Usage: /pause")
        print("Pauses the current song. Use /play to resume.")

    elif topic == "stop":
        print("\n[Help] /stop")
        print("Usage: /stop")
        print("Stops playback completely and resets the position to the start.")

    elif topic == "next":
        print("\n[Help] /next")
        print("Usage: /next")
        print("Skips to the next song in the library.")

    elif topic == "prev":
        print("\n[Help] /prev")
        print("Usage: /prev")
        print("Goes back to the previous song in the library.")

    elif topic == "seek":
        print("\n[Help] /seek")
        print("Usage: /seek <seconds> or <mm:ss>")
        print("Jumps immediately to a specific time in the track.")

    elif topic == "rw":
        print("\n[Help] /rw")
        print("Usage: /rw")
        print("Rewinds playback by 5 seconds.")

    elif topic == "ff":
        print("\n[Help] /ff")
        print("Usage: /ff")
        print("Fast-forwards playback by 5 seconds.")

    elif topic == "list":
        print("\n[Help] /list")
        print("Usage: /list")
        print("Displays the full playlist and indicates the active song.")

    elif topic == "info":
        print("\n[Help] /info")
        print("Usage: /info")
        print("Displays metadata (Title, Artist) for the current track.")

    elif topic == "progress":
        print("\n[Help] /progress")
        print("Usage: /progress")
        print("Shows the current time position numerically.")

    elif topic == "bar":
        print("\n[Help] /bar")
        print("Usage: /bar")
        print("Displays a visual progress bar representing the song duration.")

    elif topic == "volume":
        print("\n[Help] /volume")
        print("Usage: /volume <0-100>")
        print("Sets the playback volume level.")

    elif topic == "mute":
        print("\n[Help] /mute")
        print("Usage: /mute")
        print("Silences the audio immediately.")

    elif topic == "unmute":
        print("\n[Help] /unmute")
        print("Usage: /unmute")
        print("Restores the volume to its previous level.")

    elif topic == "quit":
        print("\n[Help] /quit")
        print("Usage: /quit")
        print("Exits the music player application.")

    else:
        print(f"Sorry, command '/{topic}' is not recognised.")
        print("Type '/help' to see the full list of valid commands.")