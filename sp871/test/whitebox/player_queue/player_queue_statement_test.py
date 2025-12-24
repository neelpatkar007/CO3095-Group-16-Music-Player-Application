from pathlib import Path
from types import SimpleNamespace
import pytest

from music_player.player_queue import next_track, previous_track
from music_player.player_state import PlayerState


# Test: A mock audio engine used to check if the queue system triggers the correct play and stop calls
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


# Test: Helper function to create a track object with standard information for testing
def make_track(name: str):
    return SimpleNamespace(
        path=Path(f"{name}.mp3"),
        display_name=name,
        duration_seconds=180.0,
    )


# Test: checking that the system reports no tracks available if the next song is requested from an empty library
def test_stmt_next_track_no_tracks(capsys):
    engine = DummyEngine()
    state = PlayerState(tracks=[], audio_engine=engine)

    next_track(state)
    out = capsys.readouterr().out
    assert "No tracks available" in out


# Test: verifying that skipping forward when only one song exists resets the position but keeps the same track
def test_stmt_next_track_single_track_stopped(capsys):
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


# Test: verifying that skipping forward while playing correctly triggers the engine to play the next song
def test_stmt_next_track_multi_track_while_playing(capsys):
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


# Test: checking that skipping back from the first song correctly wraps the index to the last song in the list
def test_stmt_previous_track_basic_wrap(capsys):
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