import pytest

from music_player.player_state import PlayerState
from music_player.player_audio import (
    change_volume,
)


class DummyEngine:
    """Mock engine to verify statement execution without hardware dependencies."""
    def __init__(self):
        self.last_volume = None
        self.muted = False

    def set_volume(self, val: int):
        self.last_volume = val

    def set_muted(self, flag: bool):
        self.muted = flag


def make_state():
    """Initialises a clean PlayerState for individual statement tests."""
    return PlayerState(tracks=[], audio_engine=DummyEngine())

def test_stmt_change_volume_state_none_does_not_crash():
    """
        Statement Test: Null Object Guard.
        Executes the very first lines of the function to verify the
        early-return logic when no state object is provided.
        """
    change_volume(None, "50")  # type: ignore[arg-type]


def test_stmt_change_volume_empty_input_prints_current_volume(capsys):
    """
        Statement Test: Empty String Handling.
        Covers the specific lines responsible for printing the current
        volume level when no new value is supplied.
        """
    state = make_state()
    state.volume = 42

    change_volume(state, "")
    out = capsys.readouterr().out
    assert "Current Volume: 42%" in out


def test_stmt_change_volume_valid_not_muted_updates_engine(capsys):
    """
        Statement Test: Standard Update Path.
        Executes the 'Happy Path' lines where a valid integer is processed
        and passed directly to the audio engine.
        """
    state = make_state()
    engine: DummyEngine = state.audio_engine  # type: ignore[assignment]

    change_volume(state, "37")
    out = capsys.readouterr().out

    assert state.volume == 37
    assert engine.last_volume == 37
    assert "[audio] Volume set to 37%" in out


def test_stmt_change_volume_while_muted_unmutes_and_updates(capsys):
    """
        Statement Test: Mute-Reset Logic.
        Executes the cleanup statements that reset the 'is_muted' flag
        and clear the 'saved_volume' memory when a volume change occurs.
        """
    state = make_state()
    engine: DummyEngine = state.audio_engine  # type: ignore[assignment]
    state.volume = 20
    state.is_muted = True
    state.saved_volume = 10

    change_volume(state, "50")
    out = capsys.readouterr().out

    assert state.volume == 50
    assert state.is_muted is False
    assert state.saved_volume is None
    assert engine.muted is False
    assert engine.last_volume == 50
    assert "Volume set to 50%" in out
