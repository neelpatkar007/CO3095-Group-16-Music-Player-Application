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


