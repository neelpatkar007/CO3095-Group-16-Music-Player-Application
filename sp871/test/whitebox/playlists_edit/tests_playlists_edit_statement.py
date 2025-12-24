import pytest
from types import SimpleNamespace
import music_player.playlists_edit as sut
from music_player.playlist_model import Playlist


# Test: Helper function to set up a library with one song and an empty playlist for testing
def make_state():
    # Setup a library with one song and an empty playlist named "PL"
    t1 = SimpleNamespace(display_name="Song1")
    pl = Playlist("PL", [])
    return SimpleNamespace(playlists=[pl], tracks=[t1])


# Test: verifying the basic lifecycle of a playlist by adding, moving, and removing tracks
def test_stmt_add_remove_move(capsys):
    state = make_state()

    # Test: checking that a song from the library can be successfully added to a playlist
    sut.add_track_from_library(state, "PL", "1")
    assert "Added" in capsys.readouterr().out

    # Test: manually adding a second song so there is enough data to test the reordering logic
    t2 = SimpleNamespace(display_name="Song2")
    state.playlists[0].tracks.append(t2)

    # Test: verifying that the system can successfully move a song from one position to another
    sut.move_track_within_playlist(state, "PL", "1", "2")
    assert "Moved" in capsys.readouterr().out

    # Test: checking that a song can be successfully deleted from the playlist
    sut.remove_track_from_playlist(state, "PL", "1")
    assert "Removed" in capsys.readouterr().out