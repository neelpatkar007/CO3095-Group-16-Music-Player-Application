import unittest
from unittest.mock import MagicMock, patch
from music_player.player_seek import render_progress_bar


class TestSymbolicExecution(unittest.TestCase):
    def setUp(self):
        self.mock_state = MagicMock()

    def test_pc_1_state_is_none(self):
        result = render_progress_bar(None, 15)
        self.assertEqual(result, "[ui error]")

    def test_pc_2_width_invalid_type(self):
        result = render_progress_bar(self.mock_state, "15")
        self.assertEqual(result, "[ui error]")

    def test_pc_3_width_boundary(self):
        result = render_progress_bar(self.mock_state, 0)
        self.assertEqual(result, "[ui error]")

    @patch('music_player.player_seek.get_progress')
    def test_pc_7_standard_execution(self, mock_get_progress):
        mock_get_progress.return_value = (3, 10)
        result = render_progress_bar(self.mock_state, 10)
        self.assertTrue(result.startswith("███░░░░░░░"))
        self.assertIn(" 30%", result)


if __name__ == "__main__":
    unittest.main()