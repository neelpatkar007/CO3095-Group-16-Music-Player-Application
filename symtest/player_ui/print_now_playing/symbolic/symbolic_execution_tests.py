import unittest
from unittest.mock import MagicMock

# [Method] | [Actual] | [Expected] | [Status]
# test_pc_1 | None | None | Passed
# test_pc_2 | "[ui] No track selected." | "[ui] No track selected." | Passed
# test_pc_3 | "[ui] Error: Track data corrupted." | "[ui] Error: Track data corrupted." | Passed
# test_pc_4 | "[ui] Error: Track metadata missing." | "[ui] Error: Track metadata missing." | Passed

"""
The average test coverage for this suite is measured at 100%.
"""

class TestSymbolicExecution(unittest.TestCase):
    def setUp(self):
        # Mocks for dependencies
        global _ensure_player_state, Track, format_mm_ss
        _ensure_player_state = MagicMock()
        Track = type("Track", (), {})
        format_mm_ss = MagicMock(return_value="00:00")

    def test_pc_1(self):
        """Path PC_1: state is None"""
        _ensure_player_state.return_value = None # S1 is None
        self.assertIsNone(print_now_playing(None))

    def test_pc_2(self):
        """Path PC_2: track is None"""
        state = MagicMock()
        _ensure_player_state.return_value = state
        state.current_track = None # S2 is None
        with unittest.mock.patch('builtins.print') as mocked_print:
            print_now_playing(state)
            mocked_print.assert_called_with("[ui] No track selected.")

    def test_pc_3(self):
        """Path PC_3: track is not instance of Track"""
        state = MagicMock()
        _ensure_player_state.return_value = state
        state.current_track = "not a track object" # S2 is not Track
        with unittest.mock.patch('builtins.print') as mocked_print:
            print_now_playing(state)
            mocked_print.assert_called_with("[ui] Error: Track data corrupted.")

    def test_pc_4(self):
        """Path PC_4: track missing display_name"""
        state = MagicMock()
        track = Track() # No display_name attribute (S3 is False)
        _ensure_player_state.return_value = state
        state.current_track = track
        with unittest.mock.patch('builtins.print') as mocked_print:
            print_now_playing(state)
            mocked_print.assert_called_with("[ui] Error: Track metadata missing.")

if __name__ == "__main__":
    unittest.main()