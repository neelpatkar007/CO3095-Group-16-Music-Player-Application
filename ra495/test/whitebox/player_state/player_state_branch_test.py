import types
import pytest

from music_player.player_state import PlayerState


class DummyEngine:
    """Minimal stub so PlayerState can be constructed."""
    pass


def make_state(tracks):
    return PlayerState(tracks=tracks, audio_engine=DummyEngine())

def test_current_track_branch_empty_library():
    """
    Branch test:
    - Condition 0 <= current_index < len(tracks) is FALSE because len(tracks) == 0.
    - Covers the 'False' outcome of the condition.
    """
    state = make_state([])
    state.current_index = 0
    assert state.current_track is None


def test_current_track_branch_valid_index():
    """
    Branch test:
    - Condition 0 <= current_index < len(tracks) is TRUE.
    - Covers the 'True' outcome of the condition.
    """
    track = types.SimpleNamespace(title="Track 1")
    state = make_state([track])
    state.current_index = 0
    assert state.current_track is track


def test_current_track_branch_index_out_of_range():
    """
    Branch test:
    - Condition 0 <= current_index < len(tracks) is FALSE
      because current_index >= len(tracks).
    - Also exercises the 'False' path with a different reason (out-of-range index).
    """
    track = types.SimpleNamespace(title="Track 1")
    state = make_state([track])
    state.current_index = 5  # out of range

    assert state.current_track is None
