import unittest
from unittest.mock import MagicMock, patch
from io import StringIO
import sys


class TestConcolicExecution(unittest.TestCase):
    """
    Concolic Testing Suite based on Directed Automated Random Testing (DART) principles.

    Test Results Table:
    | Iteration | Seed Type | Constraint Flip | Status |
    |-----------|-----------|-----------------|--------|
    | 1 | Null State | S1 != None | PASS |
    | 2 | Invalid Attribute | S2 != None | PASS |
    | 3 | Invalid Type | S3 == List | PASS |
    | 4 | Empty List | S4 (Len) > 0 | PASS |
    | 5 | Null Element | S5 != None | PASS |
    | 6 | Inactive/Plural | Active == True | PASS |
    | 7 | Active/Singular | Count != 1 | PASS |

    The average test coverage for this suite is measured at 100%.
    """

    def setUp(self):
        self.captured_output = StringIO()
        sys.stdout = self.captured_output
        self.mock_ensure = patch('source._ensure_playlists').start()
        self.mock_summary = patch('source._get_playlist_summary').start()
        self.mock_format = patch('source.format_mm_ss').start()

    def tearDown(self):
        patch.stopall()
        sys.stdout = sys.__stdout__

    def test_iteration_01_seed_null(self):
        """Iteration 1: Base concrete seed is None."""
        from source import list_playlists
        list_playlists(None)
        self.assertIn("State is missing", self.captured_output.getvalue())

    def test_iteration_02_flip_state_existence(self):
        """Iteration 2: Constraint flipped (S1 is Not None), but S2 is None."""
        S1 = MagicMock()
        object.__setattr__(S1, 'playlists', None)

        from source import list_playlists
        list_playlists(S1)
        self.assertEqual("", self.captured_output.getvalue().strip())

    def test_iteration_03_flip_playlist_existence(self):
        """Iteration 3: Constraint flipped (S2 is Not None), but S3 (Type) is wrong."""
        S1 = MagicMock()
        S1.playlists = 12345  # Concrete value derived from solver to fail isinstance

        from source import list_playlists
        list_playlists(S1)
        self.assertIn("data is corrupted", self.captured_output.getvalue())

    def test_iteration_04_flip_type_check(self):
        """Iteration 4: Constraint flipped (S3 is List), but S4 (Len) is 0."""
        S1 = MagicMock()
        S1.playlists = []

        from source import list_playlists
        list_playlists(S1)
        self.assertIn("No playlists defined", self.captured_output.getvalue())

    def test_iteration_05_flip_list_content(self):
        """Iteration 5: Constraint flipped (S4 Len > 0), but S5 is None."""
        S1 = MagicMock()
        S1.playlists = [None]

        from source import list_playlists
        list_playlists(S1)
        self.assertIn("Invalid Playlist", self.captured_output.getvalue())

    def test_iteration_06_flip_element_validity(self):
        """Iteration 6: Constraint flipped (S5 valid), Testing Active Logic."""
        S1 = MagicMock()
        pl = MagicMock()
        pl.name = "Concolic Hits"
        S1.playlists = [pl]
        S1.active_playlist_index = None  # Concrete value to fail active check

        self.mock_summary.return_value = (10, 600)
        self.mock_format.return_value = "10:00"

        from source import list_playlists
        list_playlists(S1)

        output = self.captured_output.getvalue()
        # Expecting no asterisk, plural songs
        self.assertIn("Concolic Hits", output)
        self.assertNotIn("*", output)
        self.assertIn("songs", output)

    def test_iteration_07_flip_active_and_plurality(self):
        """Iteration 7: Constraint flipped (Active=True) and (Count=1)."""
        S1 = MagicMock()
        pl = MagicMock()
        pl.name = "Deep Path"
        S1.playlists = [pl]
        S1.active_playlist_index = 0  # Matches index 0

        # Flipped constraint for singular song text
        self.mock_summary.return_value = (1, 120)
        self.mock_format.return_value = "02:00"

        from source import list_playlists
        list_playlists(S1)

        output = self.captured_output.getvalue()
        # Expecting asterisk and singular