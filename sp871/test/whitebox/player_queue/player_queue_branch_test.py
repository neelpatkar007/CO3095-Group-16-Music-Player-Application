"""
White-box: Branch testing for player_queue.next_track / previous_track.

Goal: Execute each branch (True/False outcomes of decisions).
"""

from pathlib import Path
from types import SimpleNamespace
import pytest

from music_player.player_queue import next_track, previous_track
from music_player.player_state import PlayerState


class DummyEngine:
    def __init__(self):
        self.play_calls = []
        self.stop_calls = 0
        self.busy = False

    def is_busy(self):
        return self.busy

    def stop(self):
        self.stop_calls += 1

    def play(self, path, start_pos: float = 0.0):
        self.play_calls.append((path, start_pos))


def make_track(name: str):
    return SimpleNamespace(
        path=Path(f"{name}.mp3"),
        display_name=name,
        duration_seconds=180.0,
    )

def test_branch_next_no_tracks(capsys):
    """B1: Branch where len(tracks) == 0 -> early return."""
    engine = DummyEngine()
    state = PlayerState(tracks=[], audio_engine=engine)

    next_track(state)
    out = capsys.readouterr().out
    assert "No tracks available" in out


def test_branch_next_single_track_stopped(capsys):
    """B2: Branch where there is a single track and we stay on index 0."""
    engine = DummyEngine()
    track = make_track("One")
    state = PlayerState(tracks=[track], audio_engine=engine)
    state.current_index = 0
    state.is_playing = False

    next_track(state)
    out = capsys.readouterr().out

    assert "Selected" in out
    assert state.current_index == 0
    assert engine.play_calls == []  # no auto play when not playing


def test_branch_next_multi_track_no_wrap(capsys):
    """B3: Multi-track and index moves forward without wrapping."""
    engine = DummyEngine()
    t1 = make_track("T1")
    t2 = make_track("T2")
    state = PlayerState(tracks=[t1, t2], audio_engine=engine)
    state.current_index = 0
    state.is_playing = False

    next_track(state)
    out = capsys.readouterr().out

    assert "Selected next" in out
    assert state.current_index == 1


def test_branch_next_multi_track_wrap(capsys):
    """B4: Multi-track and index wraps from last back to 0."""
    engine = DummyEngine()
    t1 = make_track("T1")
    t2 = make_track("T2")
    state = PlayerState(tracks=[t1, t2], audio_engine=engine)
    state.current_index = 1
    state.is_playing = False

    next_track(state)
    out = capsys.readouterr().out

    assert "Wrapped to next" in out
    assert state.current_index == 0


def test_branch_next_while_playing_triggers_engine_play(capsys):
    """B5: Branch where state.is_playing is True -> engine.play() called."""
    engine = DummyEngine()
    t1 = make_track("T1")
    t2 = make_track("T2")
    state = PlayerState(tracks=[t1, t2], audio_engine=engine)
    state.current_index = 0
    state.is_playing = True

    next_track(state)
    out = capsys.readouterr().out

    assert state.current_index == 1
    assert engine.play_calls[-1][0] == t2.path
    assert "Next" in out or "Wrapped" in out

def test_branch_prev_no_tracks(capsys):
    """B6: previous_track with empty library -> early return branch."""
    engine = DummyEngine()
    state = PlayerState(tracks=[], audio_engine=engine)

    previous_track(state)
    out = capsys.readouterr().out

    assert "No tracks available" in out


def test_branch_prev_wrap_backwards(capsys):
    """B7: previous_track wraps from index 0 to the last index."""
    engine = DummyEngine()
    t1 = make_track("T1")
    t2 = make_track("T2")
    state = PlayerState(tracks=[t1, t2], audio_engine=engine)
    state.current_index = 0
    state.is_playing = False

    previous_track(state)
    out = capsys.readouterr().out

    assert state.current_index == 1
    assert "Wrapped to prev" in out


def test_branch_prev_step_back_without_wrap(capsys):
    """B8: previous_track decrements index without wrapping."""
    engine = DummyEngine()
    t1 = make_track("T1")
    t2 = make_track("T2")
    t3 = make_track("T3")
    state = PlayerState(tracks=[t1, t2, t3], audio_engine=engine)
    state.current_index = 2  # from last to middle
    state.is_playing = False

    previous_track(state)
    out = capsys.readouterr().out

    assert state.current_index == 1
    assert "Selected prev" in out or "Prev" in out