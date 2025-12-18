import pytest

from music_player.player_state import PlayerState
from music_player.player_audio import (
    change_volume,
)


class DummyEngine:
    """Mock audio engine used to verify volume and mute state transitions."""
    def __init__(self):
        self.last_volume = None
        self.muted = False

    def set_volume(self, val: int):
        self.last_volume = val

    def set_muted(self, flag: bool):
        self.muted = flag


def make_state():
    """Factory helper to initialise a consistent PlayerState for branch testing."""
    return PlayerState(tracks=[], audio_engine=DummyEngine())

def test_branch_change_volume_non_numeric_input(capsys):
    """
        Branch Test: ValueError Exception Path.
        Forces the execution of the error-handling branch when int() conversion fails
        due to non-numeric string input.
        """
    state = make_state()

    change_volume(state, "abc")
    out = capsys.readouterr().out

    assert "must be a number" in out


def test_branch_change_volume_out_of_range_low(capsys):
    """
        Branch Test: Lower Boundary Range Check.
        Exercises the decision path triggered when a numeric input is below the
        allowable 0-100 threshold.
        """
    state = make_state()

    change_volume(state, "-1")
    out = capsys.readouterr().out

    assert "between 0 and 100" in out


def test_branch_change_volume_out_of_range_high(capsys):
    """
        Branch Test: Upper Boundary Range Check.
        Exercises the same range-validation branch using an input exceeding
        the maximum volume limit.
        """
    state = make_state()

    change_volume(state, "101")
    out = capsys.readouterr().out

    assert "between 0 and 100" in out


def test_branch_change_volume_while_muted_unmutes_and_sets_volume(capsys):
    """
        Branch Test: Mute State Auto-Correction.
        Specifically targets the logic fork where the player is currently muted.
        Verifies the branch that clears saved_volume and updates the engine status.
        """
    state = make_state()
    engine: DummyEngine = state.audio_engine  # type: ignore[assignment]

    state.volume = 20
    state.is_muted = True
    state.saved_volume = 10

    change_volume(state, "50")
    out = capsys.readouterr().out

    assert state.is_muted is False
    assert state.saved_volume is None
    assert engine.muted is False
    assert engine.last_volume == 50
    assert "Volume set to 50%" in out
