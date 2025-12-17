"""
White-box: Statement testing for playlists_advanced.
Goal is to execute merge and copy logic.
"""
import pytest
from types import SimpleNamespace
import music_player.playlists_advanced as sut
from music_player.playlist_model import Playlist

def make_state():
    t1 = SimpleNamespace(title="Song1")
    pl1 = Playlist("A", [t1])
    pl2 = Playlist("B", [])
    return SimpleNamespace(playlists=[pl1, pl2])

def test_stmt_merge_and_copy(capsys):
    state = make_state()

    # Merge A into B
    sut.merge_playlists(state, "B", "A")
    assert "Merged" in capsys.readouterr().out

    # Copy A to CopyOfA (Name must be > 2 chars to pass validation)
    sut.copy_playlist(state, "A", "CopyOfA")
    assert "Copied" in capsys.readouterr().out