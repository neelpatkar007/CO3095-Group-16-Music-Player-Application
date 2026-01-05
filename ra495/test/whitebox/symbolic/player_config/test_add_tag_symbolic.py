import unittest
from unittest.mock import MagicMock
import io
import sys
from music_player.player_config import add_tag

class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.held, sys.stdout = sys.stdout, io.StringIO()

        self.mock_track = MagicMock()
        self.mock_track.path = "/music/song.mp3"
        self.mock_track.title = "Test Song"

        self.mock_state = MagicMock()
        self.mock_state.song_tags = {}
        self.mock_state.library_tracks = [self.mock_track]

    def tearDown(self):
        sys.stdout = self.held

    def test_pc1_state_none(self):
        add_tag(None, "1", "tag")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "[tags] Error: State is None.")

    def test_pc2_invalid_index(self):
        add_tag(self.mock_state, "abc", "tag")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "[tags] Error: Invalid number format.")

    def test_pc3_corrupt_tags(self):
        self.mock_state.song_tags = []  # Incorrect type
        add_tag(self.mock_state, "1", "tag")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "[tags] Error: Tag data is unavailable/corrupted.")

    def test_pc4_corrupt_lib(self):
        self.mock_state.library_tracks = {}  # Incorrect type
        add_tag(self.mock_state, "1", "tag")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "[tags] Error: Library tracks missing/corrupted.")

    def test_pc5_index_bounds(self):
        add_tag(self.mock_state, "5", "tag")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "[tags] Error: Song index out of range.")

    def test_pc6_track_none(self):
        self.mock_state.library_tracks = [None]
        add_tag(self.mock_state, "1", "tag")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "")  # Should be silent

    def test_pc7_tag_none(self):
        add_tag(self.mock_state, "1", None)
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "[tags] Error: Tag cannot be empty.")

    def test_pc8_tag_too_long(self):
        long_tag = "A" * 16
        add_tag(self.mock_state, "1", long_tag)
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "[tags] Error: Tag is too long (max 15 chars).")

    def test_pc9_invalid_char(self):
        add_tag(self.mock_state, "1", "tag!")
        output = sys.stdout.getvalue().strip()
        self.assertIn("[tags] Error: Invalid character", output)

    def test_pc10_max_tags(self):
        path = str(self.mock_track.path)
        self.mock_state.song_tags[path] = ["t1", "t2", "t3", "t4", "t5"]

        add_tag(self.mock_state, "1", "t6")
        output = sys.stdout.getvalue().strip()
        self.assertIn("has reached the limit of 5 tags", output)

    def test_pc11_tag_exists(self):
        path = str(self.mock_track.path)
        self.mock_state.song_tags[path] = ["techno"]

        add_tag(self.mock_state, "1", "techno")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "[tags] Song already has tag #techno.")

    def test_pc12_add_success(self):
        add_tag(self.mock_state, "1", "jazz")
        output = sys.stdout.getvalue().strip()

        path = str(self.mock_track.path)
        self.assertEqual(output, "[tags] Added #jazz to 'Test Song'.")
        self.assertIn("jazz", self.mock_state.song_tags[path])


if __name__ == '__main__':
    unittest.main()