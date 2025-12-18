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
    """
        Mock Object: Simulates the audio engine backend to verify that
        the queue system correctly triggers hardware-level calls.
        """
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
    """Utility helper to initialise a Track object with consistent metadata for testing."""
    return SimpleNamespace(
        path=Path(f"{name}.mp3"),
        display_name=name,
        duration_seconds=180.0,
    )

def test_branch_next_no_tracks(capsys):
    """
        Branch B1: Lower Boundary Guard.
        Exercises the 'True' branch of 'if len(tracks) == 0' to verify
        graceful early return when the library is empty.
        """
    engine = DummyEngine()
    state = PlayerState(tracks=[], audio_engine=engine)

    next_track(state)
    out = capsys.readouterr().out
    assert "No tracks available" in out


def test_branch_next_single_track_stopped(capsys):
    """
        Branch B2: Single-Item Index Stability.
        Exercises the branch where a single track exists, ensuring the
        current_index remains clamped at 0 without error.
        """
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
    """
        Branch B3: Sequential Increment Path.
        Exercises the standard 'Next' branch where the index moves forward
        without reaching the end of the track array.
        """
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
    """
        Branch B4: Forward Circular Logic (Wrap-around).
        Exercises the decision path where the index exceeds the last
        element and must wrap back to index 0.
        """
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
    """
        Branch B5: Playback State Integration.
        Exercises the 'True' branch of 'if state.is_playing', ensuring
        the audio engine is triggered during track transition.
        """
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
    """
        Branch B6: Lower Boundary Guard (Previous).
        Verifies that the 'previous_track' function correctly triggers the
        early-return path for empty libraries.
        """
    engine = DummyEngine()
    state = PlayerState(tracks=[], audio_engine=engine)

    previous_track(state)
    out = capsys.readouterr().out

    assert "No tracks available" in out


def test_branch_prev_wrap_backwards(capsys):
    """
        Branch B7: Backward Circular Logic (Wrap-around).
        Exercises the logic fork that wraps from index 0 back to the
        tail of the track list.
        """
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
    """
        Branch B8: Standard Backward Decrement.
        Exercises the path where the index is successfully decremented
        without needing a wrap-around event.
        """
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