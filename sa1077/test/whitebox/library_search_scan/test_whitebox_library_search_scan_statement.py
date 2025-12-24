import pytest
from types import SimpleNamespace
from pathlib import Path
import music_player.library_search_scan as sut


# Test: A mock function to simulate finding a new music file during a scan
def mock_discover():
    return [SimpleNamespace(path=Path("new.mp3"), duration_seconds=60)]


# Test: A fixture to automatically replace the real scanning function with our mock version
@pytest.fixture
def mock_scanner(monkeypatch):
    monkeypatch.setattr(sut, "discover_tracks", mock_discover)


# Test: Helper function to create a basic library state with one existing song
def make_state():
    t1 = SimpleNamespace(
        title="Song", artist="Art", duration_seconds=120,
        path=Path("f.mp3")
    )
    return SimpleNamespace(tracks=[t1])


# Test: verifying that searching, viewing tables, and rescanning all work together in one sequence
def test_stmt_search_view_rescan(capsys, mock_scanner):
    state = make_state()

    # Test: checking that the search function correctly finds and displays results for a song
    sut.search_library(state, "Song")
    assert "Search results" in capsys.readouterr().out

    # Test: checking that the system can display the songs, artists, and albums tables without errors
    sut.view_songs_table(state)
    sut.view_artists_table(state)
    sut.view_albums_table(state)

    # Test: verifying that the rescan function successfully detects and adds the new mock track
    sut.rescan_for_new_tracks(state)
    assert "Added" in capsys.readouterr().out