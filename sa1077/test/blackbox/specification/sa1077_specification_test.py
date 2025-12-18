from pathlib import Path

import pytest

from music_player.library import Track
from music_player.player_seek import seek_to, nudge, get_progress
from music_player.player_state import PlayerState
from music_player.player_audio import change_volume

from music_player.player_ui import (
    print_progress,
    print_progress_bar,
)

class DummyEngine:
    def __init__(self):
        self.last_volume = None
        self.muted = False
        self.last_seek: float | None = None

    def set_volume(self, value: int) -> None:
        self.last_volume = value

    def set_muted(self, flag: bool) -> None:
        self.muted = flag

    def seek(self, position: float) -> None:
        """No-op seek; just record the position."""
        self.last_seek = float(position)

    def play(self, path, start_pos: float = 0.0) -> None:
        pass

    def stop(self) -> None:
        pass

    def is_busy(self) -> bool:
        return False


def make_state(volume: int = 30, muted: bool = False) -> PlayerState:
    engine = DummyEngine()
    state = PlayerState(tracks=[], audio_engine=engine)
    state.volume = volume
    state.is_muted = muted
    return state

