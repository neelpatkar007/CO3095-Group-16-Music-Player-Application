import types

from music_player.player_state import PlayerState


class DummyEngine:
    """Minimal stub so PlayerState can be constructed."""
    pass


def make_state(tracks):
    return PlayerState(tracks=tracks, audio_engine=DummyEngine())


def test_current_track_empty_library():
    state = make_state([])
    assert state.current_track is None


def test_current_track_valid_index():
    track = types.SimpleNamespace(title="Track 1")
    state = make_state([track])
    state.current_index = 0
    assert state.current_track is track


def test_current_track_index_out_of_range():
    track = types.SimpleNamespace(title="Track 1")
    state = make_state([track])
    state.current_index = 5
    assert state.current_track is None
