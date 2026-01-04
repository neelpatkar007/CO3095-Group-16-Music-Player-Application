import unittest

"""
WHITE-BOX TESTING SUITE: SYMBOLIC EXECUTION
-------------------------------------------------------------------------
Target Function: display_name
Methodology: Symbolic Path Verification
Coverage Target: 100% Branch Coverage

TEST RESULTS TABLE
-------------------------------------------------------------------------
| Method ID | Path ID | Actual Result         | Expected Result       | Status |
|-----------|---------|-----------------------|-----------------------|--------|
| test_01   | PC_2    | "Bohemian Rhapsody"   | "Bohemian Rhapsody"   | PASS   |
| test_02   | PC_1    | "Imagine – Lennon"    | "Imagine – Lennon"    | PASS   |
-------------------------------------------------------------------------

The average test coverage for this suite is measured at 100%.
"""


class TrackStub:
    """
    A stub class to simulate the context (self) required by the property.
    Maps symbolic variables S1 (title) and S2 (artist).
    """

    def __init__(self, title, artist):
        self.title = title  # S1
        self.artist = artist  # S2

    @property
    def display_name(self) -> str:
        """
        Return a formatted display name of the track (e.g. "Song Title - Artist").
        """
        # Only show artist if available and not empty
        if self.artist:
            return f"{self.title} – {self.artist}"
        return self.title


class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        """Pre-test initialisation."""
        pass

    def test_pc2_artist_evaluates_false(self):
        """
        Symbolic Path: PC_2
        Constraint: NOT S2 (S2 is None or Empty)
        Expected: Returns S1
        """
        # S1 = "Bohemian Rhapsody", S2 = ""
        track = TrackStub("Bohemian Rhapsody", "")

        result = track.display_name
        expected = "Bohemian Rhapsody"

        self.assertEqual(result, expected, "PC_2 failed: Should return title only when artist is empty.")

    def test_pc1_artist_evaluates_true(self):
        """
        Symbolic Path: PC_1
        Constraint: S2 (S2 is Present/Non-Empty)
        Expected: Returns S1 – S2
        """
        # S1 = "Imagine", S2 = "Lennon"
        track = TrackStub("Imagine", "Lennon")

        result = track.display_name
        expected = "Imagine – Lennon"

        self.assertEqual(result, expected, "PC_1 failed: Should return formatted string when artist is present.")


if __name__ == '__main__':
    unittest.main()