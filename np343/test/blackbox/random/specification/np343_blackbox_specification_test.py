from pathlib import Path

import pytest

from music_player.player_state import PlayerState
from music_player.player_shortcuts import handle_keypress
from music_player.library import Track
from music_player.player_seek import seek_to, nudge, get_progress


class DummyEngine:
    """Minimal stand-in for AudioEngine used in black-box seek tests."""

    def __init__(self) -> None:
        # optional: track the last seek position if you ever want to assert on it
        self.last_seek: float | None = None

    def seek(self, position: float) -> None:
        """No-op seek; just record the position."""
        self.last_seek = float(position)

def make_state_with_track(duration: float) -> PlayerState:
    """Helper used by the tests to build a valid PlayerState."""

    track = Track(
        path=Path("dummy.mp3"),
        title="Dummy",
        artist="A",
        duration_seconds=duration,
    )
    engine = DummyEngine()
    state = PlayerState(tracks=[track], audio_engine=engine)
    state.current_index = 0
    state.position_seconds = 0.0
    return state

def make_state(current_state: str) -> PlayerState:
    state = PlayerState(tracks=[], audio_engine=DummyEngine())
    if current_state == "Playing":
        state.is_playing = True
        state.is_paused = False
    elif current_state == "Paused":
        state.is_playing = False
        state.is_paused = True
    else:
        state.is_playing = False
        state.is_paused = False
    return state


def test_bb_shortcut_p_plays_when_not_playing(monkeypatch):
    state = make_state("Stopped")
    calls = {}

    def fake_play(s):
        calls["play"] = True

    def fake_pause(s):
        calls["pause"] = True

    monkeypatch.setattr("music_player.player_core.play", fake_play)
    monkeypatch.setattr("music_player.player_core.pause", fake_pause)

    handle_keypress(state, "p")
    assert "play" in calls
    assert "pause" not in calls


def test_bb_shortcut_p_pauses_when_playing(monkeypatch):
    state = make_state("Playing")
    calls = {}

    def fake_play(s):
        calls["play"] = True

    def fake_pause(s):
        calls["pause"] = True

    monkeypatch.setattr("music_player.player_core.play", fake_play)
    monkeypatch.setattr("music_player.player_core.pause", fake_pause)

    handle_keypress(state, "p")
    assert "pause" in calls
    assert "play" not in calls


def test_bb_shortcut_s_stops(monkeypatch):
    state = make_state("Playing")
    calls = {}

    def fake_stop(s):
        calls["stop"] = True

    monkeypatch.setattr("music_player.player_core.stop", fake_stop)

    handle_keypress(state, "s")
    assert "stop" in calls


def test_bb_shortcut_m_toggles_mute(monkeypatch):
    state = make_state("Playing")
    calls = {}

    def fake_toggle_mute(s):
        calls["mute"] = True

    monkeypatch.setattr("music_player.player_audio.toggle_mute", fake_toggle_mute)

    handle_keypress(state, "m")
    assert "mute" in calls


def test_bb_shortcut_other_key_no_action(capsys):
    state = make_state("Stopped")
    handle_keypress(state, "x")
    out = capsys.readouterr().out
    assert "No action bound to key 'x'" in out

def test_bb_nudge_forward_and_clamped():
    state = make_state_with_track(60.0)
    state.position_seconds = 58.0
    nudge(state, 5.0)
    assert state.position_seconds == pytest.approx(60.0)


def test_bb_nudge_backward_and_clamped():
    state = make_state_with_track(60.0)
    state.position_seconds = 2.0
    nudge(state, -5.0)
    assert state.position_seconds == pytest.approx(0.0)