from pathlib import Path
import pytest

from music_player.player_state import PlayerState
from music_player.player_ui import (
    print_now_playing,
    print_progress,
    print_progress_bar,
    print_playlist_with_indicator,
)
from music_player.library import Track


class DummyEngine:
    """Minimal stub to construct a PlayerState without real audio."""
    pass


def make_state_with_tracks(tracks):
    return PlayerState(tracks=tracks, audio_engine=DummyEngine())

def test_branch_now_playing_paused_status(capsys):
    """
    Branch test:
    - Forces the 'Paused' branch of the status selection.
    - Condition chain:
        if is_playing -> else if is_paused -> else (Stopped)
      We specifically hit the 'is_paused' case here.
    """
    track = Track(
        path=Path("a.mp3"),
        title="Song",
        artist="Artist",
        duration_seconds=60,
    )
    state = make_state_with_tracks([track])
    state.current_index = 0
    state.is_playing = False
    state.is_paused = True

    print_now_playing(state)
    out = capsys.readouterr().out
    assert "Paused:" in out


def test_branch_now_playing_stopped_status(capsys):
    """
    Branch test:
    - Forces the 'Stopped' branch.
    - Both is_playing and is_paused are False.
    """
    track = Track(
        path=Path("a.mp3"),
        title="Song",
        artist="Artist",
        duration_seconds=60,
    )
    state = make_state_with_tracks([track])
    state.current_index = 0
    state.is_playing = False
    state.is_paused = False

    print_now_playing(state)
    out = capsys.readouterr().out
    assert "Stopped:" in out

def test_branch_progress_with_track_and_total(capsys):
    """
    Branch test:
    - Forces the branch where a track exists and has a known duration.
    - Ensures both position and total are formatted and printed.
    """
    track = Track(
        path=Path("a.mp3"),
        title="Timed",
        artist="Artist",
        duration_seconds=180.0,
    )
    state = make_state_with_tracks([track])
    state.current_index = 0
    state.position_seconds = 30.0  # 00:30

    print_progress(state)
    out = capsys.readouterr().out
    assert "00:30/03:00" in out

def test_branch_progress_bar_clamps_and_percentage(capsys):
    """
    Branch test:
    - Forces clamping/percentage logic by passing a high position.
      Position beyond duration => 100% bar.
    """
    track = Track(
        path=Path("end.mp3"),
        title="End",
        artist="A",
        duration_seconds=60.0,
    )
    state = make_state_with_tracks([track])
    state.current_index = 0
    state.position_seconds = 999.0  # beyond duration -> clamp to 100%

    # Call without width kwarg – matches current signature
    print_progress_bar(state)
    out = capsys.readouterr().out

    # Just check that it's a full bar / 100%
    assert "[ui]" in out
    assert "100%" in out or "100 %" in out
    # and that some bar characters are present
    assert "█" in out or "░" in out or "#" in out
