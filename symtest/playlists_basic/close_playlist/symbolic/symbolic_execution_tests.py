import unittest
from unittest.mock import MagicMock, patch
from music_player.playlists_basic import close_playlist


class TestSymbolicExecution(unittest.TestCase):
    """
    White-box testing suite based on Symbolic Analysis (FILE 1).
    Maps strictly to PC_1, PC_2, and PC_3.
    """

    def setUp(self):
        self.state = MagicMock()

    @patch("music_player.playlists_basic.player_core.stop")
    def test_pc1_missing_library_tracks(self, mock_stop):
        """
        Path Condition 1: NOT S1
        Scenario: The state object lacks the 'library_tracks' attribute.
        """
        # S1 is False
        if hasattr(self.state, "library_tracks"):
            del self.state.library_tracks

        # S2 exists but irrelevant
        self.state.tracks = []

        close_playlist(self.state)

        mock_stop.assert_not_called()
        # Attribute must not have been assigned
        self.assertFalse("active_playlist_index" in self.state.__dict__)

    @patch("music_player.playlists_basic.player_core.stop")
    def test_pc2_already_in_main_library(self, mock_stop):
        """
        Path Condition 2: S1 AND (S2 IS S3)
        Scenario: Current tracks are aliased with library_tracks.
        """
        library_ref = ["track1", "track2"]
        self.state.library_tracks = library_ref
        self.state.tracks = library_ref

        close_playlist(self.state)

        mock_stop.assert_not_called()
        self.assertIsNone(self.state.active_playlist_index)

    @patch("music_player.playlists_basic.player_core.stop")
    def test_pc3_successful_close(self, mock_stop):
        """
        Path Condition 3: S1 AND NOT (S2 IS S3)
        Scenario: Current tracks are different from library_tracks.
        """
        library_ref = ["track1", "track2"]
        current_ref = ["track3"]

        self.state.library_tracks = library_ref
        self.state.tracks = current_ref

        close_playlist(self.state)

        mock_stop.assert_called_once_with(self.state)
        self.assertIs(self.state.tracks, self.state.library_tracks)
        self.assertEqual(self.state.current_index, 0)
        self.assertEqual(self.state.position_seconds, 0.0)
        self.assertIsNone(self.state.active_playlist_index)


if __name__ == "__main__":
    unittest.main()
