import unittest
from unittest.mock import MagicMock, patch
from music_player.playlists_basic import close_playlist


class TestSymbolicExecution(unittest.TestCase):


    def setUp(self):
        self.state = MagicMock()

    @patch("music_player.playlists_basic.player_core.stop")
    def test_pc1_missing_library_tracks(self, mock_stop):

        if hasattr(self.state, "library_tracks"):
            del self.state.library_tracks

        self.state.tracks = []

        close_playlist(self.state)

        mock_stop.assert_not_called()
        self.assertFalse("active_playlist_index" in self.state.__dict__)

    @patch("music_player.playlists_basic.player_core.stop")
    def test_pc2_already_in_main_library(self, mock_stop):

        library_ref = ["track1", "track2"]
        self.state.library_tracks = library_ref
        self.state.tracks = library_ref

        close_playlist(self.state)

        mock_stop.assert_not_called()
        self.assertIsNone(self.state.active_playlist_index)

    @patch("music_player.playlists_basic.player_core.stop")
    def test_pc3_successful_close(self, mock_stop):

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
