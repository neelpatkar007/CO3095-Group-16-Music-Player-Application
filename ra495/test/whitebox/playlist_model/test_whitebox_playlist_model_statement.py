from types import SimpleNamespace
import pytest
from music_player.playlist_model import Playlist

def make_track(duration=120):
    return SimpleNamespace(duration_seconds=duration)

def test_stmt_playlist_full_lifecycle():
    # Init
    t1 = make_track(60)
    t2 = make_track(120)
    pl = Playlist(name="MyPlaylist", tracks=[t1, t2])

    # Access properties and execute getter statements
    assert pl.name == "MyPlaylist"
    assert pl.num_tracks == 2
    assert pl.total_duration_seconds == 180.0
    assert pl.total_duration_mm_ss == "03:00"

    # Summary line statement
    summary = pl.summary_line(index=1, active=True)
    assert "* 01" in summary
    assert "MyPlaylist" in summary