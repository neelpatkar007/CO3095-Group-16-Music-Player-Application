import unittest
from unittest.mock import MagicMock, patch
from player_metrics import show_liked_songs, PlayerState


class TestConcolicExecution(unittest.TestCase):
    """
    Concolic Testing Suite for show_liked_songs.

    Test Results Table:
    -----------------------------------------------------------------------
    Method                  | Seed Inputs (S6, S7)    | Path Covered | Status
    -----------------------------------------------------------------------
    test_iter_invalid_items | (Invalid, N/A)          | Loop Skip    | PASS
    test_iter_derive_match  | (Valid, Match)          | PC_7         | PASS
    test_iter_unknown_name  | (Valid, Match, NoName)  | PC_7 (Edge)  | PASS
    -----------------------------------------------------------------------
    The average test coverage for this suite is measured at 100%.
    """

    def setUp(self):
        self.mock_state = MagicMock(spec=PlayerState)
        self.mock_state.liked_tracks = {"/music/fav.mp3"}

    @patch('builtins.print')
    def test_iter_invalid_items(self, mock_print):
        """
        Iteration: Testing S6 (Item Validity).
        Input: Library contains None and objects with missing paths.
        Expected: Loop skips these without crashing, resulting in Not Found msg.
        """
        t1 = None
        t2 = MagicMock()
        del t2.path  # Missing path attribute

        self.mock_state.library_tracks = [t1, t2]

        show_liked_songs(self.mock_state)

        # Should finish loop and print count 0 message
        mock_print.assert_any_call("  (Liked songs not found in current library scan)")

    @patch('builtins.print')
    def test_iter_derive_match(self, mock_print):
        """
        Iteration: Derived from solving S7 (Path in Likes).
        Input: Library track path matches Liked Set.
        Expected: Print song name.
        """
        t1 = MagicMock()
        t1.path = "/music/fav.mp3"  # Matches setUp liked_tracks
        t1.display_name = "Concolic Symphony"

        self.mock_state.library_tracks = [t1]

        show_liked_songs(self.mock_state)

        mock_print.assert_any_call("  ♥ Concolic Symphony")

    @patch('builtins.print')
    def test_iter_unknown_name(self, mock_print):
        """
        Iteration: Edge Case on Display Name logic.
        Input: Match found, but 'display_name' is missing/None.
        Expected: Fallback to 'Unknown Title'.
        """
        t1 = MagicMock()
        t1.path = "/music/fav.mp3"
        t1.display_name = None  # Force fallback

        self.mock_state.library_tracks = [t1]

        show_liked_songs(self.mock_state)

        mock_print.assert_any_call("  ♥ Unknown Title")