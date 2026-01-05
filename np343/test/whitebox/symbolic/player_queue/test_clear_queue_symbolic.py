import unittest
from unittest.mock import MagicMock, patch
from music_player.player_queue import clear_queue


class TestSymbolicExecution(unittest.TestCase):
    def setUp(self):
        self.mock_track = MagicMock()
        self.mock_track.display_name = "Song A"

    def test_pc1_invalid_state(self):
        for s1 in [None, "string", 123, True]:
            with patch('builtins.print') as mocked_print:
                clear_queue(s1)
                mocked_print.assert_called_with("[queue] Error: State is None.")

    def test_pc2_missing_tracks(self):
        class State:
            pass

        s1 = State()
        with patch('builtins.print') as mocked_print:
            clear_queue(s1)
            mocked_print.assert_called_with("[queue] Queue is already missing.")
            self.assertEqual(s1.tracks, [])

    def test_pc3_corrupted_type_conversion_fail(self):
        class State:
            tracks = 123

        s1 = State()
        with patch('builtins.print') as mocked_print:
            clear_queue(s1)
            mocked_print.assert_called_with("[queue] Queue corrupted (invalid type).")
            self.assertEqual(s1.tracks, [])

    def test_pc4_empty_queue(self):

        class State:
            tracks = []

        s1 = State()
        with patch('builtins.print') as mocked_print:
            clear_queue(s1)
            mocked_print.assert_called_with("[queue] Queue is already empty.")

    def test_pc5_retain_current(self):

        class State:
            tracks = [self.mock_track, MagicMock()]
            current_index = 0
            is_playing = True

        s1 = State()
        with patch('builtins.print') as mocked_print:
            clear_queue(s1)
            self.assertEqual(len(s1.tracks), 1)
            self.assertEqual(s1.tracks[0], self.mock_track)
            mocked_print.assert_called_with("[queue] Queue cleared (current song retained).")

    def test_pc6_invalid_index_clear_all(self):

        class State:
            tracks = [self.mock_track]
            current_index = 5
            is_playing = True

        s1 = State()
        with patch('builtins.print') as mocked_print:
            clear_queue(s1)
            self.assertEqual(s1.tracks, [])
            mocked_print.assert_called_with("[queue] Queue completely cleared.")

    def test_pc7_stopped_state(self):

        class State:
            tracks = [self.mock_track]
            current_index = 0
            is_playing = False
            is_paused = False  # Implies stopped

        s1 = State()
        with patch('builtins.print') as mocked_print:
            clear_queue(s1)
            mocked_print.assert_any_call("[queue] (Player is stopped)")


if __name__ == '__main__':
    unittest.main()
