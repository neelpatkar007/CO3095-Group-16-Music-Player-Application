from pathlib import Path
from types import SimpleNamespace

import pytest

import music_player.library_search_scan as sut

# Test: Creates a fake 'state' object to hold tracks during testing
class DummyState:
    def __init__(self, tracks):
        self.tracks = tracks

# Test: A helper function to quickly generate track objects with default data
def _make_track(title="T", artist="A", filename="x.mp3", dur=180.0):
    return SimpleNamespace(
        title=title,
        artist=artist,
        duration_seconds=dur,
        path=Path(filename),
    )

# Test: Handles printing the track table when no tracks exist
def test_case_0(capsys):
    sut._print_tracks_table([])
    capsys.readouterr()


# Test: Printing the table when it contains one valid track
def test_case_1(capsys):
    t0 = _make_track(title="Song", artist="Artist", filename="a.mp3", dur=120.0)
    sut._print_tracks_table([t0])
    capsys.readouterr()


# Test: How the table handles a track with missing or 'None' values
def test_case_2(capsys):
    t0 = SimpleNamespace(title=None, artist=None, duration_seconds=None, path=None)
    sut._print_tracks_table([t0])
    capsys.readouterr()


# Test: Ensuring the search function doesn't crash if the state is missing
def test_case_3(capsys):
    sut.search_library(None, "abc")
    capsys.readouterr()


# Test: Searching when the state object is empty
def test_case_4(capsys):
    sut.search_library(SimpleNamespace(), "abc")
    capsys.readouterr()


# Test: Searching when the track data is a string instead of a proper list
def test_case_5(capsys):
    st = SimpleNamespace(tracks="not-a-list")
    sut.search_library(st, "abc")
    capsys.readouterr()


# Test: Searching within an empty library list
def test_case_6(capsys):
    st = DummyState([])
    sut.search_library(st, "abc")
    capsys.readouterr()


# Test: Searching with blank input or empty spaces
def test_case_7(capsys):
    st = DummyState([_make_track()])
    sut.search_library(st, "")
    sut.search_library(st, "   ")
    capsys.readouterr()


# Test: Finding a song by searching for a word in the title
def test_case_8(capsys):
    t0 = _make_track(title="Hello World", artist="X", filename="a.mp3", dur=90.0)
    st = DummyState([t0])
    sut.search_library(st, "hello")
    capsys.readouterr()


# Test: Finding a song by searching for the artist's name
def test_case_9(capsys):
    t0 = _make_track(title="S", artist="Kanye West", filename="a.mp3", dur=90.0)
    st = DummyState([t0])
    sut.search_library(st, "west")
    capsys.readouterr()


# Test: Finding a song by searching for its filename
def test_case_10(capsys):
    t0 = _make_track(title="S", artist="A", filename="MySongFile.MP3", dur=90.0)
    st = DummyState([t0])
    sut.search_library(st, "mysongfile")
    capsys.readouterr()


# Test: Checking that no results are found for an incorrect search term
def test_case_11(capsys):
    t0 = _make_track(title="abc", artist="def", filename="x.mp3", dur=1.0)
    st = DummyState([t0])
    sut.search_library(st, "zzzzzz")
    capsys.readouterr()


# Test: Displaying the songs table with a mix of valid and broken track data
def test_case_12(capsys):
    st = DummyState([None, _make_track(), _make_track(title="", artist="", filename="x.mp3", dur=None)])
    sut.view_songs_table(st)
    capsys.readouterr()


# Test: Displaying the artist table when artist names are missing or blank
def test_case_13(capsys):
    st = DummyState([
        _make_track(title="T1", artist="", filename="x.mp3", dur=10.0),
        _make_track(title="T2", artist=None, filename="y.mp3", dur=20.0),  # type: ignore[arg-type]
        _make_track(title="T3", artist="A", filename="z.mp3", dur=30.0),
    ])
    sut.view_artists_table(st)
    capsys.readouterr()


# Test: Displaying the album table grouped by the folder names in the file path
def test_case_14(capsys):
    t0 = _make_track(title="T1", artist="A", filename="Album1/a.mp3", dur=10.0)
    t1 = _make_track(title="T2", artist="A", filename="Album1/b.mp3", dur=20.0)
    t2 = _make_track(title="T3", artist="B", filename="Album2/c.mp3", dur=30.0)
    st = DummyState([t0, t1, t2])
    sut.view_albums_table(st)
    capsys.readouterr()


# Test: Scanning for new files and adding them correctly to the track list
def test_case_15(monkeypatch, capsys):
    st = DummyState([_make_track(filename="existing.mp3")])

    # Simulate finding an existing file, a brand new file, and a broken file
    def fake_discover_tracks():
        return [
            _make_track(filename="existing.mp3", dur=100.0),
            _make_track(filename="new.mp3", dur=100.0),
            _make_track(filename="bad.mp3", dur=0.0),
        ]
    monkeypatch.setattr(sut, "discover_tracks", fake_discover_tracks)
    sut.rescan_for_new_tracks(st)
    out = capsys.readouterr().out
    assert "Scanning for new tracks" in out
    assert any(getattr(t, "path", None) and t.path.name == "new.mp3" for t in st.tracks)


# Test: Showing the correct message when no music files are found on the computer
def test_case_16(monkeypatch, capsys):
    st = DummyState([_make_track(filename="existing.mp3")])

    monkeypatch.setattr(sut, "discover_tracks", lambda: [])
    sut.rescan_for_new_tracks(st)

    out = capsys.readouterr().out
    assert "No tracks found on disk" in out


# Test: Ensuring rescan doesn't crash if the state object is missing data
def test_case_17(capsys):
    sut.rescan_for_new_tracks(SimpleNamespace())
    capsys.readouterr()


# Test: Ensuring rescan handles a corrupted track list safely
def test_case_18(capsys):
    st = SimpleNamespace(tracks="oops")
    sut.rescan_for_new_tracks(st)
    capsys.readouterr()