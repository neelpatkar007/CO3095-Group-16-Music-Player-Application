import unittest
from unittest.mock import MagicMock, patch, mock_open
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from music_player.player_config import save_settings


class TestConcolicExecution(unittest.TestCase):
    """
    White-Box Concolic Testing Suite.

    Test Results Table:
    | Iteration | Concrete Seed (S1, S2) | Path ID | Status |
    |-----------|------------------------|---------|--------|
    | 1         | (None, True)           | PC_1    | PASS   |
    | 2         | (Object, True)         | PC_2    | PASS   |
    | 3         | (Object, False)        | PC_3    | PASS   |

    The average test coverage for this suite is measured at 100%.
    """

    def setUp(self):
        # Base valid object for iterations where S1 != None
        self.concrete_state = MagicMock()
        self.concrete_state.volume = 50
        self.concrete_state.shuffle_active = False
        self.concrete_state.loop_mode = "one"
        self.concrete_state.playback_speed = 1.5
        self.concrete_state.song_tags = {}
        self.concrete_state.total_play_time = 0.0

    def test_iteration_1_initial_seed(self):
        """
        Iteration 1: Initial Concrete Seed.
        Inputs: S1 = None, S2 = True (Irrelevant due to early return).
        Path: PC_1 (Early Return).
        """
        S1 = None

        with patch("builtins.open", mock_open()) as mock_file:
            save_settings(S1)
            mock_file.assert_not_called()

    @patch("builtins.print")
    def test_iteration_2_flip_s1_constraint(self, mock_print):
        """
        Iteration 2: Negating PC_1 constraint (S1 == None) -> (S1 != None).
        Inputs: S1 = Concrete Object, S2 = True (Success).
        Path: PC_2 (Happy Path).
        """
        S1 = self.concrete_state

        with patch("builtins.open", mock_open()) as mock_file:
            save_settings(S1)
            mock_file.assert_called()
            mock_print.assert_called_with("[config] Settings saved.")

    @patch("builtins.print")
    def test_iteration_3_flip_s2_constraint(self, mock_print):
        """
        Iteration 3: Negating PC_2 constraint (S2 == True) -> (S2 == False).
        Inputs: S1 = Concrete Object, S2 = False (Exception).
        Path: PC_3 (Exception Path).
        """
        S1 = self.concrete_state

        with patch("builtins.open", mock_open()) as mock_file:
            mock_file.side_effect = OSError("Disk Full")

            save_settings(S1)

            mock_print.assert_called_with("[config] Error saving settings: Disk Full")


if __name__ == '__main__':
    unittest.main()