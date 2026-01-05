import unittest
from unittest.mock import MagicMock, patch
from music_player.playlists_advanced import copy_playlist


class TestConcolicTesting(unittest.TestCase):

    def test_iteration_2_reserved(self):
        copy_playlist(None, "any", "help")

    def test_iteration_8_isalnum(self):
        state = MagicMock()
        state.playlists = [MagicMock()]
        copy_playlist(state, "any", "My Playlist!")

    def test_iteration_11_conflict(self):
        pl_existing = MagicMock()
        pl_existing.name = "Gym"
        state = MagicMock()
        state.playlists = [pl_existing]

        with patch('music_player.playlists_advanced._get_playlist', return_value=pl_existing):
            copy_playlist(state, "Gym", "Gym")


if __name__ == "__main__":
    unittest.main()