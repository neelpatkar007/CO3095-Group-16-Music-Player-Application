"""
White-box: Statement testing for player_queue.next_track / previous_track.

Goal: Execute every statement at least once, without necessarily
covering every branch combination.
"""

from pathlib import Path
from types import SimpleNamespace
import pytest

from music_player.player_queue import next_track, previous_track
from music_player.player_state import PlayerState


class DummyEngine:
    """
        Mock Object: Simulates the audio engine to verify that the queue
        controller triggers the correct hardware-level calls.
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
    """Utility helper to initialise a Track object with consistent metadata."""
    return SimpleNamespace(
        path=Path(f"{name}.mp3"),
        display_name=name,
        duration_seconds=180.0,
    )


def test_stmt_next_track_no_tracks(capsys):
    """
        Statement Test S1: Early Return Logic.
        Executes the initial lines of the next_track function to verify
        safety guards when the library is empty.
        """
    engine = DummyEngine()
    state = PlayerState(tracks=[], audio_engine=engine)

    next_track(state)
    out = capsys.readouterr().out
    assert "No tracks available" in out


def test_stmt_next_track_single_track_stopped(capsys):
    """
        Statement Test S2: Standard Index Initialisation.
        Covers the execution path for a single-item queue, ensuring the
        index remains stable at zero while the player is stopped.
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
    assert state.position_seconds == 0.0
    # No auto play when not already playing
    assert engine.play_calls == []


def test_stmt_next_track_multi_track_while_playing(capsys):
    """
        Statement Test S3: Active State Propagation.
        Executes the specific code statements responsible for triggering the
        audio engine when a track change occurs during playback.
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


def test_stmt_previous_track_basic_wrap(capsys):
    """
        Statement Test S4: Circular Logic Execution.
        Executes the wrap-around statements in previous_track to verify
        index arithmetic at the list boundaries.
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