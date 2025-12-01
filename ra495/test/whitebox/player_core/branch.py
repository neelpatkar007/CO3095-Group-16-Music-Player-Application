# tests/whitebox/test_player_core_branch_whitebox.py
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


# --- Branch testing for play() -----------------------------------------------

def test_play_branch_no_tracks(capsys):
    """Branch: no tracks -> warning branch taken."""
    engine = DummyEngine()
    state = PlayerState(tracks=[], audio_engine=engine)

    play(state)
    out = capsys.readouterr().out
    assert "No tracks loaded" in out


def test_play_branch_already_playing_does_not_restart(capsys):
    """Branch: state.is_playing and not paused -> 'Already playing' branch."""
    state, track, engine = make_state_with_track()
    state.is_playing = True
    state.is_paused = False

    play(state)
    out = capsys.readouterr().out
    assert "Already playing" in out
    assert engine.play_calls == []


def test_play_branch_resume_from_pause(capsys):
    """Branch: paused -> resume() branch."""
    state, track, engine = make_state_with_track()
    state.is_playing = False
    state.is_paused = True

    play(state)
    out = capsys.readouterr().out
    assert "Resumed" in out
    assert engine.resumed is True
    assert state.is_playing is True
    assert state.is_paused is False


def test_play_branch_fresh_start(capsys):
    """Branch: not playing and not paused -> fresh start branch."""
    state, track, engine = make_state_with_track()
    state.is_playing = False
    state.is_paused = False
    state.position_seconds = 5.0

    play(state)
    out = capsys.readouterr().out
    assert "Playing" in out
    assert engine.play_calls == [(track.path, 5.0)]
    assert state.is_playing is True
    assert state.is_paused is False


# --- Branch testing for pause() ----------------------------------------------

def test_pause_branch_nothing_to_pause(capsys):
    """Branch: not playing or already paused -> 'Nothing to pause'."""
    state, track, engine = make_state_with_track()
    state.is_playing = False
    state.is_paused = False

    pause(state)
    out = capsys.readouterr().out
    assert "Nothing to pause" in out
    assert engine.paused is False


def test_pause_branch_success(capsys):
    """Branch: playing and not paused -> actual pause."""
    state, track, engine = make_state_with_track()
    state.is_playing = True
    state.is_paused = False

    pause(state)
    out = capsys.readouterr().out
    assert "Paused" in out
    assert engine.paused is True
    assert state.is_playing is False
    assert state.is_paused is True


# --- Branch testing for stop() -----------------------------------------------

def test_stop_branch_nothing_is_playing(capsys):
    """Branch: neither playing nor paused -> 'Nothing is playing'."""
    state, track, engine = make_state_with_track()
    state.is_playing = False
    state.is_paused = False

    stop(state)
    out = capsys.readouterr().out
    assert "Nothing is playing" in out
    assert engine.stopped is False


def test_stop_branch_from_playing(capsys):
    """Branch: playing -> stop and reset position."""
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


def test_stop_branch_from_paused(capsys):
    """Branch: paused (not playing) -> stop and reset position."""
    state, track, engine = make_state_with_track()
    state.is_playing = False
    state.is_paused = True
    state.position_seconds = 10.0

    stop(state)
    out = capsys.readouterr().out
    assert "Stopped" in out
    assert engine.stopped is True
    assert state.position_seconds == pytest.approx(0.0)


# --- Branch testing for update_playback() ------------------------------------

def test_update_playback_branch_ignores_non_positive_delta():
    """Branch: delta <= 0 -> early return, no position change."""
    state, track, engine = make_state_with_track()
    state.is_playing = True
    pos_before = state.position_seconds

    update_playback(state, 0.0)
    assert state.position_seconds == pytest.approx(pos_before)


def test_update_playback_branch_ignores_when_not_playing():
    """Branch: not playing -> ignore even if delta > 0."""
    state, track, engine = make_state_with_track()
    state.is_playing = False

    update_playback(state, 1.0)
    assert state.position_seconds == pytest.approx(0.0)


def test_update_playback_branch_ignores_when_paused():
    """Branch: paused -> ignore updates even if playing flag is True."""
    state, track, engine = make_state_with_track()
    state.is_playing = True
    state.is_paused = True

    update_playback(state, 1.0)
    assert state.position_seconds == pytest.approx(0.0)


def test_update_playback_branch_advances_and_finishes(capsys):
    """Branch: playing, not paused, delta>0 and position passes duration."""
    state, track, engine = make_state_with_track(duration=10.0)
    state.is_playing = True
    state.is_paused = False
    state.position_seconds = 9.0

    update_playback(state, 5.0)
    out = capsys.readouterr().out
    assert "Track finished" in out
    assert state.position_seconds == pytest.approx(10.0)
    assert state.is_playing is False
    assert engine.stopped is True