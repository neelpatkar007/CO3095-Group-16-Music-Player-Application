import unittest
from unittest.mock import MagicMock
from music_player.user_data import show_current_profile

class TestSymbolicExecution(unittest.TestCase):

    def test_path_pc_1_null_state(self):
        state = None
        try:
            show_current_profile(state)
        except Exception as e:
            self.fail(f"PC_1 execution failed with error: {e}")

    def test_path_pc_1_missing_attribute(self):
        state = MagicMock(spec=[])
        show_current_profile(state)

    def test_path_pc_2_valid_state(self):
        state = MagicMock()
        state.active_profile = "Default_User"
        show_current_profile(state)

if __name__ == "__main__":
    unittest.main()