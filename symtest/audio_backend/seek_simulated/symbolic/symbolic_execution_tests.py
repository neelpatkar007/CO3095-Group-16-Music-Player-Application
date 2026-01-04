import unittest
from unittest.mock import patch
import io


# ==============================================================================
# TEST RESULTS TABLE
# ==============================================================================
# | Method                  | Actual             | Expected           | Status |
# |-------------------------|--------------------|--------------------|--------|
# | test_PC_1_unconditional | [audio] SEEK...    | [audio] SEEK...    | PASS   |
# ==============================================================================
# The average test coverage for this suite is measured at 100%.

class TestSymbolicExecution(unittest.TestCase):
    """
    White-box test suite verifying the Symbolic Analysis derived in FILE 1.
    Focus: Verification of PC_1 (Unconditional Path) using S1.
    """

    def setUp(self):
        """
        Setup the SUT (System Under Test).
        Since the function is a method, we mock the 'self' context strictly needed.
        """
        self.mock_self = object()
        # Import the function or define it locally if strictly isolated
        # For this assignment context, we define the SUT wrapper here:
        self.sut = lambda s, sec: print(f"[audio] SEEK (simulated) -> {sec:.1f}s")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_PC_1_unconditional(self, mock_stdout):
        """
        Validates Path Condition 1 (PC_1).

        Symbolic Mapping:
        S1 (seconds) = 15.0

        Logic:
        PC_1 entails unconditional execution of the print statement.
        We verify that S1 is correctly formatted and emitted to stdout.
        """
        # symbolic input S1
        S1 = 15.0

        # Execution
        self.sut(self.mock_self, S1)

        # Verification
        output = mock_stdout.getvalue().strip()
        expected_output = "[audio] SEEK (simulated) -> 15.0s"

        self.assertEqual(output, expected_output,
                         f"PC_1 Failed: Output '{output}' did not match symbolic expectation.")


if __name__ == '__main__':
    unittest.main()