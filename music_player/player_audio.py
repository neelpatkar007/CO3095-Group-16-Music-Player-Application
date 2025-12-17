from music_player.player_state import PlayerState
# from player_state import PlayerState

def change_volume(state: PlayerState, raw_input: str) -> None:
    '''
    Handles volume change command.
    Sets audio engine volume and automatically unmutes if muted.
    '''
    if state is None:
        return

    # If no argument, show current volume
    if not raw_input:
        print(f"[audio] Current Volume: {state.volume}%")
        return

    # Input validation - must be integer 0-100
    try:
        val = int(raw_input)
    except ValueError:
        print("[audio] Error: Volume must be a number.")
        return

    # Check range
    if not (0 <= val <= 100):
        print("[audio] Error: Volume must be between 0 and 100.")
        return

    # Set new volume in the state
    state.volume = val

    # Setting volume unmutes if currently muted
    if state.is_muted:
        state.is_muted = False
        state.saved_volume = None # clear saved volume
        state.audio_engine.set_muted(False) # unmute

    # Apply volume to audio engine
    state.audio_engine.set_volume(val)
    print(f"[audio] Volume set to {val}%")

def toggle_mute(state: PlayerState) -> None:
    '''
    Toggles mute state and saves/restores volume as needed.
    '''
    if state is None:
        return

    if state.is_muted:
        # Unmute logic
        state.is_muted = False

        # Restore saved volume if available
        restored = state.saved_volume if state.saved_volume is not None else state.volume

        # Update state and backend
        state.volume = restored
        state.audio_engine.set_muted(False) # Clear temp mute
        state.audio_engine.set_volume(restored)
        print(f"[audio] Unmuted (volume back to {restored}%)")
        return

    # Mute logic
    state.is_muted = True

    # Save current volume
    state.saved_volume = state.volume

    # Set volume to 0 in backend
    state.audio_engine.set_muted(True)
    state.audio_engine.set_volume(0)
    print("[audio] Muted")

def handle_mute_command(state: PlayerState, raw: str) -> None:
    '''
    Handles /mute and /unmute commands.
    '''
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

    # Unknown command
    print("[audio] Unknown mute command.")