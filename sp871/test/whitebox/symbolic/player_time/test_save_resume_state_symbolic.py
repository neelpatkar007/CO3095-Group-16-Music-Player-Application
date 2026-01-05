import unittest
from unittest.mock import MagicMock, patch, mock_open
import time
import datetime
from music_player.player_time import save_resume_state


class TestSymbolicExecution(unittest.TestCase):


    def setUp(self):
        # Common setup for valid state used in deeper paths
        self.mock_state = MagicMock()
        self.mock_state.current_track = MagicMock()
        self.mock_state.current_track.path = "test/path.mp3"
        self.mock_state.position_seconds = 120.0  # Default S4 > 60

        # Patch the global constants/imports used in the function
        self.patcher_file = patch('music_player.player_time.RESUME_FILE')
        self.mock_resume_file = self.patcher_file.start()

        self.patcher_json = patch('json.dump')
        self.mock_json_dump = self.patcher_json.start()

    def tearDown(self):
        self.patcher_file.stop()
        self.patcher_json.stop()

    def test_pc1_invalid_state_s1(self):
        """PC_1: NOT S1 (State is None)"""
        save_resume_state(None)
        # Assert no file operations occurred
        self.mock_resume_file.parent.exists.assert_not_called()

    def test_pc1_state_no_track_attr(self):
        """PC_1: S1 valid but NOT hasattr(S1, 'current_track')"""
        empty_state = object()
        save_resume_state(empty_state)
        self.mock_resume_file.parent.exists.assert_not_called()

    def test_pc2_track_is_falsey_s2(self):
        """PC_2: S1 valid, but S2 is False/None"""
        self.mock_state.current_track = None
        save_resume_state(self.mock_state)
        self.mock_resume_file.parent.exists.assert_not_called()

    def test_pc3_track_no_path_attr(self):
        """PC_3: S1, S2 valid, but NOT hasattr(S2, 'path')"""
        # Create a dummy object without 'path' attribute
        del self.mock_state.current_track.path
        save_resume_state(self.mock_state)
        self.mock_resume_file.parent.exists.assert_not_called()

    def test_pc4_path_is_none_s3(self):
        """PC_4: S1, S2 valid, but S3 (path) is None"""
        self.mock_state.current_track.path = None
        save_resume_state(self.mock_state)
        self.mock_resume_file.parent.exists.assert_not_called()

    @patch('builtins.print')
    @patch('builtins.open', new_callable=mock_open)
    def test_pc5_success_mins_format(self, mock_file, mock_print):
        """PC_5: All valid, S4 >= 60, S5 False (needs mkdir)"""
        # S4: Position > 60
        self.mock_state.position_seconds = 65.5
        # S5: Parent exists returns False
        self.mock_resume_file.parent.exists.return_value = False

        save_resume_state(self.mock_state)

        # Verification
        self.mock_resume_file.parent.mkdir.assert_called_with(parents=True, exist_ok=True)
        self.mock_json_dump.assert_called()
        # Verify minutes formatting logic
        mock_print.assert_called_with("[state] Playback saved at 1m 5s.")

    @patch('builtins.print')
    @patch('builtins.open', new_callable=mock_open)
    def test_pc6_success_secs_format(self, mock_file, mock_print):
        """PC_6: All valid, S4 < 60, S5 True (dir exists)"""
        # S4: Position < 60
        self.mock_state.position_seconds = 45.0
        # S5: Parent exists returns True
        self.mock_resume_file.parent.exists.return_value = True

        save_resume_state(self.mock_state)

        # Verification
        self.mock_resume_file.parent.mkdir.assert_not_called()
        mock_print.assert_called_with("[state] Playback saved at 45s.")

    @patch('builtins.print')
    def test_pc7_os_error_s6(self, mock_print):
        """PC_7: Write causes OSError (S6 failure)"""
        self.mock_resume_file.parent.exists.return_value = True
        # Simulate S6 failure at open()
        with patch('builtins.open', side_effect=OSError("Disk full")):
            save_resume_state(self.mock_state)
            mock_print.assert_called_with("[state] File system error: Disk full")

    @patch('builtins.print')
    @patch('builtins.open', new_callable=mock_open)
    def test_pc8_type_error_s6(self, mock_file, mock_print):
        """PC_8: Write causes TypeError (S6 failure)"""
        self.mock_resume_file.parent.exists.return_value = True
        # Simulate S6 failure at json.dump
        self.mock_json_dump.side_effect = TypeError("Not serializable")

        save_resume_state(self.mock_state)
        mock_print.assert_called_with("[state] Data format error: Not serializable")

    @patch('builtins.print')
    @patch('builtins.open', new_callable=mock_open)
    def test_pc9_general_exception_s6(self, mock_file, mock_print):
        """PC_9: Unexpected Exception (S6 failure)"""
        self.mock_resume_file.parent.exists.return_value = True
        # Simulate S6 failure generic
        self.mock_json_dump.side_effect = Exception("Unknown error")

        save_resume_state(self.mock_state)
        mock_print.assert_called_with("[state] Unexpected error saving state: Unknown error")


if __name__ == '__main__':
    unittest.main()