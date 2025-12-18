import pytest
from types import SimpleNamespace
from pathlib import Path
import music_player.library_search_scan as sut


def make_state():
    t1 = SimpleNamespace(
        title="Alpha", artist="Beta", duration_seconds=120,
        path=Path("Music/gamma.mp3")
    )
    return SimpleNamespace(tracks=[t1])


def test_branch_search_matches(capsys):
    state = make_state()

    # Branch: Match Title
    sut.search_library(state, "alpha")
    assert "Alpha" in capsys.readouterr().out

    # Branch: Match Artist
    sut.search_library(state, "beta")
    assert "Alpha" in capsys.readouterr().out  # prints track

    # Branch: Match Filename
    sut.search_library(state, "gamma")
    assert "Alpha" in capsys.readouterr().out

    # Branch: No Match
    sut.search_library(state, "omega")
    assert "No matches" in capsys.readouterr().out


def test_branch_rescan_filtering(capsys, monkeypatch):
    """Branches: New file vs Existing file vs Invalid file."""
    state = make_state()
    existing_path = state.tracks[0].path

    # Existing file (should be skipped)
    # Invalid file (zero duration + skipped)
    # New valid file (added)
    def mock_discover_mixed():
        return [
            SimpleNamespace(path=existing_path, duration_seconds=120),
            SimpleNamespace(path=Path("bad.mp3"), duration_seconds=0),
            SimpleNamespace(path=Path("new.mp3"), duration_seconds=60)
        ]

    monkeypatch.setattr(sut, "discover_tracks", mock_discover_mixed)

    sut.rescan_for_new_tracks(state)
    out = capsys.readouterr().out

    # Only 1 added (the valid file)
    assert "Added 1 new track" in out
    assert len(state.tracks) == 2