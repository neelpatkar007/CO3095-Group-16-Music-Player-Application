from player_state import PlayerState


def change_volume(state: PlayerState, raw_input: str) -> None:
    if state is None:
        print("[audio] Error: State is None")
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
        print("[audio] Warning: Clamped volume to minimum (0).")
    elif val > 100:
        val = 100
        print("[audio] Warning: Clamped volume to maximum (100).")

    if val == 0:
        print("[audio] Volume set to silence.")
    elif val == 100:
        print("[audio] Volume set to max power.")

    if state.is_muted:
        state.saved_volume = val
        state.volume = val
        print(f"[audio] (Muted) Saved volume updated to {val}%. Audio remains muted.")
    else:
        state.volume = val
        state.saved_volume = val

        if state.audio_engine:
            state.audio_engine.set_volume(val)

        print(f"[audio] Volume set to {val}%")


def toggle_mute(state: PlayerState) -> None:
    pass
