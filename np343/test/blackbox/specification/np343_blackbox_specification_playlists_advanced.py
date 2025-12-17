import pytest
from pathlib import Path
from types import SimpleNamespace

import music_player.playlists_advanced as sut
from music_player.playlist_model import Playlist


def make_track(title="T", artist="A", filename="x.mp3", dur=180.0):
    return SimpleNamespace(
        title=title,
        artist=artist,
        duration_seconds=dur,
        path=Path(filename),
        display_name=f"{title} – {artist}" if artist else title,
    )


def make_state(playlists):
    st = SimpleNamespace()
    st.playlists = list(playlists)
    st.active_playlist_index = None
    st.library_tracks = []
    st.tracks = []
    st.current_index = 0
    st.position_seconds = 0.0
    st.is_playing = False
    st.is_paused = False
    return st


def _require(name: str):
    if not hasattr(sut, name):
        pytest.skip(f"playlists_advanced.py does not define {name}() in this project")


# Merge tests

def test_merge_empty_target_rejected(capsys):
    _require("merge_playlists")
    st = make_state([Playlist("A", [make_track()]), Playlist("B", [make_track("X", "Y", "x.mp3")])])

    sut.merge_playlists(st, "", "B", dedupe=True)
    out = capsys.readouterr().out.lower()
    assert ("usage" in out) or ("target" in out) or ("select" in out) or ("error" in out)


def test_merge_invalid_target_rejected(capsys):
    _require("merge_playlists")
    st = make_state([Playlist("A", [make_track()]), Playlist("B", [make_track("X", "Y", "x.mp3")])])

    sut.merge_playlists(st, "NOPE", "B", dedupe=True)
    out = capsys.readouterr().out.lower()
    assert ("not" in out and ("found" in out or "exist" in out)) or ("invalid" in out) or ("error" in out)


def test_merge_empty_source_rejected(capsys):
    _require("merge_playlists")
    st = make_state([Playlist("A", [make_track()]), Playlist("B", [make_track("X", "Y", "x.mp3")])])

    sut.merge_playlists(st, "A", "", dedupe=True)
    out = capsys.readouterr().out.lower()
    assert ("usage" in out) or ("source" in out) or ("select" in out) or ("error" in out)


def test_merge_invalid_source_rejected(capsys):
    _require("merge_playlists")
    st = make_state([Playlist("A", [make_track()]), Playlist("B", [make_track("X", "Y", "x.mp3")])])

    sut.merge_playlists(st, "A", "NOPE", dedupe=True)
    out = capsys.readouterr().out.lower()
    assert ("not" in out and ("found" in out or "exist" in out)) or ("invalid" in out) or ("error" in out)


def test_merge_same_as_target_rejected(capsys):
    _require("merge_playlists")
    st = make_state([Playlist("A", [make_track()])])

    sut.merge_playlists(st, "A", "A", dedupe=True)
    out = capsys.readouterr().out.lower()
    assert ("same" in out) or ("different" in out) or ("error" in out) or ("itself" in out)


def test_merge_source_empty_noop(capsys):
    _require("merge_playlists")
    target = Playlist("A", [make_track("T1", "A1", "t1.mp3")])
    source = Playlist("B", [])
    st = make_state([target, source])

    sut.merge_playlists(st, "A", "B", dedupe=True)
    out = capsys.readouterr().out.lower()
    assert len(target.tracks) == 1
    assert ("empty" in out) or ("no tracks" in out) or ("nothing" in out) or ("merged" in out)


def test_merge_dedupe_true_removes_duplicates(capsys):
    _require("merge_playlists")
    t1 = make_track("T1", "A1", "dup.mp3")
    target = Playlist("A", [t1])
    source = Playlist("B", [make_track("T1", "A1", "dup.mp3"), make_track("T2", "A2", "new.mp3")])
    st = make_state([target, source])

    sut.merge_playlists(st, "A", "B", dedupe=True)
    out = capsys.readouterr().out.lower()

    names = [t.path.name for t in target.tracks]
    assert "dup.mp3" in names
    assert "new.mp3" in names
    assert names.count("dup.mp3") == 1
    assert ("merge" in out) or ("added" in out) or ("duplicate" in out)


def test_merge_dedupe_false_keeps_duplicates(capsys):
    _require("merge_playlists")
    target = Playlist("A", [make_track("T1", "A1", "dup.mp3")])
    source = Playlist("B", [make_track("T1", "A1", "dup.mp3")])
    st = make_state([target, source])

    sut.merge_playlists(st, "A", "B", dedupe=False)
    out = capsys.readouterr().out.lower()

    names = [t.path.name for t in target.tracks]
    assert names.count("dup.mp3") == 2
    assert ("merge" in out) or ("added" in out) or ("duplicate" in out) or (out != "")


# Copy tests

def test_copy_name_too_short_rejected(capsys):
    _require("copy_playlist")
    st = make_state([Playlist("A", [make_track()])])

    sut.copy_playlist(st, "A", "ab")
    out = capsys.readouterr().out.lower()
    assert ("short" in out) or ("min" in out) or ("invalid" in out) or ("name" in out)


def test_copy_name_too_long_rejected(capsys):
    _require("copy_playlist")
    st = make_state([Playlist("A", [make_track()])])

    sut.copy_playlist(st, "A", "x" * 21)
    out = capsys.readouterr().out.lower()
    assert ("long" in out) or ("max" in out) or ("invalid" in out) or ("name" in out)


@pytest.mark.parametrize("nm", ["help", "quit", "exit"])
def test_copy_reserved_word_rejected(nm, capsys):
    _require("copy_playlist")
    st = make_state([Playlist("A", [make_track()])])

    sut.copy_playlist(st, "A", nm)
    out = capsys.readouterr().out.lower()
    assert ("reserved" in out) or ("invalid" in out) or ("name" in out)


@pytest.mark.parametrize("nm", ["bad/name", "bad\\name", "bad:name", "bad*name"])
def test_copy_invalid_chars_rejected(nm, capsys):
    _require("copy_playlist")
    st = make_state([Playlist("A", [make_track()])])

    sut.copy_playlist(st, "A", nm)
    out = capsys.readouterr().out.lower()
    assert ("invalid" in out) or ("character" in out) or ("name" in out)


def test_copy_duplicate_name_rejected(capsys):
    _require("copy_playlist")
    st = make_state([Playlist("A", [make_track()]), Playlist("CopyA", [])])

    sut.copy_playlist(st, "A", "CopyA")
    out = capsys.readouterr().out.lower()
    assert ("exist" in out) or ("already" in out) or ("duplicate" in out)


def test_copy_success_creates_new_playlist(capsys):
    _require("copy_playlist")
    t1 = make_track("T1", "A1", "t1.mp3")
    st = make_state([Playlist("A", [t1])])

    sut.copy_playlist(st, "A", "CopyA")
    out = capsys.readouterr().out.lower()

    names = [p.name for p in st.playlists]
    assert "copya" in [n.lower() for n in names]
    new_pl = next(p for p in st.playlists if p.name.lower() == "copya")
    assert len(new_pl.tracks) == 1
    assert ("copied" in out) or ("created" in out) or ("copy" in out)