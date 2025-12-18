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
    """
    Helper to create a fresh PlayerState for each test.
    """
    return PlayerState(tracks=tracks, audio_engine=DummyEngine())

# White box testing technique - branch coverage
# These tests ensure that every logical branch - if/elif/else - within the UI
# printing functions is executed.
def test_branch_now_playing_paused_status(capsys):
    """
    Technique - White-Box Branch Coverage.
    Target Branch - The `elif state.is_paused:` block.

    Explanation:
    The status logic typically follows a chain: `if is_playing` -> `elif is_paused` -> `else`.
    We set `is_playing=False` and `is_paused=True` to force the execution flow
    into the middle 'Paused' branch.
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

    # Verification : The Paused branch was executed.
    assert "Paused:" in out


def test_branch_now_playing_stopped_status(capsys):
    """
    Technique is White-Box Branch Coverage.
    Target Branch is the final `else:` (Stopped) block.

    Explanation -
    We set both `is_playing` and `is_paused` to False.
    This forces the logic
    to fall through all previous checks and execute the final `else` block,
    which corresponds to the 'Stopped' state.
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

    # Verification - >  The Stopped branch was executed.
    assert "Stopped:" in out

def test_branch_playlist_invalid_tracks_structure(capsys):
    """
    Technique : White-Box Branch Coverage.
    Target Branch : The error handling block for example - `except TypeError:` or `if not isinstance...`

    Explanation:
    We intentionally break the internal state by assigning a string to `tracks`
    instead of a list.
    This forces the code to enter the error/exception
    handling branch that deals with corrupted data structures.
    """
    state = make_state_with_tracks([])
    # Break the invariant: tracks is not a list
    state.tracks = "not-a-list"  # type: ignore[assignment]

    print_playlist_with_indicator(state)
    out = capsys.readouterr().out

    # Verifications - The invalid state branch was executed.
    assert "Library is in an invalid state" in out


def test_branch_playlist_single_track_with_warnings(capsys):
    """
    Technique is : White-Box Branch Coverage.
    Target Branches are :
    1. The `if not track.title:` warning branch.
    2. And the `if len(tracks) == 1:` warning branch.

    Explanation:
    We create a track with empty metadata and put it in a single-item list.
    This forces the execution of TWO specific warning branches:
    one for
    missing titles and one for small libraries.

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

    # Verification : Both warning branches were executed
    assert "Some tracks have missing titles" in out
    assert "Only one track in the library" in out

    # Verify that the marker branch logic is still hit
    assert "•" in out or "▶" in out or "‖" in out


def test_branch_playlist_multi_track_clamps_index_and_markers(capsys):
    """
    Technique is  White-Box Branch Coverage.
    Target Branches are :
    1. The index clamping logic (e.g., `if current_index >= len(tracks): current_index = len(tracks)-1`).
    2. The 'Playing' marker branch (Printing the '▶' symbol).

    Explanation:
    We set the index to 10 (out of bounds).
    This forces the clamping logic
    branch to execute and resetting it to 2.
    Then, setting `is_playing=True`
    forces the printer to enter the branch that displays the 'Playing' icon.
    """

    t1 = Track(path=Path("t1.mp3"), title="T1", artist="A", duration_seconds=60)
    t2 = Track(path=Path("t2.mp3"), title="T2", artist="A", duration_seconds=60)
    t3 = Track(path=Path("t3.mp3"), title="T3", artist="A", duration_seconds=60)

    state = make_state_with_tracks([t1, t2, t3])
    state.current_index = 10  # out of range - > should clamp to 2
    state.is_playing = True

    print_playlist_with_indicator(state)
    out = capsys.readouterr().out
    # Verification : The clamped track (T3) is printed as the active one.
    assert "03: T3 – A" in out