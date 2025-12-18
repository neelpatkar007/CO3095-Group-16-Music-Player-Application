import pytest

from music_player.player_state import PlayerState
from music_player.player_audio import (
    toggle_mute,
    handle_mute_command,
)


class DummyEngine:
    """Mock engine developed to verify audio state changes without hardware dependencies."""
    def __init__(self):
        self.last_volume = None
        self.muted = False

    def set_volume(self, val: int):
        self.last_volume = val

    def set_muted(self, flag: bool):
        self.muted = flag


def make_state():
    """Utility to initialise a standardised PlayerState for isolation testing."""
    return PlayerState(tracks=[], audio_engine=DummyEngine())


def test_stmt_toggle_mute_mutes_from_unmuted(capsys):
    """
        Statement Test: Transition to Silenced.
        Exercises the specific branch where the player is currently active, verifying
        volume caching logic.
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
        Statement Test: Restoration Logic.
        Exercises the data restoration path, ensuring 'saved_volume' is correctly
        reassigned to the active engine.
        """
    state = make_state()
    engine: DummyEngine = state.audio_engine  # type: ignore[assignment]
    state.volume = 10
    state.saved_volume = 55
    state.is_muted = True

    toggle_mute(state) # Executes the logic branch responsible for restoring cached audio levels
    out = capsys.readouterr().out

    assert state.is_muted is False
    assert state.volume == 55
    assert engine.muted is False
    assert engine.last_volume == 55
    assert "Unmuted (volume back to 55%)" in out

def test_stmt_handle_mute_state_none_does_not_crash():
    """
        Statement Test: Null Safety Guard.
        Executes the early-return path to ensure system resilience when
        receiving null inputs.
        """
    handle_mute_command(None, "/mute")  # type: ignore[arg-type]


def test_stmt_handle_mute_command_mute_when_unmuted(capsys):
    """
        Statement Test: String Command Parsing (Mute).
        Covers the specific string-match branch used for silencing the
        application via user command.
        """
    state = make_state()
    handle_mute_command(state, "/mute")
    out = capsys.readouterr().out

    assert state.is_muted is True
    assert "Muted" in out


def test_stmt_handle_mute_command_unmute_when_muted(capsys):
    """
        Statement Test: String Command Parsing (Unmute).
        Covers the specific logic fork used for re-activating audio via
        direct command.
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
        Statement Test: Robustness Fallback.
        Exercises the default error-handling path for unrecognised
        input commands.
        """
    state = make_state()
    handle_mute_command(state, "/something")
    out = capsys.readouterr().out

    assert "Unknown mute command" in out