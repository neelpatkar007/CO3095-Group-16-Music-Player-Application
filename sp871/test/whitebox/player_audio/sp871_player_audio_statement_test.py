import pytest

from music_player.player_state import PlayerState
from music_player.player_audio import (
    toggle_mute,
    handle_mute_command,
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


def test_stmt_toggle_mute_mutes_from_unmuted(capsys):
    """
    Statement test:
    - Covers the path where is_muted is initially False
      and we go into the 'mute' branch.
    """
    state = make_state()
    engine: DummyEngine = state.audio_engine  # type: ignore[assignment]
    state.volume = 30

    toggle_mute(state)
    out = capsys.readouterr().out

    assert state.is_muted is True
    assert state.saved_volume == 30
    assert engine.muted is True
    assert engine.last_volume == 0
    assert "Muted" in out


def test_stmt_toggle_mute_unmutes_restoring_saved_volume(capsys):
    """
    Statement test:
    - Covers the complementary path where is_muted is True and
      we restore the saved volume.
    """
    state = make_state()
    engine: DummyEngine = state.audio_engine  # type: ignore[assignment]
    state.volume = 10
    state.saved_volume = 55
    state.is_muted = True

    toggle_mute(state)
    out = capsys.readouterr().out

    assert state.is_muted is False
    assert state.volume == 55
    assert engine.muted is False
    assert engine.last_volume == 55
    assert "Unmuted (volume back to 55%)" in out

def test_stmt_handle_mute_state_none_does_not_crash():
    """
    Statement test:
    - Covers early return when state is None.
    """
    handle_mute_command(None, "/mute")  # type: ignore[arg-type]


def test_stmt_handle_mute_command_mute_when_unmuted(capsys):
    """
    Statement test:
    - Covers the '/mute' command path where the state is not muted.
    """
    state = make_state()
    handle_mute_command(state, "/mute")
    out = capsys.readouterr().out

    assert state.is_muted is True
    assert "Muted" in out


def test_stmt_handle_mute_command_unmute_when_muted(capsys):
    """
    Statement test:
    - Covers '/unmute' command where state is currently muted.
    """
    state = make_state()
    state.is_muted = True
    state.saved_volume = state.volume

    handle_mute_command(state, "/unmute")
    out = capsys.readouterr().out

    assert state.is_muted is False
    assert "Unmuted" in out


def test_stmt_handle_mute_command_unknown_command(capsys):
    """
    Statement test:
    - Covers the 'unknown command' fallback branch.
    """
    state = make_state()
    handle_mute_command(state, "/something")
    out = capsys.readouterr().out

    assert "Unknown mute command" in out