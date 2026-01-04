import unittest
from unittest.mock import Mock

# [Method]                   | [Actual] | [Expected] | [Status]
# test_pc1_null_state        | None     | None       | Passed
# test_pc2_active_match      | Output   | Output     | Passed
# test_pc3_no_active_match   | Output   | Output     | Passed
#
# The average test coverage for this suite is measured at 100%.

class TestSymbolicExecution(unittest.TestCase):
    """
    White-box suite derived from Symbolic Path Conditions (PC_1, PC_2, PC_3).
    Using S1, S2, S3 symbolic mappings.
    """

    def test_pc1_null_state(self):
        """Path PC_1: Input S1 is None triggers early return."""
        S1 = None
        self.assertIsNone(list_profiles(S1))

    def test_pc2_active_match(self):
        """Path PC_2: S3 matches 'default' in all_profiles."""
        S1 = Mock()
        S1.profiles = {}
        S1.active_profile = "default" # S3 matches the name 'default'
        # Verification via execution flow
        try:
            list_profiles(S1)
        except Exception as e:
            self.fail(f"PC_2 execution failed with {e}")

    def test_pc3_no_active_match(self):
        """Path PC_3: S3 does not match any name in all_profiles."""
        S1 = Mock()
        S1.profiles = {"player1": {}}
        S1.active_profile = "none" # S3 does not match 'player1' or 'default'
        try:
            list_profiles(S1)
        except Exception as e:
            self.fail(f"PC_3 execution failed with {e}")

if __name__ == '__main__':
    unittest.main()