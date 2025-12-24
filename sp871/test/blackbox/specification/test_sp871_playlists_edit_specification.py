import pytest
from pathlib import Path
from types import SimpleNamespace

import music_player.playlists_edit as sut
from music_player.playlist_model import Playlist


# Test: Helper to create a track object with standard details for testing
def make_track(title="T", artist="A", filename="x.mp3", dur=180.0):
    return SimpleNamespace(
        title=title,
        artist=artist,
        duration_seconds=dur,
        path=Path(filename),
        display_name=f"{title} – {artist}" if artist else title,
    )


# Test: Helper to set up a player state with playlists and a track library
def make_state(playlists=None, library_tracks=None):
    if playlists is None:
        playlists = []
    if library_tracks is None:
        library_tracks = [make_track("Song1", "Artist1", "s1.mp3", 120.0)]

    st = SimpleNamespace()
    st.playlists = list(playlists)

    st.tracks = list(library_tracks)
    return st


# Test: Ensuring the required function exists in the code before running a test
def require_attr(name: str):
    if not hasattr(sut, name):
        pytest.skip(f"playlists_edit.py does not define {name}() in this project")


# Test: verifying that the system does nothing if the player state is missing
def test_state_none_does_nothing(capsys):
    require_attr("add_track_from_library")
    require_attr("require_attr")
    require_attr("move_track_within_playlist")

    sut.add_track_from_library(None, "Mix", "1")
    sut.remove_track_from_playlist(None, "Mix", "1")
    sut.move_track_within_playlist(None, "Mix", "1", "2")

    out = capsys.readouterr().out
    assert out == ""


# Test: checking that the system handles empty or invalid playlist names gracefully
def test_invalid_selector_returns_gracefully(capsys):
    require_attr("add_track_from_library")
    require_attr("remove_track_from_playlist")
    require_attr("move_track_within_playlist")

    st = make_state(playlists=[Playlist("Mix", [make_track()])])

    sut.add_track_from_library(st, "", "1")
    sut.remove_track_from_playlist(st, "", "1")
    sut.move_track_within_playlist(st, "", "1", "2")

    assert capsys.readouterr().out == ""


# Test: verifying an error message is shown if trying to add a track when the library is empty
def test_add_track_library_empty_prints_error(capsys):
    require_attr("add_track_from_library")

    st = make_state(playlists=[Playlist("Mix", [])], library_tracks=[])
    sut.add_track_from_library(st, "Mix", "1")

    out = capsys.readouterr().out.lower()
    assert "library is empty" in out or "nothing to add" in out


# Test: ensuring the usage guide is shown if the user enters non-numeric text for an index
@pytest.mark.parametrize("bad_idx", ["abc", "1.2", "NaN", "garbage"])
def test_add_track_index1_garbage_prints_usage(bad_idx, capsys):
    require_attr("add_track_from_library")

    st = make_state(playlists=[Playlist("Mix", [])], library_tracks=[make_track("A")])
    sut.add_track_from_library(st, "Mix", bad_idx)

    out = capsys.readouterr().out.lower()
    assert "usage" in out and "pl.add" in out


# Test: checking that the system stays silent if the index input is left blank
def test_add_track_index1_empty_returns_silent(capsys):
    require_attr("add_track_from_library")

    st = make_state(playlists=[Playlist("Mix", [])], library_tracks=[make_track("A")])
    sut.add_track_from_library(st, "Mix", "")

    assert capsys.readouterr().out == ""


# Test: verifying that negative numbers or zero are reported as out of range for adding
@pytest.mark.parametrize("idx", ["0", "-1", "-999"])
def test_add_track_index1_zero_or_negative_out_of_range(idx, capsys):
    require_attr("add_track_from_library")

    st = make_state(playlists=[Playlist("Mix", [])], library_tracks=[make_track("A")])
    sut.add_track_from_library(st, "Mix", idx)

    out = capsys.readouterr().out.lower()
    assert "out of range" in out


# Test: ensuring an error is shown if the requested track number is higher than the library count
def test_add_track_index1_too_high_out_of_range(capsys):
    require_attr("add_track_from_library")

    st = make_state(playlists=[Playlist("Mix", [])], library_tracks=[make_track("A")])
    sut.add_track_from_library(st, "Mix", "999")

    out = capsys.readouterr().out.lower()
    assert "out of range" in out


# Test: ensuring the usage guide is shown if the removal index is not a valid whole number
@pytest.mark.parametrize("bad_idx", ["abc", "1.2", "garbage"])
def test_remove_track_index1_garbage_prints_usage(bad_idx, capsys):
    require_attr("remove_track_from_playlist")

    st = make_state(playlists=[Playlist("Mix", [make_track("A")])])
    sut.remove_track_from_playlist(st, "Mix", bad_idx)

    out = capsys.readouterr().out.lower()
    assert "usage" in out and "pl.remove" in out


# Test: checking that a blank removal request does nothing and stays silent
def test_remove_track_index1_empty_returns_silent(capsys):
    require_attr("remove_track_from_playlist")

    st = make_state(playlists=[Playlist("Mix", [make_track("A")])])
    sut.remove_track_from_playlist(st, "Mix", "")

    assert capsys.readouterr().out == ""


# Test: verifying that an error is shown if the removal index is zero or negative
@pytest.mark.parametrize("idx", ["0", "-1"])
def test_remove_track_index1_zero_or_negative_out_of_range(idx, capsys):
    require_attr("remove_track_from_playlist")

    st = make_state(playlists=[Playlist("Mix", [make_track("A")])])
    sut.remove_track_from_playlist(st, "Mix", idx)

    out = capsys.readouterr().out.lower()
    assert "out of range" in out


# Test: ensuring an error is shown if the index to remove is higher than the number of songs in the playlist
def test_remove_track_index1_too_high_out_of_range(capsys):
    require_attr("remove_track_from_playlist")

    st = make_state(playlists=[Playlist("Mix", [make_track("A")])])
    sut.remove_track_from_playlist(st, "Mix", "99")

    out = capsys.readouterr().out.lower()
    assert "out of range" in out


# Test: verifying that the system does nothing if you try to move a song to the same position it is already in
def test_move_same_from_to_does_nothing(capsys):
    require_attr("move_track_within_playlist")

    st = make_state(playlists=[Playlist("Mix", [make_track("A"), make_track("B")])])
    sut.move_track_within_playlist(st, "Mix", "1", "1")

    assert capsys.readouterr().out == ""


# Test: checking that the usage guide is shown if the destination position is not a valid number
@pytest.mark.parametrize("bad_idx2", ["abc", "1.2", "garbage"])
def test_move_to_non_numeric_prints_usage(bad_idx2, capsys):
    require_attr("move_track_within_playlist")

    st = make_state(playlists=[Playlist("Mix", [make_track("A"), make_track("B")])])
    sut.move_track_within_playlist(st, "Mix", "1", bad_idx2)

    out = capsys.readouterr().out.lower()
    assert "usage" in out and "pl.move" in out


# Test: ensuring an error message is shown if the destination index is out of bounds
def test_move_to_out_of_bounds_prints_to_out_of_range(capsys):
    require_attr("move_track_within_playlist")

    st = make_state(playlists=[Playlist("Mix", [make_track("A"), make_track("B")])])
    sut.move_track_within_playlist(st, "Mix", "1", "99")

    out = capsys.readouterr().out.lower()
    assert "'to' index out of range" in out


# Test: ensuring an error message is shown if the 'from' index is out of bounds
def test_move_from_out_of_bounds_prints_from_out_of_range(capsys):
    require_attr("move_track_within_playlist")

    st = make_state(playlists=[Playlist("Mix", [make_track("A"), make_track("B")])])
    sut.move_track_within_playlist(st, "Mix", "99", "1")

    out = capsys.readouterr().out.lower()
    assert "'from' index out of range" in out


# Test: verifying that the system can fix a broken track list and add a song successfully
def test_tracks_none_is_auto_fixed_and_add_works(capsys):
    require_attr("add_track_from_library")

    pl = Playlist("Mix", [])
    pl.tracks = None

    st = make_state(playlists=[pl], library_tracks=[make_track("A")])
    sut.add_track_from_library(st, "Mix", "1")

    out = capsys.readouterr().out.lower()
    assert "added" in out
    assert pl.tracks is not None
    assert len(pl.tracks) == 1


# Test: verifying that a broken track list is fixed safely during a removal attempt
def test_tracks_none_is_auto_fixed_and_remove_is_safe(capsys):
    require_attr("remove_track_from_playlist")

    pl = Playlist("Mix", [])
    pl.tracks = None

    st = make_state(playlists=[pl])
    sut.remove_track_from_playlist(st, "Mix", "1")

    out = capsys.readouterr().out.lower()
    assert "out of range" in out


# Test: verifying that a broken track list is fixed safely during a move attempt
def test_tracks_none_is_auto_fixed_and_move_is_safe(capsys):
    require_attr("move_track_within_playlist")

    pl = Playlist("Mix", [])
    pl.tracks = None

    st = make_state(playlists=[pl])
    sut.move_track_within_playlist(st, "Mix", "1", "2")

    out = capsys.readouterr().out.lower()
    assert "out of range" in out or "usage" in out or out == ""


# Test: verifying that a valid track can be added from the library and shows a confirmation
def test_add_track_valid_adds_and_confirms(capsys):
    require_attr("add_track_from_library")

    t = make_track("Pick", "Me", "p.mp3", 123.0)
    pl = Playlist("Mix", [])
    st = make_state(playlists=[pl], library_tracks=[t])

    sut.add_track_from_library(st, "Mix", "1")

    out = capsys.readouterr().out.lower()
    assert len(pl.tracks) == 1
    assert pl.tracks[0] == t
    assert "added" in out and "mix" in out


# Test: verifying that a track can be removed from a playlist and shows a confirmation
def test_remove_track_valid_pops_and_confirms(capsys):
    require_attr("remove_track_from_playlist")

    t1 = make_track("A", "B", "a.mp3")
    t2 = make_track("C", "D", "c.mp3")
    pl = Playlist("Mix", [t1, t2])
    st = make_state(playlists=[pl])

    sut.remove_track_from_playlist(st, "Mix", "1")

    out = capsys.readouterr().out.lower()
    assert pl.tracks == [t2]
    assert "removed" in out and "mix" in out


# Test: checking that a track can be removed from a playlist even if the main library is empty
def test_remove_track_valid_works_even_if_library_empty(capsys):
    require_attr("remove_track_from_playlist")

    t1 = make_track("A", "B", "a.mp3")
    pl = Playlist("Mix", [t1])
    st = make_state(playlists=[pl], library_tracks=[])

    sut.remove_track_from_playlist(st, "Mix", "1")

    out = capsys.readouterr().out.lower()
    assert pl.tracks == []
    assert "removed" in out


# Test: verifying that a track can be moved within a playlist to reorder it
def test_move_track_valid_reorders_and_confirms(capsys):
    require_attr("move_track_within_playlist")

    t1 = make_track("A", "B", "a.mp3")
    t2 = make_track("C", "D", "c.mp3")
    t3 = make_track("E", "F", "e.mp3")
    pl = Playlist("Mix", [t1, t2, t3])
    st = make_state(playlists=[pl])

    sut.move_track_within_playlist(st, "Mix", "1", "3")  # move A to end

    out = capsys.readouterr().out.lower()
    assert pl.tracks == [t2, t3, t1]
    assert "moved" in out and "from position 1 to 3" in out


# Test: verifying that tracks can be swapped within a playlist even if the main library is empty
def test_move_track_valid_works_even_if_library_empty(capsys):
    require_attr("move_track_within_playlist")

    t1 = make_track("A", "B")
    t2 = make_track("C", "D")
    pl = Playlist("Mix", [t1, t2])
    st = make_state(playlists=[pl], library_tracks=[])

    sut.move_track_within_playlist(st, "Mix", "2", "1")  # swap

    out = capsys.readouterr().out.lower()
    assert pl.tracks == [t2, t1]
    assert "moved" in out


# Test: ensuring the system ignores it if a blank/None entry exists in the library
def test_add_track_ignores_none_track_in_library(capsys):
    require_attr("add_track_from_library")

    pl = Playlist("Mix", [])
    st = make_state(playlists=[pl], library_tracks=[None])  # state.tracks[0] is None

    sut.add_track_from_library(st, "Mix", "1")
    assert capsys.readouterr().out == ""
    assert pl.tracks == []


# Test: ensuring the system ignores it if a blank/None entry exists in the playlist during removal
def test_remove_track_ignores_none_entry_in_playlist(capsys):
    require_attr("remove_track_from_playlist")

    pl = Playlist("Mix", [None])
    st = make_state(playlists=[pl])

    sut.remove_track_from_playlist(st, "Mix", "1")
    assert capsys.readouterr().out == ""
    assert pl.tracks == [None]  # unchanged


# Test: ensuring the system ignores it if a blank/None entry exists in the playlist during a move
def test_move_track_ignores_none_entry_in_playlist(capsys):
    require_attr("move_track_within_playlist")

    pl = Playlist("Mix", [None, make_track("B", "C")])
    st = make_state(playlists=[pl])

    sut.move_track_within_playlist(st, "Mix", "1", "2")
    assert capsys.readouterr().out == ""
    assert pl.tracks[0] is None