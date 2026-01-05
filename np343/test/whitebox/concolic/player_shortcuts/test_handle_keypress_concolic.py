import unittest
from unittest.mock import MagicMock, patch
from music_player.player_state import PlayerState
from music_player.player_shortcuts import handle_keypress


class TestConcolicTesting(unittest.TestCase):

    def setUp(self):
        self.mock_state = MagicMock(spec=PlayerState)
        self.mock_state.library_tracks = []
        self.mock_state.is_playing = False
        self.mock_state.volume = 50

    @patch('music_player.player_shortcuts.player_core')
    def test_pc5_stop(self, mock_core):
        self.mock_state.is_playing = True
        handle_keypress(self.mock_state, "s")
        mock_core.stop.assert_called_once()

    @patch('music_player.player_shortcuts.player_audio')
    def test_pc7_mute(self, mock_audio):
        handle_keypress(self.mock_state, "m")
        mock_audio.toggle_mute.assert_called_once()

    def test_pc8_vol_up(self):
        self.mock_state.volume = 50
        handle_keypress(self.mock_state, "+")
        self.assertEqual(self.mock_state.volume, 60)

    def test_pc9_vol_max(self):
        self.mock_state.volume = 100
        handle_keypress(self.mock_state, "+")
        self.assertEqual(self.mock_state.volume, 100)

    def test_pc11_vol_min(self):
        self.mock_state.volume = 0
        handle_keypress(self.mock_state, "-")
        self.assertEqual(self.mock_state.volume, 0)

if __name__ == "__main__":
    unittest.main()