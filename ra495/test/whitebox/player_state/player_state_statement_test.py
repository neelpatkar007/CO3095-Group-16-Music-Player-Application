import types
import pytest

from music_player.player_state import PlayerState


class DummyEngine:
    """Minimal stub so PlayerState can be constructed."""
    pass


def make_state(tracks):
    '''Helped to create a fresh PlayerState for each test. '''
    return PlayerState(tracks=tracks, audio_engine=DummyEngine())

# White box statement tests
# These tests ensure that specific return statements within the current_track property are executed
# at least once

def test_current_track_statement_empty_library():
    """
    White box Statement coverage
    Target - 'return None' statement when index is invalid or list is empty

    Explanation:
    We initialise the state with an empty track list. This is to force the
    code to evaluate the validation check and execute the specific line that returns
    'None'

    """
    state = make_state([])

    # Access the property to trigger the code execution
    _ = state.current_track  # just to execute the property

    # Verification to ensure the statement returning None was executed
    assert state.current_track is None


def test_current_track_statement_valid_index():
    """
    White box statement coverage
    Target - 'return self.tracks[self.current_index]' statement

    Explanation:
    We provide a valid track and a valid index of 0 to
    force the code to pass any validation checks and execute
    the specific line that retrieves and returns
    the actual track object.

    """
    track = types.SimpleNamespace(title="Track 1")
    state = make_state([track])
    state.current_index = 0

    # Verification to ensure the statement returning the track object was executed
    assert state.current_track is track
