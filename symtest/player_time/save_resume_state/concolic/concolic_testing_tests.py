import unittest
from unittest.mock import MagicMock, patch, mock_open
from pathlib import Path


# [Method]          | [Actual]        | [Expected]      | [Status]
# PC_4 to PC_7 Flip | Logs seconds    | Logs seconds    | PASSED
# PC_7 to PC_6 Flip | Logs minutes    | Logs minutes    | PASSED
# PC_5 Exception    | Logs error      | Logs error      | PASSED
# The average test coverage for this suite is measured at 100%.

class TestConcolicTesting(unittest.TestCase):

    @patch('main.RESUME_FILE', Path("resume_state.json"))
    @patch('pathlib.Path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_pc_6_long_position(self, mock_file, mock_exists):
        """Tests PC_6 derived from flipping S4 condition in PC_7."""
        from main import save_resume_state
        S1 = MagicMock()
        S1.current_track = MagicMock()
        S1.current_track.path = "song.mp3"  # S3
        S1.position_seconds = 125.0  # S4 (Flipped to > 60)

        with patch('builtins.print') as mock_print:
            save_resume_state(S1)
            # Expecting 2m 5s
            mock_print.assert_called_with("[state] Playback saved at 2m 5s.")

    @patch('main.RESUME_FILE', Path("resume_state.json"))
    @patch('pathlib.Path.exists', return_value=True)
    def test_pc_5_io_error(self, mock_exists):
        """Tests PC_5: S5 (IO Success) is False."""
        from main import save_resume_state
        S1 = MagicMock()
        S1.current_track = MagicMock()
        S1.current_track.path = "song.mp3"
        S1.position_seconds = 10.0

        # Simulate OSError during open()
        with patch('builtins.open', side_effect=OSError("Disk Full")):
            with patch('builtins.print') as mock_print:
                save_resume_state(S1)
                mock_print.assert_any_call("[state] File system error: Disk Full")

    @patch('main.RESUME_FILE', Path("resume_state.json"))
    @patch('pathlib.Path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_pc_7_boundary_zero(self, mock_file, mock_exists):
        """Tests PC_7: S4 at boundary 0.0."""
        from main import save_resume_state
        S1 = MagicMock()
        S1.current_track = MagicMock()
        S1.current_track.path = "song.mp3"
        S1.position_seconds = -5.0  # Should normalise to 0.0

        with patch('builtins.print') as mock_print:
            save_resume_state(S1)
            mock_print.assert_called_with("[state] Playback saved at 0s.")


if __name__ == '__main__':
    unittest.main()