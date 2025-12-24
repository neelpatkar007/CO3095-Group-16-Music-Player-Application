from pathlib import Path

import pytest

from music_player.library import Track
from music_player.player_seek import seek_to, nudge, get_progress
from music_player.player_state import PlayerState
from music_player.player_audio import change_volume

from music_player.player_ui import (
    print_progress,
    print_progress_bar,
)

# Test: A mock audio engine used to record actions without needing real hardware
class DummyEngine:
    def __init__(self):
        self.last_volume = None
        self.muted = False
        self.last_seek: float | None = None

    def set_volume(self, value: int) -> None:
        self.last_volume = value

    def set_muted(self, flag: bool) -> None:
        self.muted = flag

    def seek(self, position: float) -> None:
        """No-op seek; just record the position."""
        self.last_seek = float(position)

    def play(self, path, start_pos: float = 0.0) -> None:
        pass

    def stop(self) -> None:
        pass

    def is_busy(self) -> bool:
        return False


# Test: Helper to create a basic player state for testing
def make_state(volume: int = 30, muted: bool = False) -> PlayerState:
    engine = DummyEngine()
    state = PlayerState(tracks=[], audio_engine=engine)
    state.volume = volume
    state.is_muted = muted
    return state

# Test: Helper to create a player state specifically for UI testing
def make_state_ui(tracks, current_index: int = 0) -> PlayerState:
    state = PlayerState(tracks=tracks, audio_engine=DummyEngine())
    state.current_index = current_index
    return state


# Test: Helper to create a single track object with default data
def make_track(title: str = "Song", artist: str = "Unknown", duration: float = 180.0) -> Track:
    return Track(
        path=Path(f"{title}.mp3"),
        title=title,
        artist=artist,
        duration_seconds=duration,
    )

# Test: Helper to build a valid state that already has a track loaded
def make_state_with_track(duration: float) -> PlayerState:
    """Helper used by the tests to build a valid PlayerState."""

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

# Test: checking that leaving the volume input blank just displays the current volume
def test_bb_change_volume_show_current_from_empty_input(capsys):
    state = make_state(volume=42, muted=False)
    change_volume(state, "")
    out = capsys.readouterr().out
    assert "Current Volume: 42%" in out
    assert state.volume == 42
    assert state.is_muted is False


# Test: ensuring an error is shown if the volume input is text instead of a number
def test_bb_change_volume_error_non_numeric(capsys):
    state = make_state(volume=30, muted=False)
    change_volume(state, "abc")
    out = capsys.readouterr().out
    assert "[audio] Error: Volume must be a number.\n" in out
    assert state.volume == 30


# Test: ensuring the system rejects volume settings below zero
def test_bb_change_volume_error_range_low(capsys):
    state = make_state(volume=30, muted=False)
    change_volume(state, "-1")
    out = capsys.readouterr().out
    assert "between 0 and 100" in out
    assert state.volume == 30


# Test: ensuring the system rejects volume settings above 100
def test_bb_change_volume_error_range_high(capsys):
    state = make_state(volume=30, muted=False)
    change_volume(state, "101")
    out = capsys.readouterr().out
    assert "between 0 and 100" in out
    assert state.volume == 30

# Test: verifying that seeking to a specific second updates the position correctly
def test_bb_seek_seconds_within_range():
    state = make_state_with_track(60.0)
    seek_to(state, "30")
    assert state.position_seconds == pytest.approx(30.0)
    pos, total = get_progress(state)
    assert pos == pytest.approx(30.0)
    assert total == 60.0


# Test: ensuring that seeking past the end of a track stops exactly at the finish time
def test_bb_seek_seconds_clamped_to_end():
    state = make_state_with_track(60.0)
    seek_to(state, "100")
    assert state.position_seconds == pytest.approx(60.0)


# Test: checking that time codes (minutes:seconds) are correctly converted to seconds
def test_bb_seek_mmss_string():
    state = make_state_with_track(200.0)
    seek_to(state, "01:30")
    assert state.position_seconds == pytest.approx(90.0)


# Test: ensuring that a blank seek input is treated as the start of the song (zero)
def test_bb_seek_empty_string_parsed_to_zero():
    state = make_state_with_track(200.0)
    seek_to(state, "")
    assert state.position_seconds == pytest.approx(0.0)


# Test: ensuring that invalid text in the seek bar resets the position to the start
def test_bb_seek_invalid_string_parsed_to_zero():
    state = make_state_with_track(200.0)
    seek_to(state, "xVSd6\tE")
    assert state.position_seconds == pytest.approx(0.0)


# Test: ensuring that trying to seek to a negative time resets to zero
def test_bb_seek_negative_clamped_to_zero():
    state = make_state_with_track(60.0)
    seek_to(state, "-10")
    assert state.position_seconds == pytest.approx(0.0)


# Test: verifying that skipping forward near the end of a song doesn't go past the end
def test_bb_nudge_forward_and_clamped():
    state = make_state_with_track(60.0)
    state.position_seconds = 58.0
    nudge(state, 5.0)
    assert state.position_seconds == pytest.approx(60.0)


# Test: verifying that skipping backward near the start of a song doesn't go below zero
def test_bb_nudge_backward_and_clamped(capsys):
    state = make_state_with_track(60.0)
    state.position_seconds = 2.0
    nudge(state, -5.0)
    assert state.position_seconds == pytest.approx(0.0)

    # Test: checking that the UI prints an error if it receives a True/False value instead of a state
    print_progress(True)  # type: ignore[arg-type]
    out = capsys.readouterr().out
    assert "[ui] Invalid player state for progress." in out


# Test: ensuring that '??:??' is shown for total time when the track list is empty
def test_ui_progress_valid_state_no_track_unknown_time(capsys):
    state = make_state_ui(tracks=[])
    print_progress(state)
    out = capsys.readouterr().out
    assert "[ui] Progress: 00:00/??:??" in out


# Test: checking that the UI handles tracks that have no duration data by showing placeholders
def test_ui_progress_valid_state_track_without_duration(capsys):
    track = make_track(title="DurLess", artist="A", duration=0.0)
    track.duration_seconds = None

    state = make_state_ui(tracks=[track])
    state.current_index = 0
    print_progress(state)
    out = capsys.readouterr().out

    assert "[ui] Progress: 00:00/??:??" in out


# Test: verifying that progress is formatted as minutes and seconds (e.g., 00:30/03:00)
def test_ui_progress_with_known_duration_shows_formatted_times(capsys):
    track = make_track(title="Timed", artist="A", duration=180.0)
    state = make_state_ui(tracks=[track])
    state.current_index = 0
    state.position_seconds = 30.0

    print_progress(state)
    out = capsys.readouterr().out

    assert "[ui] Progress: 00:30/03:00" in out

# Test: ensuring the progress bar system ignores invalid input types
def test_ui_bar_invalid_state_prints_null(capsys):
    print_progress_bar(False)  # type: ignore[arg-type]
    out = capsys.readouterr().out
    assert "[ui] Invalid player state for progress_bar." in out


# Test: verifying the progress bar displays "[Time null]" when no music is present
def test_ui_bar_no_track_unknown_bar(capsys):
    state = make_state_ui(tracks=[])
    print_progress_bar(state)
    out = capsys.readouterr().out
    assert "[ui] [Time null]" in out


# Test: checking that the progress bar handles tracks with missing time metadata safely
def test_ui_bar_track_without_duration_unknown_bar(capsys):
    track = make_track(title="DurLess", duration=0.0)
    track.duration_seconds = None
    state = make_state_ui(tracks=[track])
    state.current_index = 0

    print_progress_bar(state)
    out = capsys.readouterr().out
    assert "[ui] [Time null]" in out


# Test: verifying that the visual progress bar renders correctly for a song in progress
def test_ui_bar_within_range_shows_bar_and_percentage(capsys):
    track = make_track(title="Half", duration=60.0)
    state = make_state_ui(tracks=[track])
    state.current_index = 0
    state.position_seconds = 30.0

    print_progress_bar(state)
    out = capsys.readouterr().out

    assert "[ui]" in out
    assert "Invalid player state for progress_bar" not in out
    assert "[Time null]" not in out


# Test: ensuring the progress bar doesn't break if the internal timer goes beyond the song length
def test_ui_bar_clamps_position_beyond_duration(capsys):
    track = make_track(title="End", duration=60.0)
    state = make_state_ui(tracks=[track])
    state.current_index = 0
    state.position_seconds = 999.0

    print_progress_bar(state)
    out = capsys.readouterr().out

    assert "[ui]" in out
    assert "Invalid player state for progress_bar" not in out
    assert "[Time null]" not in out

# Test: verifying that an error message is printed if an incorrect data type is used for progress
def test_ui_progress_invalid_state_type_prints_null(capsys):
    print_progress(True)  # type: ignore[arg-type]
    out = capsys.readouterr().out
    assert "[ui] Invalid player state for progress." in out


# Test: ensuring the UI defaults to safe placeholders when there are no tracks loaded
def test_ui_progress_valid_state_no_track_unknown_time(capsys):
    state = make_state_ui(tracks=[])
    print_progress(state)
    out = capsys.readouterr().out
    assert "[ui] Progress: 00:00/??:??" in out


# Test: ensuring the UI handles tracks without duration data without crashing
def test_ui_progress_valid_state_track_without_duration(capsys):
    track = make_track(title="DurLess", artist="A", duration=0.0)
    track.duration_seconds = None

    state = make_state_ui(tracks=[track])
    state.current_index = 0
    print_progress(state)
    out = capsys.readouterr().out

    assert "[ui] Progress: 00:00/??:??" in out