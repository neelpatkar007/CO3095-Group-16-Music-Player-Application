import pytest
from types import SimpleNamespace
import music_player.playlists_basic as sut
from music_player.playlist_model import Playlist


def make_state():
    return SimpleNamespace(
        playlists=[Playlist("A"), Playlist("B")],
        tracks=[],
        library_tracks=[],
        active_playlist_index=None
    )


def test_branch_resolve_playlist(capsys):
    """Empty selector, Int match/fail, Name match/fail."""
    state = make_state()

    assert sut._resolve_playlist(state, "") is None

    assert sut._resolve_playlist(state, "1").name == "A"

    assert sut._resolve_playlist(state, "99") is None

    assert sut._resolve_playlist(state, "b").name == "B"

    assert sut._resolve_playlist(state, "missing") is None


def test_branch_delete_active_logic(capsys):
    """Deleting a playlist before/at/after current active index."""
    state = make_state()
    state.active_playlist_index = 1

    sut.delete_playlist(state, "A")
    assert state.active_playlist_index == 0

    state = make_state()
    state.active_playlist_index = 0

    sut.delete_playlist(state, "A")
    assert state.active_playlist_index == 0


def test_branch_close_playlist_logic(capsys, monkeypatch):
    """No library to return to + Already in library."""
    monkeypatch.setattr(sut, "player_core", SimpleNamespace(stop=lambda s: None))
    state = make_state()

    del state.library_tracks
    sut.close_playlist(state)
    assert "No main library" in capsys.readouterr().out

    state.library_tracks = []
    state.tracks = state.library_tracks
    sut.close_playlist(state)
    assert "Already in" in capsys.readouterr().out