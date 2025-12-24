import pytest

from music_player.player_state import PlayerState
from music_player.player_audio import (
    change_volume,
)


# Test: A mock audio engine used to check if volume and mute settings change correctly
class DummyEngine:
    """Mock audio engine used to verify volume and mute state transitions."""
    def __init__(self):
        self.last_volume = None
        self.muted = False

    def set_volume(self, val: int):
        self.last_volume = val

    def set_muted(self, flag: bool):
        self.muted = flag


# Test: A helper function to create a fresh player state for testing
def make_state():
    """Factory helper to initialise a consistent PlayerState for branch testing."""
    return PlayerState(tracks=[], audio_engine=DummyEngine())

# Test: checking that the system correctly catches and reports errors when text is entered instead of a number
def test_branch_change_volume_non_numeric_input(capsys):
    state = make_state()

    change_volume(state, "abc")
    out = capsys.readouterr().out

    assert "must be a number" in out


# Test: ensuring the system triggers a range error when the volume input is below zero
def test_branch_change_volume_out_of_range_low(capsys):
    state = make_state()

    change_volume(state, "-1")
    out = capsys.readouterr().out

    assert "between 0 and 100" in out


# Test: ensuring the system triggers a range error when the volume input is above 100
def test_branch_change_volume_out_of_range_high(capsys):
    state = make_state()

    change_volume(state, "101")
    out = capsys.readouterr().out

    assert "between 0 and 100" in out


# Test: verifying that manually changing the volume automatically unmutes the player
def test_branch_change_volume_while_muted_unmutes_and_sets_volume(capsys):
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