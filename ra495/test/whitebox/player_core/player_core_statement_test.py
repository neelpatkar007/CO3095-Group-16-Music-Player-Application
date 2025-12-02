# tests/whitebox/test_player_core_statement_whitebox.py
from pathlib import Path
from types import SimpleNamespace

import pytest

from music_player.player_core import play, pause, stop, update_playback
from music_player.player_state import PlayerState


class DummyEngine:
    def __init__(self):
        self.play_calls = []
        self.paused = False
        self.resumed = False
        self.stopped = False

    def play(self, path, start_pos=0.0):
        self.play_calls.append((path, start_pos))

    def pause(self):
        self.paused = True

    def resume(self):
        self.resumed = True

    def stop(self):
        self.stopped = True


def make_state_with_track(duration: float = 180.0):
    engine = DummyEngine()
    track = SimpleNamespace(
        path=Path("dummy.mp3"),
        display_name="Dummy Track",
        duration_seconds=duration,
    )
    state = PlayerState(tracks=[track], audio_engine=engine)
    state.current_index = 0
    return state, track, engine

def test_play_no_tracks_executes_warning_statement(capsys):
    """Covers the 'no tracks loaded' path inside play()."""
    engine = DummyEngine()
    state = PlayerState(tracks=[], audio_engine=engine)

    play(state)
    out = capsys.readouterr().out
    assert "No tracks loaded" in out


def test_play_fresh_start_executes_main_play_path(capsys):
    """Covers the normal play path (engine.play call, flags update)."""
    state, track, engine = make_state_with_track()
    state.position_seconds = 5.0

    play(state)
    out = capsys.readouterr().out
    assert "Playing" in out
    assert engine.play_calls == [(track.path, 5.0)]
    assert state.is_playing is True
    assert state.is_paused is False

def test_pause_success_executes_pause_path(capsys):
    """Covers the successful pause path (engine.pause, flags)."""
    state, track, engine = make_state_with_track()
    state.is_playing = True
    state.is_paused = False

    pause(state)
    out = capsys.readouterr().out
    assert "Paused" in out
    assert engine.paused is True
    assert state.is_playing is False
    assert state.is_paused is True

def test_stop_from_playing_executes_stop_path(capsys):
    """Covers the path where something is playing and we stop it."""
    state, track, engine = make_state_with_track()
    state.is_playing = True
    state.is_paused = False
    state.position_seconds = 10.0

    stop(state)
    out = capsys.readouterr().out
    assert "Stopped" in out
    assert engine.stopped is True
    assert state.is_playing is False
    assert state.is_paused is False
    assert state.position_seconds == pytest.approx(0.0)

def test_update_playback_advances_and_finishes_track(capsys):
    """
    Covers the main update path: advance position, clamp at duration,
    and execute 'track finished' logic.
    """
    state, track, engine = make_state_with_track(duration=10.0)
    state.is_playing = True
    state.is_paused = False
    state.position_seconds = 9.0

    update_playback(state, 5.0)  # go past the end
    out = capsys.readouterr().out
    assert "Track finished" in out
    assert state.position_seconds == pytest.approx(10.0)
    assert state.is_playing is False
    assert engine.stopped is True
