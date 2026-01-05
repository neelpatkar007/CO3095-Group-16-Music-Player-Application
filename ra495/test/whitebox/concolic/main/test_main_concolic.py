import unittest
from unittest.mock import MagicMock, patch
from music_player import main as app_main

class TestConcolicMain(unittest.TestCase):

    def setUp(self):
        self.mock_state_cls = patch('music_player.main.PlayerState').start()
        patch('music_player.main.AudioEngine').start()
        patch('music_player.main.discover_tracks').start()
        patch('music_player.main.player_config').start()
        patch('music_player.main.player_metrics').start()
        patch('music_player.main.player_time').start()
        patch('music_player.main.user_data').start()
        patch('threading.Thread').start()
        patch('threading.Event').start()
        self.mock_state = self.mock_state_cls.return_value

    def tearDown(self):
        patch.stopall()

    def test_iteration_1_base_path(self):
        with patch('builtins.input', side_effect=["/play", "/quit"]):
            with patch('music_player.main.handle_command', side_effect=[True, False]) as mock_handle:
                with patch('builtins.print'):
                    app_main.main()
                args, _ = mock_handle.call_args_list[0]
                self.assertEqual(args[1], "/play")

    def test_iteration_2_flip_predicate(self):
        with patch('builtins.input', return_value="/quit"):
            with patch('music_player.main.handle_command', return_value=False) as mock_handle:
                with patch('builtins.print'):
                    app_main.main()

                mock_handle.assert_called_once()
                self.mock_state.audio_engine.stop.assert_called_once()

    def test_iteration_3_flip_exception(self):
        with patch('builtins.input', side_effect=EOFError):
            with patch('music_player.main.handle_command') as mock_handle:
                with patch('builtins.print'):
                    app_main.main()

                mock_handle.assert_not_called()
                self.mock_state.audio_engine.stop.assert_called_once()


if __name__ == '__main__':
    unittest.main()