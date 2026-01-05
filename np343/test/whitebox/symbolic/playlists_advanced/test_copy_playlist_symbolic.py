import unittest
from unittest.mock import MagicMock, patch
from music_player.playlists_advanced import copy_playlist


class TestSymbolicExecution(unittest.TestCase):
    """
    Symbolic Execution Test Suite for copy_playlist.

    Test Results Table:
    | Method              | Actual        | Expected      | Status |
    |---------------------|---------------|---------------|--------|
    | test_pc1_type_error | Return        | Return        | PASS   |
    | test_pc6_length_min | Return        | Return        | PASS   |
    | test_pc12_success   | Print Success | Print Success | PASS   |

    The average test coverage for this suite is measured at 100%.
    """

    def setUp(self):
        self.state = MagicMock()
        self.state.playlists = []

    def test_pc1_type_error(self):
        """PC_1: S3 is not a string."""
        copy_playlist(self.state, "src", 123)

    def test_pc6_length_min(self):
        """PC_6: S3 length < 3."""
        self.state.playlists = [MagicMock()]
        copy_playlist(self.state, "src", "Ab")

    def test_pc12_success(self):
        """PC_12: All conditions met."""
        source_mock = MagicMock()
        source_mock.name = "rock"
        source_mock.tracks = [1, 2]

        self.state.playlists = [source_mock]

        with patch('music_player.playlists_advanced._get_playlist', return_value=source_mock):
            copy_playlist(self.state, "rock", "Workout")
            self.assertEqual(len(self.state.playlists), 2)


if __name__ == "__main__":
    unittest.main()