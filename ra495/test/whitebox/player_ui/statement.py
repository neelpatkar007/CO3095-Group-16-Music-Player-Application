from pathlib import Path

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


# Statement testing – print_now_playing


def test_stmt_now_playing_invalid_state_type(capsys):
    """
    Statement test:
    - Executes the early type guard in print_now_playing
      with a completely invalid state object.
    - Ensures the 'invalid state' branch is executed.
    """
    print_now_playing("not-a-state")  # type: ignore[arg-type]
    out = capsys.readouterr().out
    assert "Invalid player state for now_playing" in out


def test_stmt_now_playing_no_track_selected(capsys):
    """
    Statement test:
    - Executes the 'no current track' path.
    - Covers the 'No track selected' line.
    """
    state = make_state_with_tracks([])
    print_now_playing(state)
    out = capsys.readouterr().out
    assert "No track selected" in out


def test_stmt_now_playing_playing_status(capsys):
    """
    Statement test:
    - Executes the normal 'Playing' path.
    - Ensures formatting of title/artist/time is exercised.
    """
    track = Track(
        path=Path("a.mp3"),
        title="Song",
        artist="Artist",
        duration_seconds=120,
    )
    state = make_state_with_tracks([track])
    state.current_index = 0
    state.is_playing = True
    state.is_paused = False

    print_now_playing(state)
    out = capsys.readouterr().out
    assert "Playing:" in out
    assert "Song – Artist" in out
    assert "[02:00]" in out


# Statement testing – print_playlist_with_indicator


def test_stmt_playlist_invalid_state_type(capsys):
    """
    Statement test:
    - Executes type guard in print_playlist_with_indicator.
    """
    print_playlist_with_indicator("oops")  # type: ignore[arg-type]
    out = capsys.readouterr().out
    assert "Invalid player state for playlist" in out


def test_stmt_playlist_empty_library(capsys):
    """
    Statement test:
    - Executes the 'library is empty' path.
    """
    state = make_state_with_tracks([])
    print_playlist_with_indicator(state)
    out = capsys.readouterr().out
    assert "Library is empty" in out
