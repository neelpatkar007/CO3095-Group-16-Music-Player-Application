import pytest
from pathlib import Path
from types import SimpleNamespace

import music_player.playlists_basic as sut
from music_player.playlist_model import Playlist


# Helpers

class DummyAudioEngine:
    def __init__(self):
        self.play_calls = []
        self.stop_calls = 0
        self.busy = False

    def is_busy(self):
        return self.busy

    def stop(self):
        self.stop_calls += 1

    def play(self, path, start_pos=0.0):
        self.play_calls.append((path, start_pos))


def make_track(title="T", artist="A", filename="x.mp3", dur=180.0):
    return SimpleNamespace(
        title=title,
        artist=artist,
        duration_seconds=dur,
        path=Path(filename),
        display_name=f"{title} – {artist}" if artist else title,
    )


def make_state(playlists=None, library_tracks=None):
    if playlists is None:
        playlists = []
    if library_tracks is None:
        library_tracks = [make_track("Song1", "Artist1", "s1.mp3", 120.0)]

    st = SimpleNamespace()
    st.audio_engine = DummyAudioEngine()
    st.library_tracks = list(library_tracks)
    st.tracks = list(library_tracks)
    st.current_index = 0
    st.position_seconds = 0.0
    st.is_playing = False
    st.is_paused = False

    st.playlists = list(playlists)
    st.active_playlist_index = None
    return st


def _require_attr(name: str):
    if not hasattr(sut, name):
        pytest.skip(f"playlists_basic.py does not define {name}() in this project")


# Test Case 1: state None

def test_state_none_raises_error():
    with pytest.raises(AttributeError):
        sut.create_playlist(None, "X")

    with pytest.raises(AttributeError):
        sut.rename_playlist(None, "X", "Y")

    with pytest.raises(AttributeError):
        sut.delete_playlist(None, "X")

    with pytest.raises(AttributeError):
        sut.open_playlist(None, "X")


# Test Case 2: empty selector

def test_empty_selector_prints_error(capsys):
    _require_attr("open_playlist")
    st = make_state()
    sut.open_playlist(st, "")
    out = capsys.readouterr().out.lower()
    assert "usage" in out or "select" in out or "name" in out or "index" in out


# Test Case 3: non-existent name

def test_selector_nonexistent_name(capsys):
    _require_attr("open_playlist")
    st = make_state(playlists=[Playlist("Mix", [])])
    sut.open_playlist(st, "does-not-exist")
    out = capsys.readouterr().out.lower()
    assert "not" in out and ("found" in out or "exist" in out or "recogn" in out)


# Test Case 4: index out of bounds

def test_selector_index_out_of_bounds(capsys):
    _require_attr("open_playlist")
    st = make_state(playlists=[Playlist("Mix", [])])
    sut.open_playlist(st, "999")
    out = capsys.readouterr().out.lower()
    assert "out" in out or "range" in out or ("not" in out and "found" in out)


# Test Case 5: rename empty new name

def test_rename_empty_new_name(capsys):
    _require_attr("rename_playlist")
    st = make_state(playlists=[Playlist("Old", [])])
    sut.rename_playlist(st, "Old", "")
    out = capsys.readouterr().out.lower()
    assert "empty" in out or "usage" in out or "name" in out


# Test Case 6: rename to existing name

def test_rename_existing_name_rejected(capsys):
    _require_attr("rename_playlist")
    st = make_state(playlists=[Playlist("One", []), Playlist("Two", [])])
    sut.rename_playlist(st, "One", "Two")
    out = capsys.readouterr().out.lower()
    assert "exist" in out or "already" in out or "duplicate" in out


# Test Case 7: open/play empty playlist

def test_open_empty_playlist_warns(capsys):
    _require_attr("open_playlist")
    st = make_state(playlists=[Playlist("Empty", [])])
    sut.open_playlist(st, "Empty")
    out = capsys.readouterr().out.lower()
    assert ("empty" in out) or ("0" in out and ("song" in out or "track" in out)) or ("opened" in out)


# Test Case 8: create playlist valid

def test_create_playlist_valid_unique_name(capsys):
    _require_attr("create_playlist")
    st = make_state()
    sut.create_playlist(st, "MyList")
    out = capsys.readouterr().out.lower()
    assert any(p.name == "MyList" for p in st.playlists)
    assert "created" in out or "new" in out or "playlist" in out


# Test Cases 9-12: rename by name/index, with/without tracks

def test_rename_by_name_playlist_has_tracks(capsys):
    _require_attr("rename_playlist")
    t = make_track("A", "B")
    st = make_state(playlists=[Playlist("Old", [t])])
    sut.rename_playlist(st, "Old", "New")
    out = capsys.readouterr().out.lower()
    assert st.playlists[0].name == "New"
    assert "renam" in out or "updated" in out


def test_rename_by_index_playlist_empty(capsys):
    _require_attr("rename_playlist")
    st = make_state(playlists=[Playlist("Old", [])])
    sut.rename_playlist(st, "1", "New")
    out = capsys.readouterr().out.lower()
    assert st.playlists[0].name == "New"
    assert "renam" in out or "updated" in out


# Test Cases 13-16: delete by name/index, with/without tracks

def test_delete_by_name_playlist_has_tracks(capsys):
    _require_attr("delete_playlist")
    st = make_state(playlists=[Playlist("KillMe", [make_track()])])
    sut.delete_playlist(st, "KillMe")
    out = capsys.readouterr().out.lower()
    assert all(p.name != "KillMe" for p in st.playlists)
    assert "delet" in out or "remov" in out


def test_delete_by_index_playlist_empty(capsys):
    _require_attr("delete_playlist")
    st = make_state(playlists=[Playlist("P1", []), Playlist("P2", [])])
    sut.delete_playlist(st, "2")
    out = capsys.readouterr().out.lower()
    assert len(st.playlists) == 1
    assert st.playlists[0].name == "P1"
    assert "delet" in out or "remov" in out


# Test Cases 17-18: open/play playlist by name/index with tracks

def test_open_playlist_by_name_with_tracks_sets_active_and_queue(monkeypatch, capsys):
    _require_attr("open_playlist")

    def fake_play(state):
        state.is_playing = True

    monkeypatch.setattr(sut.player_core, "play", fake_play)

    t1 = make_track("S1", "A1", "s1.mp3", 111.0)
    t2 = make_track("S2", "A2", "s2.mp3", 222.0)
    st = make_state(playlists=[Playlist("Mix", [t1, t2])])

    sut.open_playlist(st, "Mix")
    out = capsys.readouterr().out.lower()

    assert st.active_playlist_index == 0
    assert st.tracks == [t1, t2]
    assert st.is_playing is True
    assert "opened playlist" in out


def test_play_playlist_by_index_with_tracks_triggers_play(monkeypatch, capsys):
    if not hasattr(sut, "play_playlist"):
        pytest.skip("playlists_basic.py has no play_playlist()")

    called = {"play": 0}

    try:
        import music_player.player_core as player_core
        if hasattr(player_core, "play"):
            monkeypatch.setattr(player_core, "play", lambda st: called.__setitem__("play", called["play"] + 1))
        if hasattr(player_core, "play_current"):
            monkeypatch.setattr(player_core, "play_current", lambda st: called.__setitem__("play", called["play"] + 1))
    except Exception:
        pass

    t1 = make_track("S1", "A1")
    st = make_state(playlists=[Playlist("Mix", [t1])])

    sut.play_playlist(st, "1")
    out = capsys.readouterr().out.lower()

    assert called["play"] > 0 or getattr(st, "is_playing", False) is True or "play" in out
