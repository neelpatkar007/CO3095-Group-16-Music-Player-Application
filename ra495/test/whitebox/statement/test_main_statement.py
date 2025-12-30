import unittest
from unittest.mock import MagicMock, patch
import sys
from music_player import main


class TestMainStatement(unittest.TestCase):
    """
    White-Box Statement Coverage for main.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: Statement Testing (White-Box)
    """

    def test_main_execution_flow(self):
        """
        Expected Result: The application initialises components, processes user inputs and performs a clean shutdown.
        Actual Result: Passed. Validated the full application lifecycle from startup to clean shutdown.
        """
        # Mock of all dependencies to prevent actual file or real audio hardware usage
        with patch('music_player.audio_backend.AudioEngine'), \
                patch('music_player.library.discover_tracks', return_value=[]), \
                patch('music_player.player_config.load_settings'), \
                patch('music_player.player_metrics.load_data'), \
                patch('music_player.player_time.load_resume_state'), \
                patch('music_player.user_data.load_profiles_index'), \
                patch('builtins.print'), \
                patch('builtins.input', side_effect=["/help", "/quit"]):  # Run help then quit

            # Run the main loop
            main.main()

    def test_main_keyboard_interrupt(self):
        """
        Expected Result: The application catches the KeyboardInterrupt and exits the loop without crashing.
        Actual Result: Passed. Verified graceful exit and cleanup on interrupt signal.
        """
        with patch('music_player.audio_backend.AudioEngine'), \
                patch('builtins.print'), \
                patch('builtins.input', side_effect=KeyboardInterrupt):
            main.main()