import unittest
from unittest.mock import MagicMock
from io import StringIO
import sys
from music_player.playlists_basic import _ensure_playlists



class PlayerState:
    pass


class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.captured_output = StringIO()
        sys.stdout = self.captured_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_pc_1_state_is_none(self):
        state = None

        _ensure_playlists(state)

        output = self.captured_output.getvalue().strip()
        self.assertEqual(output, "[pl] Error: State is None.")

    def test_pc_2_state_has_no_attribute(self):

        state = PlayerState()
        if hasattr(state, 'playlists'):
            del state.playlists

        _ensure_playlists(state)

        output = self.captured_output.getvalue().strip()
        self.assertEqual(output, "[pl] Error: State is None.")

    def test_pc_3_attribute_is_none(self):
        state = PlayerState()
        state.playlists = None

        _ensure_playlists(state)

        self.assertEqual(state.playlists, [], "S3 should be mutated to an empty list")
        self.assertEqual(self.captured_output.getvalue(), "", "No error should be printed")

    def test_pc_4_attribute_is_valid(self):
        state = PlayerState()
        initial_list = [1, 2]
        state.playlists = initial_list

        _ensure_playlists(state)

        self.assertIs(state.playlists, initial_list, "S3 should remain unchanged")
        self.assertEqual(self.captured_output.getvalue(), "", "No error should be printed")


if __name__ == '__main__':
    unittest.main()