import unittest
from io import StringIO
import sys
from music_player.playlists_basic import _ensure_playlists

class PlayerState:
    pass

class TestConcolicExecution(unittest.TestCase):

    def setUp(self):
        self.captured_output = StringIO()
        sys.stdout = self.captured_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_iteration_1_base_case(self):
        """
        Iteration 1: Concrete Seed = None.
        Constraint: S1 == None.
        Path: PC_1.
        """
        # Concrete Seed Generation
        s1 = None

        _ensure_playlists(s1)

        # Assertion verifies we hit the error branch (PC_1)
        self.assertIn("[pl] Error", self.captured_output.getvalue())

    def test_iteration_2_negate_s1(self):
        """
        Iteration 2: Negate S1 -> S1 != None.
        Concrete Seed = Object (Empty).
        Constraint: NOT S2 (hasattr is False).
        Path: PC_2.
        """
        # New Derived Input from Iteration 1 flip
        s1 = PlayerState()
        # Explicitly ensuring S2 is False
        if hasattr(s1, 'playlists'):
            del s1.playlists

        _ensure_playlists(s1)

        # Assertion verifies we hit the error branch (PC_2)
        self.assertIn("[pl] Error", self.captured_output.getvalue())

    def test_iteration_3_negate_s2(self):
        """
        Iteration 3: Negate S2 -> S2 is True.
        Concrete Seed = Object (playlists=None).
        Constraint: S3 == None.
        Path: PC_3.
        """
        # New Derived Input from Iteration 2 flip
        s1 = PlayerState()
        s1.playlists = None  # S2 is True, S3 is None

        _ensure_playlists(s1)

        # Assertion verifies we hit the assignment branch (PC_3)
        self.assertEqual(s1.playlists, [])

    def test_iteration_4_negate_s3(self):
        """
        Iteration 4: Negate S3 -> S3 != None.
        Concrete Seed = Object (playlists=[Data]).
        Path: PC_4.
        """
        # New Derived Input from Iteration 3 flip
        s1 = PlayerState()
        s1.playlists = ["existing_data"]  # S3 is not None

        _ensure_playlists(s1)

        # Assertion verifies we hit the no-op branch (PC_4)
        self.assertEqual(s1.playlists, ["existing_data"])


if __name__ == '__main__':
    unittest.main()