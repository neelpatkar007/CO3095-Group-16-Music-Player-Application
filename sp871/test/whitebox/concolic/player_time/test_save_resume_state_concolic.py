import unittest
from unittest.mock import MagicMock, patch, mock_open
from music_player.player_time import save_resume_state


class TestConcolicExecution(unittest.TestCase):


    def setUp(self):
        self.patcher_file = patch('music_player.player_time.RESUME_FILE')
        self.mock_resume_file = self.patcher_file.start()
        self.patcher_json = patch('json.dump')
        self.mock_json_dump = self.patcher_json.start()
        self.patcher_print = patch('builtins.print')
        self.mock_print = self.patcher_print.start()
        self.patcher_open = patch('builtins.open', new_callable=mock_open)
        self.mock_open = self.patcher_open.start()

    def tearDown(self):
        self.patcher_file.stop()
        self.patcher_json.stop()
        self.patcher_print.stop()
        self.patcher_open.stop()

    def test_iteration_1_invalid_s1(self):
        save_resume_state(None)

        self.mock_resume_file.parent.exists.assert_not_called()

    def test_iteration_2_invalid_s2(self):
        seed_state = MagicMock()
        seed_state.current_track = None

        save_resume_state(seed_state)

        self.mock_resume_file.parent.exists.assert_not_called()

    def test_iteration_3_invalid_attr(self):
        seed_state = MagicMock()
        del seed_state.current_track.path

        save_resume_state(seed_state)

        # Verification
        self.mock_resume_file.parent.exists.assert_not_called()

    def test_iteration_4_path_none(self):
        seed_state = MagicMock()
        seed_state.current_track.path = None

        save_resume_state(seed_state)

        self.mock_resume_file.parent.exists.assert_not_called()

    def test_iteration_5_minutes_branch(self):
        seed_state = MagicMock()
        seed_state.current_track.path = "/music/song.mp3"
        seed_state.position_seconds = 125.0  # Forces S4 >= 60
        self.mock_resume_file.parent.exists.return_value = False  # Forces mkdir

        save_resume_state(seed_state)

        self.mock_resume_file.parent.mkdir.assert_called_once()
        self.mock_print.assert_called_with("[state] Playback saved at 2m 5s.")

    def test_iteration_6_seconds_branch(self):
        seed_state = MagicMock()
        seed_state.current_track.path = "/music/song.mp3"
        seed_state.position_seconds = 30.0  # Forces S4 < 60
        self.mock_resume_file.parent.exists.return_value = True

        save_resume_state(seed_state)

        self.mock_print.assert_called_with("[state] Playback saved at 30s.")

    def test_iteration_7_oserror(self):
        seed_state = MagicMock()
        seed_state.current_track.path = "/music/song.mp3"
        seed_state.position_seconds = 30.0

        self.mock_open.side_effect = OSError("Permission denied")

        save_resume_state(seed_state)
        self.mock_print.assert_called_with("[state] File system error: Permission denied")

    def test_iteration_8_typeerror(self):
        seed_state = MagicMock()
        seed_state.current_track.path = "/music/song.mp3"
        seed_state.position_seconds = 30.0

        self.mock_json_dump.side_effect = TypeError("Object not JSON serializable")

        save_resume_state(seed_state)
        self.mock_print.assert_called_with("[state] Data format error: Object not JSON serializable")

    def test_iteration_9_unexpected_error(self):
        seed_state = MagicMock()
        seed_state.current_track.path = "/music/song.mp3"
        seed_state.position_seconds = 30.0

        self.mock_json_dump.side_effect = Exception("System Fault")

        save_resume_state(seed_state)
        self.mock_print.assert_called_with("[state] Unexpected error saving state: System Fault")


if __name__ == '__main__':
    unittest.main()