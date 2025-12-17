"""
White-box: Branch testing for playlists_advanced.
Goal: Cover deduplication logic, naming constraints, and self-merge checks.
"""
import pytest
from types import SimpleNamespace
import music_player.playlists_advanced as sut
from music_player.playlist_model import Playlist

def make_state():
    t1 = SimpleNamespace(title="T1")
    plA = Playlist("A", [t1])
    plB = Playlist("B", [t1]) # Duplicate track
    return SimpleNamespace(playlists=[plA, plB])

def test_branch_merge_dedupe_logic(capsys):
    state = make_state()

    # Branch - Dedupe True (Default) -> Track in target -> Skip
    sut.merge_playlists(state, "A", "B", dedupe=True)
    # A should still have 1 track (T1), B's T1 was skipped
    assert len(state.playlists[0].tracks) == 1
    assert "with duplicates removed" in capsys.readouterr().out

    # Branch - Dedupe False -> Track in target -> Append
    sut.merge_playlists(state, "A", "B", dedupe=False)
    assert len(state.playlists[0].tracks) == 2
    assert "including duplicates" in capsys.readouterr().out

def test_branch_merge_self_check(capsys):
    state = make_state()
    # Branch - Target is Source
    sut.merge_playlists(state, "A", "A")
    assert "itself" in capsys.readouterr().out

def test_branch_copy_constraints(capsys):
    state = make_state()

    # Branch - Reserved name
    sut.copy_playlist(state, "A", "help")
    assert "reserved" in capsys.readouterr().out

    # Branch - Length < 3
    sut.copy_playlist(state, "A", "xy")
    assert "at least 3" in capsys.readouterr().out

    # Branch - Duplicate Name
    # We must use a name > 2 chars that exists to bypass the length check
    state.playlists.append(Playlist("Existing", []))
    sut.copy_playlist(state, "A", "Existing")
    assert "already exists" in capsys.readouterr().out