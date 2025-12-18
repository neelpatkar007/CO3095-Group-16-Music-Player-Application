# tests/whitebox/test_player_core_statement_whitebox.py
from pathlib import Path
from types import SimpleNamespace

import pytest

from music_player.player_core import play, pause, stop, update_playback
from music_player.player_state import PlayerState


class DummyEngine:
    """
    Minimal stub to isolate the Core logic from the actual Audio Engine.
    And allows us to verify if the .play(), .pause(), etc. are called without playing the real audio.
    """
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
    """
    Helper to create a valid PlayerState with one track.
    """
    engine = DummyEngine()
    track = SimpleNamespace(
        path=Path("dummy.mp3"),
        display_name="Dummy Track",
        duration_seconds=duration,
    )
    state = PlayerState(tracks=[track], audio_engine=engine)
    state.current_index = 0
    return state, track, engine

# White box testing - statement coverage
# These tests ensure that specific executable statements within the core
# player logic - play / pause / stop / update - are reached and executed.

def test_play_no_tracks_executes_warning_statement(capsys):
    """
    Technique is White-Box Statement Coverage.
    Target Statement - `print("No tracks loaded")` (or similar warning).

    Explanation:
    We initialise a state with an empty track list.
    And this forces the code to
    enter the `if not state.tracks:` block and execute the specific print statement
    that warns the user.
    """
    engine = DummyEngine()
    state = PlayerState(tracks=[], audio_engine=engine)

    play(state)
    out = capsys.readouterr().out

    # Verification - The warning statement was executed.
    assert "No tracks loaded" in out


def test_play_fresh_start_executes_main_play_path(capsys):
    """
    Technique - White-Box Statement Coverage.
    Target Statements this time are
    1. `audio_engine.play(...)`
    2. and `state.is_playing = True`

    Explanation:
    We provide a valid track and start from scratch.
    This ensures that the main
    logic block that initiates playback is executed.
    """
    state, track, engine = make_state_with_track()
    state.position_seconds = 5.0

    play(state)
    out = capsys.readouterr().out

    # Verification : The engine.play() statement and state update statements were executed.
    assert "Playing" in out
    assert engine.play_calls == [(track.path, 5.0)]
    assert state.is_playing is True
    assert state.is_paused is False

def test_pause_success_executes_pause_path(capsys):
    """
    Technique : White-Box Statement Coverage.
    Target Statements are :
    1. `audio_engine.pause()`
    2. `state.is_paused = True`

    Explanation:

    We set the state to 'Playing'.
    Calling pause() forces the execution of
    the statements responsible for pausing the engine and updating the flags.
    """
    state, track, engine = make_state_with_track()
    state.is_playing = True
    state.is_paused = False

    pause(state)
    out = capsys.readouterr().out

    # Verification that the engine.pause() statement was executed.
    assert "Paused" in out
    assert engine.paused is True
    assert state.is_playing is False
    assert state.is_paused is True

def test_stop_from_playing_executes_stop_path(capsys):
    """
    Technique - White Box Statement Coverage.
    Target Statements -
    1. `audio_engine.stop()`
    2. `state.position_seconds = 0.0`

    Explanation below:
    We simulate a playing track.
    Calling stop() must execute the statements
    that reset the position to zero and stop the engine.
    """
    state, track, engine = make_state_with_track()
    state.is_playing = True
    state.is_paused = False
    state.position_seconds = 10.0

    stop(state)
    out = capsys.readouterr().out
    # Verification: The statement resetting position to 0.0 was executed.
    assert "Stopped" in out
    assert engine.stopped is True
    assert state.is_playing is False
    assert state.is_paused is False
    assert state.position_seconds == pytest.approx(0.0)

def test_update_playback_advances_and_finishes_track(capsys):
    """
    Technique - White - Box Statement Coverage.
    Target Statements -
    1. `state.position_seconds += delta_time`
    2. and - `if state.position_seconds >= track.duration:`

    Explanation is below:
    We set the position near the end of the track and advance time past the duration.
    This forces the execution of the statements that handle "Track Finished" logic
    and hence clamping position and stopping the player.
    """
    state, track, engine = make_state_with_track(duration=10.0)
    state.is_playing = True
    state.is_paused = False
    state.position_seconds = 9.0

    update_playback(state, 5.0)  # go past the end
    out = capsys.readouterr().out

    # Verification -  The track completion statements were executed.
    assert "Track finished" in out
    assert state.position_seconds == pytest.approx(10.0)
    assert state.is_playing is False
    assert engine.stopped is True
