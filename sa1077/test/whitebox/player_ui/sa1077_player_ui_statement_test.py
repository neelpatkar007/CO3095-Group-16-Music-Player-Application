from pathlib import Path

from music_player.player_state import PlayerState
from music_player.player_ui import (
    print_progress,
    print_progress_bar,
)
from music_player.library import Track


# Test: A minimal fake engine used to skip the real audio hardware during UI testing
class DummyEngine:
    pass


# Test: Helper function to quickly set up a player state for testing
def make_state_with_tracks(tracks):
    return PlayerState(tracks=tracks, audio_engine=DummyEngine())


# Test: ensuring the system handles incorrect data types (like a boolean) without crashing
def test_stmt_progress_invalid_state_type(capsys):
    print_progress(True)  # type: ignore[arg-type]
    out = capsys.readouterr().out
    assert "Invalid player state for progress" in out


# Test: checking that the UI shows unknown time markers when the track list is empty
def test_stmt_progress_no_track_total_unknown(capsys):
    state = make_state_with_tracks([])
    print_progress(state)
    out = capsys.readouterr().out
    assert "00:00/??:??" in out


# Test: ensuring the progress bar system correctly catches and reports invalid input types
def test_stmt_progress_bar_invalid_state_type(capsys):
    print_progress_bar(123)  # type: ignore[arg-type]
    out = capsys.readouterr().out
    assert "Invalid player state for progress_bar" in out


# Test: verifying that a standard progress bar is rendered correctly for a song in progress
def test_stmt_progress_bar_normal(capsys):
    track = Track(
        path=Path("a.mp3"),
        title="Song",
        artist="Artist",
        duration_seconds=100,
    )
    state = make_state_with_tracks([track])
    state.current_index = 0
    state.position_seconds = 50.0

    print_progress_bar(state)
    out = capsys.readouterr().out
    # Just assert that a bar was printed
    assert "█" in out or "░" in out