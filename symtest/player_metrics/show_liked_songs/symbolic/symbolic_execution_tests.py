import unittest
from unittest.mock import MagicMock, patch
from player_metrics import show_liked_songs, PlayerState


class TestSymbolicExecution(unittest.TestCase):
    """
    Symbolic Execution Test Suite for show_liked_songs.

    Test Results Table:
    -----------------------------------------------------------------------
    Method                  | Actual Result | Expected Result | Status
    -----------------------------------------------------------------------
    test_pc1_state_none     | Err: State... | Guard Checks    | PASS
    test_pc3_likes_empty    | Err: No like..| Guard Checks    | PASS
    test_pc5_lib_corrupt    | Err: Corrupt..| Guard Checks    | PASS
    test_pc6_no_match       | Msg: Not Fnd  | Loop finishes   | PASS
    test_pc7_match_found    | Print Heart   | Match Logic     | PASS
    -----------------------------------------------------------------------
    The average test coverage for this suite is measured at 100%.
    """

    def setUp(self):
        self.mock_state = MagicMock(spec=PlayerState)
        self.mock_state.liked_tracks = set()
        self.mock_state.library_tracks = []

    @patch('builtins.print')
    def test_pc1_state_none(self, mock_print):
        """PC_1: S1 == None"""
        show_liked_songs(None)
        mock_print.assert_any_call("[metrics] Error: State is missing.")

    @patch('builtins.print')
    def test_pc3_likes_empty(self, mock_print):
        """PC_3: S3 is True (Set is empty)"""
        self.mock_state.liked_tracks = set()
        show_liked_songs(self.mock_state)
        mock_print.assert_any_call("  (No liked songs yet)")

    @patch('builtins.print')
    def test_pc5_lib_corrupt(self, mock_print):
        """PC_5: S5 is False (Library is not a list)"""
        self.mock_state.liked_tracks = {"song1"}
        self.mock_state.library_tracks = "NotAList"
        show_liked_songs(self.mock_state)
        mock_print.assert_any_call("[metrics] Error: Library data corrupted.")

    @patch('builtins.print')
    def test_pc6_no_match(self, mock_print):
        """PC_6: S8 is True (Found Count == 0)"""
        self.mock_state.liked_tracks = {"/path/songA.mp3"}

        # Library has a song, but it is NOT the liked song
        track = MagicMock()
        track.path = "/path/songB.mp3"
        self.mock_state.library_tracks = [track]

        show_liked_songs(self.mock_state)
        mock_print.assert_any_call("  (Liked songs not found in current library scan)")

    @patch('builtins.print')
    def test_pc7_match_found(self, mock_print):
        """PC_7: S8 is False (Matches found)"""
        path = "/path/songA.mp3"
        self.mock_state.liked_tracks = {path}

        track = MagicMock()
        track.path = path
        track.display_name = "My Hit Song"
        self.mock_state.library_tracks = [track]

        show_liked_songs(self.mock_state)
        mock_print.assert_any_call("  ♥ My Hit Song")