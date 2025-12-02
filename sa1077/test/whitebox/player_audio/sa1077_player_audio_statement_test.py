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

def test_stmt_change_volume_state_none_does_not_crash():
    """
    Statement test:
    - Covers the early-return path when state is None.
    - Ensures no exception is raised.
    """
    change_volume(None, "50")  # type: ignore[arg-type]


def test_stmt_change_volume_empty_input_prints_current_volume(capsys):
    """
    Statement test:
    - Covers the branch where the input string is empty.
    - Ensures current volume is printed.
    """
    state = make_state()
    state.volume = 42

    change_volume(state, "")
    out = capsys.readouterr().out
    assert "Current Volume: 42%" in out


def test_stmt_change_volume_valid_not_muted_updates_engine(capsys):
    """
    Statement test:
    - Covers the main 'happy path' where the new volume is valid
      and the state is not muted.
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
    Statement test:
    - Covers the path where the player is muted and we change volume,
      causing unmute + saved_volume reset.
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
