from music_player.player_state import PlayerState
# from player_state import PlayerState

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
    if not (0 <= val <= 100):
        print("[audio] Error: Volume must be between 0 and 100.")
        return
    state.volume = val
    if state.is_muted:
        state.is_muted = False
        state.saved_volume = None
        state.audio_engine.set_muted(False)
    state.audio_engine.set_volume(val)
    print(f"[audio] Volume set to {val}%")

def toggle_mute(state: PlayerState) -> None:
    if state is None:
        return
    if state.is_muted:
        state.is_muted = False
        restored = state.saved_volume if state.saved_volume is not None else state.volume
        state.volume = restored
        state.audio_engine.set_muted(False)
        state.audio_engine.set_volume(restored)
        print(f"[audio] Unmuted (volume back to {restored}%)")
        return
    state.is_muted = True
    state.saved_volume = state.volume
    state.audio_engine.set_muted(True)
    state.audio_engine.set_volume(0)
    print("[audio] Muted")

def handle_mute_command(state: PlayerState, raw: str) -> None:
    if state is None:
        return
    cmd = raw.strip().lower()
    if cmd == "/mute":
        if state.is_muted:
            print("[audio] Already muted.")
            return
        toggle_mute(state)
        return
    if cmd == "/unmute":
        if not state.is_muted:
            print("[audio] Already unmuted.")
            return
        toggle_mute(state)
        return
    print("[audio] Unknown mute command.")