from pathlib import Path
from types import SimpleNamespace

from music_player.player_core import play, pause, stop, update_playback
from music_player.player_state import PlayerState


class DummyEngine:
    """
        Minimal stub to isolate the Core logic.
        We track calls - play_calls, paused, stopped - to verify which branch of code was executed.
    """
    def __init__(self):
        self.play_calls = []
        self.paused = False
        self.stopped = False
        self.resumed = False

    def play(self, path, start_pos=0.0):
        self.play_calls.append((path, start_pos))

    def pause(self):
        self.paused = True

    def stop(self):
        self.stopped = True

    def resume(self):
        self.resumed = True


def make_state_with_track(duration=120.0):
    """
    Helper to create a fresh PlayerState with a single track for each test.
    """
    engine = DummyEngine()
    # SimpleNamespace is enough – only .path, .display_name and duration_seconds are used.
    track = SimpleNamespace(
        path=Path("song.mp3"),
        display_name="Song",
        duration_seconds=duration,
    )
    state = PlayerState(tracks=[track], audio_engine=engine)
    state.current_index = 0
    return state, track, engine

# White box testing technique - branch coverage
# These tests ensure that every logical branch (if/elif/else) within the core
# playback functions is executed at least once.
def test_play_already_playing_branch(capsys):
    """
        Technique: White-Box Branch Coverage.
        Target Branch: The `if state.is_playing:` branch within play().

        Explanation:
        We set `is_playing=True` before calling play().
        This forces the code to
        enter the "Already Playing" guard clause/branch instead
        of starting playback.
    """
    state, _, _ = make_state_with_track()
    state.is_playing = True
    state.is_paused = False

    play(state)
    out = capsys.readouterr().out
    assert "Already playing" in out


def test_play_resumes_from_pause(capsys):
    """
        Technique: White-Box Branch Coverage.
        Target Branch: The `elif state.is_paused:` branch within play().

        Explanation:
        We set `is_paused=True`. The code evaluates `is_playing` (False),
        then
        evaluates `is_paused` (True), entering the specific
        branch that resumes
        the audio engine rather than starting from scratch.
    """
    state, track, engine = make_state_with_track()
    state.is_playing = False
    state.is_paused = True

    play(state)
    out = capsys.readouterr().out

    # Verification - The resume() method was called - unique to this branch .
    assert engine.resumed is True
    assert state.is_playing is True
    assert state.is_paused is False
    assert f"Resumed: {track.display_name}" in out


def test_play_fresh_play_starts_engine(capsys):
    """
        Technique: White-Box Branch Coverage.
        Target Branch: The final `else` branch within play().

        Explanation:
        Both `is_playing` and `is_paused` are False.
        This forces the code to fall
        through to the default branch, which handles
        starting a fresh track via `engine.play()`.
    """
    state, track, engine = make_state_with_track()
    # default is not playing and not paused
    state.position_seconds = 5.0

    play(state)
    out = capsys.readouterr().out

    # Verification - engine.play() was called.
    assert engine.play_calls == [(track.path, 5.0)]
    assert state.is_playing is True
    assert state.is_paused is False
    assert f"Playing: {track.display_name}" in out


def test_pause_nothing_to_pause_branch(capsys):
    """
        Technique: White-Box Branch Coverage.
        Target Branch: The `if not state.is_playing:` (or failure)
        branch within pause().

        Explanation:
        We verify the branch that handles invalid requests.
        If nothing is playing,
        the code enters the guard clause and prints a warning.
    """
    state, _, _ = make_state_with_track()
    # default: not playing
    pause(state)
    out = capsys.readouterr().out

    # Verification : The warning branch was executed.
    assert "Nothing to pause" in out


def test_pause_happy_path(capsys):
    """
        Technique: White-Box Branch Coverage.
        Target Branch: The successful pause branch.

        Explanation:
        We set `is_playing=True`. The guard clause evaluates to False, forcing
        execution into the main body of the function where `engine.pause()` is called.
    """
    state, _, engine = make_state_with_track()
    state.is_playing = True
    state.is_paused = False

    pause(state)
    out = capsys.readouterr().out

    # Verification : The pause logic branch was executed.
    assert engine.paused is True
    assert state.is_playing is False
    assert state.is_paused is True
    assert "Paused." in out


def test_stop_nothing_is_playing_branch(capsys):
    """
        Technique: White-Box Branch Coverage.
        Target Branch: The `if not is_playing and not is_paused:`
        branch within stop().

        Explanation:
        We ensure the code handles the case where the player is
        already stopped.
        This triggers the early return branch.
    """
    state, _, _ = make_state_with_track()
    state.is_playing = False
    state.is_paused = False

    stop(state)
    out = capsys.readouterr().out

    # Verification : The warning branch was executed.
    assert "Nothing is playing" in out


def test_stop_happy_path(capsys):
    """
        Technique: White-Box Branch Coverage.
        Target Branch: The successful stop branch.

        Explanation:
        We set `is_playing=True`. The early return check fails, and the code
        proceeds to the branch that resets position and calls `engine.stop()`.
    """
    state, _, engine = make_state_with_track()
    state.is_playing = True
    state.is_paused = False
    state.position_seconds = 42.0

    stop(state)
    out = capsys.readouterr().out

    # Verification : The stop logic branch was executed
    assert engine.stopped is True
    assert state.is_playing is False
    assert state.is_paused is False
    assert state.position_seconds == 0.0
    assert "Stopped." in out


def test_update_playback_ignores_non_positive_delta():
    """
        Technique: White-Box Branch Coverage.
        Target Branch: The `if delta_time <= 0:`
        guard branch.

        Explanation:
        We pass a zero delta. The code should detect
        this condition and
        skip the update logic (the 'True' branch of
        the guard check).
    """
    state, _, _ = make_state_with_track()
    state.is_playing = True
    before = state.position_seconds

    update_playback(state, 0.0)

    # Verification : Position did not change.
    assert state.position_seconds == before


def test_update_playback_stops_at_track_end(capsys):
    """
        Technique: White-Box Branch Coverage.
        Target Branch: The `if position >= duration:`
        branch (Track Finish).

        Explanation:
        We simulate time passing such that `position + delta > duration`.
        This forces the `if` condition to be True,
        entering the branch
        that handles track completion (stopping the
        engine).
    """
    state, track, engine = make_state_with_track(duration=100.0)
    state.is_playing = True
    state.is_paused = False
    state.position_seconds = 95.0

    # delta pushes beyond duration
    update_playback(state, 10.0)
    out = capsys.readouterr().out

    # Verification : The track finish branch was executed (position clamped, engine stopped).
    assert state.position_seconds == track.duration_seconds
    assert state.is_playing is False
    assert engine.stopped is True
    assert "Track finished" in out
