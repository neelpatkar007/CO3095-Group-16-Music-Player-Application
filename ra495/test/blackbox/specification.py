from pathlib import Path
from types import SimpleNamespace

import pytest

from music_player.player_state import PlayerState
from music_player.player_core import play, pause, stop


class DummyEngine:
    def __init__(self):
        self.play_calls = 0
        self.paused = False
        self.resumed = False
        self.stopped = False

    def play(self, path, start_pos=0.0):
        self.play_calls += 1

    def pause(self):
        self.paused = True

    def resume(self):
        self.resumed = True

    def stop(self):
        self.stopped = True


def make_state(has_track: bool, current_state: str) -> PlayerState:
    engine = DummyEngine()
    tracks = []
    if has_track:
        t = SimpleNamespace(path=Path("dummy.mp3"), display_name="Dummy", duration_seconds=180.0)
        tracks = [t]
    state = PlayerState(tracks=tracks, audio_engine=engine)
    if has_track:
        state.current_index = 0

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


def test_bb_play_no_tracks(capsys):
    # P1
    state = make_state(has_track=False, current_state="Stopped")
    play(state)
    out = capsys.readouterr().out
    assert "No tracks loaded" in out
    assert state.is_playing is False


def test_bb_play_from_stopped_starts_playing(capsys):
    # P2
    state = make_state(has_track=True, current_state="Stopped")
    play(state)
    out = capsys.readouterr().out
    assert "Playing" in out
    assert state.is_playing is True
    assert state.is_paused is False


def test_bb_play_when_already_playing(capsys):
    # P3
    state = make_state(has_track=True, current_state="Playing")
    play(state)
    out = capsys.readouterr().out
    assert "Already playing" in out
    assert state.is_playing is True


def test_bb_play_from_paused_resumes(capsys):
    # P4
    state = make_state(has_track=True, current_state="Paused")
    play(state)
    out = capsys.readouterr().out
    assert "Resumed" in out
    assert state.is_playing is True
    assert state.is_paused is False


def test_bb_pause_from_playing(capsys):
    # P5
    state = make_state(has_track=True, current_state="Playing")
    pause(state)
    out = capsys.readouterr().out
    assert "Paused" in out
    assert state.is_playing is False
    assert state.is_paused is True


def test_bb_pause_when_nothing_playing(capsys):
    # P6
    state = make_state(has_track=True, current_state="Stopped")
    pause(state)
    out = capsys.readouterr().out
    assert "Nothing to pause" in out
    assert state.is_paused is False


def test_bb_stop_from_playing(capsys):
    # P7
    state = make_state(has_track=True, current_state="Playing")
    state.position_seconds = 10.0
    stop(state)
    out = capsys.readouterr().out
    assert "Stopped" in out
    assert state.is_playing is False
    assert state.is_paused is False
    assert state.position_seconds == pytest.approx(0.0)


def test_bb_stop_when_already_stopped(capsys):
    # P8
    state = make_state(has_track=True, current_state="Stopped")
    stop(state)
    out = capsys.readouterr().out
    assert "Nothing is playing" in out
