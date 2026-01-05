import unittest
from unittest.mock import MagicMock, patch
import sys
from music_player import main


class TestMainStatement(unittest.TestCase):
    def test_main_execution_flow(self):

        with patch('music_player.audio_backend.AudioEngine'), \
                patch('music_player.library.discover_tracks', return_value=[]), \
                patch('music_player.player_config.load_settings'), \
                patch('music_player.player_metrics.load_data'), \
                patch('music_player.player_time.load_resume_state'), \
                patch('music_player.user_data.load_profiles_index'), \
                patch('builtins.print'), \
                patch('builtins.input', side_effect=["/help", "/quit"]):  # Run help then quit

            main.main()

    def test_main_keyboard_interrupt(self):
        with patch('music_player.audio_backend.AudioEngine'), \
                patch('builtins.print'), \
                patch('builtins.input', side_effect=KeyboardInterrupt):
            main.main()