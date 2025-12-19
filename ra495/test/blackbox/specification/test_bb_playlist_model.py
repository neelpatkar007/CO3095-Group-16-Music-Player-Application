import pytest
from types import SimpleNamespace

from music_player.playlist_model import Playlist


def make_track(dur):
    return SimpleNamespace(duration_seconds=dur)


# Test Case 1 <single>: Name Input empty string
def test_playlist_name_empty_string_is_allowed_and_summarises():
    pl = Playlist(name="", tracks=[])
    line = pl.summary_line(index=1, active=False)
    assert "01" in line
    assert "0 tracks" in line
    assert "00:00" in line


# Test Case 2 <error>: Name Input None
def test_playlist_name_none_causes_error_when_formatting_summary():
    pl = Playlist(name=None, tracks=[])
    with pytest.raises(TypeError):
        _ = pl.summary_line(index=1, active=False)


# Test Case 3 <error>: Tracks Initialization None
def test_playlist_tracks_none_causes_error_when_accessing_properties():
    pl = Playlist(name="X", tracks=None)
    with pytest.raises(TypeError):
        _ = pl.num_tracks
    with pytest.raises(TypeError):
        _ = pl.total_duration_seconds


# Test Case 4/5: Valid name, default empty tracks, active True/False
def test_playlist_default_empty_tracks_summary_active_true():
    pl = Playlist(name="MyPlaylist")
    assert pl.num_tracks == 0
    assert pl.total_duration_seconds == 0.0
    assert pl.total_duration_mm_ss == "00:00"

    line = pl.summary_line(index=1, active=True)
    assert line.startswith("*")
    assert "01" in line
    assert "MyPlaylist" in line
    assert "0 tracks" in line
    assert "00:00" in line


def test_playlist_default_empty_tracks_summary_active_false():
    pl = Playlist(name="MyPlaylist")
    line = pl.summary_line(index=1, active=False)
    assert line.startswith(" ")
    assert "01" in line
    assert "MyPlaylist" in line
    assert "0 tracks" in line
    assert "00:00" in line


# Test Case 6/7: Provided populated list, all valid durations, active True/False
def test_playlist_populated_all_valid_durations_active_true():
    tracks = [make_track(60.0), make_track(120.0), make_track(30.0)]
    pl = Playlist(name="ValidDur", tracks=tracks)

    assert pl.num_tracks == 3
    assert pl.total_duration_seconds == pytest.approx(210.0)
    assert pl.total_duration_mm_ss == "03:30"  # 210s

    line = pl.summary_line(index=2, active=True)
    assert line.startswith("*")
    assert "02" in line
    assert "ValidDur" in line
    assert "3 tracks" in line
    assert "03:30" in line


def test_playlist_populated_all_valid_durations_active_false():
    tracks = [make_track(10.0), make_track(10.0)]
    pl = Playlist(name="ValidDur", tracks=tracks)

    assert pl.num_tracks == 2
    assert pl.total_duration_seconds == pytest.approx(20.0)
    assert pl.total_duration_mm_ss == "00:20"

    line = pl.summary_line(index=2, active=False)
    assert line.startswith(" ")
    assert "02" in line
    assert "2 tracks" in line
    assert "00:20" in line


# Test Case 8/9: Mixed valid/None durations, active True/False
def test_playlist_populated_mixed_durations_active_true():
    tracks = [make_track(60.0), make_track(None), make_track(15.0)]
    pl = Playlist(name="MixedDur", tracks=tracks)

    assert pl.num_tracks == 3
    assert pl.total_duration_seconds == pytest.approx(75.0)
    assert pl.total_duration_mm_ss == "01:15"

    line = pl.summary_line(index=3, active=True)
    assert line.startswith("*")
    assert "03" in line
    assert "3 tracks" in line
    assert "01:15" in line


def test_playlist_populated_mixed_durations_active_false():
    tracks = [make_track(None), make_track(5.0)]
    pl = Playlist(name="MixedDur", tracks=tracks)

    assert pl.num_tracks == 2
    assert pl.total_duration_seconds == pytest.approx(5.0)
    assert pl.total_duration_mm_ss == "00:05"

    line = pl.summary_line(index=3, active=False)
    assert line.startswith(" ")
    assert "2 tracks" in line
    assert "00:05" in line


# Test Case 10/11: All durations None, active True/False
def test_playlist_populated_all_none_durations_active_true():
    tracks = [make_track(None), make_track(None)]
    pl = Playlist(name="NoneDur", tracks=tracks)

    assert pl.num_tracks == 2
    assert pl.total_duration_seconds == pytest.approx(0.0)
    assert pl.total_duration_mm_ss == "00:00"

    line = pl.summary_line(index=4, active=True)
    assert line.startswith("*")
    assert "2 tracks" in line
    assert "00:00" in line


def test_playlist_populated_all_none_durations_active_false():
    tracks = [make_track(None)]
    pl = Playlist(name="NoneDur", tracks=tracks)

    assert pl.num_tracks == 1
    assert pl.total_duration_seconds == pytest.approx(0.0)
    assert pl.total_duration_mm_ss == "00:00"

    line = pl.summary_line(index=4, active=False)
    assert line.startswith(" ")
    assert "1 tracks" in line
    assert "00:00" in line
