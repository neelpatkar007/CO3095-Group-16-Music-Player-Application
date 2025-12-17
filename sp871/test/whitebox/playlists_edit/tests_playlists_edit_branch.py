
import pytest
from types import SimpleNamespace
import music_player.playlists_edit as sut
from music_player.playlist_model import Playlist


def make_state():
    # Helper to set up a dummy playlist and track so we don't repeat code
    t1 = SimpleNamespace(display_name="T1")
    pl = Playlist("PL", [t1])
    return SimpleNamespace(playlists=[pl], tracks=[t1])


def test_branch_add_track_validation(capsys):
    state = make_state()

    # Safety check: don't crash if state is missing
    sut.add_track_from_library(None, "PL", "1")

    # What if they forgot to pick a playlist?
    sut.add_track_from_library(state, "", "1")

    # Can't add from an empty library
    state.tracks = []
    sut.add_track_from_library(state, "PL", "1")
    assert "empty" in capsys.readouterr().out

    # Try to add track #99 when we only have 1
    state.tracks = [SimpleNamespace(display_name="T1")]
    sut.add_track_from_library(state, "PL", "99")
    assert "out of range" in capsys.readouterr().out


def test_branch_remove_track_validation(capsys):
    state = make_state()

    # User typed 'abc' instead of a number
    sut.remove_track_from_playlist(state, "PL", "abc")
    assert "Usage" in capsys.readouterr().out

    # Too low (indices start at 1 here)
    sut.remove_track_from_playlist(state, "PL", "0")

    # Too high (out of bounds)
    sut.remove_track_from_playlist(state, "PL", "99")
    assert "out of range" in capsys.readouterr().out


def test_branch_move_track_redundant(capsys):
    """Branch: from_index == to_index."""
    state = make_state()
    # Need valid track at index 0
    sut.move_track_within_playlist(state, "PL", "1", "1")
    # Moving a track to its own spot shouldn't do anything
    assert "" == capsys.readouterr().out