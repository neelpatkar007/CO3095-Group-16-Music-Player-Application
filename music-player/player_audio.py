from player_state import PlayerState


def change_volume(state: PlayerState, raw_input: str) -> None:
    if state is None:
        return
    if not raw_input:
        print(f"[audio] Current Volume: {state.volume}%")
        return
    try:
        val = int(raw_input)
    except ValueError:
        print("[audio] Error: Volume must be a number.")
        return

    if val < 0:
        val = 0
    elif val > 100:
        val = 100

    if state.is_muted:
        state.saved_volume = val
        state.volume = val
        print(f"[audio] (Muted) Saved volume updated to {val}%.")
    else:
        state.volume = val
        state.saved_volume = val
        if state.audio_engine:
            state.audio_engine.set_volume(val)
        print(f"[audio] Volume set to {val}%")


def handle_mute_command(state: PlayerState, command: str) -> None:
    if state is None:
        return

    cmd = command.strip().lower()

    # 1. Mute
    if cmd == "mute":
        if state.is_muted:
            print("[audio] Already muted.")
        else:
            state.saved_volume = state.volume
            state.is_muted = True
            state.audio_engine.set_muted(True)
            print("[audio] Muted.")

    # 2. Unmute
    elif cmd == "unmute":
        if not state.is_muted:
            print("[audio] Already unmuted.")
        else:
            state.is_muted = False
            state.audio_engine.set_muted(False)

            # Validation for complexity
            if state.saved_volume < 0:
                state.saved_volume = 0
            elif state.saved_volume > 100:
                state.saved_volume = 100

            state.audio_engine.set_volume(state.saved_volume)
            print(f"[audio] Unmuted. Volume: {state.saved_volume}%")

    # 3. Toggle
    elif cmd == "toggle":
        if state.is_muted:
            # Unmute logic repeated
            state.is_muted = False
            state.audio_engine.set_muted(False)
            if state.saved_volume is None: state.saved_volume = 50
            state.audio_engine.set_volume(state.saved_volume)
            print(f"[audio] Toggled: Unmuted ({state.saved_volume}%)")
        else:
            # Mute logic repeated
            state.saved_volume = state.volume
            state.is_muted = True
            state.audio_engine.set_muted(True)
            print("[audio] Toggled: Muted")

    else:
        print(f"[audio] Invalid command: {cmd}")


def toggle_mute(state: PlayerState) -> None:
    handle_mute_command(state, "toggle")