from pathlib import Path

import pytest

# Assumes that the music_player package is available in the python path
from music_player.player_state import PlayerState
from music_player.player_shortcuts import handle_keypress
from music_player.library import Track
from music_player.player_seek import seek_to, nudge, get_progress


class DummyEngine:
    """
    Minimal stand-in for AudioEngine used in black-box seek tests.
    Used to also isolate the logic being tested without relying on actual hardware or audio drivers.
    """

    def __init__(self) -> None:
        # optional: track the last seek position if you ever want to assert on it
        self.last_seek: float | None = None

    def seek(self, position: float) -> None:
        """No-op seek, just record the position."""
        self.last_seek = float(position)

def make_state_with_track(duration: float) -> PlayerState:
    """
    Helper used by the tests to build a valid PlayerState with a specific track duration.
    """

    track = Track(
        path=Path("dummy.mp3"),
        title="Dummy",
        artist="A",
        duration_seconds=duration,
    )
    engine = DummyEngine()
    state = PlayerState(tracks=[track], audio_engine=engine)
    state.current_index = 0
    state.position_seconds = 0.0
    return state

def make_state(current_state: str) -> PlayerState:
    '''
    Helped to create a PlayerState in a specific logical state.
    (Playing, Paused, Stopped).
    '''

    state = PlayerState(tracks=[], audio_engine=DummyEngine())
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

# Black box testing specification based. These tests verify that the input keys
# trigger the correct state transitions regardless of internal implementations.

def test_bb_shortcut_p_plays_when_not_playing(monkeypatch):
    '''
    Black-box specification testing.
    Verifies that the 'p' key acts as the 'Play' command when the application is currently in a 'Stopped' state.
    '''
    state = make_state("Stopped")
    calls = {}

    def fake_play(s):
        calls["play"] = True

    def fake_pause(s):
        calls["pause"] = True

    # Mocking the core internal functions to verify the interfaces logic.
    monkeypatch.setattr("music_player.player_core.play", fake_play)
    monkeypatch.setattr("music_player.player_core.pause", fake_pause)

    handle_keypress(state, "p")

    # Expectation is Play is to be called and Pause is not called.
    assert "play" in calls
    assert "pause" not in calls


def test_bb_shortcut_p_pauses_when_playing(monkeypatch):
    '''
    Black-box specification testing.
    Verifies that the 'p' key acts as the 'Pause' command when the application is currently in a 'Playing' state.
    '''
    state = make_state("Playing")
    calls = {}

    def fake_play(s):
        calls["play"] = True

    def fake_pause(s):
        calls["pause"] = True

    monkeypatch.setattr("music_player.player_core.play", fake_play)
    monkeypatch.setattr("music_player.player_core.pause", fake_pause)

    # Expectation is Pause is to be called and Play is not called.
    handle_keypress(state, "p")
    assert "pause" in calls
    assert "play" not in calls


def test_bb_shortcut_s_stops(monkeypatch):
    '''
    Black-box specification testing.
    Verifies that the 's' key triggers the 'Stop' functionality.
    '''
    state = make_state("Playing")
    calls = {}

    def fake_stop(s):
        calls["stop"] = True

    monkeypatch.setattr("music_player.player_core.stop", fake_stop)

    handle_keypress(state, "s")
    assert "stop" in calls


def test_bb_shortcut_m_toggles_mute(monkeypatch):
    '''
    Black-box specification testing.
    Verifies that the 'm' key triggers the mute toggle functionality.
    '''
    state = make_state("Playing")
    calls = {}

    def fake_toggle_mute(s):
        calls["mute"] = True

    monkeypatch.setattr("music_player.player_audio.toggle_mute", fake_toggle_mute)

    handle_keypress(state, "m")
    assert "mute" in calls


def test_bb_shortcut_other_key_no_action(capsys):
    '''
    Black-box specification testing.
    Verifies that the 'Invalid Input' partition - (any key other than 'p', 's', 'm') should result in a
    user warning rather than a crash.
    '''
    state = make_state("Stopped")
    handle_keypress(state, "x")
    out = capsys.readouterr().out
    assert "No action bound to key 'x'" in out

# Black-box testing specification based tests for focusing on the boundaries of the track duration.
def test_bb_nudge_forward_and_clamped():
    '''
    Black-box boundary value analysis - tests the upper boundary of track.
    It nudges past the total duration of 60 seconds and should clamp the position
    to the max duration of 60 seconds, and not exceed it.
    '''
    state = make_state_with_track(60.0)
    # Set the position close to the boundary
    state.position_seconds = 58.0

    # Nudge past the boundary. So 58 + 5 = 63 which is > than 60
    nudge(state, 5.0)

    # Verify clamping at the boundary of 60 seconds
    assert state.position_seconds == pytest.approx(60.0)


def test_bb_nudge_backward_and_clamped():
    '''
    Black-box boundary value analysis - tests the lower boundary of track.
    It nudges backwards past the start of 0 seconds and should clamp the position
    to the 0 seconds, and not becoming negative.
    '''
    state = make_state_with_track(60.0)
    # Set the position close to the boundary
    state.position_seconds = 2.0

    # Nudge past the boundary. So 2 - 5 is -3 which is < than 0
    nudge(state, -5.0)

    # Verify clamping at the boundary of 0 seconds
    assert state.position_seconds == pytest.approx(0.0)