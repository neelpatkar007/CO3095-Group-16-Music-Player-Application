import pytest
from types import SimpleNamespace
from pathlib import Path
import music_player.library_search_scan as sut


# Mock discover_tracks
def mock_discover():
    return [SimpleNamespace(path=Path("new.mp3"), duration_seconds=60)]


@pytest.fixture
def mock_scanner(monkeypatch):
    monkeypatch.setattr(sut, "discover_tracks", mock_discover)


def make_state():
    t1 = SimpleNamespace(
        title="Song", artist="Art", duration_seconds=120,
        path=Path("f.mp3")
    )
    return SimpleNamespace(tracks=[t1])


def test_stmt_search_view_rescan(capsys, mock_scanner):
    state = make_state()

    # Search
    sut.search_library(state, "Song")
    assert "Search results" in capsys.readouterr().out

    # Views
    sut.view_songs_table(state)
    sut.view_artists_table(state)
    sut.view_albums_table(state)

    # Rescan
    sut.rescan_for_new_tracks(state)
    assert "Added" in capsys.readouterr().out
test_white