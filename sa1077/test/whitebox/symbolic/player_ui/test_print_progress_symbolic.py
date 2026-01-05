import unittest
from unittest.mock import MagicMock, patch
from music_player.player_ui import print_progress


class TestSymbolicExecution(unittest.TestCase):

    @patch('builtins.print')
    @patch('music_player.player_ui.format_mm_ss')
    @patch('music_player.player_ui.get_progress')
    @patch('music_player.player_ui._ensure_player_state')
    def test_pc1_early_return(self, mock_ensure, mock_get_progress, mock_fmt, mock_print):

        S1 = None

        mock_ensure.return_value = None

        print_progress(S1)

        mock_ensure.assert_called_once_with(S1, "progress")
        mock_get_progress.assert_not_called()
        mock_print.assert_not_called()

    @patch('builtins.print')
    @patch('music_player.player_ui.format_mm_ss')
    @patch('music_player.player_ui.get_progress')
    @patch('music_player.player_ui._ensure_player_state')
    def test_pc2_full_path(self, mock_ensure, mock_get_progress, mock_fmt, mock_print):

        S1 = MagicMock(name="ValidPlayerState")

        mock_ensure.return_value = S1

        mock_get_progress.return_value = (79, 204)

        mock_fmt.side_effect = ["01:19", "03:24"]

        print_progress(S1)

        mock_ensure.assert_called_once_with(S1, "progress")
        mock_get_progress.assert_called_once_with(S1)

        mock_print.assert_called_once_with("[ui] Progress: 01:19/03:24")


if __name__ == '__main__':
    unittest.main()