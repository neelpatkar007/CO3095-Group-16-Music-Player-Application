import unittest
from unittest.mock import MagicMock, patch
from music_player.player_shortcuts import handle_keypress
from music_player.player_state import PlayerState


class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.state = MagicMock(spec=PlayerState)
        self.state.tracks = []
        self.state.is_playing = False
        self.state.volume = 50

    def test_pc1_early_ret(self):
        self.assertIsNone(handle_keypress(self.state, ""))

    @patch('builtins.print')
    def test_pc2_no_tracks(self, mock_print):
        handle_keypress(self.state, "p")

    @patch('music_player.player_shortcuts.player_core')
    def test_pc3_pause(self, mock_core):
        self.state.tracks = ["track1"]
        self.state.is_playing = True
        handle_keypress(self.state, "p")
        mock_core.pause.assert_called_with(self.state)

    @patch('music_player.player_shortcuts.player_core')
    def test_pc4_play(self, mock_core):
        self.state.tracks = ["track1"]
        self.state.is_playing = False
        handle_keypress(self.state, "p")
        mock_core.play.assert_called_with(self.state)

    def test_pc12_invalid(self):
        handle_keypress(self.state, "z")

if __name__ == "__main__":
    unittest.main()