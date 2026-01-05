import unittest
from unittest.mock import MagicMock, patch
from music_player.player_audio import handle_mute_command

class TestConcolicExecution(unittest.TestCase):

    def setUp(self):
        self.mock_state = MagicMock()

    @patch('music_player.player_audio.toggle_mute')
    def test_iteration_1_null_state(self, mock_toggle):
        S1 = None
        S2 = "test"

        handle_mute_command(S1, S2)

        mock_toggle.assert_not_called()

    @patch('music_player.player_audio.toggle_mute')
    def test_iteration_2_invalid_type(self, mock_toggle):
        S1 = self.mock_state
        S2 = 12345

        handle_mute_command(S1, S2)

        mock_toggle.assert_not_called()

    @patch('music_player.player_audio.toggle_mute')
    def test_iteration_3_unknown_command(self, mock_toggle):
        S1 = self.mock_state
        S1.is_muted = False
        S2 = "test"

        handle_mute_command(S1, S2)

        mock_toggle.assert_not_called()


if __name__ == '__main__':
    unittest.main()