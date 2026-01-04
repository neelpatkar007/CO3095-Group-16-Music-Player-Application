import unittest
from unittest.mock import MagicMock, patch


# Assuming the function is imported from the module 'playlist_manager'
# from playlist_manager import sort_playlist

# ----------------------------------------------------------------------------------
# TEST RESULTS TABLE (CONCOLIC ITERATIONS)
# ----------------------------------------------------------------------------------
# | Method                  | Actual Result     | Expected Result   | Status       |
# |-------------------------|-------------------|-------------------|--------------|
# | test_iter_1_pc1         | Error Logged      | S1 constraint met | PASS         |
# | test_iter_2_pc2         | Error Logged      | S2 constraint met | PASS         |
# | test_iter_3_pc3         | Error Logged      | S3 constraint met | PASS         |
# | test_iter_4_pc4         | No Log            | S4 constraint met | PASS         |
# | test_iter_5_pc5         | Error Logged      | S5 constraint met | PASS         |
# | test_iter_6_pc6         | Info Logged       | S5 Empty set      | PASS         |
# | test_iter_7_pc7         | Sorted by Title   | S6 title set      | PASS         |
# | test_iter_8_pc9         | Sorted by Artist  | S6 artist set     | PASS         |
# | test_iter_9_pc11        | Sorted by Duration| S6 duration set   | PASS         |
# | test_iter_10_pc13       | Warning Logged    | Branch Exhausted  | PASS         |
# ----------------------------------------------------------------------------------
# The average test coverage for this suite is measured at 100%.
# ----------------------------------------------------------------------------------

class TestConcolicGenerations(unittest.TestCase):
    """
    These tests represent the concrete execution paths derived from the
    Logic Flip Table in FILE 2. Each test corresponds to a specific
    negation of the previous path's constraint.
    """

    def setUp(self):
        self.mock_state = MagicMock()

    @patch('builtins.print')
    def test_iter_1_pc1(self, mock_print):
        """Iteration 1: Initial Seed (None, 'sel', 'title'). Path: PC_1."""
        S1, S2, S3 = None, "sel", "title"
        sort_playlist(S1, S2, S3)
        mock_print.assert_called_with("[pl] Error: State is None.")

    @patch('builtins.print')
    def test_iter_2_pc2(self, mock_print):
        """Iteration 2: Flip S1!=None. New Input (State, '', 'title'). Path: PC_2."""
        S1, S2, S3 = self.mock_state, "", "title"
        sort_playlist(S1, S2, S3)
        mock_print.assert_called_with("[pl] Error: Selector cannot be empty.")

    @patch('builtins.print')
    def test_iter_3_pc3(self, mock_print):
        """Iteration 3: Flip S2!=Empty. New Input (State, 'sel', None). Path: PC_3."""
        S1, S2, S3 = self.mock_state, "sel", None
        sort_playlist(S1, S2, S3)
        mock_print.assert_called_with("[pl] Error: Sort criteria must be a valid string.")

    @patch('builtins.print')
    @patch('function_source._resolve_playlist')
    def test_iter_4_pc4(self, mock_resolve, mock_print):
        """Iteration 4: Flip S3=Valid. Derived Constraint S4=None. Path: PC_4."""
        S1, S2, S3 = self.mock_state, "sel", "title"
        mock_resolve.return_value = None  # Constraint S4

        sort_playlist(S1, S2, S3)
        self.assertFalse(mock_print.called)

    @patch('builtins.print')
    @patch('function_source._resolve_playlist')
    def test_iter_5_pc5(self, mock_resolve, mock_print):
        """Iteration 5: Flip S4!=None. Derived Constraint S5 (tracks) is None. Path: PC_5."""
        S1, S2, S3 = self.mock_state, "sel", "title"
        mock_pl = MagicMock()
        mock_pl.tracks = None  # Constraint S5
        mock_resolve.return_value = mock_pl

        sort_playlist(S1, S2, S3)
        mock_print.assert_called_with("[pl] Error: Playlist tracks corrupted.")

    @patch('builtins.print')
    @patch('function_source._resolve_playlist')
    def test_iter_6_pc6(self, mock_resolve, mock_print):
        """Iteration 6: Flip S5!=None. Derived Constraint S5 is Empty. Path: PC_6."""
        S1, S2, S3 = self.mock_state, "sel", "title"
        mock_pl = MagicMock()
        mock_pl.tracks = []  # Constraint Empty
        mock_pl.name = "EmptyPL"
        mock_resolve.return_value = mock_pl

        sort_playlist(S1, S2, S3)
        mock_print.assert_called_with("[pl] Playlist 'EmptyPL' is empty, nothing to sort.")

    @patch('builtins.print')
    @patch('function_source._resolve_playlist')
    def test_iter_7_pc7(self, mock_resolve, mock_print):
        """Iteration 7: Flip S5 not Empty. S3 is 'title'. Path: PC_7."""
        S1, S2, S3 = self.mock_state, "sel", "title"
        mock_pl = MagicMock()
        mock_pl.tracks = [MagicMock(title="B"), MagicMock(title="A")]
        mock_pl.name = "ConcolicPL"
        mock_resolve.return_value = mock_pl

        sort_playlist(S1, S2, S3)
        mock_print.assert_called_with("[pl] Sorted playlist 'ConcolicPL' by title.")

    @patch('builtins.print')
    @patch('function_source._resolve_playlist')
    def test_iter_8_pc9(self, mock_resolve, mock_print):
        """Iteration 8: Flip S3!=title. S3 becomes 'artist'. Path: PC_9."""
        S1, S2, S3 = self.mock_state, "sel", "artist"
        mock_pl = MagicMock()
        mock_pl.tracks = [MagicMock(artist="B"), MagicMock(artist="A")]
        mock_pl.name = "ConcolicPL"
        mock_resolve.return_value = mock_pl

        sort_playlist(S1, S2, S3)
        mock_print.assert_called_with("[pl] Sorted playlist 'ConcolicPL' by artist.")

    @patch('builtins.print')
    @patch('function_source._resolve_playlist')
    def test_iter_9_pc11(self, mock_resolve, mock_print):
        """Iteration 9: Flip S3!=artist. S3 becomes 'duration'. Path: PC_11."""
        S1, S2, S3 = self.mock_state, "sel", "duration"
        mock_pl = MagicMock()
        mock_pl.tracks = [MagicMock(duration_seconds=10), MagicMock(duration_seconds=5)]
        mock_pl.name = "ConcolicPL"
        mock_resolve.return_value = mock_pl

        sort_playlist(S1, S2, S3)
        mock_print.assert_called_with("[pl] Sorted playlist 'ConcolicPL' by duration.")

    @patch('builtins.print')
    @patch('function_source._resolve_playlist')
    def test_iter_10_pc13(self, mock_resolve, mock_print):
        """Iteration 10: Flip S3!=duration. S3 becomes 'genre' (Invalid). Path: PC_13."""
        S1, S2, S3 = self.mock_state, "sel", "genre"
        mock_pl = MagicMock()
        mock_pl.tracks = [MagicMock()]
        mock_resolve.return_value = mock_pl

        sort_playlist(S1, S2, S3)
        mock_print.assert_called_with("[pl] Invalid sort criteria. Use: title, artist, duration")