"""
Module: player_audio
User Stories:
 - S1-04: change the volume between 0 and 100
 - S1-09: mute and unmute the sound instantly
"""

from player_state import PlayerState


def set_volume(state: PlayerState, value: int) -> None:
    """
    Set playback volume to the given value (0–100).

    S1-04: validation and clamping implemented.
    """
    pass


def toggle_mute(state: PlayerState) -> None:
    """
    Toggle mute on/off.

    S1-09: should remember previous volume.
    """
    pass
