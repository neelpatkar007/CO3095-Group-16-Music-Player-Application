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


def test_stmt_next_track_no_tracks(capsys):
    """S1: Execute the early-return path when there are no tracks."""
    engine = DummyEngine()
    state = PlayerState(tracks=[], audio_engine=engine)

    next_track(state)
    out = capsys.readouterr().out
    assert "No tracks available" in out


def test_stmt_next_track_single_track_stopped(capsys):
    """S2: Single track; ensure normal flow without auto-play."""
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
    """S3: Move to next track and trigger engine.play() when playing."""
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
    """S4: Execute previous_track including wrap-around behaviour at least once."""
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