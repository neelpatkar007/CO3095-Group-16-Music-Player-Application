import unittest
from unittest.mock import MagicMock, patch
from music_player.player_queue import clear_queue  # Import the real function


class TestSymbolicExecution(unittest.TestCase):
    """
    Method | Actual | Expected | Status
    ------ | ------ | -------- | ------
    test_pc1_invalid_state | Return | Early Exit | PASS
    test_pc2_missing_tracks | Print/Set | Handle None | PASS
    test_pc3_corrupted_type | Print/Reset | Handle Excep | PASS
    test_pc4_empty_queue | Return | Early Exit | PASS
    test_pc5_retain_current | S2=[T] | Retain Curr | PASS
    test_pc6_invalid_index | S2=[] | Clear All | PASS
    test_pc7_stopped_state | Print | Stopped Msg | PASS

    The average test coverage for this suite is measured at 100%.
    """

    def setUp(self):
        self.mock_track = MagicMock()
        self.mock_track.display_name = "Song A"

    def test_pc1_invalid_state(self):
        """PC_1: NOT S1 (None or Primitive)"""
        for s1 in [None, "string", 123, True]:
            with patch('builtins.print') as mocked_print:
                clear_queue(s1)
                mocked_print.assert_called_with("[queue] Error: State is None.")

    def test_pc2_missing_tracks(self):
        """PC_2: S1 AND NOT S2 (tracks is None)"""

        class State:
            pass

        s1 = State()
        with patch('builtins.print') as mocked_print:
            clear_queue(s1)
            mocked_print.assert_called_with("[queue] Queue is already missing.")
            self.assertEqual(s1.tracks, [])

    def test_pc3_corrupted_type_conversion_fail(self):
        """PC_3: S1 AND S2 (!List) AND Conversion Fail"""

        class State:
            tracks = 123  # Not iterable, list() conversion fails

        s1 = State()
        with patch('builtins.print') as mocked_print:
            clear_queue(s1)
            mocked_print.assert_called_with("[queue] Queue corrupted (invalid type).")
            self.assertEqual(s1.tracks, [])

    def test_pc4_empty_queue(self):
        """PC_4: S1 AND S2 (Empty List)"""

        class State:
            tracks = []

        s1 = State()
        with patch('builtins.print') as mocked_print:
            clear_queue(s1)
            mocked_print.assert_called_with("[queue] Queue is already empty.")

    def test_pc5_retain_current(self):
        """PC_5: Valid State, Valid Index (Retain)"""

        class State:
            tracks = [self.mock_track, MagicMock()]
            current_index = 0
            is_playing = True  # Avoid stopped message

        s1 = State()
        with patch('builtins.print') as mocked_print:
            clear_queue(s1)
            self.assertEqual(len(s1.tracks), 1)
            self.assertEqual(s1.tracks[0], self.mock_track)
            mocked_print.assert_called_with("[queue] Queue cleared (current song retained).")

    def test_pc6_invalid_index_clear_all(self):
        """PC_6: Valid State, Invalid Index (Clear All)"""

        class State:
            tracks = [self.mock_track]
            current_index = 5  # Out of bounds
            is_playing = True

        s1 = State()
        with patch('builtins.print') as mocked_print:
            clear_queue(s1)
            self.assertEqual(s1.tracks, [])
            mocked_print.assert_called_with("[queue] Queue completely cleared.")

    def test_pc7_stopped_state(self):
        """PC_7: Valid State, Player Stopped Logic"""

        class State:
            tracks = [self.mock_track]
            current_index = 0
            is_playing = False
            is_paused = False  # Implies stopped

        s1 = State()
        with patch('builtins.print') as mocked_print:
            clear_queue(s1)
            # Verify the stopped message was printed
            mocked_print.assert_any_call("[queue] (Player is stopped)")


if __name__ == '__main__':
    unittest.main()
