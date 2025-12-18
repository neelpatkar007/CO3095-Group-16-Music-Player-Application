import pytest

from music_player.player_shortcuts import handle_keypress
from music_player.player_state import PlayerState


class DummyEngine:
    """Minimal stub so PlayerState can be constructed without real audio."""
    pass


def make_state() -> PlayerState:
    '''Helped to create a fresh PlayerState for each test'''
    return PlayerState(tracks=[], audio_engine=DummyEngine())


# White-box testing - branch coverage - These tests ensure that each control branch (if/elif/else) in
# the handle_keypress function is executed at least once.

def test_branch_key_p_triggers_play_when_not_playing(monkeypatch):
    """
    White box branch coverage
    The target branch is the nested 'else' block inside the 'p' key check

    Logic:
    1. Input - Key 'p' is pressed
    2. Condition - is_playing is False
    3. Expected Path - Enters 'if key == 'p', fails 'if is_playing', goes to 'else' - calls play()
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

    # Assert - that the play() branch was taken
    assert calls.get("play") is True
    # Assert - that the pause() branch was not taken
    assert "pause" not in calls


def test_branch_key_p_triggers_pause_when_playing(monkeypatch):
    """
    White box branch coverage
    The target branch is the nested 'if' block inside the 'p' key check

    Logic:
    1. Input - Key 'p' is pressed
    2. Condition - is_playing is True
    3. Expected Path - Enters 'if key == 'p', passes 'if is_playing' - calls pause()
    """
    state = make_state()
    state.is_playing = True

    calls = {}

    def fake_play(st):
        calls["play"] = True

    def fake_pause(st):
        calls["pause"] = True

    monkeypatch.setattr("music_player.player_core.play", fake_play)
    monkeypatch.setattr("music_player.player_core.pause", fake_pause)

    handle_keypress(state, "p")

    # Assert - that the pause() branch was taken
    assert calls.get("pause") is True
    # Assert - that the play() branch was not taken
    assert "play" not in calls


def test_branch_key_s_triggers_stop(monkeypatch):
    """
    White box branch coverage
    The target branch is the 'elif key == "s"' branch

    Logic:
    1. Input - Key 's' is pressed
    2. Expected Path - Skips 'p', matches "s"' - calls stop()
    """
    state = make_state()
    calls = {}

    def fake_stop(st):
        calls["stop"] = True

    monkeypatch.setattr("music_player.player_core.stop", fake_stop)

    handle_keypress(state, "s")

    assert calls.get("stop") is True


def test_branch_key_m_triggers_toggle_mute(monkeypatch):
    """
    White box branch coverage
    The target branch is the 'elif key == "m"' branch

    Logic:
    1. Input - Key 'm' is pressed
    2. Expected Path - Skips 'p' and 's', matches "m"' - calls toggle_mute()
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

    assert calls.get("mute") is True


def test_branch_unknown_key_prints_message(capsys):
    """
    White box branch coverage
    The target branch is the final 'else' block (catch-all for unknown keys)

    Logic:
    1. Input - Key 'X' is pressed (matches no known keys)
    2. Expected Path - Fails all 'if' and 'elif' checks - hits final 'else' - prints warning message
    """
    state = make_state()

    handle_keypress(state, "X")  # also shows key.lower() is used
    out = capsys.readouterr().out

    assert "No action bound to key 'x'" in out