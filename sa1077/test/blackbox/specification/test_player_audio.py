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

        # Valid Set
        player_audio.change_volume(self.state, "75")
        self.assertEqual(self.state.volume, 75)
        self.state.audio_engine.set_volume.assert_called_with(75)

        # Valid Set while Muted
        self.state.is_muted = True
        self.state.saved_volume = 30
        player_audio.change_volume(self.state, "20")

        self.assertFalse(self.state.is_muted)
        self.assertIsNone(self.state.saved_volume)
        self.state.audio_engine.set_muted.assert_called_with(False)
        self.state.audio_engine.set_volume.assert_called_with(20)

    # Toggle Mute

    def test_toggle_mute_spec(self):
        """
        Expected Result: Returns on None and otherwise toggles backend saves or restores volume.
        Actual Result:
            PASSED [100%][audio] Muted
            [audio] Unmuted (volume back to 60%)
        """
        # State None
        player_audio.toggle_mute(None)

        # Mute
        self.state.is_muted = False
        self.state.volume = 60

        player_audio.toggle_mute(self.state)

        self.assertTrue(self.state.is_muted)
        self.assertEqual(self.state.saved_volume, 60)
        self.state.audio_engine.set_muted.assert_called_with(True)
        self.state.audio_engine.set_volume.assert_called_with(0)

        # Unmute
        # Setup muted state
        self.state.is_muted = True
        self.state.saved_volume = 60
        self.state.volume = 0

        player_audio.toggle_mute(self.state)

        self.assertFalse(self.state.is_muted)
        self.assertEqual(self.state.volume, 60)  # Restore Volume
        self.state.audio_engine.set_muted.assert_called_with(False)
        self.state.audio_engine.set_volume.assert_called_with(60)

    # Handle Mute Command

    def test_handle_mute_command_spec(self):
        """
        Expected Result: Calls toggle_mute if the state changes, otherwise prints "Already muted/unmuted".
        Actual Result: Passed.
        """
        # State None
        player_audio.handle_mute_command(None, "/mute")

        # /mute when already muted
        self.state.is_muted = True
        with patch("builtins.print") as m_print:
            player_audio.handle_mute_command(self.state, "/mute")
            m_print.assert_called_with("[audio] Already muted.")

        # /mute
        self.state.is_muted = False
        with patch("music_player.player_audio.toggle_mute") as m_toggle:
            player_audio.handle_mute_command(self.state, "/mute")
            m_toggle.assert_called_once()

        # /unmute when already unmuted
        self.state.is_muted = False
        with patch("builtins.print") as m_print:
            player_audio.handle_mute_command(self.state, "/unmute")
            m_print.assert_called_with("[audio] Already unmuted.")

        # /unmute
        self.state.is_muted = True
        with patch("music_player.player_audio.toggle_mute") as m_toggle:
            player_audio.handle_mute_command(self.state, "/unmute")
            m_toggle.assert_called_once()

        # Unknown Command
        with patch("builtins.print") as m_print:
            player_audio.handle_mute_command(self.state, "/garbage")
            m_print.assert_called_with("[audio] Unknown mute command.")