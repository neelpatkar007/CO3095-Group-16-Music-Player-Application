import pytest

from music_player.player_state import PlayerState
from music_player.player_audio import (
    toggle_mute,
    handle_mute_command,
)


class DummyEngine:
    """Mock audio engine used to verify mute state transitions and volume memory."""
    def __init__(self):
        self.last_volume = None
        self.muted = False

    def set_volume(self, val: int):
        self.last_volume = val

    def set_muted(self, flag: bool):
        self.muted = flag


def make_state():
    """Factory helper to initialise a PlayerState with a clean test double engine."""
    return PlayerState(tracks=[], audio_engine=DummyEngine())

def test_branch_toggle_mute_mutes_when_unmuted(capsys):
    """
        Branch Test: Transition to Muted.
        Exercises the branch where is_muted is False, verifying that the
        current volume is cached in 'saved_volume' before silencing.
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
        Branch Test: Transition to Unmuted.
        Exercises the branch where is_muted is True, ensuring the 'saved_volume'
        is correctly restored to both the state and the audio engine.
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
        Branch Test: Command-based Muting.
        Verifies the specific branch for the '/mute' string command
        when the player is in an active (unmuted) state.
        """
    state = make_state()
    state.is_muted = False

    handle_mute_command(state, "/mute")
    out = capsys.readouterr().out

    assert state.is_muted is True
    assert "Muted" in out


def test_branch_handle_mute_command_mute_when_already_muted(capsys):
    """
        Branch Test: Mute Redundancy.
        Exercises the decision path for the '/mute' command when the
        player is already muted, ensuring no state corruption occurs.
        """
    state = make_state()
    state.is_muted = True

    handle_mute_command(state, "/mute")
    out = capsys.readouterr().out

    assert "Already muted" in out


def test_branch_handle_mute_command_unmute_when_muted(capsys):
    """
        Branch Test: Command-based Unmuting.
        Verifies the specific branch for the '/unmute' string command
        when the player is in a silenced (muted) state.
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
        Branch Test: Unmute Redundancy.
        Exercises the decision path for '/unmute' when the player is
        already active, verifying the appropriate console feedback.
        """
    state = make_state()
    state.is_muted = False

    handle_mute_command(state, "/unmute")
    out = capsys.readouterr().out

    assert "Already unmuted" in out


def test_branch_handle_mute_command_unknown(capsys):
    """
        Branch Test: Default/Error Branch.
        Exercises the final 'else' statement in the command handler
        to verify resilience against unrecognised mute commands.
        """
    state = make_state()

    handle_mute_command(state, "/something-else")
    out = capsys.readouterr().out

    assert "Unknown mute command" in out