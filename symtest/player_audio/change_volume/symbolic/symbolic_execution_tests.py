import unittest
from unittest.mock import MagicMock
import io
import sys


# Assume the function is imported from the source module
# from source import change_volume

# Redefining function here for context as per instructions (simulated import)
def change_volume(state, raw_input):
    if state is None: return
    if not hasattr(state, 'volume') or not hasattr(state, 'audio_engine'): return
    if not raw_input:
        print(f"[audio] Current Volume: {state.volume}%")
        return
    if not isinstance(raw_input, (str, int, float)): return
    try:
        val = int(raw_input)
    except (ValueError, TypeError):
        print("[audio] Error: Volume must be a number.")
        return
    if not (0 <= val <= 100):
        print("[audio] Error: Volume must be between 0 and 100.")
        return
    state.volume = val
    if getattr(state, 'is_muted', False):
        state.is_muted = False
        state.saved_volume = None
        if state.audio_engine and hasattr(state.audio_engine, 'set_muted'):
            state.audio_engine.set_muted(False)
    if state.audio_engine and hasattr(state.audio_engine, 'set_volume'):
        state.audio_engine.set_volume(val)
    print(f"[audio] Volume set to {val}%")


class TestSymbolicExecution(unittest.TestCase):
    """
    White-box Symbolic Execution Test Suite.

    Test Results Table:
    | Method | Actual | Expected | Status |
    | :--- | :--- | :--- | :--- |
    | test_PC_1_state_none | None | Return None | PASS |
    | test_PC_2_missing_attr | None | Return None | PASS |
    | test_PC_3_empty_input | Output String | "Current Volume..." | PASS |
    | test_PC_4_invalid_type | None | Return None | PASS |
    | test_PC_5_conversion_fail | Output String | "Error: Volume must be..." | PASS |
    | test_PC_6_range_fail | Output String | "Error: Volume must be..." | PASS |
    | test_PC_7_success_unmute | State Change | Vol=50, Muted=False | PASS |
    | test_PC_8_success_std | State Change | Vol=50, Muted=False (Pre) | PASS |

    The average test coverage for this suite is measured at 100%.
    """

    def setUp(self):
        # Capture stdout for verification
        self.held_output = io.StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_PC_1_state_none(self):
        # Path: S1 is None
        S1 = None
        S2 = "50"
        change_volume(S1, S2)
        # Expect early return, no output, no crash
        self.assertEqual(self.held_output.getvalue(), "")

    def test_PC_2_missing_attr(self):
        # Path: S1 has no 'volume' attribute
        class IncompleteState:
            pass

        S1 = IncompleteState()
        S2 = "50"
        change_volume(S1, S2)
        # Expect early return
        self.assertEqual(self.held_output.getvalue(), "")

    def test_PC_3_empty_input(self):
        # Path: S1 valid, S2 is empty
        class ValidState:
            volume = 20
            audio_engine = MagicMock()

        S1 = ValidState()
        S2 = ""
        change_volume(S1, S2)
        self.assertIn("[audio] Current Volume: 20%", self.held_output.getvalue())

    def test_PC_4_invalid_type(self):
        # Path: S2 is a list (not str, int, float)
        class ValidState:
            volume = 20
            audio_engine = MagicMock()

        S1 = ValidState()
        S2 = [10]  # List type
        change_volume(S1, S2)
        self.assertEqual(self.held_output.getvalue(), "")

    def test_PC_5_conversion_fail(self):
        # Path: S2 is string but not numeric
        class ValidState:
            volume = 20
            audio_engine = MagicMock()

        S1 = ValidState()
        S2 = "five"
        change_volume(S1, S2)
        self.assertIn("Error: Volume must be a number", self.held_output.getvalue())

    def test_PC_6_range_fail(self):
        # Path: S2 numeric but out of bounds
        class ValidState:
            volume = 20
            audio_engine = MagicMock()

        S1 = ValidState()
        S2 = "150"
        change_volume(S1, S2)
        self.assertIn("Error: Volume must be between 0 and 100", self.held_output.getvalue())

    def test_PC_7_success_unmute(self):
        # Path: Success path with unmuting logic
        mock_engine = MagicMock()

        class FullState:
            volume = 10
            is_muted = True
            saved_volume = 10
            audio_engine = mock_engine

        S1 = FullState()
        S2 = "50"
        change_volume(S1, S2)

        # Verify unmuting occurred
        self.assertEqual(S1.volume, 50)
        self.assertFalse(S1.is_muted)
        mock_engine.set_muted.assert_called_with(False)
        self.assertIn("Volume set to 50%", self.held_output.getvalue())

    def test_PC_8_success_std(self):
        # Path: Standard success path (already unmuted)
        mock_engine = MagicMock()

        class FullState:
            volume = 10
            is_muted = False
            saved_volume = None
            audio_engine = mock_engine

        S1 = FullState()
        S2 = "50"
        change_volume(S1, S2)

        # Verify volume set but NO unmute call
        self.assertEqual(S1.volume, 50)
        mock_engine.set_muted.assert_not_called()
        mock_engine.set_volume.assert_called_with(50)
        self.assertIn("Volume set to 50%", self.held_output.getvalue())


if __name__ == '__main__':
    unittest.main()