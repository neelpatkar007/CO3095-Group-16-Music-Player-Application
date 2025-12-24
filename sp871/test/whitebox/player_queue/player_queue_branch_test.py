from pathlib import Path
from types import SimpleNamespace
import pytest

from music_player.player_queue import next_track, previous_track
from music_player.player_state import PlayerState


# Test: A mock audio engine to check if the queue logic triggers play and stop correctly
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


# Test: Helper function to create a basic track object for testing
def make_track(name: str):
    return SimpleNamespace(
        path=Path(f"{name}.mp3"),
        display_name=name,
        duration_seconds=180.0,
    )

# Test: verifying that the system reports no tracks available if the library is empty
def test_branch_next_no_tracks(capsys):
    engine = DummyEngine()
    state = PlayerState(tracks=[], audio_engine=engine)

    next_track(state)
    out = capsys.readouterr().out
    assert "No tracks available" in out


# Test: checking that skipping forward when only one song exists keeps the index at zero
def test_branch_next_single_track_stopped(capsys):
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


# Test: verifying that the queue moves to the next song normally when not at the end of the list
def test_branch_next_multi_track_no_wrap(capsys):
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


# Test: ensuring that skipping forward on the last song wraps the queue back to the first song
def test_branch_next_multi_track_wrap(capsys):
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


# Test: verifying that skipping forward while a song is playing automatically starts the next song
def test_branch_next_while_playing_triggers_engine_play(capsys):
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

# Test: ensuring the system reports no tracks when skipping backwards in an empty library
def test_branch_prev_no_tracks(capsys):
    engine = DummyEngine()
    state = PlayerState(tracks=[], audio_engine=engine)

    previous_track(state)
    out = capsys.readouterr().out

    assert "No tracks available" in out


# Test: verifying that skipping backwards from the first song wraps to the very last song in the list
def test_branch_prev_wrap_backwards(capsys):
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


# Test: verifying that the queue moves back by one song correctly when not at the start
def test_branch_prev_step_back_without_wrap(capsys):
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