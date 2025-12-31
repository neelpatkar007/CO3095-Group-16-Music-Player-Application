import unittest
from unittest.mock import MagicMock, patch
from music_player import playlists_edit
from music_player.player_state import PlayerState


class TestPlaylistsEditStatement(unittest.TestCase):
    """
    White-Box Statement Tests for playlists_edit.py.
    Tool: Python unittest + unittest.mock
    Technique: White-Box Statement Testing
    """

    def setUp(self):
        # Create Mock Track objects
        self.track_a = MagicMock()
        self.track_a.display_name = "Track A"

        self.track_b = MagicMock()
        self.track_b.display_name = "Track B"

        self.lib_track_1 = MagicMock()
        self.lib_track_1.display_name = "LibTrack1"

        self.mock_playlist = MagicMock()
        self.mock_playlist.name = "MyMix"
        # Populate with mock objects
        self.mock_playlist.tracks = [self.track_a, self.track_b]

        self.state = PlayerState([], MagicMock())
        self.state.playlists = [self.mock_playlist]
        # Populate library with mock objects
        self.state.tracks = [self.lib_track_1, self.track_b]

    def test_resolve_playlist_failure_statement(self):
        """
        Expected Result: The function returns None and prints an error message when a playlist is not found.
        Actual Result: Passed. Verified None return and error printed.
        """
        with patch("builtins.print") as mock_print:
            # Pass a name that doesn't exist
            res = playlists_edit._resolve_playlist(self.state, "ABCDEFG")
            self.assertIsNone(res)
            mock_print.assert_called()

    def test_add_success_statement(self):
        """
        Expected Result: The function prints a success message
        Actual Result: Passed. Verified success message printed.
        """
        with patch("builtins.print") as mock_print:
            playlists_edit.add_track_from_library(self.state, "MyMix", "1")
            args_list = mock_print.call_args[0]
            self.assertTrue(str(args_list[0]).startswith("[pl] Added"))

    def test_remove_internal_error_statements(self):
        """
        Expected Result: Internal exception handlers catch ValueError and IndexError printing appropriate error messages.
        Actual Result: Passed. Verified error messages printed for both exceptions.
        """
        # Force ValueError
        with patch("builtins.print") as mock_print:
            playlists_edit.remove_track_from_playlist(self.state, "MyMix", "abc")
            mock_print.assert_called()

        # Force IndexError
        with patch("builtins.print") as mock_print:
            playlists_edit.remove_track_from_playlist(self.state, "MyMix", "99")
            mock_print.assert_called()

    def test_move_internal_statements(self):
        """
        Expected Result:
          Invalid inputs trigger exception handlers/error prints.
          Valid inputs trigger the success message "[pl] Moved".
        Actual Result: Passed. Confirmed error prints for invalid inputs and success message for valid move.
        """
        # ValueError
        with patch("builtins.print") as mock_print:
            playlists_edit.move_track_within_playlist(self.state, "MyMix", "1", "abc")
            mock_print.assert_called()

        # Bounds Check Failure
        with patch("builtins.print") as mock_print:
            playlists_edit.move_track_within_playlist(self.state, "MyMix", "1", "99")
            mock_print.assert_called()

        # Success
        with patch("builtins.print") as mock_print:
            playlists_edit.move_track_within_playlist(self.state, "MyMix", "1", "2")
            # Verify success message
            args_list = mock_print.call_args[0]
            self.assertTrue(str(args_list[0]).startswith("[pl] Moved"))