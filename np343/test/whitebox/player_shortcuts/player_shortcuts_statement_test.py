import pytest

from music_player.player_shortcuts import handle_keypress
from music_player.player_state import PlayerState


class DummyEngine:
    """Minimal stub so PlayerState can be constructed without real audio."""
    pass


def make_state() -> PlayerState:
    return PlayerState(tracks=[], audio_engine=DummyEngine())


# STATEMENT TESTS FOR handle_keypress


def test_stmt_key_p_triggers_play_when_not_playing(monkeypatch):
    """
    Statement test:
    - Executes the 'p' branch where state.is_playing is False,
      so player_core.play(...) is called.
    - Covers: key.lower(), first if key == 'p', inner else.
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


def test_stmt_key_s_triggers_stop(monkeypatch):
    """
    Statement test:
    - Executes the 'elif key == "s"' branch, calling stop().
    """
    state = make_state()
    calls = {}

    def fake_stop(st):
        calls["stop"] = True

    monkeypatch.setattr("music_player.player_core.stop", fake_stop)

    handle_keypress(state, "s")

    assert calls.get("stop") is True


def test_stmt_key_m_triggers_toggle_mute(monkeypatch):
    """
    Statement test:
    - Executes the 'elif key == "m"' branch, calling toggle_mute().
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


def test_stmt_unknown_key_prints_message(capsys):
    """
    Statement test:
    - Executes the final 'else' branch, where no action is bound.
    """
    state = make_state()

    handle_keypress(state, "x")
    out = capsys.readouterr().out

    assert "No action bound to key 'x'" in out