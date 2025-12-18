from pathlib import Path
from types import SimpleNamespace

import pytest

import music_player.library_search_scan as sut


class DummyState:
    def __init__(self, tracks):
        self.tracks = tracks


def _make_track(title="T", artist="A", filename="x.mp3", dur=180.0):
    return SimpleNamespace(
        title=title,
        artist=artist,
        duration_seconds=dur,
        path=Path(filename),
    )

def test_case_0(capsys):
    sut._print_tracks_table([])
    capsys.readouterr()


def test_case_1(capsys):
    t0 = _make_track(title="Song", artist="Artist", filename="a.mp3", dur=120.0)
    sut._print_tracks_table([t0])
    capsys.readouterr()


def test_case_2(capsys):
    t0 = SimpleNamespace(title=None, artist=None, duration_seconds=None, path=None)
    sut._print_tracks_table([t0])
    capsys.readouterr()


def test_case_3(capsys):
    sut.search_library(None, "abc")
    capsys.readouterr()


def test_case_4(capsys):
    sut.search_library(SimpleNamespace(), "abc")
    capsys.readouterr()


def test_case_5(capsys):
    st = SimpleNamespace(tracks="not-a-list")
    sut.search_library(st, "abc")
    capsys.readouterr()


def test_case_6(capsys):
    st = DummyState([])
    sut.search_library(st, "abc")
    capsys.readouterr()


def test_case_7(capsys):
    st = DummyState([_make_track()])
    sut.search_library(st, "")
    sut.search_library(st, "   ")
    capsys.readouterr()


def test_case_8(capsys):
    t0 = _make_track(title="Hello World", artist="X", filename="a.mp3", dur=90.0)
    st = DummyState([t0])
    sut.search_library(st, "hello")
    capsys.readouterr()


def test_case_9(capsys):
    t0 = _make_track(title="S", artist="Kanye West", filename="a.mp3", dur=90.0)
    st = DummyState([t0])
    sut.search_library(st, "west")
    capsys.readouterr()


def test_case_10(capsys):
    t0 = _make_track(title="S", artist="A", filename="MySongFile.MP3", dur=90.0)
    st = DummyState([t0])
    sut.search_library(st, "mysongfile")
    capsys.readouterr()


def test_case_11(capsys):
    t0 = _make_track(title="abc", artist="def", filename="x.mp3", dur=1.0)
    st = DummyState([t0])
    sut.search_library(st, "zzzzzz")
    capsys.readouterr()


def test_case_12(capsys):
    st = DummyState([None, _make_track(), _make_track(title="", artist="", filename="x.mp3", dur=None)])
    sut.view_songs_table(st)
    capsys.readouterr()


def test_case_13(capsys):
    st = DummyState([
        _make_track(title="T1", artist="", filename="x.mp3", dur=10.0),
        _make_track(title="T2", artist=None, filename="y.mp3", dur=20.0),  # type: ignore[arg-type]
        _make_track(title="T3", artist="A", filename="z.mp3", dur=30.0),
    ])
    sut.view_artists_table(st)
    capsys.readouterr()
