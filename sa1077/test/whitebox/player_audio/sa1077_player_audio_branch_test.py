import pytest

from music_player.player_state import PlayerState
from music_player.player_audio import (
    change_volume,
)


class DummyEngine:
    def __init__(self):
        self.last_volume = None
        self.muted = False

    def set_volume(self, val: int):
        self.last_volume = val

    def set_muted(self, flag: bool):
        self.muted = flag


def make_state():
    return PlayerState(tracks=[], audio_engine=DummyEngine())

def test_branch_change_volume_non_numeric_input(capsys):
    """
    Branch test for change_volume:
    - Forces the ValueError path when int() fails,
      exercising the 'must be a number' error branch.
    """
    state = make_state()

    change_volume(state, "abc")
    out = capsys.readouterr().out

    assert "must be a number" in out


def test_branch_change_volume_out_of_range_low(capsys):
    """
    Branch test:
    - Input below 0 triggers 'between 0 and 100' branch.
    """
    state = make_state()

    change_volume(state, "-1")
    out = capsys.readouterr().out

    assert "between 0 and 100" in out


def test_branch_change_volume_out_of_range_high(capsys):
    """
    Branch test:
    - Input above 100 triggers the same 'between 0 and 100' branch.
    """
    state = make_state()

    change_volume(state, "101")
    out = capsys.readouterr().out

    assert "between 0 and 100" in out


def test_branch_change_volume_while_muted_unmutes_and_sets_volume(capsys):
    """
    Branch test:
    - Specifically targets the branch where is_muted is True and
      change_volume must unmute and clear saved_volume.
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
