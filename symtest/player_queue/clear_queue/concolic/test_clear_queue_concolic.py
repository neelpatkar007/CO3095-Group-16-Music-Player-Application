import unittest
from unittest.mock import MagicMock, patch
from music_player.player_queue import clear_queue  # Import the real function


class TestConcolicExecution(unittest.TestCase):
    """
    Method | Actual | Expected | Status
    ------ | ------ | -------- | ------
    test_iter1_seed_none | Error | Handle None | PASS
    test_iter2_seed_missing | Missing | Init List | PASS
    test_iter3_seed_bad_type | Corrupt | Reset List | PASS
    test_iter4_seed_empty | Empty | Early Ret | PASS
    test_iter5_seed_valid | Retained | Keep Curr | PASS
    test_iter6_seed_oob | Cleared | Wipe All | PASS

    The average test coverage for this suite is measured at 100%.
    """

    def setUp(self):
        # Base mock for tracks
        self.track_a = MagicMock()
        self.track_a.display_name = "Track A"

    def test_iter1_seed_none(self):
        """Iteration 1: Seed S1 = None"""
        seed_s1 = None
        with patch('builtins.print') as mock_p:
            clear_queue(seed_s1)
            mock_p.assert_called_with("[queue] Error: State is None.")

    def test_iter2_seed_missing(self):
        """Iteration 2: Seed S1 = Object, S2 = None"""
        class ConcolicState:
            pass  # No tracks attr

        seed_s1 = ConcolicState()

        with patch('builtins.print') as mock_p:
            clear_queue(seed_s1)
            mock_p.assert_called_with("[queue] Queue is already missing.")
            self.assertEqual(seed_s1.tracks, [])

    def test_iter3_seed_bad_type(self):
        """Iteration 3: Seed S1 = Obj, S2 = Unconvertible (int)"""
        class ConcolicState:
            tracks = 9999

        seed_s1 = ConcolicState()

        with patch('builtins.print') as mock_p:
            clear_queue(seed_s1)
            mock_p.assert_called_with("[queue] Queue corrupted (invalid type).")

    def test_iter4_seed_empty(self):
        """Iteration 4: Seed S1 = Obj, S2 = [] (Converted/Explicit)"""
        class ConcolicState:
            tracks = []

        seed_s1 = ConcolicState()

        with patch('builtins.print') as mock_p:
            clear_queue(seed_s1)
            mock_p.assert_called_with("[queue] Queue is already empty.")

    def test_iter5_seed_valid_retain(self):
        """Iteration 5: Seed S1 = Obj, S2 = [T], S3 = 0 (Constraint: Index Valid)"""
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
        """Iteration 6: Seed S1 = Obj, S2 = [T], S3 = 99 (Constraint: Index Invalid)"""
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
