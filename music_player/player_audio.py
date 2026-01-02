from music_player.player_state import PlayerState
# from player_state import PlayerState

#S1-04: Change_volume function that meets code complexity requirement
def change_volume(state: PlayerState, raw_input: str) -> None:
    '''
    Handles volume change command.
    Sets audio engine volume and automatically unmutes if muted.
    '''
    if state is None:
        return

    # Check to ensure state object has necessary attributes
    if not hasattr(state, 'volume') or not hasattr(state, 'audio_engine'):
        return

    # If no argument show current volume
    if not raw_input:
        print(f"[audio] Current Volume: {state.volume}%")
        return

    # Ensure input is a string or number before conversion
    if not isinstance(raw_input, (str, int, float)):
        return

    # Input validation must be integer 0-100
    try:
        val = int(raw_input)
    except (ValueError, TypeError):
        print("[audio] Error: Volume must be a number.")
        return

    # Check range
    if not (0 <= val <= 100):
        print("[audio] Error: Volume must be between 0 and 100.")
        return

    # Set new volume in the state
    state.volume = val

    # Setting volume unmutes if currently muted
    if getattr(state, 'is_muted', False):
        state.is_muted = False
        state.saved_volume = None  # clear saved volume

        # Check audio engine method existence
        if state.audio_engine and hasattr(state.audio_engine, 'set_muted'):
            state.audio_engine.set_muted(False)  # unmute

    # Apply volume to audio engine
    if state.audio_engine and hasattr(state.audio_engine, 'set_volume'):
        state.audio_engine.set_volume(val)

    print(f"[audio] Volume set to {val}%")

#S1-09: Toggle_mute function that meets code complexity requirement
def toggle_mute(state: PlayerState) -> None:
    '''
    Toggles mute state and saves/restores volume as needed.
    '''
    if state is None:
        return

    # Check for required state attributes
    if not hasattr(state, 'is_muted') or not hasattr(state, 'audio_engine'):
        return

    if state.is_muted:
        # Unmute logic
        state.is_muted = False

        # Restore saved volume if available
        saved = getattr(state, 'saved_volume', None)
        restored = saved if saved is not None else getattr(state, 'volume', 50)

        # Update state and backend
        state.volume = restored

        # Check audio engine methods
        if state.audio_engine:
            if hasattr(state.audio_engine, 'set_muted'):
                state.audio_engine.set_muted(False)  # Clear temp mute
            if hasattr(state.audio_engine, 'set_volume'):
                state.audio_engine.set_volume(restored)

        print(f"[audio] Unmuted (volume back to {restored}%)")
        return

    # Mute logic
    state.is_muted = True

    # Save current volume
    state.saved_volume = getattr(state, 'volume', 0)

    # Set volume to 0 in backend
    # Check audio engine methods
    if state.audio_engine:
        if hasattr(state.audio_engine, 'set_muted'):
            state.audio_engine.set_muted(True)
        if hasattr(state.audio_engine, 'set_volume'):
            state.audio_engine.set_volume(0)

    print("[audio] Muted")


def handle_mute_command(state: PlayerState, raw: str) -> None:
    '''
    Handles /mute and /unmute commands.
    Acts as a wrapper around toggle_mute to prevent any double toggles
    '''
    if state is None:
        return

    # Validate input type
    if not isinstance(raw, str):
        return

    cmd = raw.strip().lower()

    # Ensure state has is_muted attribute
    is_muted = getattr(state, 'is_muted', False)

    if cmd == "/mute":
        # Only mute if not already muted
        if is_muted:
            print("[audio] Already muted.")
        else:
            toggle_mute(state)
    elif cmd == "/unmute":
        # Only unmute if currently muted
        if not is_muted:
            print("[audio] Already unmuted.")
        else:
            toggle_mute(state)
    else:
        print("[audio] Unknown mute command.")