import unittest
from unittest.mock import MagicMock, patch
from typing import List
from music_player.playlists_basic import rename_playlist


class TestConcolicExecution(unittest.TestCase):
    def setUp(self):
        self.mock_state = MagicMock()
        self.pl_alpha = MagicMock()
        self.pl_alpha.name = "Alpha"
        self.pl_beta = MagicMock()
        self.pl_beta.name = "Beta"

        self.mock_state.playlists = [self.pl_alpha, self.pl_beta]

    @patch('builtins.print')
    @patch('music_player.playlists_basic._resolve_playlist')
    @patch('music_player.playlists_basic._ensure_playlists')
    def test_concolic_iterations(self, mock_ensure, mock_resolve, mock_print):
        S1 = self.mock_state
        S2 = "1"
        S3 = ""

        rename_playlist(S1, S2, S3)
        mock_print.assert_called_with("[pl] Usage: /pl.rename <old> <new>")

        S3 = "Gamma"  # Derived valid input
        S2 = "999"  # Invalid selector causing None return
        mock_resolve.return_value = None

        rename_playlist(S1, S2, S3)
        S2 = "1"
        S3 = "Alpha"

        mock_resolve.return_value = self.pl_beta

        rename_playlist(S1, S2, S3)
        mock_print.assert_called_with(f"[pl] Another playlist already has the name '{S3}'.")

        S3 = "Delta"
        mock_resolve.return_value = self.pl_beta

        rename_playlist(S1, S2, S3)

        self.assertEqual(self.pl_beta.name, "Delta")
        mock_print.assert_called_with("[pl] Renamed playlist 'Beta' -> 'Delta'.")


if __name__ == '__main__':
    unittest.main()