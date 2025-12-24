import pytest
from types import SimpleNamespace
import music_player.playlists_edit as sut
from music_player.playlist_model import Playlist


# Test: Helper function to create a dummy playlist and track to avoid repeating setup code
def make_state():
    t1 = SimpleNamespace(display_name="T1")
    pl = Playlist("PL", [t1])
    return SimpleNamespace(playlists=[pl], tracks=[t1])


# Test: verifying that adding a track to a playlist handles errors like missing data or empty libraries
def test_branch_add_track_validation(capsys):
    state = make_state()

    # Test: checking the safety guard to ensure the system doesn't crash if the state is missing
    sut.add_track_from_library(None, "PL", "1")

    # Test: checking the system handles the situation where the user forgets to select a playlist
    sut.add_track_from_library(state, "", "1")

    # Test: verifying that an error is shown when trying to add a track from an empty library
    state.tracks = []
    sut.add_track_from_library(state, "PL", "1")
    assert "empty" in capsys.readouterr().out

    # Test: ensuring an error is shown if the user picks a track number that doesn't exist
    state.tracks = [SimpleNamespace(display_name="T1")]
    sut.add_track_from_library(state, "PL", "99")
    assert "out of range" in capsys.readouterr().out


# Test: verifying that removing a track correctly handles invalid inputs like text or wrong numbers
def test_branch_remove_track_validation(capsys):
    state = make_state()

    # Test: checking that the system catches cases where the user types letters instead of a number
    sut.remove_track_from_playlist(state, "PL", "abc")
    assert "Usage" in capsys.readouterr().out

    # Test: verifying that the system catches indices that are too low (below 1)
    sut.remove_track_from_playlist(state, "PL", "0")

    # Test: verifying that the system catches indices that are too high (beyond the playlist length)
    sut.remove_track_from_playlist(state, "PL", "99")
    assert "out of range" in capsys.readouterr().out


# Test: ensuring the system handles redundant move requests where the track stays in the same spot
def test_branch_move_track_redundant(capsys):
    # Test: checking logic for when the starting position and ending position are the same
    state = make_state()
    # Need valid track at index 0
    sut.move_track_within_playlist(state, "PL", "1", "1")
    # Moving a track to its own spot shouldn't do anything
    assert "" == capsys.readouterr().out