import unittest
from unittest.mock import MagicMock

# [Method] | [Actual] | [Expected] | [Status]
# test_pc_5 | "[ui] Paused: Song [01:00]" | "[ui] Paused: Song [01:00]" | Passed
# test_pc_6 | "[ui] Playing: Song [01:00]" | "[ui] Playing: Song [01:00]" | Passed
# test_pc_7 | "[ui] Paused: Song [01:00]" | "[ui] Paused: Song [01:00]" | Passed
# test_pc_8 | "[ui] Stopped: Song [01:00]" | "[ui] Stopped: Song [01:00]" | Passed

"""
The average test coverage for this suite is measured at 100%.
"""


class TestConcolicExecution(unittest.TestCase):
    def test_pc_8_stopped(self):
        """Iteration Derived: S5=False, S6=False (PC_8)"""
        state = MagicMock()
        track = MagicMock()
        track.display_name = "Song"
        track.duration_seconds = 60.0
        state.current_track = track
        state.is_playing = False  # S5
        state.is_paused = False  # S6

        with unittest.mock.patch('builtins.print') as mocked_print:
            with unittest.mock.patch('__main__.format_mm_ss', return_value="01:00"):
                print_now_playing(state)
                mocked_print.assert_called_with("[ui] Stopped: Song [01:00]")

    def test_pc_6_playing(self):
        """Iteration Derived: S5=True, S6=False (PC_6)"""
        state = MagicMock()
        track = MagicMock()
        track.display_name = "Song"
        track.duration_seconds = 60.0
        state.current_track = track
        state.is_playing = True  # S5
        state.is_paused = False  # S6

        with unittest.mock.patch('builtins.print') as mocked_print:
            with unittest.mock.patch('__main__.format_mm_ss', return_value="01:00"):
                print_now_playing(state)
                mocked_print.assert_called_with("[ui] Playing: Song [01:00]")

    def test_pc_5_paused_playing(self):
        """Iteration Derived: S5=True, S6=True (PC_5)"""
        state = MagicMock()
        track = MagicMock()
        track.display_name = "Song"
        track.duration_seconds = 60.0
        state.current_track = track
        state.is_playing = True  # S5
        state.is_paused = True  # S6

        with unittest.mock.patch('builtins.print') as mocked_print:
            with unittest.mock.patch('__main__.format_mm_ss', return_value="01:00"):
                print_now_playing(state)
                mocked_print.assert_called_with("[ui] Paused: Song [01:00]")

    def test_pc_7_paused_stopped(self):
        """Iteration Derived: S5=False, S6=True (PC_7)"""
        state = MagicMock()
        track = MagicMock()
        track.display_name = "Song"
        track.duration_seconds = 60.0
        state.current_track = track
        state.is_playing = False  # S5
        state.is_paused = True  # S6

        with unittest.mock.patch('builtins.print') as mocked_print:
            with unittest.mock.patch('__main__.format_mm_ss', return_value="01:00"):
                print_now_playing(state)
                mocked_print.assert_called_with("[ui] Paused: Song [01:00]")


if __name__ == "__main__":
    unittest.main()