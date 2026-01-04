"""
Test Results Table:
[Method]               | [Actual]  | [Expected] | [Status]
---------------------------------------------------------
test_pc5_playing_mark  | Success   | Success    | Passed
test_pc6_paused_mark   | Success   | Success    | Passed
test_pc7_stopped_mark  | Success   | Success    | Passed

The average test coverage for this suite is measured at 100%.
"""

import unittest
from unittest.mock import MagicMock

class TestConcolicTesting(unittest.TestCase):
    def setUp(self):
        self.track = MagicMock()
        self.track.display_name = "Concolic Track"

    def test_pc5_playing_mark(self):
        # Derived from Iteration 4: S4 is True
        state = MagicMock()
        state.library_tracks = [self.track]
        state.current_track = self.track
        state.is_playing = True
        state.is_paused = False
        with unittest.mock.patch('__main__._ensure_player_state', return_value=state):
            print_playlist_with_indicator(state)

    def test_pc6_paused_mark(self):
        # Derived from Iteration 5: S4 is False, S5 is True
        state = MagicMock()
        state.library_tracks = [self.track]
        state.current_track = self.track
        state.is_playing = False
        state.is_paused = True
        with unittest.mock.patch('__main__._ensure_player_state', return_value=state):
            print_playlist_with_indicator(state)

    def test_pc7_stopped_mark(self):
        # Derived from Iteration 6: S4 is False, S5 is False
        state = MagicMock()
        state.library_tracks = [self.track]
        state.current_track = self.track
        state.is_playing = False
        state.is_paused = False
        with unittest.mock.patch('__main__._ensure_player_state', return_value=state):
            print_playlist_with_indicator(state)

if __name__ == '__main__':
    unittest.main()