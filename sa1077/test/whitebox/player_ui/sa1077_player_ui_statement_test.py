from pathlib import Path

from music_player.player_state import PlayerState
from music_player.player_ui import (
    print_progress,
    print_progress_bar,
)
from music_player.library import Track


class DummyEngine:
    """Minimal test double to bypass the audio backend for UI testing."""
    pass


def make_state_with_tracks(tracks):
    """Utility to quickly set up a PlayerState for unit tests."""
    return PlayerState(tracks=tracks, audio_engine=DummyEngine())


def test_stmt_progress_invalid_state_type(capsys):
    """Statement test: Exercises the guard clause for invalid data types."""
    print_progress(True)  # type: ignore[arg-type]
    out = capsys.readouterr().out
    assert "Invalid player state for progress" in out


def test_stmt_progress_no_track_total_unknown(capsys):
    """Statement test: Checks UI behavior when the tracklist is empty."""
    state = make_state_with_tracks([])
    print_progress(state)
    out = capsys.readouterr().out
    assert "00:00/??:??" in out


def test_stmt_progress_bar_invalid_state_type(capsys):
    """Statement test: Hits the error path for invalid inputs in the progress bar."""
    print_progress_bar(123)  # type: ignore[arg-type]
    out = capsys.readouterr().out
    assert "Invalid player state for progress_bar" in out


def test_stmt_progress_bar_normal(capsys):
    """Statement test: Standard execution path for rendering the ASCII bar."""
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
