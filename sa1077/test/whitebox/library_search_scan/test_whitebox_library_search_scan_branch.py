import pytest
from types import SimpleNamespace
from pathlib import Path
import music_player.library_search_scan as sut


# Test: Helper function to create a basic library state with one song for branching tests
def make_state():
    t1 = SimpleNamespace(
        title="Alpha", artist="Beta", duration_seconds=120,
        path=Path("Music/gamma.mp3")
    )
    return SimpleNamespace(tracks=[t1])


# Test: verifying that the search function can find a song by its title, artist, or filename
def test_branch_search_matches(capsys):
    state = make_state()

    # Branch: Testing if the system finds a match using the song title
    sut.search_library(state, "alpha")
    assert "Alpha" in capsys.readouterr().out

    # Branch: Testing if the system finds a match using the artist name
    sut.search_library(state, "beta")
    assert "Alpha" in capsys.readouterr().out  # prints track

    # Branch: Testing if the system finds a match using the actual filename
    sut.search_library(state, "gamma")
    assert "Alpha" in capsys.readouterr().out

    # Branch: Testing that the system correctly reports when no match is found
    sut.search_library(state, "omega")
    assert "No matches" in capsys.readouterr().out


# Test: ensuring the rescan logic correctly filters out duplicates and broken files
def test_branch_rescan_filtering(capsys, monkeypatch):
    """Branches: New file vs Existing file vs Invalid file."""
    state = make_state()
    existing_path = state.tracks[0].path

    # We simulate a folder containing:
    # 1. A file already in the library (should be ignored)
    # 2. A broken file with 0 duration (should be ignored)
    # 3. A brand new valid song (should be added)
    def mock_discover_mixed():
        return [
            SimpleNamespace(path=existing_path, duration_seconds=120),
            SimpleNamespace(path=Path("bad.mp3"), duration_seconds=0),
            SimpleNamespace(path=Path("new.mp3"), duration_seconds=60)
        ]

    monkeypatch.setattr(sut, "discover_tracks", mock_discover_mixed)

    sut.rescan_for_new_tracks(state)
    out = capsys.readouterr().out

    # The system should only add the 1 valid new file
    assert "Added 1 new track" in out
    assert len(state.tracks) == 2