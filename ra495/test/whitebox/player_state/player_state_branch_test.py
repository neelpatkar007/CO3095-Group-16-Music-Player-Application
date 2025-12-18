import types
import pytest

from music_player.player_state import PlayerState


class DummyEngine:
    """
    Minimal stub so PlayerState can be constructed.
    """
    pass


def make_state(tracks):
    '''
    Helper to create a PlayerState for each test.
    '''
    return PlayerState(tracks=tracks, audio_engine=DummyEngine())

# White box testing branch coverage
# These tests ensure the conditional check within 'current_track' property evaluates
# to both True and False outcomes.
def test_current_track_branch_empty_library():
    """
    White box branch coverage
    Target branch - the 'false' outcome of the index validity check.

    Explanation:
    Condition: 0 <= current_index < len(tracks) relies on the list length.
    And by passing an empty list, len(tracks) is 0, making the condition FALSE
    We then verify that the code handles this case correctly by returning None.
    """
    state = make_state([])
    state.current_index = 0

    # Assert that the False branch returns None
    assert state.current_track is None


def test_current_track_branch_valid_index():
    """
    White box branch coverage
    Target branch - the 'true' outcome of the index validation check.

    Explanation:
    We provide a state where the list exists and index is within bounds.
    THe condition 0 <= current_index < len(tracks) evaluates to TRUE.
    We then verify that the code enters the 'if' block and returns the correct object.
    """
    track = types.SimpleNamespace(title="Track 1")
    state = make_state([track])
    state.current_index = 0
    assert state.current_track is track


def test_current_track_branch_index_out_of_range():
    """
    White box branch coverage
    Target branch - the 'false' outcome boundary check

    Explanation:
    We set current_index to a value greater than the last valid index.
    This makes the condition 0 <= current_index < len(tracks) evaluate to FALSE.
    We then verify that the code correctly returns None for an out-of-bounds index.

    """
    track = types.SimpleNamespace(title="Track 1")
    state = make_state([track])
    state.current_index = 5  # out of range index

    assert state.current_track is None
