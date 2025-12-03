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

def test_branch_toggle_mute_mutes_when_unmuted(capsys):
    """
    Branch test:
    - Covers the branch where is_muted is initially False.
    """
    state = make_state()
    engine: DummyEngine = state.audio_engine  # type: ignore[assignment]

    state.volume = 25
    state.is_muted = False

    toggle_mute(state)
    out = capsys.readouterr().out

    assert state.is_muted is True
    assert state.saved_volume == 25
    assert engine.muted is True
    assert engine.last_volume == 0
    assert "Muted" in out


def test_branch_toggle_mute_unmutes_when_muted(capsys):
    """
    Branch test:
    - Covers the branch where is_muted is True and we restore saved_volume.
    """
    state = make_state()
    engine: DummyEngine = state.audio_engine  # type: ignore[assignment]

    state.volume = 5
    state.saved_volume = 60
    state.is_muted = True

    toggle_mute(state)
    out = capsys.readouterr().out

    assert state.is_muted is False
    assert state.volume == 60
    assert engine.muted is False
    assert engine.last_volume == 60
    assert "Unmuted (volume back to 60%)" in out

def test_branch_handle_mute_mutes_when_unmuted(capsys):
    """
    Branch test:
    - For '/mute' when is_muted is False.
    """
    state = make_state()
    state.is_muted = False

    handle_mute_command(state, "/mute")
    out = capsys.readouterr().out

    assert state.is_muted is True
    assert "Muted" in out


def test_branch_handle_mute_command_mute_when_already_muted(capsys):
    """
    Branch test:
    - '/mute' when is_muted is already True -> 'Already muted'.
    """
    state = make_state()
    state.is_muted = True

    handle_mute_command(state, "/mute")
    out = capsys.readouterr().out

    assert "Already muted" in out


def test_branch_handle_mute_command_unmute_when_muted(capsys):
    """
    Branch test:
    - '/unmute' when is_muted is True.
    """
    state = make_state()
    state.is_muted = True
    state.saved_volume = state.volume

    handle_mute_command(state, "/unmute")
    out = capsys.readouterr().out

    assert state.is_muted is False
    assert "Unmuted" in out


def test_branch_handle_mute_command_unmute_when_already_unmuted(capsys):
    """
    Branch test:
    - '/unmute' when is_muted is False -> 'Already unmuted'.
    """
    state = make_state()
    state.is_muted = False

    handle_mute_command(state, "/unmute")
    out = capsys.readouterr().out

    assert "Already unmuted" in out


def test_branch_handle_mute_command_unknown(capsys):
    """
    Branch test:
    - Exercises the final else: unknown mute command.
    """
    state = make_state()

    handle_mute_command(state, "/something-else")
    out = capsys.readouterr().out

    assert "Unknown mute command" in out