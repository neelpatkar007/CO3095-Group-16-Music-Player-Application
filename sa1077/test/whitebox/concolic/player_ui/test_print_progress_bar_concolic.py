import unittest
from unittest.mock import MagicMock, patch

from music_player.player_ui import print_progress_bar

class TestConcolicExecution(unittest.TestCase):

    @patch('music_player.player_ui.render_progress_bar')
    @patch('music_player.player_ui._ensure_player_state')
    def test_iteration_1_seed_none(self, mock_ensure, mock_render):
        s1_seed = None

        mock_ensure.return_value = None

        print_progress_bar(s1_seed)

        mock_ensure.assert_called_with(s1_seed, "progress_bar")
        mock_render.assert_not_called()

    @patch('builtins.print')
    @patch('music_player.player_ui.render_progress_bar')
    @patch('music_player.player_ui._ensure_player_state')
    def test_iteration_2_derived_obj(self, mock_ensure, mock_render, mock_print):
        s1_derived = MagicMock(name="DerivedState")

        mock_ensure.return_value = s1_derived
        mock_render.return_value = "|||||| 100%"

        print_progress_bar(s1_derived)

        mock_ensure.assert_called_with(s1_derived, "progress_bar")
        mock_render.assert_called_with(s1_derived)
        mock_print.assert_called_with("[ui] |||||| 100%")


if __name__ == '__main__':
    unittest.main()