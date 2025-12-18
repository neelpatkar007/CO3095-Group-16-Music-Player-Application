import pytest
from types import SimpleNamespace
import music_player.playlists_basic as sut
from music_player.playlist_model import Playlist


# Mock player_core
class DummyCore:
    def play(self, state): pass

    def stop(self, state): pass


@pytest.fixture
def mock_deps(monkeypatch):
    monkeypatch.setattr(sut, "player_core", DummyCore())


def make_state():
    pl = Playlist("Existing")
    pl.tracks = [SimpleNamespace(display_name="Song", duration_seconds=60)]
    return SimpleNamespace(
        playlists=[pl],
        tracks=[],
        library_tracks=[],
        active_playlist_index=None,
        current_index=0,
        position_seconds=0.0
    )


def test_stmt_lifecycle_create_rename_delete(capsys, mock_deps):
    """Execute statements for CRUD operations."""
    state = make_state()

    # Create
    sut.create_playlist(state, "NewPL")
    assert "Created" in capsys.readouterr().out

    # Rename
    sut.rename_playlist(state, "NewPL", "RenamedPL")
    assert "Renamed" in capsys.readouterr().out

    # Delete
    sut.delete_playlist(state, "RenamedPL")
    assert "Deleted" in capsys.readouterr().out


def test_stmt_listing_and_activation(capsys, mock_deps):
    """Execute statements for listing, opening, and closing."""
    state = make_state()

    # List
    sut.list_playlists(state)
    assert "Existing" in capsys.readouterr().out

    # Open (activates queue)
    sut.open_playlist(state, "Existing")
    assert "Opened" in capsys.readouterr().out

    # Show Current
    sut.show_current_playlist(state)
    assert "Current playlist" in capsys.readouterr().out

    # Close
    sut.close_playlist(state)
    assert "Closed" in capsys.readouterr().out