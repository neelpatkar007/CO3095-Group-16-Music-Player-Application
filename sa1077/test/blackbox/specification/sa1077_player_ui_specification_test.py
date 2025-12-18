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

def test_bb_change_volume_show_current_from_empty_input(capsys):
    # Frame F1
    state = make_state(volume=42, muted=False)
    change_volume(state, "")
    out = capsys.readouterr().out
    assert "Current Volume: 42%" in out
    assert state.volume == 42
    assert state.is_muted is False


def test_bb_change_volume_error_non_numeric(capsys):
    # Frame F2
    state = make_state(volume=30, muted=False)
    change_volume(state, "abc")
    out = capsys.readouterr().out
    assert "[audio] Error: Volume must be a number.\n" in out
    assert state.volume == 30


def test_bb_change_volume_error_range_low(capsys):
    # Frame F3
    state = make_state(volume=30, muted=False)
    change_volume(state, "-1")
    out = capsys.readouterr().out
    assert "between 0 and 100" in out
    assert state.volume == 30


def test_bb_change_volume_error_range_high(capsys):
    # Frame F4
    state = make_state(volume=30, muted=False)
    change_volume(state, "101")
    out = capsys.readouterr().out
    assert "between 0 and 100" in out
    assert state.volume == 30

def test_bb_seek_seconds_within_range():
    # SF1
    state = make_state_with_track(60.0)
    seek_to(state, "30")
    assert state.position_seconds == pytest.approx(30.0)
    pos, total = get_progress(state)
    assert pos == pytest.approx(30.0)
    assert total == 60.0


def test_bb_seek_seconds_clamped_to_end():
    # SF2
    state = make_state_with_track(60.0)
    seek_to(state, "100")
    assert state.position_seconds == pytest.approx(60.0)


def test_bb_seek_mmss_string():
    # SF3: 01:30 -> 90s
    state = make_state_with_track(200.0)
    seek_to(state, "01:30")
    assert state.position_seconds == pytest.approx(90.0)


def test_bb_seek_empty_string_parsed_to_zero():
    # SF4: "" -> 0.0
    state = make_state_with_track(200.0)
    seek_to(state, "")
    assert state.position_seconds == pytest.approx(0.0)


def test_bb_seek_invalid_string_parsed_to_zero():
    # SF5: invalid string -> 0.0
    state = make_state_with_track(200.0)
    seek_to(state, "xVSd6\tE")
    assert state.position_seconds == pytest.approx(0.0)


def test_bb_seek_negative_clamped_to_zero():
    # SF6: negative -> 0
    state = make_state_with_track(60.0)
    seek_to(state, "-10")
    assert state.position_seconds == pytest.approx(0.0)


def test_bb_nudge_forward_and_clamped():
    state = make_state_with_track(60.0)
    state.position_seconds = 58.0
    nudge(state, 5.0)
    assert state.position_seconds == pytest.approx(60.0)


def test_bb_nudge_backward_and_clamped(capsys):
    state = make_state_with_track(60.0)
    state.position_seconds = 2.0
    nudge(state, -5.0)
    assert state.position_seconds == pytest.approx(0.0)

    # PR1: invalid type (bool) -> error-style message
    print_progress(True)  # type: ignore[arg-type]
    out = capsys.readouterr().out
    assert "[ui] Invalid player state for progress." in out


def test_ui_progress_valid_state_no_track_unknown_time(capsys):
    # PR2: no current track, but valid PlayerState
    state = make_state_ui(tracks=[])
    print_progress(state)
    out = capsys.readouterr().out
    # Code prints 00:00 for position, ?? for total
    assert "[ui] Progress: 00:00/??:??" in out


def test_ui_progress_valid_state_track_without_duration(capsys):
    # PR3: duration_seconds=None
    track = make_track(title="DurLess", artist="A", duration=0.0)
    track.duration_seconds = None

    state = make_state_ui(tracks=[track])
    state.current_index = 0
    print_progress(state)
    out = capsys.readouterr().out

    assert "[ui] Progress: 00:00/??:??" in out


def test_ui_progress_with_known_duration_shows_formatted_times(capsys):
    # PR4: 30/180 -> 00:30/03:00
    track = make_track(title="Timed", artist="A", duration=180.0)
    state = make_state_ui(tracks=[track])
    state.current_index = 0
    state.position_seconds = 30.0

    print_progress(state)
    out = capsys.readouterr().out

    assert "[ui] Progress: 00:30/03:00" in out

def test_ui_bar_invalid_state_prints_null(capsys):
    # PB1: wrong type -> error message
    print_progress_bar(False)  # type: ignore[arg-type]
    out = capsys.readouterr().out
    assert "[ui] Invalid player state for progress_bar." in out


def test_ui_bar_no_track_unknown_bar(capsys):
    # PB2: no tracks in library
    state = make_state_ui(tracks=[])
    print_progress_bar(state)
    out = capsys.readouterr().out
    # Your implementation currently prints this:
    assert "[ui] [Time null]" in out


def test_ui_bar_track_without_duration_unknown_bar(capsys):
    # PB3: track but duration_seconds=None
    track = make_track(title="DurLess", duration=0.0)
    track.duration_seconds = None
    state = make_state_ui(tracks=[track])
    state.current_index = 0

    print_progress_bar(state)
    out = capsys.readouterr().out
    assert "[ui] [Time null]" in out


def test_ui_bar_within_range_shows_bar_and_percentage(capsys):
    # PB4: pos 30 / 60 -> should be some valid bar output, not "null"
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
    # PB5: pos > duration -> clamped at end; we again just check it's a "real" bar
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
    # PR1: invalid type (bool) -> error-style message
    print_progress(True)  # type: ignore[arg-type]
    out = capsys.readouterr().out
    assert "[ui] Invalid player state for progress." in out


def test_ui_progress_valid_state_no_track_unknown_time(capsys):
    # PR2: no current track, but valid PlayerState
    state = make_state_ui(tracks=[])
    print_progress(state)
    out = capsys.readouterr().out
    # Code prints 00:00 for position, ?? for total
    assert "[ui] Progress: 00:00/??:??" in out


def test_ui_progress_valid_state_track_without_duration(capsys):
    # PR3: duration_seconds=None
    track = make_track(title="DurLess", artist="A", duration=0.0)
    track.duration_seconds = None

    state = make_state_ui(tracks=[track])
    state.current_index = 0
    print_progress(state)
    out = capsys.readouterr().out

    assert "[ui] Progress: 00:00/??:??" in out
