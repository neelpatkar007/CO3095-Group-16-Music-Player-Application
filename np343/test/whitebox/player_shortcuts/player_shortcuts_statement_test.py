import pytest

from music_player.player_shortcuts import handle_keypress
from music_player.player_state import PlayerState


class DummyEngine:
    """Minimal stub so PlayerState can be constructed without real audio."""
    pass


def make_state() -> PlayerState:
    '''Helper to create a fresh PlayerState for each test.'''
    return PlayerState(tracks=[], audio_engine=DummyEngine())


# Whitebox statement coverage tests
# These tests aim to execute specific lines within the code to ensure
# that no dead code exists and each and every command is reachable


def test_stmt_key_p_triggers_play_when_not_playing(monkeypatch):
    """
    Whitebox statement coverage test
    Target statement - 'player_core.play(state)'

    Explanation is:
    By setting the 'is_playing' attribute of the PlayerState to False and pressing 'p', we force the execution
    flow to reach and execute the play() statement.

    """
    state = make_state()
    state.is_playing = False

    calls = {}

    def fake_play(st):
        calls["play"] = True

    def fake_pause(st):
        calls["pause"] = True

    monkeypatch.setattr("music_player.player_core.play", fake_play)
    monkeypatch.setattr("music_player.player_core.pause", fake_pause)

    handle_keypress(state, "p")

    # Verification for the play() call was executed
    assert calls.get("play") is True
    assert "pause" not in calls


def test_stmt_key_p_triggers_pause_when_playing(monkeypatch):
    """
    White-Box Statement Coverage.
    Target Statement - `player_core.pause(state)`

    Explanation:
    To ensure each and every line of code is executed, we must test the scenario where
    music is playing.
    This forces the 'if state.is_playing:' condition to be True,
    executing the specific line that calls pause().

    """
    state = make_state()
    # Set the state to Playing to force the code into the 'True' block
    state.is_playing = True

    calls = {}

    def fake_play(st):
        calls["play"] = True

    def fake_pause(st):
        calls["pause"] = True

    monkeypatch.setattr("music_player.player_core.play", fake_play)
    monkeypatch.setattr("music_player.player_core.pause", fake_pause)

    handle_keypress(state, "p")

    # Verification -  The specific statement `player_core.pause(state)` was executed.
    assert calls.get("pause") is True
    assert "play" not in calls

def test_stmt_key_s_triggers_stop(monkeypatch):
    """
    White box statement coverage
    Target statement - 'player_core.stop(state)'

    Explanation is:
    Input of 's' forces the code to enter the elif block. And hence execute the stop() statement.

    """
    state = make_state()
    calls = {}

    def fake_stop(st):
        calls["stop"] = True

    monkeypatch.setattr("music_player.player_core.stop", fake_stop)

    handle_keypress(state, "s")

    # Verification for calling the stop() was executed
    assert calls.get("stop") is True


def test_stmt_key_m_triggers_toggle_mute(monkeypatch):
    """
    White box statement coverage
    Target statement - 'player_audio.toggle_mute(state)'

    Explanation:
    Input of 'm' forces the code to enter the specific elif block and execute the toggle_mute() statement.

    """
    state = make_state()
    calls = {}

    def fake_toggle_mute(st):
        calls["mute"] = True

    monkeypatch.setattr(
        "music_player.player_audio.toggle_mute",
        fake_toggle_mute,
    )

    handle_keypress(state, "m")

    # Verification - the statement for calling the toggle_mute() was executed
    assert calls.get("mute") is True


def test_stmt_unknown_key_prints_message(capsys):
    """
    White box statement coverage
    Target statement is - 'print(f"No action bound to key '{key}'")'

    Explanation is:
    Input of 'x' which is an unmapped key forces the execution of the final else block
    and hence ensuring the print statement is executed.
    """
    state = make_state()

    handle_keypress(state, "x")
    out = capsys.readouterr().out

    # Verification - the print statement for unknown key was executed
    assert "No action bound to key 'x'" in out