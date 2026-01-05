import unittest
from unittest.mock import patch, mock_open, MagicMock
from music_player.user_data import _save_profiles


class TestConcolicTesting(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_pc_4(self, mock_json, mock_file):
        state = MagicMock()
        state.active_profile = "Hero"
        state.profiles = {"Hero": {"level": 10}}

        _save_profiles(state)

        mock_file.assert_called_once()
        mock_json.assert_called_once()

    @patch("builtins.open", side_effect=IOError("Disk Full"))
    def test_pc_5(self, mock_file):
        state = MagicMock()
        state.active_profile = "Hero"
        state.profiles = {"Hero": {"level": 10}}

        with patch('builtins.print') as mock_print:
            _save_profiles(state)
            mock_print.assert_called_with("[profile] Error saving: Disk Full")


if __name__ == "__main__":
    unittest.main()