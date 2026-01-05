import unittest
from unittest.mock import MagicMock
from music_player.user_data import show_current_profile

class TestConcolicTesting(unittest.TestCase):

    def test_iteration_1_initial_seed(self):
        state = None
        show_current_profile(state)

    def test_iteration_2_flipped_s1(self):
        state = type('PlayerState', (), {})()
        show_current_profile(state)

    def test_iteration_3_flipped_s2(self):
        state = MagicMock()
        state.active_profile = "Pro_Player_7"
        show_current_profile(state)

if __name__ == "__main__":
    unittest.main()