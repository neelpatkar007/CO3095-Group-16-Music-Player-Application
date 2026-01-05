import unittest
from unittest.mock import MagicMock, patch
from music_player.player_ui import print_progress


class TestConcolicExecution(unittest.TestCase):

    @patch('builtins.print')
    @patch('music_player.player_ui.format_mm_ss')
    @patch('music_player.player_ui.get_progress')
    @patch('music_player.player_ui._ensure_player_state')
    def test_iter1_concrete_null(self, mock_ensure, mock_get_progress, mock_fmt, mock_print):

        S1 = None

        mock_ensure.return_value = None

        print_progress(S1)

        mock_ensure.assert_called_with(S1, "progress")
        mock_print.assert_not_called()


    @patch('builtins.print')
    @patch('music_player.player_ui.format_mm_ss')
    @patch('music_player.player_ui.get_progress')
    @patch('music_player.player_ui._ensure_player_state')
    def test_iter2_concrete_valid(self, mock_ensure, mock_get_progress, mock_fmt, mock_print):
        S1 = MagicMock(name="DerivedValidState")

        mock_ensure.return_value = S1
        mock_get_progress.return_value = (10, 20)
        mock_fmt.return_value = "00:XX"

        print_progress(S1)

        mock_ensure.assert_called_with(S1, "progress")
        mock_get_progress.assert_called_with(S1)
        mock_print.assert_called_once()



if __name__ == '__main__':
    unittest.main()