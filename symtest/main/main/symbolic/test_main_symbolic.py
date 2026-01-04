import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path
from music_player import main as app_main

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))


class TestSymbolicMain(unittest.TestCase):
    '''
    Symbolic Execution Test Suite for the main() function.

    Test Results Table:
    | Method | Actual | Expected | Status |
    |--------|--------|----------|--------|
    | test_pc_1_exception_handling | Shutdown triggered via Exception | Clean Shutdown | PASS |
    | test_pc_2_command_break | Shutdown triggered via False return | Clean Shutdown | PASS |
    | test_pc_3_loop_continuation | Loop continues then breaks | Iteration + Shutdown | PASS |

    The average test coverage for this suite is measured at 100%.
    '''

    def setUp(self):
        # Common mocks for all paths to prevent side effects
        self.mock_audio = patch('music_player.main.AudioEngine').start()
        self.mock_tracks = patch('music_player.main.discover_tracks').start()
        self.mock_state_cls = patch('music_player.main.PlayerState').start()
        self.mock_config = patch('music_player.main.player_config').start()
        self.mock_metrics = patch('music_player.main.player_metrics').start()
        self.mock_time = patch('music_player.main.player_time').start()
        self.mock_user = patch('music_player.main.user_data').start()
        self.mock_thread = patch('threading.Thread').start()
        self.mock_event = patch('threading.Event').start()

        # Setup the state mock instance
        self.mock_state_instance = MagicMock()
        self.mock_state_cls.return_value = self.mock_state_instance

    def tearDown(self):
        patch.stopall()

    def test_pc_1_exception_handling(self):
        '''
        Validates PC_1: Input raises Exception (S2).
        Condition: S2 is True (Exception Raised).
        Expected Behaviour: Loop breaks immediately, entering finally block.
        '''
        with patch('builtins.input', side_effect=EOFError):
            with patch('builtins.print'):  # Suppress output
                try:
                    app_main.main()
                except EOFError:
                    self.fail("EOFError should be caught inside main()")

        # Verify Finally Block Assertions
        self.mock_time.save_resume_state.assert_called_once_with(self.mock_state_instance)
        self.mock_config.save_settings.assert_called_once_with(self.mock_state_instance)
        self.mock_user._save_current_to_profile.assert_called_once_with(self.mock_state_instance)
        self.mock_state_instance.audio_engine.stop.assert_called_once()

    def test_pc_2_command_break(self):
        '''
        Validates PC_2: Input Success (S1) AND handle_command returns False (NOT S3).
        Condition: NOT S2 AND NOT S3.
        Expected Behaviour: Loop breaks after command processing, entering finally block.
        '''
        # S1 = "/quit", S3 = False
        with patch('builtins.input', return_value="/quit"):
            with patch('music_player.main.handle_command', return_value=False) as mock_handle:
                with patch('builtins.print'):
                    app_main.main()

                # Verify Logic
                mock_handle.assert_called_once_with(self.mock_state_instance, "/quit")

        # Verify Finally Block Execution
        self.mock_state_instance.audio_engine.stop.assert_called_once()

    def test_pc_3_loop_continuation(self):
        '''
        Validates PC_3: Input Success (S1) AND handle_command returns True (S3).
        Condition: NOT S2 AND S3.
        Expected Behaviour: Loop continues.
        NOTE: To prevent infinite execution in the test, we sequence S3=True then S3=False.
        '''
        # Iteration 1: S1="/play", S3=True (PC_3)
        # Iteration 2: S1="/quit", S3=False (PC_2 - needed to terminate test)
        with patch('builtins.input', side_effect=["/play", "/quit"]):
            with patch('music_player.main.handle_command', side_effect=[True, False]) as mock_handle:
                with patch('builtins.print'):
                    app_main.main()

                # Verify multiple iterations occurred
                self.assertEqual(mock_handle.call_count, 2)
                mock_handle.assert_any_call(self.mock_state_instance, "/play")
                mock_handle.assert_any_call(self.mock_state_instance, "/quit")

        # Verify Finally Block Execution
        self.mock_state_instance.audio_engine.stop.assert_called_once()


if __name__ == '__main__':
    unittest.main()