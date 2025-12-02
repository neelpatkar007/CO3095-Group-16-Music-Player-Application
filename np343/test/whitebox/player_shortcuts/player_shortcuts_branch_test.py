import pytest

from music_player.player_shortcuts import handle_keypress
from music_player.player_state import PlayerState


class DummyEngine:
    """Minimal stub so PlayerState can be constructed without real audio."""
    pass


def make_state() -> PlayerState:
    return PlayerState(tracks=[], audio_engine=DummyEngine())


# BRANCH TESTS FOR handle_keypress

def test_branch_key_p_triggers_play_when_not_playing(monkeypatch):
    """
    Branch test:
    - key == 'p' AND state.is_playing == False
    - Should take the inner 'else' branch -> player_core.play(...)
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

    assert calls.get("play") is True
    assert "pause" not in calls


def test_branch_key_p_triggers_pause_when_playing(monkeypatch):
    """
    Branch test:
    - key == 'p' AND state.is_playing == True
    - Should take the inner 'if' branch -> player_core.pause(...)
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

    assert calls.get("pause") is True
    assert "play" not in calls


def test_branch_key_s_triggers_stop(monkeypatch):
    """
    Branch test:
    - key == 's' hits the 'elif key == "s"' branch.
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
    Branch test:
    - key == 'm' hits the 'elif key == "m"' branch.
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
    Branch test:
    - key not in {'p', 's', 'm'} hits the final 'else' branch.
    """
    state = make_state()

    handle_keypress(state, "X")  # also shows key.lower() is used
    out = capsys.readouterr().out

    assert "No action bound to key 'x'" in out