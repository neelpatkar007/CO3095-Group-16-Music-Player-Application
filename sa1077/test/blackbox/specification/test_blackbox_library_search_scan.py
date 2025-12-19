from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

import music_player.library_search_scan as sut


# Helpers
class DummyState:
    def __init__(self, tracks):
        self.tracks = tracks


def make_track(
    title="Song",
    artist="Artist",
    filename="song.mp3",
    dur=180.0,
    parent_name="AlbumA",
):
    p = Path(parent_name) / filename
    return SimpleNamespace(title=title, artist=artist, duration_seconds=dur, path=p)


# _print_tracks_table (S2-04)
def test_print_tracks_table_empty_prints_no_tracks(capsys):
    sut._print_tracks_table([])
    out = capsys.readouterr().out
    assert "(no tracks)" in out


def test_print_tracks_table_all_none_prints_no_tracks(capsys):
    sut._print_tracks_table([None, None])
    out = capsys.readouterr().out
    assert "(no tracks)" in out


def test_print_tracks_table_prints_header_and_rows(capsys):
    t1 = make_track(title="T", artist="A", dur=60.0)
    t2 = make_track(title="LongTitle" * 10, artist="LongArtist" * 10, dur=None)
    sut._print_tracks_table([t1, None, t2])

    out = capsys.readouterr().out
    assert "No" in out and "Title" in out and "Artist" in out and "Time" in out
    assert "T" in out
    assert "A" in out
    assert "??:??" in out


# search_library (S2-03)
def test_search_library_state_none_prints_error(capsys):
    sut.search_library(None, "x")  # type: ignore[arg-type]
    out = capsys.readouterr().out
    assert "Library state is not available" in out


def test_search_library_tracks_not_list_prints_corrupted(capsys):
    st = DummyState(tracks="not-a-list")  # type: ignore[assignment]
    sut.search_library(st, "x")
    out = capsys.readouterr().out
    assert "tracks data is corrupted" in out


def test_search_library_empty_library_prints_empty(capsys):
    st = DummyState([])
    sut.search_library(st, "x")
    out = capsys.readouterr().out
    assert "Library is empty" in out


def test_search_library_blank_query_prints_usage(capsys):
    st = DummyState([make_track()])
    sut.search_library(st, "   ")
    out = capsys.readouterr().out
    assert "Usage: /search" in out


def test_search_library_matches_title_artist_and_filename(capsys):
    t1 = make_track(title="Hello World", artist="Someone", filename="x.mp3")
    t2 = make_track(title="Other", artist="Kanye West", filename="kanye_file.mp3")
    t3 = make_track(title="Nope", artist="Nope", filename="special_name.mp3")
    st = DummyState([t1, t2, t3])

    sut.search_library(st, "hello")
    out = capsys.readouterr().out.lower()
    assert "search results for 'hello'" in out
    assert "hello world" in out

    sut.search_library(st, "kanye")
    out = capsys.readouterr().out.lower()
    assert "kanye west" in out

    sut.search_library(st, "special_name")
    out = capsys.readouterr().out.lower()
    assert "nope" in out


def test_search_library_no_matches_prints_message(capsys):
    st = DummyState([make_track(title="A", artist="B", filename="c.mp3")])
    sut.search_library(st, "zzz")
    out = capsys.readouterr().out
    assert "No matches found" in out
    assert "Search results for" in out
    assert "(no tracks)" in out


# view_songs_table (S2-04)
def test_view_songs_table_prints_header_and_table(capsys):
    st = DummyState([None, make_track(title="T1"), make_track(title="T2")])
    sut.view_songs_table(st)
    out = capsys.readouterr().out
    assert "[lib] Songs (library):" in out
    assert "T1" in out and "T2" in out


# view_artists_table (S2-04)
def test_view_artists_table_invalid_state_prints_error(capsys):
    sut.view_artists_table(None)
    out = capsys.readouterr().out
    assert "Library state is not available" in out


def test_view_artists_table_tracks_not_list_prints_corrupted(capsys):
    st = DummyState(tracks=123)
    sut.view_artists_table(st)
    out = capsys.readouterr().out
    assert "tracks data is corrupted" in out


def test_view_artists_table_empty_library_prints_empty(capsys):
    st = DummyState([])
    sut.view_artists_table(st)
    out = capsys.readouterr().out
    assert "Library is empty" in out


def test_view_artists_table_no_artist_info_prints_message(capsys):
    st = DummyState([make_track(artist=""), make_track(artist=None)])
    sut.view_artists_table(st)
    out = capsys.readouterr().out
    assert "No artist information available" in out


def test_view_artists_table_aggregates_counts_and_time(capsys):
    st = DummyState(
        [
            make_track(artist="A", dur=60.0),
            make_track(artist="A", dur=40.0),
            make_track(artist="B", dur=30.0),
            None,
        ]
    )
    sut.view_artists_table(st)
    out = capsys.readouterr().out
    assert "Artist" in out and "Tracks" in out and "Time" in out
    assert "A" in out
    assert "2" in out
    assert "01:40" in out
    assert "B" in out
    assert "00:30" in out


# view_albums_table (S2-04)
def test_view_albums_table_groups_by_parent_folder(capsys):
    st = DummyState(
        [
            make_track(parent_name="Album1", filename="a.mp3", dur=60.0),
            make_track(parent_name="Album1", filename="b.mp3", dur=30.0),
            make_track(parent_name="Album2", filename="c.mp3", dur=10.0),
        ]
    )
    sut.view_albums_table(st)
    out = capsys.readouterr().out
    assert "Album (folder)" in out
    assert "Album1" in out
    assert "Album2" in out
    assert "01:30" in out


# rescan_for_new_tracks (S2-09)
def test_rescan_invalid_state_prints_error(capsys):
    sut.rescan_for_new_tracks(None)
    out = capsys.readouterr().out
    assert "Library state is not available" in out


def test_rescan_tracks_not_list_prints_corrupted(capsys):
    st = DummyState(tracks="oops")
    sut.rescan_for_new_tracks(st)
    out = capsys.readouterr().out
    assert "tracks data is corrupted" in out


def test_rescan_no_tracks_found_on_disk(monkeypatch, capsys):
    st = DummyState([make_track(filename="existing.mp3")])

    monkeypatch.setattr(sut, "discover_tracks", lambda: [])
    sut.rescan_for_new_tracks(st)

    out = capsys.readouterr().out
    assert "Scanning for new tracks" in out
    assert "No tracks found on disk" in out


def test_rescan_filters_duplicates_and_invalid_duration(monkeypatch, capsys):
    existing = make_track(filename="a.mp3", dur=60.0)
    st = DummyState([existing])

    dup = make_track(filename="a.mp3", dur=50.0)
    bad = make_track(filename="bad.mp3", dur=0.0)
    new = make_track(filename="new.mp3", dur=10.0)

    monkeypatch.setattr(sut, "discover_tracks", lambda: [dup, bad, new])

    sut.rescan_for_new_tracks(st)
    out = capsys.readouterr().out

    assert "Added 1 new track(s)" in out
    assert any(getattr(t, "path", None) == new.path for t in st.tracks)


def test_rescan_bulk_message_over_50(monkeypatch, capsys):
    st = DummyState([make_track(filename="existing.mp3")])

    new_tracks = [make_track(filename=f"n{i}.mp3", dur=10.0) for i in range(60)]
    monkeypatch.setattr(sut, "discover_tracks", lambda: new_tracks)

    sut.rescan_for_new_tracks(st)
    out = capsys.readouterr().out
    assert "Bulk imported 60 new tracks" in out