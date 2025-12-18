from pathlib import Path
import pytest

from music_player.player_state import PlayerState
from music_player.player_ui import (
    print_now_playing,
    print_playlist_with_indicator,
)
from music_player.library import Track


class DummyEngine:
    """
    Minimal stub to construct a PlayerState without real audio.
    """
    pass


def make_state_with_tracks(tracks):
    '''
    Helper to create PlayerState for each test
    '''
    return PlayerState(tracks=tracks, audio_engine=DummyEngine())

# Whitebox Statement coverage tests to ensure each print statement and logical branch
# within the UI printing functions is executed at least once.
def test_stmt_now_playing_invalid_state_type(capsys):
    """
    Whitebox Statement coverage
    Target statement - 'print("Invalid player state for now_playing")'

    Explanation:
    We pass a string instead of a PlayerState object.
    This forces defensive type-check `if not isinstance()` to evaluate
    to True and execute the error printing  statement.
    """
    print_now_playing("not-a-state")  # type: ignore[arg-type]
    out = capsys.readouterr().out

    # Verification - The error message statement was executed.
    assert "Invalid player state for now_playing" in out


def test_stmt_now_playing_no_track_selected(capsys):
    """
    White-Box Statement Coverage.
    Target Statement - print("No track selected")`

    Explanation:
    We provide a valid state but with an empty track list (or invalid index).
    This forces the `if state.current_track is None:` check
    to be True, executing the specific line that
    informs the user no track is active.
    """
    state = make_state_with_tracks([])
    print_now_playing(state)
    out = capsys.readouterr().out

    # Verification - The "No track" statement was executed.
    assert "No track selected" in out


def test_stmt_now_playing_playing_status(capsys):
    """
    Technique is White-Box Statement Coverage.
    Target Statement - `print(f"Playing: {track.title}...")`

    Explanation behind test:
    We provide a valid state with a currently playing track.
    This forces the code to bypass the error checks and execute the main
    formatting and printing statements for the song details.
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

    # Verification - The formatted print statements were executed.
    assert "Playing:" in out
    assert "Song – Artist" in out
    assert "[02:00]" in out

def test_stmt_playlist_invalid_state_type(capsys):
    """
    Technique is White-Box Statement Coverage.
    Target Statement -  `print("Invalid player state for playlist")`

    Explanation behind the test:
    Similar to the now_playing test, we pass invalid input to force the
    defensive type-guard statement to execute.
    """
    print_playlist_with_indicator("oops")  # type: ignore[arg-type]
    out = capsys.readouterr().out

    # Verification - The error statement was executed.
    assert "Invalid player state for playlist" in out


def test_stmt_playlist_empty_library(capsys):
    """
    Technique is the White-Box Statement Coverage.
    Target Statement is `print("Library is empty")`

    Explanation -
    We pass a state with 0 tracks. This forces the `if not state.tracks:`
    check to be True, executing the empty library message.
    """
    state = make_state_with_tracks([])
    print_playlist_with_indicator(state)
    out = capsys.readouterr().out

    # Verification - The empty library statement was executed.
    assert "Library is empty" in out
