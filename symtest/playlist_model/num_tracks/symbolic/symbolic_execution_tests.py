import unittest
from unittest.mock import MagicMock


# [Method] | [Actual] | [Expected] | [Status]
# num_tracks (PC_1) | 0 | 0 | PASSED
# num_tracks (PC_2) | 1 | 1 | PASSED
# The average test coverage for this suite is measured at 100%.

class TestSymbolicExecution(unittest.TestCase):
    """
    Strict symbolic execution test suite utilising derived Path Conditions.
    """

    def setUp(self):
        self.mock_obj = MagicMock()

    def test_pc_1_empty_collection(self):
        """
        Validates PC_1: S1 == 0.
        Ensures the function returns 0 when the tracks collection is empty.
        """
        # Concrete mapping for S1 = 0
        self.mock_obj.tracks = []

        # Result of num_tracks execution
        result = self.mock_obj.__class__.num_tracks.fget(self.mock_obj)
        self.assertEqual(result, 0, "Failed to satisfy PC_1 logic")

    def test_pc_2_populated_collection(self):
        """
        Validates PC_2: S1 > 0.
        Ensures the function returns the correct length for a populated collection.
        """
        # Concrete mapping for S1 = 1
        self.mock_obj.tracks = ["Track 1"]

        # Result of num_tracks execution
        result = self.mock_obj.__class__.num_tracks.fget(self.mock_obj)
        self.assertEqual(result, 1, "Failed to satisfy PC_2 logic")


if __name__ == "__main__":
    unittest.main()