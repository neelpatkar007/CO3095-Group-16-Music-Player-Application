from typing import Optional

def print_help(command: Optional[str] = None) -> None:
    if command is None or command.strip() == "":
        print("--- Help: Available Commands ---")
        print("Commands: /play, /pause, /stop, /next")
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

    else:
        print(f"Sorry, command '/{topic}' is not recognised.")
        print("Type '/help' to see the full list of valid commands.")