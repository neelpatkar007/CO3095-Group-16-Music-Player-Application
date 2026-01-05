import unittest
from unittest.mock import MagicMock, patch
from music_player.player_audio import handle_mute_command

class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.mock_state = MagicMock()

    @patch('music_player.player_audio.toggle_mute')
    def test_pc1_s1_is_none(self, mock_toggle):
        S1 = None
        S2 = "/mute"

        handle_mute_command(S1, S2)
        mock_toggle.assert_not_called()

    @patch('music_player.player_audio.toggle_mute')
    def test_pc2_s2_is_not_string(self, mock_toggle):
        S1 = self.mock_state
        S2 = 12345

        handle_mute_command(S1, S2)
        mock_toggle.assert_not_called()

    @patch('sys.stdout')
    @patch('music_player.player_audio.toggle_mute')
    def test_pc3_mute_when_already_muted(self, mock_toggle, mock_stdout):
        S1 = self.mock_state
        S1.is_muted = True
        S2 = "/mute"

        handle_mute_command(S1, S2)
        mock_toggle.assert_not_called()

    @patch('music_player.player_audio.toggle_mute')
    def test_pc4_mute_when_unmuted(self, mock_toggle):
        S1 = self.mock_state
        S1.is_muted = False  # S3
        S2 = "/mute "

        handle_mute_command(S1, S2)
        mock_toggle.assert_called_once_with(S1)

    @patch('music_player.player_audio.toggle_mute')
    def test_pc5_unmute_when_already_unmuted(self, mock_toggle):
        S1 = self.mock_state
        S1.is_muted = False
        S2 = "/unmute"

        handle_mute_command(S1, S2)
        mock_toggle.assert_not_called()

    @patch('music_player.player_audio.toggle_mute')
    def test_pc6_unmute_when_muted(self, mock_toggle):
        S1 = self.mock_state
        S1.is_muted = True
        S2 = "/UNMUTE"

        handle_mute_command(S1, S2)
        mock_toggle.assert_called_once_with(S1)

    @patch('music_player.player_audio.toggle_mute')
    def test_pc7_unknown_command(self, mock_toggle):
        S1 = self.mock_state
        S1.is_muted = False
        S2 = "/dance"

        handle_mute_command(S1, S2)

        mock_toggle.assert_not_called()


if __name__ == '__main__':
    unittest.main()