import unittest
from unittest.mock import MagicMock, patch
from music_player.playlists_advanced import copy_playlist


class TestSymbolicExecution(unittest.TestCase):
    def setUp(self):
        self.state = MagicMock()
        self.state.playlists = []

    def test_pc1_type_error(self):
        copy_playlist(self.state, "src", 123)

    def test_pc6_length_min(self):
        self.state.playlists = [MagicMock()]
        copy_playlist(self.state, "src", "Ab")

    def test_pc12_success(self):
        source_mock = MagicMock()
        source_mock.name = "rock"
        source_mock.tracks = [1, 2]

        self.state.playlists = [source_mock]

        with patch('music_player.playlists_advanced._get_playlist', return_value=source_mock):
            copy_playlist(self.state, "rock", "Workout")
            self.assertEqual(len(self.state.playlists), 2)


if __name__ == "__main__":
    unittest.main()