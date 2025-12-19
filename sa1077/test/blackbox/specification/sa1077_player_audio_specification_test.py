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

class DummyEngine:
    """Mock audio engine used to record state changes without needing hardware access."""
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

# --- Helper functions to maintain consistent test state across cases ---
def make_state(volume: int = 30, muted: bool = False) -> PlayerState:
    engine = DummyEngine()
    state = PlayerState(tracks=[], audio_engine=engine)
    state.volume = volume
    state.is_muted = muted
    return state

def make_state_ui(tracks, current_index: int = 0) -> PlayerState:
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

# --- Black-Box Specification Testing: Volume Control ---

def test_bb_change_volume_show_current_from_empty_input(capsys):
    # Equivalence Partition (EP): Verifying that empty input acts as a 'query' for current volume.
    state = make_state(volume=42, muted=False)
    change_volume(state, "")
    out = capsys.readouterr().out
    assert "Current Volume: 42%" in out
    assert state.volume == 42
    assert state.is_muted is False


def test_bb_change_volume_error_non_numeric(capsys):
    # EP: Confirming that alphanumeric strings are caught by the input sanitisation logic.
    state = make_state(volume=30, muted=False)
    change_volume(state, "abc")
    out = capsys.readouterr().out
    assert "[audio] Error: Volume must be a number.\n" in out
    assert state.volume == 30


def test_bb_change_volume_error_range_low(capsys):
    # Boundary Value Analysis (BVA): Testing the lower limit boundary (input < 0).
    state = make_state(volume=30, muted=False)
    change_volume(state, "-1")
    out = capsys.readouterr().out
    assert "between 0 and 100" in out
    assert state.volume == 30


def test_bb_change_volume_error_range_high(capsys):
    # BVA: Testing the upper limit boundary (input > 100).
    state = make_state(volume=30, muted=False)
    change_volume(state, "101")
    out = capsys.readouterr().out
    assert "between 0 and 100" in out
    assert state.volume == 30

    # --- Black-Box Specification Testing: Seek & Nudge Logic ---

def test_bb_seek_seconds_within_range():
    # Specification Test: Ensuring standard numeric seek correctly updates playhead position.
    state = make_state_with_track(60.0)
    seek_to(state, "30")
    assert state.position_seconds == pytest.approx(30.0)
    pos, total = get_progress(state)
    assert pos == pytest.approx(30.0)
    assert total == 60.0


def test_bb_seek_seconds_clamped_to_end():
    # BVA: Verifying that seeking beyond the track duration is clamped to the end time.
    state = make_state_with_track(60.0)
    seek_to(state, "100")
    assert state.position_seconds == pytest.approx(60.0)


def test_bb_seek_mmss_string():
    # Specification Test: Validating timecode parsing for the 'mm:ss' string format.
    state = make_state_with_track(200.0)
    seek_to(state, "01:30")
    assert state.position_seconds == pytest.approx(90.0)


def test_bb_seek_empty_string_parsed_to_zero():
    # EP: Verifying that an empty string is treated as a 0.0 value to prevent system crashes.
    state = make_state_with_track(200.0)
    seek_to(state, "")
    assert state.position_seconds == pytest.approx(0.0)


def test_bb_seek_invalid_string_parsed_to_zero():
    # Robustness Test: Ensuring malformed alphanumeric strings default to the start of the track.
    state = make_state_with_track(200.0)
    seek_to(state, "xVSd6\tE")
    assert state.position_seconds == pytest.approx(0.0)


def test_bb_seek_negative_clamped_to_zero():
    # BVA: Lower boundary check—ensuring negative seek values are clamped to 0.0.
    state = make_state_with_track(60.0)
    seek_to(state, "-10")
    assert state.position_seconds == pytest.approx(0.0)


def test_bb_nudge_forward_and_clamped():
    # BVA: Verifying that nudging forward near the end of a track does not exceed the duration.
    state = make_state_with_track(60.0)
    state.position_seconds = 58.0
    nudge(state, 5.0)
    assert state.position_seconds == pytest.approx(60.0)


def test_bb_nudge_backward_and_clamped(capsys):
    # BVA: Verifying that nudging backward near the start of a track does not go below 0.0.
    state = make_state_with_track(60.0)
    state.position_seconds = 2.0
    nudge(state, -5.0)
    assert state.position_seconds == pytest.approx(0.0)

    # Type Verification: Confirming the UI layer rejects boolean types for progress updates.
    print_progress(True)  # type: ignore[arg-type]
    out = capsys.readouterr().out
    assert "[ui] Invalid player state for progress." in out


def test_ui_progress_valid_state_no_track_unknown_time(capsys):
    # Null-Case Testing: Verifying the UI correctly indicates unknown time when no track is loaded.
    state = make_state_ui(tracks=[])
    print_progress(state)
    out = capsys.readouterr().out
    # Code prints 00:00 for position, ?? for total
    assert "[ui] Progress: 00:00/??:??" in out


def test_ui_progress_valid_state_track_without_duration(capsys):
    # Edge Case: Ensuring tracks with missing duration metadata default to placeholder displays.
    track = make_track(title="DurLess", artist="A", duration=0.0)
    track.duration_seconds = None

    state = make_state_ui(tracks=[track])
    state.current_index = 0
    print_progress(state)
    out = capsys.readouterr().out

    assert "[ui] Progress: 00:00/??:??" in out


def test_ui_progress_with_known_duration_shows_formatted_times(capsys):
    # Specification Test: Confirming high-precision formatting for standard playhead positions.
    track = make_track(title="Timed", artist="A", duration=180.0)
    state = make_state_ui(tracks=[track])
    state.current_index = 0
    state.position_seconds = 30.0

    print_progress(state)
    out = capsys.readouterr().out

    assert "[ui] Progress: 00:30/03:00" in out

def test_ui_bar_invalid_state_prints_null(capsys):
    # Robustness Test: Verifying that the progress bar rendering system traps type errors.
    print_progress_bar(False)  # type: ignore[arg-type]
    out = capsys.readouterr().out
    assert "[ui] Invalid player state for progress_bar." in out


def test_ui_bar_no_track_unknown_bar(capsys):
    # Null-Case Testing: Verifying the progress bar renders a 'null' state when no music is present.
    state = make_state_ui(tracks=[])
    print_progress_bar(state)
    out = capsys.readouterr().out
    # Your implementation currently prints this:
    assert "[ui] [Time null]" in out


def test_ui_bar_track_without_duration_unknown_bar(capsys):
    # Boundary Case: Testing the progress bar's resilience when duration metadata is missing.
    track = make_track(title="DurLess", duration=0.0)
    track.duration_seconds = None
    state = make_state_ui(tracks=[track])
    state.current_index = 0

    print_progress_bar(state)
    out = capsys.readouterr().out
    assert "[ui] [Time null]" in out


def test_ui_bar_within_range_shows_bar_and_percentage(capsys):
    # Specification Test: Verifying the correct visual rendering of the ASCII progress bar at 50%.
    track = make_track(title="Half", duration=60.0)
    state = make_state_ui(tracks=[track])
    state.current_index = 0
    state.position_seconds = 30.0

    print_progress_bar(state)
    out = capsys.readouterr().out

    # Minimal, implementation-friendly checks:
    assert "[ui]" in out
    # Ensure we didn't hit the null/invalid paths
    assert "Invalid player state for progress_bar" not in out
    assert "[Time null]" not in out


def test_ui_bar_clamps_position_beyond_duration(capsys):
    # BVA: Verifying that the progress bar clamps to 100% even if internal position exceeds duration.
    track = make_track(title="End", duration=60.0)
    state = make_state_ui(tracks=[track])
    state.current_index = 0
    state.position_seconds = 999.0

    print_progress_bar(state)
    out = capsys.readouterr().out

    assert "[ui]" in out
    assert "Invalid player state for progress_bar" not in out
    assert "[Time null]" not in out

def test_ui_progress_invalid_state_type_prints_null(capsys):
    # Type Guard Verification: Confirming the UI layer properly catches and reports boolean type errors.
    print_progress(True)  # type: ignore[arg-type]
    out = capsys.readouterr().out
    assert "[ui] Invalid player state for progress." in out


def test_ui_progress_valid_state_no_track_unknown_time(capsys):
    # Logic Path Verification: Ensuring no track loads lead to the '??:??' unknown time format.
    state = make_state_ui(tracks=[])
    print_progress(state)
    out = capsys.readouterr().out
    # Code prints 00:00 for position, ?? for total
    assert "[ui] Progress: 00:00/??:??" in out


def test_ui_progress_valid_state_track_without_duration(capsys):
    # Data Robustness: Ensuring the UI defaults to safe placeholders if track duration is missing.
    track = make_track(title="DurLess", artist="A", duration=0.0)
    track.duration_seconds = None

    state = make_state_ui(tracks=[track])
    state.current_index = 0
    print_progress(state)
    out = capsys.readouterr().out

    assert "[ui] Progress: 00:00/??:??" in out
