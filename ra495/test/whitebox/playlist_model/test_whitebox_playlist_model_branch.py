from types import SimpleNamespace
import pytest
from music_player.playlist_model import Playlist

def test_branch_duration_none_vs_valid():
    """Branch: if t.duration_seconds is not None."""
    # Branch True (Valid)
    t1 = SimpleNamespace(duration_seconds=60)
    pl1 = Playlist("A", [t1])
    assert pl1.total_duration_seconds == 60.0

    # Branch False (None)
    t2 = SimpleNamespace(duration_seconds=None)
    pl2 = Playlist("B", [t2])
    assert pl2.total_duration_seconds == 0.0

def test_branch_formatting_empty_vs_populated():
    """Branch: if not self.tracks (for mm_ss)."""
    # Branch True (Empty)
    pl_empty = Playlist("Empty", [])
    assert pl_empty.total_duration_mm_ss == "00:00"

    # Branch False (Populated)
    t1 = SimpleNamespace(duration_seconds=65)
    pl_full = Playlist("Full", [t1])
    assert pl_full.total_duration_mm_ss == "01:05"

def test_branch_summary_index_and_active():
    """Branches: index is None/Int, active is True/False."""
    pl = Playlist("Test", [])

    # Index None, Active False
    s1 = pl.summary_line(index=None, active=False)
    assert "--" in s1
    assert " " == s1[0]  # No asterisk

    # Index Int, Active True
    s2 = pl.summary_line(index=5, active=True)
    assert "05" in s2
    assert "*" == s2[0]