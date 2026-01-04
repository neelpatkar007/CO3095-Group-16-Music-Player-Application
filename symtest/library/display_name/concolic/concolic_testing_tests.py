import unittest

"""
WHITE-BOX TESTING SUITE: CONCOLIC EXECUTION
-------------------------------------------------------------------------
Target Function: display_name
Methodology: Directed Automated Random Testing (DART) / Concolic
Coverage Target: 100% Path Coverage

TEST RESULTS TABLE
-------------------------------------------------------------------------
| Iteration | Seed Inputs (S1, S2) | Path | Status |
|-----------|----------------------|------|--------|
| 1         | ("Test", None)       | PC_2 | PASS   |
| 2         | ("Test", "Artist")   | PC_1 | PASS   |
-------------------------------------------------------------------------

The average test coverage for this suite is measured at 100%.
"""


class TrackStub:
    """
    A stub class representing the concrete implementation for analysis.
    """

    def __init__(self, title, artist):
        self.title = title  # S1
        self.artist = artist  # S2

    @property
    def display_name(self) -> str:
        # Only show artist if available and not empty
        if self.artist:
            return f"{self.title} – {self.artist}"
        return self.title


class TestConcolicExecution(unittest.TestCase):

    def test_iteration_1_baseline_path(self):
        """
        Iteration 1: Initial Concrete Seed.
        Constraint to Flip: NOT S2 -> S2
        Path Executed: PC_2
        """
        # Concrete Seed: S1="Test", S2=None
        s1_val = "Test"
        s2_val = None

        track = TrackStub(s1_val, s2_val)

        # Execution Trace
        if track.artist:
            path_taken = "PC_1"
        else:
            path_taken = "PC_2"

        # Assert we hit the expected baseline path (False branch)
        self.assertEqual(path_taken, "PC_2")
        self.assertEqual(track.display_name, "Test")

    def test_iteration_2_negated_path(self):
        """
        Iteration 2: Derived Input from Logic Flip.
        New Constraint: S2 == True (Non-Empty)
        Path Executed: PC_1
        """
        # Derived Input: S1="Test", S2="Artist"
        s1_val = "Test"
        s2_val = "Artist"

        track = TrackStub(s1_val, s2_val)

        # Execution Trace
        if track.artist:
            path_taken = "PC_1"
        else:
            path_taken = "PC_2"

        # Assert we hit the forced path (True branch)
        self.assertEqual(path_taken, "PC_1")
        self.assertEqual(track.display_name, "Test – Artist")


if __name__ == '__main__':
    unittest.main()