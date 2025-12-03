from pathlib import Path
import pytest

from music_player.player_state import PlayerState
from music_player.player_ui import (
    print_progress,
    print_progress_bar,
)
from music_player.library import Track


class DummyEngine:
    """Minimal stub to construct a PlayerState without real audio."""
    pass


def make_state_with_tracks(tracks):
    return PlayerState(tracks=tracks, audio_engine=DummyEngine())


def test_stmt_progress_invalid_state_type(capsys):
    """
    Statement test:

Executes the type guard in print_progress."""


print_progress(True)  # type: ignore[arg-type]
out = capsys.readouterr().out
assert "Invalid player state for progress" in out


def test_stmt_progress_no_track_total_unknown(capsys):
    """
    Statement test:

Executes print_progress on a valid state with no tracks.
Ensures the 'no total duration' path is exercised(total shown as '??:??')."""


state = make_state_with_tracks([])
print_progress(state)
out = capsys.readouterr().out
assert "00:00/??:??" in out


def test_stmt_progress_bar_invalid_state_type(capsys):
    """
    Statement test:

Executes the type guard in print_progress_bar."""


print_progress_bar(123)  # type: ignore[arg-type]
out = capsys.readouterr().out
assert "Invalid player state for progress_bar" in out


def test_stmt_progress_bar_normal(capsys):
    """
    Statement test:

Executes the normal rendering of a progress bar."""


track = Track(
    path=Path("a.mp3"),
    title="Song",
    artist="Artist",
    duration_seconds=100, )
state = make_state_with_tracks([track])
state.current_index = 0
state.position_seconds = 50.0

print_progress_bar(state)
out = capsys.readouterr().out
# Just assert that a bar was printed
assert "█" in out or "░" in out
