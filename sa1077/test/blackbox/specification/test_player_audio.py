import unittest
from unittest.mock import MagicMock, patch
from music_player import player_audio
from music_player.player_state import PlayerState


class TestPlayerAudioSpec(unittest.TestCase):
    """
    Black-Box Specification Testing for player_audio.py.
    Source: TSL Generated Test Frames playerAudio.txt.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: Category Partition Method
    """

    def setUp(self):
        # Create a valid mocked state
        self.state = MagicMock(spec=PlayerState)
        self.state.volume = 50
        self.state.is_muted = False
        self.state.saved_volume = None
        self.state.audio_engine = MagicMock()

   # Change Volume

    def test_change_volume_spec(self):
        """
        Expected Result: Safely handles volume changes, validates inputs, and unmutes automatically on valid updates.
        Actual Result:
            PASSED [100%][audio] Volume set to 75%
            [audio] Volume set to 20%
        """
        # State None
        player_audio.change_volume(None, "50")

        # Empty Input
        with patch("builtins.print") as m_print:
            player_audio.change_volume(self.state, "")
            m_print.assert_called_with(f"[audio] Current Volume: {self.state.volume}%")

        # Invalid Number Error
        with patch("builtins.print") as m_print:
            player_audio.change_volume(self.state, "abc")
            m_print.assert_called_with("[audio] Error: Volume must be a number.")

        # Out of Range Error
        with patch("builtins.print") as m_print:
            player_audio.change_volume(self.state, "150")
            m_print.assert_called_with("[audio] Error: Volume must be between 0 and 100.")