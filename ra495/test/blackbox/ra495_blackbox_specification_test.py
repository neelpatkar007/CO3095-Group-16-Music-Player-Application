from pathlib import Path
from types import SimpleNamespace

import pytest

from music_player.player_state import PlayerState
from music_player.player_core import play, pause, stop
from music_player.library import Track
from music_player.player_ui import (
    print_playlist_with_indicator,
    print_now_playing,
    )


class DummyEngine:
    """
    Minimal stub used to isolate Black-Box tests from hardware dependencies.
    """
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
    """
    Helper: to set up specific states for State Transition Testing.
    """
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

def make_state_indicator(tracks, current_index: int = 0) -> PlayerState:
    state = PlayerState(tracks=tracks, audio_engine=DummyEngine())
    state.current_index = current_index
    return state


def make_track(title: str = "Song", artist: str = "Unknown", duration: float = 180.0) -> Track:
    return Track(
        path=Path(f"{title}.mp3"),
        title=title,
        artist=artist,
        duration_seconds=duration,
    )

# Black Box testing of Player Core state transitions
# These tests verify that the system correctly transitions between finite states -
# Stopped, Playing, Paused - based on specific input events - play, pause, stop.

def test_bb_play_no_tracks(capsys):
    """
        Technique: Black-Box State Transition Testing (Invalid Transition).
        State: Stopped (Empty Library) - > Input : Play - > Outcome: Warning (No State Change).
    """
    # P1
    state = make_state(has_track=False, current_state="Stopped")
    play(state)
    out = capsys.readouterr().out
    assert "No tracks loaded" in out
    assert state.is_playing is False


def test_bb_play_from_stopped_starts_playing(capsys):
    """
        Technique: Black-Box State Transition Testing (Valid Transition).
        State: Stopped -> Input: Play -> State: Playing.
    """
    # P2
    state = make_state(has_track=True, current_state="Stopped")
    play(state)
    out = capsys.readouterr().out
    assert "Playing" in out
    assert state.is_playing is True
    assert state.is_paused is False


def test_bb_play_when_already_playing(capsys):
    """
    Technique: Black-Box State Transition Testing (No Transition).
    State: Playing -> Input: Play -> State: Playing (Warning issued).
    """
    # P3
    state = make_state(has_track=True, current_state="Playing")
    play(state)
    out = capsys.readouterr().out
    assert "Already playing" in out
    assert state.is_playing is True


def test_bb_play_from_paused_resumes(capsys):
    """
    Technique: Black-Box State Transition Testing (Valid Transition).
    State: Paused -> Input: Play -> State: Playing (Resumed).
    """
    # P4
    state = make_state(has_track=True, current_state="Paused")
    play(state)
    out = capsys.readouterr().out
    assert "Resumed" in out
    assert state.is_playing is True
    assert state.is_paused is False


def test_bb_pause_from_playing(capsys):
    """
    Technique: Black-Box State Transition Testing (Valid Transition).
    State: Playing -> Input: Pause -> State: Paused.
    """
    # P5
    state = make_state(has_track=True, current_state="Playing")
    pause(state)
    out = capsys.readouterr().out
    assert "Paused" in out
    assert state.is_playing is False
    assert state.is_paused is True


def test_bb_pause_when_nothing_playing(capsys):
    """
    Technique: Black-Box State Transition Testing (Invalid Transition).
    State: Stopped -> Input: Pause -> Outcome: Warning (No State Change).
    """
    # P6
    state = make_state(has_track=True, current_state="Stopped")
    pause(state)
    out = capsys.readouterr().out
    assert "Nothing to pause" in out
    assert state.is_paused is False


def test_bb_stop_from_playing(capsys):
    """
    Technique: Black-Box State Transition Testing (Valid Transition).
    State: Playing -> Input: Stop -> State: Stopped (Position Reset).
    """
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
    """
    Technique: Black-Box State Transition Testing (No Transition).
    State: Stopped -> Input: Stop -> State: Stopped (Warning issued).
    """
    # P8
    state = make_state(has_track=True, current_state="Stopped")
    stop(state)
    out = capsys.readouterr().out
    assert "Nothing is playing" in out

# Black box testing : equivalence partitioning and boundary value analysis
# These tests verify the UI logic by partitioning inputs into valid/invalid classes -
# Empty, Single, Multiple -  and testing boundary conditions - Out of range indices.
def test_ui_list_empty_library_warns(capsys):
    """
    Technique: Black-Box Equivalence Partitioning.
    Partition: Empty List (Invalid).
    Expectation: Warning message.
    """
    # L1
    state = make_state_indicator(tracks=[])
    print_playlist_with_indicator(state)
    out = capsys.readouterr().out
    assert "[ui] Warning: Library is empty." in out


def test_ui_list_single_track_shows_note_and_indicator(capsys):
    """
    Technique: Black-Box Boundary Value Analysis.
    Boundary: Minimum valid list size (1).
    Expectation: Correct formatted output and note.
    """
    # L2
    track = make_track(title="Solo")
    state = make_state_indicator(tracks=[track])
    state.is_playing = True

    print_playlist_with_indicator(state)
    out = capsys.readouterr().out

    assert "[ui] Note: Only one track in the library." in out
    # Expect first (and only) line to have ▶ marker and index 01
    assert "▶ 01: Solo – Unknown" in out


def test_ui_list_out_of_range_index_is_clamped(capsys):
    """
    Technique: Black-Box Boundary Value Analysis.
    Boundary: Index > List Length (Upper Bound Violation).
    Expectation: System should clamp to the last valid index instead of crashing.
    """
    # L3: current_index too large => clamped to last track
    tracks = [
        make_track(title="T1"),
        make_track(title="T2"),
        make_track(title="T3"),
    ]
    state = make_state_indicator(tracks=tracks)
    state.current_index = 10  # out of range, should clamp to len(tracks)-1

    print_playlist_with_indicator(state)
    out = capsys.readouterr().out

    # Last track (T3) should be marked as current, default marker • if not playing/paused
    assert "• 03: T3 – Unknown" in out


def test_ui_list_warns_on_missing_titles(capsys):
    """
    Technique: Black-Box Equivalence Partitioning - Error Guessing
    Partition: Invalid Data - Missing attributes.
    Expectation: Graceful failure or warning message.
    """
    class FakeTrack:
        def __init__(self, display_name: str):
            self.display_name = display_name

    good = make_track(title="Good", artist="Artist")
    bad = FakeTrack("")  # Missing display_name

    state = make_state_indicator(tracks=[good, bad])

    print_playlist_with_indicator(state)
    out = capsys.readouterr().out

    # UPDATED:
    assert "[ui] Warning: Library is in an invalid state." in out

def test_ui_info_no_track_selected(capsys):
    """
    Technique  : Black-Box Equivalence Partitioning.
    Partition : 'None' Selection State.
    Expectation : "No track selected" message.
    """
    # INF1
    state = make_state_indicator(tracks=[])  # current_track is None
    print_now_playing(state)
    out = capsys.readouterr().out
    assert "[ui] No track selected." in out


def test_ui_info_shows_playing_status_and_metadata(capsys):
    """
    Technique: Black-Box Equivalence Partitioning.
    Partition: Valid Active State.
    Expectation: Correctly formatted metadata string.
    """
    # INF2
    track = make_track(title="Hello", artist="World", duration=180.0)
    state = make_state_indicator(tracks=[track])
    state.is_playing = True
    state.is_paused = False

    print_now_playing(state)
    out = capsys.readouterr().out

    assert "[ui] Playing:" in out
    assert "Hello – World" in out
    assert "[03:00]" in out  # 180 seconds formatted