import unittest
from unittest.mock import MagicMock, patch
import io

from music_player.playlists_basic import show_current_playlist


class TestConcolicGenerations(unittest.TestCase):
    def setUp(self):
        self._target_function = show_current_playlist

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_iter_1_concrete_seed(self, mock_stdout):
        state = None
        self._target_function(state)
        self.assertEqual(
            mock_stdout.getvalue().strip(),
            "[pl] Error: State is None.\n[pl] Error: State is None."
        )

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_iter_2_flip_s2(self, mock_stdout):

        class StateObj: pass

        state = StateObj()

        self._target_function(state)
        self.assertEqual(
            mock_stdout.getvalue().strip(),
            "[pl] Error: State is None.\n[pl] Error: State is None."
        )

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_iter_3_flip_s3(self, mock_stdout):
        state = MagicMock()
        state.playlists = []
        state.active_playlist_index = None

        self._target_function(state)
        self.assertEqual(mock_stdout.getvalue().strip(), "[pl] No active playlist. Use /pl.open <name|index>.")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_iter_4_flip_s4(self, mock_stdout):
        state = MagicMock()
        state.active_playlist_index = 0
        state.playlists = []

        self._target_function(state)
        self.assertEqual(mock_stdout.getvalue().strip(), "[pl] No active playlist. Use /pl.open <name|index>.")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_iter_5_full_path(self, mock_stdout):
        state = MagicMock()
        mock_pl = MagicMock()
        mock_pl.name = "Concolic Hits"

        state.active_playlist_index = 0
        state.playlists = [mock_pl]

        self._target_function(state)
        self.assertIn("Concolic Hits", mock_stdout.getvalue().strip())


if __name__ == '__main__':
    unittest.main()