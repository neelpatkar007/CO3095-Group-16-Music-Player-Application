
import pytest
from types import SimpleNamespace
import music_player.playlists_edit as sut
from music_player.playlist_model import Playlist


def make_state():
    # Setup a library with one song and an empty playlist named "PL"
    t1 = SimpleNamespace(display_name="Song1")
    pl = Playlist("PL", [])
    return SimpleNamespace(playlists=[pl], tracks=[t1])


def test_stmt_add_remove_move(capsys):
    state = make_state()

    # 1. Add: Put the first song from library into the playlist
    sut.add_track_from_library(state, "PL", "1")
    assert "Added" in capsys.readouterr().out

    # 2. Move: Need to add a second track manually so we have something to swap with
    t2 = SimpleNamespace(display_name="Song2")
    state.playlists[0].tracks.append(t2)

    # Move the track at index 1 to index 2
    sut.move_track_within_playlist(state, "PL", "1", "2")
    assert "Moved" in capsys.readouterr().out

    # 3. Remove: Delete the first track from the playlist
    sut.remove_track_from_playlist(state, "PL", "1")
    assert "Removed" in capsys.readouterr().out