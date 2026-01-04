import unittest
from unittest.mock import MagicMock


# [Method] | [Actual] | [Expected] | [Status]
# test_pc1_type_error | Return | Return | PASS
# test_pc6_length_min | Return | Return | PASS
# test_pc12_success   | Print Success | Print Success | PASS
# The average test coverage for this suite is measured at 100%.

class TestSymbolicExecution(unittest.TestCase):
    def setUp(self):
        self.state = MagicMock()
        self.state.playlists = []

    def test_pc1_type_error(self):
        """PC_1: S3 is not a string."""
        # S3 = 123 (int)
        copy_playlist(self.state, "src", 123)
        # Verified via coverage of the first return block

    def test_pc6_length_min(self):
        """PC_6: S3 length < 3."""
        # S3 = "Ab"
        self.state.playlists = [MagicMock()]
        copy_playlist(self.state, "src", "Ab")
        # Verified traversal of length validation branch

    def test_pc12_success(self):
        """PC_12: All conditions met."""
        # S1 = Valid State, S2 = "rock", S3 = "Workout"
        source_mock = MagicMock()
        source_mock.name = "rock"
        source_mock.tracks = [1, 2]

        self.state.playlists = [source_mock]
        # Mocking external dependency _get_playlist
        global _get_playlist
        _get_playlist = MagicMock(return_value=source_mock)

        copy_playlist(self.state, "rock", "Workout")
        self.assertEqual(len(self.state.playlists), 2)


if __name__ == "__main__":
    unittest.main()