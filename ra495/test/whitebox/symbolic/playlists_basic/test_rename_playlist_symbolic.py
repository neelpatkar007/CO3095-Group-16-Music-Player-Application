import unittest
from unittest.mock import MagicMock, patch
from typing import List
from music_player.playlists_basic import rename_playlist

class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):

        self.mock_state = MagicMock()
        self.mock_playlist_1 = MagicMock()
        self.mock_playlist_1.name = "Classic"
        self.mock_playlist_2 = MagicMock()
        self.mock_playlist_2.name = "Jazz"

        self.mock_state.playlists = [self.mock_playlist_1, self.mock_playlist_2]

    @patch('builtins.print')
    @patch('music_player.playlists_basic._resolve_playlist')
    @patch('music_player.playlists_basic._ensure_playlists')
    def test_pc_1_empty_input_validation(self, mock_ensure, mock_resolve, mock_print):

        S1 = self.mock_state
        S2 = "any_selector"
        S3 = "   "



        rename_playlist(S1, S2, S3)

        mock_print.assert_called_with("[pl] Usage: /pl.rename <old> <new>")
        mock_resolve.assert_not_called()

    @patch('builtins.print')
    @patch('music_player.playlists_basic._resolve_playlist')
    @patch('music_player.playlists_basic._ensure_playlists')
    def test_pc_2_resolution_failure(self, mock_ensure, mock_resolve, mock_print):

        S1 = self.mock_state
        S2 = "invalid_selector"
        S3 = "NewName"


        mock_resolve.return_value = None


        rename_playlist(S1, S2, S3)

        mock_resolve.assert_called_with(S1, S2)

        self.assertEqual(self.mock_playlist_1.name, "Classic")

    @patch('builtins.print')
    @patch('music_player.playlists_basic._resolve_playlist')
    @patch('music_player.playlists_basic._ensure_playlists')
    def test_pc_3_name_collision(self, mock_ensure, mock_resolve, mock_print):

        S1 = self.mock_state
        S2 = "1"
        S3 = "Classic"


        mock_resolve.return_value = self.mock_playlist_2



        rename_playlist(S1, S2, S3)

        mock_print.assert_called_with(f"[pl] Another playlist already has the name '{S3}'.")
        self.assertEqual(self.mock_playlist_2.name, "Jazz")

    @patch('builtins.print')
    @patch('music_player.playlists_basic._resolve_playlist')
    @patch('music_player.playlists_basic._ensure_playlists')
    def test_pc_4_successful_rename(self, mock_ensure, mock_resolve, mock_print):

        S1 = self.mock_state
        S2 = "1"
        S3 = "Heavy Metal"

        mock_resolve.return_value = self.mock_playlist_2



        rename_playlist(S1, S2, S3)

        self.assertEqual(self.mock_playlist_2.name, "Heavy Metal")
        mock_print.assert_called_with("[pl] Renamed playlist 'Jazz' -> 'Heavy Metal'.")


if __name__ == '__main__':
    unittest.main()