import unittest
from unittest.mock import MagicMock, patch
from music_player.playlists_basic import close_playlist




class TestConcolicGeneration(unittest.TestCase):


    def setUp(self):
        self.state = MagicMock()

    @patch("music_player.playlists_basic.player_core.stop")
    def test_iter1_flip_constraint_s1(self, mock_stop):

        if hasattr(self.state, "library_tracks"):
            del self.state.library_tracks

        close_playlist(self.state)

        mock_stop.assert_not_called()

    @patch("music_player.playlists_basic.player_core.stop")
    def test_iter2_flip_constraint_identity(self, mock_stop):

        shared_list = [1, 2, 3]
        self.state.library_tracks = shared_list
        self.state.tracks = shared_list


        close_playlist(self.state)


        mock_stop.assert_not_called()
        self.assertIsNone(self.state.active_playlist_index)

    @patch("music_player.playlists_basic.player_core.stop")
    def test_iter3_path_exploration_success(self, mock_stop):


        self.state.library_tracks = [1, 2, 3]
        self.state.tracks = [4, 5, 6]


        close_playlist(self.state)


        mock_stop.assert_called_once()
        self.assertIs(self.state.tracks, self.state.library_tracks)


if __name__ == "__main__":
    unittest.main()
