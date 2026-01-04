import unittest
from unittest.mock import MagicMock
import io
import sys
from music_player.player_state import PlayerState
from music_player.player_audio import change_volume

class TestConcolicDriven(unittest.TestCase):

    def setUp(self):
        self.held_output = io.StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_iteration_1_null_state(self):
        # Derived from Flip Table Iteration 1
        S1 = None
        S2 = "50"
        change_volume(S1, S2)
        self.assertEqual(self.held_output.getvalue(), "")

    def test_iteration_2_missing_structure(self):
        # Derived from Flip Table Iteration 2
        # Negating: S1 is None -> S1 is Object (but missing attributes)
        class EmptyState: pass

        S1 = EmptyState()
        S2 = "50"
        change_volume(S1, S2)
        self.assertEqual(self.held_output.getvalue(), "")

    def test_iteration_3_empty_input(self):
        # Derived from Flip Table Iteration 3
        # Negating: hasattr -> True, but S2 is empty
        class State:
            volume = 30
            audio_engine = None

        S1 = State()
        S2 = ""
        change_volume(S1, S2)
        self.assertIn("Current Volume: 30%", self.held_output.getvalue())

    def test_iteration_4_invalid_type_structure(self):
        # Derived from Flip Table Iteration 4
        # Negating: S2 is empty -> S2 is list (invalid type)
        class State:
            volume = 30
            audio_engine = None

        S1 = State()
        S2 = ["invalid"]
        change_volume(S1, S2)
        self.assertEqual(self.held_output.getvalue(), "")

    def test_iteration_5_conversion_error(self):
        # Derived from Flip Table Iteration 5
        # Negating: Type check -> Valid type, but non-numeric content
        class State:
            volume = 30
            audio_engine = None

        S1 = State()
        S2 = "NotANumber"
        change_volume(S1, S2)
        self.assertIn("Error: Volume must be a number", self.held_output.getvalue())

    def test_iteration_6_boundary_violation(self):
        # Derived from Flip Table Iteration 6
        # Negating: int(S2) throws -> int(S2) works, but out of bounds
        class State:
            volume = 30
            audio_engine = None

        S1 = State()
        S2 = "-10"  # Lower bound violation
        change_volume(S1, S2)
        self.assertIn("Error: Volume must be between 0 and 100", self.held_output.getvalue())

    def test_iteration_7_deep_state_mutation(self):
        # Derived from Flip Table Iteration 7
        # Negating: Range check -> Valid range, exploring is_muted path
        mock_eng = MagicMock()

        class State:
            volume = 30
            audio_engine = mock_eng
            is_muted = True  # Forces PC_7
            saved_volume = 30

        S1 = State()
        S2 = "75"
        change_volume(S1, S2)

        # Validation of the deep path execution
        self.assertEqual(S1.is_muted, False)
        self.assertIn("Volume set to 75%", self.held_output.getvalue())

    def test_iteration_8_standard_success(self):
        # Derived from Flip Table Iteration 8
        # Negating: is_muted True -> is_muted False (Standard PC_8)
        mock_eng = MagicMock()

        class State:
            volume = 30
            audio_engine = mock_eng
            is_muted = False  # Forces PC_8
            saved_volume = None

        S1 = State()
        S2 = "25"
        change_volume(S1, S2)

        # Validation that unmute logic was SKIPPED but volume was set
        mock_eng.set_muted.assert_not_called()
        mock_eng.set_volume.assert_called_with(25)
        self.assertIn("Volume set to 25%", self.held_output.getvalue())


if __name__ == '__main__':
    unittest.main()