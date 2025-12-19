from pathlib import Path
from types import SimpleNamespace

import pytest

from music_player.player_help import print_help
from music_player.player_state import PlayerState
from music_player.player_audio import change_volume
from music_player.player_queue import next_track, previous_track


# --- Test Doubles (Mocks & Stubs) for Backend Isolation ---
class DummyEngine:
    """
        Mock Object: Records volume and mute state changes without audio hardware.
        Used to verify that the Backend-to-Audio-Engine interface functions correctly.
        """
    def __init__(self):
        self.last_volume = None
        self.muted = False

    def set_volume(self, value: int) -> None:
        # Just record the number so we can check it later in the test
        self.last_volume = value

    def set_muted(self, flag: bool) -> None:
        self.muted = flag


# Helper function to quickly set up a player state with a specific volume/mute setting
def make_state_vol(volume: int = 30, muted: bool = False) -> PlayerState:
    """Factory helper to initialise player state with specific volume parameters."""
    engine = DummyEngine()
    state = PlayerState(tracks=[], audio_engine=engine)
    state.volume = volume
    state.is_muted = muted
    return state


# Test to see if the general help command prints the expected list of commands
def test_bb_help_general(capsys):
    print_help()
    out = capsys.readouterr().out
    assert "Available Commands" in out
    assert "/play" in out


# Test to see if asking for help on a specific command works (without the slash)
def test_bb_help_known_command_name(capsys):
    print_help("play")
    out = capsys.readouterr().out
    assert "[Help] /play" in out


# Test to see if asking for help works even if the user includes the slash
def test_bb_help_known_command_with_slash(capsys):
    print_help("/pause")
    out = capsys.readouterr().out
    assert "[Help] /pause" in out


# Test to see if the system handles nonsense commands gracefully
def test_bb_help_unknown_command(capsys):
    print_help("foobar")
    out = capsys.readouterr().out
    assert "not recognised" in out


# Test changing volume normally when the player is NOT muted
def test_bb_change_volume_valid_not_muted(capsys):
    # Frame F5
    state = make_state_vol(volume=30, muted=False)
    engine: DummyEngine = state.audio_engine  # type: ignore[assignment]

    # Change volume to 37
    change_volume(state, "37")
    out = capsys.readouterr().out

    # Check if the state updated and the engine got the message
    assert state.volume == 37
    assert engine.last_volume == 37
    assert "Volume set to 37%" in out
    assert state.is_muted is False


# Test changing volume while muted. This should automatically UNMUTE the player.
def test_bb_change_volume_valid_while_muted_unmutes(capsys):
    # Frame F6
    state = make_state_vol(volume=20, muted=True)
    engine: DummyEngine = state.audio_engine  # type: ignore[assignment]
    state.saved_volume = 20

    # Change volume to 50
    change_volume(state, "50")
    out = capsys.readouterr().out

    # Volume should update, mute should be OFF, and saved volume cleared
    assert state.volume == 50
    assert state.is_muted is False
    assert state.saved_volume is None
    assert engine.last_volume == 50
    assert engine.muted is False
    assert "Volume set to 50%" in out


# Creates a fake song object with just enough info for the queue system to work
def make_track(name: str):
    """Simple stand-in for a Track object with the attributes queue cares about."""
    return SimpleNamespace(
        path=Path(f"{name}.mp3"),
        display_name=name,
        duration_seconds=180.0,
    )


# A fake engine that simulates normal playback (always succeeds).
# It can pretend to be "busy" playing something or not.
class NormalEngine:
    """Engine where is_busy can be configured, play always succeeds."""

    def __init__(self, busy: bool = False, has_is_busy: bool = True):
        self._busy = busy
        self._has_is_busy = has_is_busy
        self.play_calls: list[tuple[Path, float]] = []  # Log calls to play()
        self.stop_calls: int = 0  # Count calls to stop()

    def is_busy(self) -> bool:
        if not self._has_is_busy:
            # Simulate engine without is_busy by not having attribute.
            raise AttributeError("no is_busy")
        return self._busy

    @property
    def has_is_busy(self) -> bool:
        return self._has_is_busy

    def stop(self) -> None:
        self.stop_calls += 1

    def play(self, path, start_pos: float = 0.0) -> None:
        self.play_calls.append((path, start_pos))


# A fake engine that simulates crashes/errors during playback.
# Useful for testing error handling logic.
class FlakyEngine:
    """
    Engine that can fail on the first or both play() attempts.
    Used for PlayFirstFailsSecondOK and PlayBothFail frames.
    """

    def __init__(self, fail_first: bool = False, fail_both: bool = False):
        self.fail_first = fail_first
        self.fail_both = fail_both
        self.play_calls: list[tuple[Path, float]] = []
        self.stop_calls: int = 0
        self._play_count: int = 0

    def is_busy(self) -> bool:
        return False

    def stop(self) -> None:
        self.stop_calls += 1

    def play(self, path, start_pos: float = 0.0) -> None:
        self._play_count += 1
        if self.fail_both:
            raise RuntimeError("play failed (both)")
        if self.fail_first and self._play_count == 1:
            raise RuntimeError("play failed (first)")
        self.play_calls.append((path, start_pos))


# A special test state where the "current track" always vanishes.
# This forces the code into the "Selected track missing" error path.
class TrackMissingState(PlayerState):
    """
    Abnormal state where current_track always returns None,
    to exercise the 'Selected track missing' branch as per NF10 / PF9.
    """

    @property
    def current_track(self):
        return None


# Helper to build a standard player state for the queue tests
def make_state(tracks, engine) -> PlayerState:
    state = PlayerState(tracks=tracks, audio_engine=engine)
    # default flags
    state.current_index = 0
    state.is_playing = False
    state.is_paused = False
    state.position_seconds = 123.0  # something non-zero to see resets
    return state


# Test 'next_track' when the library is empty.
# Expected: Print a message, do not crash, do not change anything.
def test_next_empty_library_prints_message_and_no_change(capsys):
    engine = NormalEngine(busy=False)
    state = make_state([], engine)

    next_track(state)
    out = capsys.readouterr().out

    assert "[queue] No tracks available." in out
    assert state.position_seconds == 123.0
    assert engine.play_calls == []


# Test 'next_track' with only 1 song.
# Expected: It selects the same song again and resets the time to 0.
def test_next_single_stopped_selects_same_track_and_resets_position(capsys):
    engine = NormalEngine(busy=False)
    t1 = make_track("One")
    state = make_state([t1], engine)
    state.is_playing = False
    state.is_paused = False

    next_track(state)
    out = capsys.readouterr().out

    assert state.current_index == 0
    assert state.position_seconds == 0.0
    assert "Selected: One" in out
    assert engine.play_calls == []


# Test 'next_track' with multiple songs (stopped).
# Expected: Move index to the next song.
def test_next_multiple_stopped_moves_to_next_track(capsys):
    engine = NormalEngine(busy=False)
    t1 = make_track("T1")
    t2 = make_track("T2")
    t3 = make_track("T3")
    tracks = [t1, t2, t3]

    state = make_state(tracks, engine)
    state.current_index = 1
    state.is_playing = False
    state.is_paused = False

    next_track(state)
    out = capsys.readouterr().out

    assert state.current_index == 2
    assert state.position_seconds == 0.0
    assert "Selected next: T3" in out
    assert engine.play_calls == []


# Test 'next_track' when currently on the LAST song.
# Expected: Wrap around to the FIRST song.
def test_next_multiple_stopped_wraps_at_end(capsys):
    # NF4_MultiStoppedWrap
    engine = NormalEngine(busy=False)
    t1 = make_track("T1")
    t2 = make_track("T2")
    t3 = make_track("T3")
    tracks = [t1, t2, t3]

    state = make_state(tracks, engine)
    state.current_index = 2  # last
    state.is_playing = False
    state.is_paused = False

    next_track(state)
    out = capsys.readouterr().out

    assert state.current_index == 0
    assert state.position_seconds == 0.0
    assert "Wrapped to next: T1" in out
    assert engine.play_calls == []


# Test 'next_track' while playing (and engine is ready/not busy).
# Expected: Switch to next track and immediately start playing it.
def test_next_multiple_playing_not_busy_starts_playback(capsys):
    # NF5_PlayingNormal
    engine = NormalEngine(busy=False)
    t1 = make_track("T1")
    t2 = make_track("T2")
    tracks = [t1, t2]

    state = make_state(tracks, engine)
    state.current_index = 0
    state.is_playing = True
    state.is_paused = False

    next_track(state)
    out = capsys.readouterr().out

    assert state.current_index == 1
    assert state.position_seconds == 0.0
    assert state.is_playing is True
    assert state.is_paused is False
    assert engine.play_calls[-1][0] == t2.path
    assert "Next: T2" in out or "Wrapped to next: T2" in out


# Test 'next_track' while playing (and engine IS busy).
# Expected: STOP the current track explicitly, then play the next one.
def test_next_multiple_playing_busy_stops_then_plays(capsys):
    # NF6_PlayingBusy
    engine = NormalEngine(busy=True)
    t1 = make_track("T1")
    t2 = make_track("T2")
    tracks = [t1, t2]

    state = make_state(tracks, engine)
    state.current_index = 0
    state.is_playing = True
    state.is_paused = False

    next_track(state)
    out = capsys.readouterr().out

    assert engine.stop_calls >= 1
    assert engine.play_calls[-1][0] == t2.path
    assert state.current_index == 1
    assert state.is_playing is True
    assert state.is_paused is False
    assert "Next: T2" in out or "Wrapped to next: T2" in out


# Test retry logic: The first play attempt fails, but the second works.
# Expected: Player shouldn't crash, should end up playing successfully.
def test_next_play_first_fails_second_ok(capsys):
    # NF7_PlayFirstFailsSecondOK
    engine = FlakyEngine(fail_first=True, fail_both=False)
    t1 = make_track("T1")
    t2 = make_track("T2")
    tracks = [t1, t2]

    state = make_state(tracks, engine)
    state.current_index = 0
    state.is_playing = True
    state.is_paused = False

    next_track(state)
    out = capsys.readouterr().out

    # play attempted at least twice: first fail, second OK
    assert engine.stop_calls >= 1
    assert len(engine.play_calls) == 1
    assert engine.play_calls[0][0] == t2.path
    assert state.is_playing is True
    assert "ERROR starting playback" not in out


# Test catastrophic failure: Playback fails on every attempt.
# Expected: Stop trying, mark state as not playing, print error.
def test_next_play_both_fail_sets_not_playing_and_prints_error(capsys):
    # NF8_PlayBothFail
    engine = FlakyEngine(fail_first=True, fail_both=True)
    t1 = make_track("T1")
    t2 = make_track("T2")
    tracks = [t1, t2]

    state = make_state(tracks, engine)
    state.current_index = 0
    state.is_playing = True
    state.is_paused = False

    next_track(state)
    out = capsys.readouterr().out

    # Both attempts fail, so no successful play_calls recorded
    assert len(engine.play_calls) == 0
    assert state.is_playing is False
    assert state.is_paused is False
    assert "ERROR starting playback" in out


# Test 'next_track' while paused.
# Expected: Move to next track, reset time, but STAY paused (don't auto-play).
def test_next_paused_wraps_and_mentions_paused(capsys):
    # NF9_PausedWrap
    engine = NormalEngine(busy=False)
    t1 = make_track("T1")
    t2 = make_track("T2")
    tracks = [t1, t2]

    state = make_state(tracks, engine)
    state.current_index = 1  # last
    state.is_playing = False
    state.is_paused = True

    next_track(state)
    out = capsys.readouterr().out

    assert state.current_index == 0
    assert state.position_seconds == 0.0
    assert "paused" in out.lower()
    assert engine.play_calls == []  # still paused, not playing


# Test 'next_track' where the track object exists but the file is gone/invalid.
# Expected: Print a warning about missing track.
def test_next_track_missing_prints_warning(capsys):
    # NF10_TrackMissing
    engine = NormalEngine(busy=False)
    tracks = [make_track("T1"), make_track("T2")]
    # abnormal state: current_track is forced to None
    state = TrackMissingState(tracks=tracks, audio_engine=engine)
    state.current_index = 0
    state.is_playing = False
    state.is_paused = False

    next_track(state)
    out = capsys.readouterr().out

    assert "[queue] Selected track missing." in out
    assert engine.play_calls == []


# Test 'previous_track' with empty library.
# Expected: Just print "No tracks".
def test_previous_empty_library_prints_message(capsys):
    engine = NormalEngine(busy=False)
    state = make_state([], engine)

    previous_track(state)
    out = capsys.readouterr().out

    assert "[queue] No tracks available." in out
    assert engine.play_calls == []


# Test 'previous_track' with only 1 song.
# Expected: Selects itself again (restarts).
def test_previous_single_stopped_selects_same_track(capsys):
    engine = NormalEngine(busy=False)
    t1 = make_track("One")
    state = make_state([t1], engine)
    state.is_playing = False
    state.is_paused = False

    previous_track(state)
    out = capsys.readouterr().out

    assert state.current_index == 0
    assert state.position_seconds == 0.0
    # Accept either wording:
    assert ("Selected: One" in out) or ("Wrapped to prev: One" in out)


# Test 'previous_track' moving back normally (e.g., from track 3 to 2).
def test_previous_multi_stopped_moves_back_one(capsys):
    engine = NormalEngine(busy=False)
    t1 = make_track("T1")
    t2 = make_track("T2")
    t3 = make_track("T3")
    tracks = [t1, t2, t3]

    state = make_state(tracks, engine)
    state.current_index = 2  # last
    state.is_playing = False
    state.is_paused = False

    previous_track(state)
    out = capsys.readouterr().out

    assert state.current_index == 1
    assert "Selected prev: T2" in out
    assert engine.play_calls == []


# Test 'previous_track' when at the START of the list.
# Expected: Wrap around to the LAST song.
def test_previous_multi_stopped_wraps_from_first_to_last(capsys):
    engine = NormalEngine(busy=False)
    t1 = make_track("T1")
    t2 = make_track("T2")
    tracks = [t1, t2]

    state = make_state(tracks, engine)
    state.current_index = 0
    state.is_playing = False
    state.is_paused = False

    previous_track(state)
    out = capsys.readouterr().out

    assert state.current_index == 1
    assert "Wrapped to prev: T2" in out
    assert engine.play_calls == []


# Test 'previous_track' while playing (busy engine).
# Expected: Stop current song, play the previous one.
def test_previous_playing_busy_stops_then_plays_previous(capsys):
    engine = NormalEngine(busy=True)
    t1 = make_track("T1")
    t2 = make_track("T2")
    tracks = [t1, t2]

    state = make_state(tracks, engine)
    state.current_index = 1
    state.is_playing = True
    state.is_paused = False

    previous_track(state)
    out = capsys.readouterr().out

    assert engine.stop_calls >= 1
    assert engine.play_calls[-1][0] == t1.path
    assert state.current_index == 0
    assert state.is_playing is True
    assert "Previous: T1" in out or "Wrapped to prev: T1" in out


# Test 'previous_track' where playback fails totally.
# Expected: Print error and stop playing.
def test_previous_play_both_fail_prints_error_and_stops(capsys):
    engine = FlakyEngine(fail_first=True, fail_both=True)
    t1 = make_track("T1")
    t2 = make_track("T2")
    tracks = [t1, t2]

    state = make_state(tracks, engine)
    state.current_index = 1
    state.is_playing = True
    state.is_paused = False

    previous_track(state)
    out = capsys.readouterr().out

    assert len(engine.play_calls) == 0
    assert state.is_playing is False
    assert state.is_paused is False
    assert "ERROR starting playback" in out


# Test 'previous_track' while paused.
# Expected: Change track, stay paused.
def test_previous_paused_wraps_and_mentions_paused(capsys):
    engine = NormalEngine(busy=False)
    t1 = make_track("T1")
    t2 = make_track("T2")
    tracks = [t1, t2]

    state = make_state(tracks, engine)
    state.current_index = 0
    state.is_playing = False
    state.is_paused = True

    previous_track(state)
    out = capsys.readouterr().out

    assert state.current_index == 1
    assert "paused" in out.lower()
    assert engine.play_calls == []


# Test 'previous_track' where the file is missing/invalid.
# Expected: Print warning.
def test_previous_track_missing_prints_warning(capsys):
    engine = NormalEngine(busy=False)
    tracks = [make_track("T1"), make_track("T2")]
    state = TrackMissingState(tracks=tracks, audio_engine=engine)
    state.current_index = 0
    state.is_playing = False
    state.is_paused = False

    previous_track(state)
    out = capsys.readouterr().out

    assert "[queue] Selected track missing." in out
    assert engine.play_calls == []