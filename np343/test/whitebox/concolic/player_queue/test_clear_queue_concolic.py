import unittest
from unittest.mock import MagicMock, patch
from music_player.player_queue import clear_queue


class TestConcolicExecution(unittest.TestCase):

    def setUp(self):
        self.track_a = MagicMock()
        self.track_a.display_name = "Track A"

    def test_iter1_seed_none(self):
        seed_s1 = None
        with patch('builtins.print') as mock_p:
            clear_queue(seed_s1)
            mock_p.assert_called_with("[queue] Error: State is None.")

    def test_iter2_seed_missing(self):
        class ConcolicState:
            pass

        seed_s1 = ConcolicState()

        with patch('builtins.print') as mock_p:
            clear_queue(seed_s1)
            mock_p.assert_called_with("[queue] Queue is already missing.")
            self.assertEqual(seed_s1.tracks, [])

    def test_iter3_seed_bad_type(self):
        class ConcolicState:
            tracks = 9999

        seed_s1 = ConcolicState()

        with patch('builtins.print') as mock_p:
            clear_queue(seed_s1)
            mock_p.assert_called_with("[queue] Queue corrupted (invalid type).")

    def test_iter4_seed_empty(self):
        class ConcolicState:
            tracks = []

        seed_s1 = ConcolicState()

        with patch('builtins.print') as mock_p:
            clear_queue(seed_s1)
            mock_p.assert_called_with("[queue] Queue is already empty.")

    def test_iter5_seed_valid_retain(self):
        class ConcolicState:
            tracks = [self.track_a]
            current_index = 0
            is_playing = True

        seed_s1 = ConcolicState()

        with patch('builtins.print') as mock_p:
            clear_queue(seed_s1)
            mock_p.assert_called_with("[queue] Queue cleared (current song retained).")
            self.assertEqual(seed_s1.tracks, [self.track_a])

    def test_iter6_seed_out_of_bounds(self):
        class ConcolicState:
            tracks = [self.track_a]
            current_index = 99
            is_playing = True

        seed_s1 = ConcolicState()

        with patch('builtins.print') as mock_p:
            clear_queue(seed_s1)
            mock_p.assert_called_with("[queue] Queue completely cleared.")
            self.assertEqual(seed_s1.tracks, [])


if __name__ == '__main__':
    unittest.main()
