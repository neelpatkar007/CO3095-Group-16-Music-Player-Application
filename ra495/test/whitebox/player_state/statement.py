import types

from music_player.player_state import PlayerState


class DummyEngine:
    """Minimal stub so PlayerState can be constructed."""
    pass


def make_state(tracks):
    return PlayerState(tracks=tracks, audio_engine=DummyEngine())


# --- Statement testing for current_track ---


def test_current_track_statement_empty_library():
    """
    Statement test:
    - Execute the function when the library is empty.
    - Ensures the 'if' is evaluated and the 'return None' line is executed.
    """
    state = make_state([])
    _ = state.current_track  # just to execute the property
    assert state.current_track is None


def test_current_track_statement_valid_index():
    """
    Statement test:
    - Execute the function when there is at least one track
      and the index is valid.
    - Ensures the 'if' body line is executed.
    """
    track = types.SimpleNamespace(title="Track 1")
    state = make_state([track])
    state.current_index = 0

    # This executes the true branch and returns the track
    assert state.current_track is track
