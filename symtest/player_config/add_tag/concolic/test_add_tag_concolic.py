import unittest
from unittest.mock import MagicMock
import io
import sys
from music_player.player_config import add_tag


class TestConcolicIntegration(unittest.TestCase):
    def setUp(self):
        self.held, sys.stdout = sys.stdout, io.StringIO()
        self.mock_track = MagicMock()
        self.mock_track.path = "track_path"
        self.mock_track.title = "Concolic Song"

        self.mock_state = MagicMock()
        self.mock_state.song_tags = {}
        self.mock_state.library_tracks = [self.mock_track]

    def tearDown(self):
        sys.stdout = self.held

    def test_iter1_state_null(self):
        add_tag(None, "1", "test")
        self.assertIn("State is None", sys.stdout.getvalue())

    def test_iter2_bad_int(self):
        add_tag(self.mock_state, "NOT_INT", "test")
        self.assertIn("Invalid number format", sys.stdout.getvalue())

    def test_iter3_bad_dict(self):
        del self.mock_state.song_tags
        add_tag(self.mock_state, "1", "test")
        self.assertIn("Tag data is unavailable", sys.stdout.getvalue())

    def test_iter4_bad_list(self):
        del self.mock_state.library_tracks
        add_tag(self.mock_state, "1", "test")
        self.assertIn("Library tracks missing", sys.stdout.getvalue())

    def test_iter5_bounds(self):
        # S5 is valid, but we flip the index condition
        self.mock_state.library_tracks = []  # Empty list, index 1 is out of bounds
        add_tag(self.mock_state, "1", "test")
        self.assertIn("Song index out of range", sys.stdout.getvalue())

    def test_iter6_null_track(self):
        self.mock_state.library_tracks = [None]
        add_tag(self.mock_state, "1", "test")
        self.assertEqual("", sys.stdout.getvalue().strip())

    def test_iter7_tag_none(self):
        add_tag(self.mock_state, "1", None)
        self.assertIn("Tag cannot be empty", sys.stdout.getvalue())

    def test_iter8_len_limit(self):
        add_tag(self.mock_state, "1", "1234567890123456")
        self.assertIn("Tag is too long", sys.stdout.getvalue())

    def test_iter9_char_limit(self):
        add_tag(self.mock_state, "1", "tag$")
        self.assertIn("Invalid character", sys.stdout.getvalue())

    def test_iter10_max_tags(self):
        self.mock_state.song_tags["track_path"] = ["1", "2", "3", "4", "5"]
        add_tag(self.mock_state, "1", "6")
        self.assertIn("reached the limit", sys.stdout.getvalue())

    def test_iter11_dupe(self):
        self.mock_state.song_tags["track_path"] = ["existing"]
        add_tag(self.mock_state, "1", "existing")
        self.assertIn("already has tag", sys.stdout.getvalue())

    def test_iter12_success(self):
        add_tag(self.mock_state, "1", "new_tag")
        self.assertIn("Added #new_tag", sys.stdout.getvalue())


if __name__ == '__main__':
    unittest.main()