import pytest

from music_player.player_state import PlayerState
from music_player.player_audio import (
    toggle_mute,
    handle_mute_command,
)


# Test: A fake audio engine used to check how mute and volume settings change
class DummyEngine:
    def __init__(self):
        self.last_volume = None
        self.muted = False

    def set_volume(self, val: int):
        self.last_volume = val

    def set_muted(self, flag: bool):
        self.muted = flag


# Test: Helper function to create a clean player state for each test
def make_state():
    return PlayerState(tracks=[], audio_engine=DummyEngine())


# Test: checking that muting the audio saves the current volume level before silencing
def test_stmt_toggle_mute_mutes_from_unmuted(capsys):
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


# Test: verifying that unmuting restores the previously saved volume level correctly
def test_stmt_toggle_mute_unmutes_restoring_saved_volume(capsys):
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


# Test: ensuring the system doesn't crash if the player state is missing when a mute command is sent
def test_stmt_handle_mute_state_none_does_not_crash():
    handle_mute_command(None, "/mute")  # type: ignore[arg-type]


# Test: checking that the '/mute' command successfully silences the player
def test_stmt_handle_mute_command_mute_when_unmuted(capsys):
    state = make_state()
    handle_mute_command(state, "/mute")
    out = capsys.readouterr().out

    assert state.is_muted is True
    assert "Muted" in out


# Test: checking that the '/unmute' command successfully turns the sound back on
def test_stmt_handle_mute_command_unmute_when_muted(capsys):
    state = make_state()
    state.is_muted = True
    state.saved_volume = state.volume

    handle_mute_command(state, "/unmute")
    out = capsys.readouterr().out

    assert state.is_muted is False
    assert "Unmuted" in out


# Test: verifying that the system shows an error if an unrecognised mute command is entered
def test_stmt_handle_mute_command_unknown_command(capsys):
    state = make_state()
    handle_mute_command(state, "/something")
    out = capsys.readouterr().out

    assert "Unknown mute command" in out