import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
from music_player import playlists_edit
from music_player.player_state import PlayerState
from music_player.playlist_model import Playlist
from music_player.library import Track


class TestPlaylistsEditSpec(unittest.TestCase):
    """
    Black-Box Specification-based Testing for playlists_edit.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: Category Partition Method
    Source: TSL Generated Test Cases playlistsEdit.txt.
    """

    def setUp(self):
        # Create Dummy Tracks
        self.t1 = Track(Path("a.mp3"), "Track A", "Artist A", 100)
        self.t2 = Track(Path("b.mp3"), "Track B", "Artist B", 200)
        self.t3 = Track(Path("c.mp3"), "Track C", "Artist C", 300)

        # Create Mock State
        self.mock_library = [self.t1, self.t2, self.t3]
        self.pl = Playlist("MyMix")
        self.pl.tracks = [self.t1, self.t2]  # [A, B]

        self.state = PlayerState(self.mock_library, MagicMock())
        self.state.playlists = [self.pl]

    # Error Cases

    def test_case_01_state_none(self):
        """
        Test Case 1: Player State : None
        Expected Result: Functions handle None state without crashing.
        Actual Result: Passed. Functions returned safely without runtime errors.
        """
        with patch("builtins.print") as mock_print:
            playlists_edit.add_track_from_library(None, "MyMix", "1")
            playlists_edit.remove_track_from_playlist(None, "MyMix", "1")
            playlists_edit.move_track_within_playlist(None, "MyMix", "1", "2")

    def test_case_02_playlist_invalid(self):
        """
        Test Case 2: Target Playlist Selector : Invalid/Missing
        Expected Result: Error message printed, no changes.
        Actual Result: Passed. Verified playlist length remained unchanged.
        """
        with patch("builtins.print") as mock_print:
            playlists_edit.add_track_from_library(self.state, "Ghost", "1")
            self.assertEqual(len(self.pl.tracks), 2)  # No change

    def test_case_03_library_empty(self):
        """
        Test Case 3: Main Library Content : Library Empty
        Expected Result: Cannot add track from empty library.
        Actual Result: Passed.
        """
        self.state.tracks = []  # Empty library
        with patch("builtins.print") as mock_print:
            playlists_edit.add_track_from_library(self.state, "MyMix", "1")
            mock_print.assert_called()

    def test_case_04_index1_garbage(self):
        """
        Test Case 4: Index 1 Input : Non-numeric
        Expected Result: Prints Usage message when input format is invalid.
        Actual Result: PASSED [100%].
        """
        with patch("builtins.print") as mock_print:
            playlists_edit.add_track_from_library(self.state, "MyMix", "abc")
            mock_print.assert_called_with("[pl] Usage: /pl.add <playlist> <library-index>")

    def test_case_05_index1_empty(self):
        """
        Test Case 5: Index 1 Input : Empty String
        Expected Result: Function returns or prints usage.
        Actual Result: PASSED [100%].
        """
        with patch("builtins.print") as mock_print:
            playlists_edit.add_track_from_library(self.state, "MyMix", "")
            mock_print.assert_not_called()

    def test_case_06_index1_zero_negative(self):
        """
        Test Case 6: Index 1 Input : Zero or Negative
        Expected Result: 0 or negative inputs trigger invalid index error.
        Actual Result: Passed.
        """
        with patch("builtins.print") as mock_print:
            playlists_edit.remove_track_from_playlist(self.state, "MyMix", "0")
            mock_print.assert_called()

    def test_case_07_index1_oob_high(self):
        """
        Test Case 7: Index 1 Input : Out of Bounds
        Expected Result: Error Library index out of range.
        Actual Result: Passed.
        """
        with patch("builtins.print") as mock_print:
            playlists_edit.add_track_from_library(self.state, "MyMix", "99")
            mock_print.assert_called_with("[pl] Library index out of range.")

    def test_case_08_move_same_index(self):
        """
        Test Case 8: Index 2 Input : Same as Index 1
        Expected Result: Playlist order remains identical.
        Actual Result: Passed. Track list matches original state.
        """
        original_tracks = list(self.pl.tracks)
        playlists_edit.move_track_within_playlist(self.state, "MyMix", "1", "1")
        self.assertEqual(self.pl.tracks, original_tracks)

    def test_case_09_move_dest_non_numeric(self):
        """
        Test Case 9: Index 2 Input : Non-numeric
        Expected Result: Error message printed.
        Actual Result: Passed.
        """
        with patch("builtins.print") as mock_print:
            playlists_edit.move_track_within_playlist(self.state, "MyMix", "1", "abc")
            mock_print.assert_called()

    def test_case_10_move_dest_oob(self):
        """
        Test Case 10: Index 2 Input : Out of Bounds
        Expected Result: Error Invalid source or destination index printed.
        Actual Result: Passed.
        """
        with patch("builtins.print") as mock_print:
            playlists_edit.move_track_within_playlist(self.state, "MyMix", "1", "99")
            mock_print.assert_called()

    def test_case_11_playlist_tracks_none(self):
        """
        Test Case 11: Playlist Tracks Integrity : Tracks list is None
        Expected Result: Should detect corruption and return safely without crash.
        Actual Result: Passed.
        """
        self.pl.tracks = None  # Corrupt
        with patch("builtins.print") as mock_print:
            # Add to a corrupted playlist
            playlists_edit.add_track_from_library(self.state, "MyMix", "1")

    # Valid Cases

    def test_case_12_add_valid(self):
        """
        Test Case 12: Add Track.
        Expected Result: Track is successfully added to the playlist.
        Actual Result: PASSED [100%][pl] Added 'Track C – Artist C' to playlist 'MyMix'.
        """
        # Add Track C
        playlists_edit.add_track_from_library(self.state, "MyMix", "3")
        self.assertIn(self.t3, self.pl.tracks)
        self.assertEqual(len(self.pl.tracks), 3)

    def test_case_13_14_remove_valid(self):
        """
        Test Case 13, 14: Remove Track.
        Expected Result: Track is successfully removed from the playlist.
        Actual Result: PASSED [100%][pl] Removed 'Track A – Artist A' from playlist 'MyMix'.
        """
        # Remove Track A
        playlists_edit.remove_track_from_playlist(self.state, "MyMix", "1")
        self.assertNotIn(self.t1, self.pl.tracks)
        self.assertEqual(len(self.pl.tracks), 1)  # Only B is left

    def test_case_15_16_move_valid(self):
        """
        Test Case 15, 16: Move Track.
        Expected Result: Track is moved from source index to destination index.
        Actual Result: PASSED [100%][pl] Moved 'Track A – Artist A' in playlist 'MyMix' from position 1 to 2.
        """
        # Move Track A to position 2
        # [A, B]
        playlists_edit.move_track_within_playlist(self.state, "MyMix", "1", "2")

        # Assert [B, A]
        self.assertEqual(self.pl.tracks[0], self.t2)
        self.assertEqual(self.pl.tracks[1], self.t1)