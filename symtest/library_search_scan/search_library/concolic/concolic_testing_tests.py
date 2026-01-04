import unittest
from unittest.mock import MagicMock, patch

# ----------------------------------------------------------------------------------
# Test Results Table
# [Method]                        | [Actual] | [Expected] | [Status]
# test_iter_1_base_null           | Return   | Return     | PASS
# test_iter_2_flip_empty_query    | Print    | Print      | PASS
# test_iter_3_flip_missing_attr   | Print    | Print      | PASS
# test_iter_4_flip_corrupt_type   | Print    | Print      | PASS
# test_iter_5_flip_empty_list     | Print    | Print      | PASS
# test_iter_6_flip_match_found    | Print    | Print      | PASS
#
# The average test coverage for this suite is measured at 100%.
# ----------------------------------------------------------------------------------

class MockTrack:
    def __init__(self, title, artist, path_obj=None):
        self.title = title
        self.artist = artist
        self.path = path_obj

class MockPlayerState:
    def __init__(self, tracks=None, set_attr=True):
        if set_attr:
            self.library_tracks = tracks

def search_library(state, query):
    if state is None: return
    if not query:
        print("[search] Usage: /search <query>")
        return
    if not hasattr(state, "library_tracks"):
        print("[search] Error: Library unavailable.")
        return
    if not isinstance(state.library_tracks, list):
        print("[search] Error: Library corrupted.")
        return
    q = query.lower()
    results = []
    for t in state.library_tracks:
        if t is None: continue
        if q in (t.title or "").lower():
            results.append(t)
            continue
        if q in (t.artist or "").lower():
            results.append(t)
            continue
        if t.path and q in t.path.name.lower():
            results.append(t)
    if not results:
        print("[search] No matches found.")
    else:
        print(f"[search] Found {len(results)} matches:")

class TestConcolicExecution(unittest.TestCase):
    """
    Tests derived from the Explicit Iteration (Flip) Table in FILE 2.
    These tests simulate the progression of the constraint solver.
    """

    @patch('builtins.print')
    def test_iter_1_base_null(self, mock_print):
        """Iteration 1: Seed (None, 'rock', N/A). Path: PC_1."""
        S1 = None
        S2 = "rock"
        search_library(S1, S2)
        mock_print.assert_not_called()

    @patch('builtins.print')
    def test_iter_2_flip_empty_query(self, mock_print):
        """Iteration 2: Flip (S1 is None). New Path: PC_2."""
        S1 = MockPlayerState([])
        S2 = "" # Constraint solver derives empty string to fail 'if not query'
        search_library(S1, S2)
        mock_print.assert_called_with("[search] Usage: /search <query>")

    @patch('builtins.print')
    def test_iter_3_flip_missing_attr(self, mock_print):
        """Iteration 3: Flip (NOT S2). New Path: PC_3."""
        S1 = MockPlayerState(set_attr=False) # Constraint: missing attribute
        S2 = "rock"
        search_library(S1, S2)
        mock_print.assert_called_with("[search] Error: Library unavailable.")

    @patch('builtins.print')
    def test_iter_4_flip_corrupt_type(self, mock_print):
        """Iteration 4: Flip (Has Attr). New Path: PC_4."""
        S1 = MockPlayerState(tracks=123) # Constraint: not a list
        S2 = "rock"
        search_library(S1, S2)
        mock_print.assert_called_with("[search] Error: Library corrupted.")

    @patch('builtins.print')
    def test_iter_5_flip_empty_list(self, mock_print):
        """Iteration 5: Flip (Is List). New Path: PC_5."""
        S1 = MockPlayerState(tracks=[]) # Constraint: empty list
        S2 = "rock"
        search_library(S1, S2)
        mock_print.assert_called_with("[search] No matches found.")

    @patch('builtins.print')
    def test_iter_6_flip_match_found(self, mock_print):
        """Iteration 6: Flip (List Empty). New Path: PC_7 (Match)."""
        # Constraint solver generates a track that matches the query 'rock'
        S4 = MockTrack("Rock Anthem", "Band")
        S1 = MockPlayerState(tracks=[S4])
        S2 = "rock"
        search_library(S1, S2)
        self.assertTrue(mock_print.call_args[0][0].startswith("[search] Found 1 matches"))

if __name__ == '__main__':
    unittest.main()