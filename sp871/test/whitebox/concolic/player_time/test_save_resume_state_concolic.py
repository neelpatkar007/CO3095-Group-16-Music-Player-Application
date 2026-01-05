import unittest
from unittest.mock import MagicMock, patch, mock_open
from music_player.player_time import save_resume_state


class TestConcolicExecution(unittest.TestCase):


    def setUp(self):
        # Base Mocks
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
        """Iteration 1: Concrete Seed (S1=None). Target: PC_1 (Early Return)."""
        # Execution
        save_resume_state(None)

        # Verification of Constraints
        self.mock_resume_file.parent.exists.assert_not_called()

    def test_iteration_2_invalid_s2(self):
        """Iteration 2: Flip (S1 Valid). Seed (S1=Obj, S2=None). Target: PC_2."""
        # Derived Input
        seed_state = MagicMock()
        seed_state.current_track = None

        # Execution
        save_resume_state(seed_state)

        # Verification
        self.mock_resume_file.parent.exists.assert_not_called()

    def test_iteration_3_invalid_attr(self):
        """Iteration 3: Flip (S2 Valid). Seed (S2=Obj, No 'path'). Target: PC_3."""
        # Derived Input
        seed_state = MagicMock()
        del seed_state.current_track.path  # Simulating missing attribute

        # Execution
        save_resume_state(seed_state)

        # Verification
        self.mock_resume_file.parent.exists.assert_not_called()

    def test_iteration_4_path_none(self):
        """Iteration 4: Flip (Has 'path'). Seed (S3=None). Target: PC_4."""
        # Derived Input
        seed_state = MagicMock()
        seed_state.current_track.path = None

        # Execution
        save_resume_state(seed_state)

        # Verification
        self.mock_resume_file.parent.exists.assert_not_called()

    def test_iteration_5_minutes_branch(self):
        """Iteration 5: Flip (S3 Valid). Seed (S4=125.0). Target: PC_5."""
        # Derived Input
        seed_state = MagicMock()
        seed_state.current_track.path = "/music/song.mp3"
        seed_state.position_seconds = 125.0  # Forces S4 >= 60
        self.mock_resume_file.parent.exists.return_value = False  # Forces mkdir

        # Execution
        save_resume_state(seed_state)

        # Verification
        self.mock_resume_file.parent.mkdir.assert_called_once()
        self.mock_print.assert_called_with("[state] Playback saved at 2m 5s.")

    def test_iteration_6_seconds_branch(self):
        """Iteration 6: Flip (S4 < 60). Seed (S4=30.0). Target: PC_6."""
        # Derived Input
        seed_state = MagicMock()
        seed_state.current_track.path = "/music/song.mp3"
        seed_state.position_seconds = 30.0  # Forces S4 < 60
        self.mock_resume_file.parent.exists.return_value = True

        # Execution
        save_resume_state(seed_state)

        # Verification
        self.mock_print.assert_called_with("[state] Playback saved at 30s.")

    def test_iteration_7_oserror(self):
        """Iteration 7: Flip (S6 Success). Seed (S6=OSError). Target: PC_7."""
        seed_state = MagicMock()
        seed_state.current_track.path = "/music/song.mp3"
        seed_state.position_seconds = 30.0

        # Inject Symbolic Constraint S6 failure
        self.mock_open.side_effect = OSError("Permission denied")

        save_resume_state(seed_state)
        self.mock_print.assert_called_with("[state] File system error: Permission denied")

    def test_iteration_8_typeerror(self):
        """Iteration 8: Flip (S6 OSError). Seed (S6=TypeError). Target: PC_8."""
        seed_state = MagicMock()
        seed_state.current_track.path = "/music/song.mp3"
        seed_state.position_seconds = 30.0

        # Inject Symbolic Constraint S6 failure
        self.mock_json_dump.side_effect = TypeError("Object not JSON serializable")

        save_resume_state(seed_state)
        self.mock_print.assert_called_with("[state] Data format error: Object not JSON serializable")

    def test_iteration_9_unexpected_error(self):
        """Iteration 9: Flip (S6 TypeError). Seed (S6=Exception). Target: PC_9."""
        seed_state = MagicMock()
        seed_state.current_track.path = "/music/song.mp3"
        seed_state.position_seconds = 30.0

        # Inject Symbolic Constraint S6 failure
        self.mock_json_dump.side_effect = Exception("System Fault")

        save_resume_state(seed_state)
        self.mock_print.assert_called_with("[state] Unexpected error saving state: System Fault")


if __name__ == '__main__':
    unittest.main()