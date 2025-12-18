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


