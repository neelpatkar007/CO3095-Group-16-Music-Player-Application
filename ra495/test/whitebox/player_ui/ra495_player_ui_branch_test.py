from pathlib import Path
import pytest

from music_player.player_state import PlayerState
from music_player.player_ui import (
    print_now_playing,
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


# -------------------------------
# Branch testing – print_playlist_with_indicator
# -------------------------------


def test_branch_playlist_invalid_tracks_structure(capsys):
    """
    Branch test:
    - Forces the branch where 'tracks' is not a proper list of Track-like
      objects, triggering the 'invalid state' warning.
    """
    state = make_state_with_tracks([])
    # Break the invariant: tracks is not a list
    state.tracks = "not-a-list"  # type: ignore[assignment]

    print_playlist_with_indicator(state)
    out = capsys.readouterr().out
    assert "Library is in an invalid state" in out


def test_branch_playlist_single_track_with_warnings(capsys):
    """
    Branch test:
    - Forces both:
        * missing-metadata warning (empty title/artist/display_name)
        * 'only one track' warning
      and ensures that the active marker is printed.
    """
    bad_track = Track(
        path=Path("x.mp3"),
        title="",
        artist="",
        duration_seconds=60,
    )
    state = make_state_with_tracks([bad_track])

    print_playlist_with_indicator(state)
    out = capsys.readouterr().out
    assert "Some tracks have missing titles" in out
    assert "Only one track in the library" in out
    assert "•" in out or "▶" in out or "‖" in out


def test_branch_playlist_multi_track_clamps_index_and_markers(capsys):
    """
    Branch test:
    - Forces:
        * current_index >= len(tracks) -> clamping to last index
        * 'playing' marker for the clamped index.
    """
    t1 = Track(path=Path("t1.mp3"), title="T1", artist="A", duration_seconds=60)
    t2 = Track(path=Path("t2.mp3"), title="T2", artist="A", duration_seconds=60)
    t3 = Track(path=Path("t3.mp3"), title="T3", artist="A", duration_seconds=60)

    state = make_state_with_tracks([t1, t2, t3])
    state.current_index = 10  # out of range -> should clamp to 2
    state.is_playing = True

    print_playlist_with_indicator(state)
    out = capsys.readouterr().out
    assert "03: T3 – A" in out