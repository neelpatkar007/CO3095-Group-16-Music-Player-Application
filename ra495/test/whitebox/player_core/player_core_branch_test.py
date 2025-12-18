# tests/whitebox/test_player_core_branch_whitebox.py
from pathlib import Path
from types import SimpleNamespace

import pytest

from music_player.player_core import play, pause, stop, update_playback
from music_player.player_state import PlayerState


class DummyEngine:
    """
    Minimal stub to isolate the Core logic from the actual Audio Engine.
    Allows us to verify if .play(), .pause(), etc. are called without playing real audio.
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
    Helper to create a fresh PlayerState with a single track for each test.
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

# White box testing - branch coverage
# These tests ensure every logical branch within the core
# playback functions is executed at least once.
def test_play_branch_no_tracks(capsys):
    """
        Technique: White-Box Branch Coverage.
        Target Branch: The `if not state.tracks:` Empty Library branch.

        Explanation:
        We initialise a state with an empty track list.
        This forces the code to
        enter the guard clause that warns the user and returns early.
    """

    engine = DummyEngine()
    state = PlayerState(tracks=[], audio_engine=engine)

    play(state)
    out = capsys.readouterr().out
    assert "No tracks loaded" in out


def test_play_branch_already_playing_does_not_restart(capsys):
    """
        Technique: White-Box Branch Coverage.
        Target Branch: The `if state.is_playing:` Already Playing branch.

        Explanation:
        We set `is_playing=True`.
        This forces the code to enter the branch that
        prints 'Already playing' instead of restarting the track.
    """
    state, track, engine = make_state_with_track()
    state.is_playing = True
    state.is_paused = False

    play(state)
    out = capsys.readouterr().out
    assert "Already playing" in out
    assert engine.play_calls == []


def test_play_branch_resume_from_pause(capsys):
    """
        Technique: White-Box Branch Coverage.
        Target Branch: The `elif state.is_paused:` Resume branch.

        Explanation:
        We set `is_paused=True`.
        The code bypasses the 'playing' check but catches
        on the 'paused' check, entering the specific
        branch that calls `resume()`.
    """
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
    """
        Technique: White-Box Branch Coverage.
        Target Branch: The `else:` Fresh Start branch.

        Explanation:
        Both `is_playing` and `is_paused` are False.
        This forces the code to fall
        through to the default branch, which handles starting a
        fresh track via `engine.play()`.
    """
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

def test_pause_branch_nothing_to_pause(capsys):
    """
        Technique: White-Box Branch Coverage.
        Target Branch: The `if not state.is_playing:` Failure branch.

        Explanation:
        We verify the branch that handles invalid requests.
        If nothing is playing,
        the code enters the guard clause and prints a warning.
        """
    state, track, engine = make_state_with_track()
    state.is_playing = False
    state.is_paused = False

    pause(state)
    out = capsys.readouterr().out
    assert "Nothing to pause" in out
    assert engine.paused is False


def test_pause_branch_success(capsys):
    """
        Technique: White-Box Branch Coverage.
        Target Branch: The `else:` Success branch.

        Explanation:
        We set `is_playing=True`.
        The guard clause evaluates to False, forcing
        execution into the main body where `engine.pause()`
        is called.
    """
    state, track, engine = make_state_with_track()
    state.is_playing = True
    state.is_paused = False

    pause(state)
    out = capsys.readouterr().out
    assert "Paused" in out
    assert engine.paused is True
    assert state.is_playing is False
    assert state.is_paused is True

def test_stop_branch_nothing_is_playing(capsys):
    """
        Technique: White-Box Branch Coverage.
        Target Branch: The `if not is_playing and not is_paused:`
        Already Stopped branch.

        Explanation:
        We ensure the code handles the case where the
        player is already stopped.
        This triggers the early return branch.
    """
    state, track, engine = make_state_with_track()
    state.is_playing = False
    state.is_paused = False

    stop(state)
    out = capsys.readouterr().out
    assert "Nothing is playing" in out
    assert engine.stopped is False


def test_stop_branch_from_playing(capsys):
    """
        Technique: White-Box Branch Coverage.
        Target Branch: The `is_playing` logic path within Stop.

        Explanation:
        Verifies that stopping works correctly when the
        system is currently playing.
    """
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
    """
        Technique: White-Box Branch Coverage.
        Target Branch: The `is_paused` logic path within Stop.

        Explanation:
        Verifies that stopping works correctly when the
        system is currently paused
        which is distinct from 'playing' in the boolean logic.
    """
    state, track, engine = make_state_with_track()
    state.is_playing = False
    state.is_paused = True
    state.position_seconds = 10.0

    stop(state)
    out = capsys.readouterr().out
    assert "Stopped" in out
    assert engine.stopped is True
    assert state.position_seconds == pytest.approx(0.0)

def test_update_playback_branch_ignores_non_positive_delta():
    """
        Technique: White-Box Branch Coverage.
        Target Branch: The `if delta_time <= 0:` guard branch.

        Explanation:
        We pass a zero delta. The code should detect
        this condition and
        skip the update logic.
    """
    state, track, engine = make_state_with_track()
    state.is_playing = True
    pos_before = state.position_seconds

    update_playback(state, 0.0)
    assert state.position_seconds == pytest.approx(pos_before)


def test_update_playback_branch_ignores_when_not_playing():
    """
        Technique: White-Box Branch Coverage.
        Target Branch: The `if not state.is_playing:` guard branch.

        Explanation:
        Even if delta is positive, we should not update if
        the player is Stopped.
    """
    state, track, engine = make_state_with_track()
    state.is_playing = False

    update_playback(state, 1.0)
    assert state.position_seconds == pytest.approx(0.0)


def test_update_playback_branch_ignores_when_paused():
    """
        Technique: White-Box Branch Coverage.
        Target Branch: The `if state.is_paused:` guard branch.

        Explanation:
        Even if `is_playing` might be conceptually true
        depending on implementation,
        if `is_paused` is explicitly True, we must enter
        the branch that skips updates.
    """
    state, track, engine = make_state_with_track()
    state.is_playing = True
    state.is_paused = True

    update_playback(state, 1.0)
    assert state.position_seconds == pytest.approx(0.0)


def test_update_playback_branch_advances_and_finishes(capsys):
    """
        Technique: White-Box Branch Coverage.
        Target Branch: The `if position >= duration:` Track Complete branch.

        Explanation:
        We simulate time passing such that `position + delta > duration`.
        This forces the `if` condition to be True, entering
        the branch
        that handles track completion - stopping the engine.
    """
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