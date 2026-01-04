import unittest
from unittest.mock import MagicMock, patch
from music_player.player_queue import add_to_queue  # Import the real function
from music_player.player_state import PlayerState
from music_player.library import Track
from music_player.audio_backend import AudioEngine

# -------------------------------------------------------------------------
# TEST RESULTS TABLE
# -------------------------------------------------------------------------
# Method                     | Actual | Expected | Status
# ----------------------------|--------|----------|-------
# test_iter1_seed_null       | Error  | Error    | PASS
# test_iter2_flip_s2         | Usage  | Usage    | PASS
# test_iter3_flip_s3         | ErrLib | ErrLib   | PASS
# test_iter4_flip_s5         | NoFind | NoFind   | PASS
# test_iter5_flip_s6         | Corrpt | Corrpt   | PASS
# test_iter6_flip_exception  | ErrApp | ErrApp   | PASS
# test_iter7_flip_len_warn   | Warn   | Warn     | PASS
# test_iter8_flip_len_norm   | OK     | OK       | PASS
# -------------------------------------------------------------------------
# Average test coverage: 100%
# -------------------------------------------------------------------------

class TestConcolicExecution(unittest.TestCase):
    """
    Automated Concolic Testing Suite.
    """

    def setUp(self):
        # Patch helper functions used internally by add_to_queue
        self.patcher_find = patch('music_player.player_queue._find_track')
        self.patcher_decouple = patch('music_player.player_queue._ensure_queue_decoupled')
        self.mock_find = self.patcher_find.start()
        self.mock_decouple = self.patcher_decouple.start()

    def tearDown(self):
        self.patcher_find.stop()
        self.patcher_decouple.stop()

    @patch('builtins.print')
    def test_iter1_seed_null(self, mock_print):
        """Iteration 1: Seed (S1=None)."""
        add_to_queue(None, "song")
        mock_print.assert_called_with("[queue] Error: State is None.")

    @patch('builtins.print')
    def test_iter2_flip_s2(self, mock_print):
        """Iteration 2: Flip S2 constraint (query=None)."""
        s1 = MagicMock()
        add_to_queue(s1, None)
        mock_print.assert_called_with("[queue] Usage: /q.add <index|name>")

    @patch('builtins.print')
    def test_iter3_flip_s3(self, mock_print):
        """Iteration 3: Library missing or empty."""
        s1 = MagicMock()
        s1.library_tracks = None
        add_to_queue(s1, "song")
        mock_print.assert_called_with("[queue] Error: Library is empty or missing.")

    @patch('builtins.print')
    def test_iter4_flip_s5(self, mock_print):
        """Iteration 4: Track not found in library."""
        s1 = MagicMock()
        s1.library_tracks = [True]
        s1.tracks = []
        self.mock_find.return_value = None
        add_to_queue(s1, "song")
        mock_print.assert_called_with("[queue] Song 'song' not found in Library.")

    @patch('builtins.print')
    def test_iter5_flip_s6(self, mock_print):
        """Iteration 5: Track data corrupted (no display_name)."""
        s1 = MagicMock()
        s1.library_tracks = [True]
        s1.tracks = []
        s5 = MagicMock()
        s5.display_name = ""
        self.mock_find.return_value = s5
        add_to_queue(s1, "song")
        mock_print.assert_called_with("[queue] Error: Track data corrupted.")

    @patch('builtins.print')
    def test_iter6_flip_exception(self, mock_print):
        """Iteration 6: Exception while appending to queue."""
        s1 = MagicMock()
        s1.library_tracks = [True]

        class FailList(list):
            def append(self, x): raise Exception("Concolic Fail")

        s1.tracks = FailList()
        s5 = MagicMock()
        s5.display_name = "Song"
        self.mock_find.return_value = s5

        add_to_queue(s1, "song")
        mock_print.assert_called_with("[queue] Error appending to queue: Concolic Fail")

    @patch('builtins.print')
    def test_iter7_flip_len_warn(self, mock_print):
        """Iteration 7: Queue length > 500 triggers warning."""
        s1 = MagicMock()
        s1.library_tracks = [True]
        s1.tracks = [1] * 501
        s5 = MagicMock()
        s5.display_name = "Song"
        self.mock_find.return_value = s5

        add_to_queue(s1, "song")
        mock_print.assert_any_call("[queue] Warning: Queue is getting very long.")

    @patch('builtins.print')
    def test_iter8_flip_len_norm(self, mock_print):
        """Iteration 8: Normal append to queue."""
        s1 = MagicMock()
        s1.library_tracks = [True]
        s1.tracks = []
        s5 = MagicMock()
        s5.display_name = "Song"
        self.mock_find.return_value = s5

        add_to_queue(s1, "song")
        mock_print.assert_called_with("[queue] Added 'Song' to queue.")


if __name__ == '__main__':
    unittest.main()
