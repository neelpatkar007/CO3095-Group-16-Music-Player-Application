import unittest
from io import StringIO
import sys
from music_player.player_config import list_all_tags

class TestConcolicGenerative(unittest.TestCase):

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_iteration_1_seed_none(self):
        s1 = None
        list_all_tags(s1)
        self.assertIn("State is None", self.held_output.getvalue())

    def test_iteration_2_flip_s1_existence(self):
        from unittest.mock import MagicMock
        s1 = MagicMock(spec=[])
        list_all_tags(s1)
        self.assertIn("Tag data is unavailable", self.held_output.getvalue())

    def test_iteration_3_flip_s2_type(self):
        from unittest.mock import MagicMock
        s1 = MagicMock()
        s1.song_tags = "InvalidString"
        list_all_tags(s1)
        self.assertIn("Tag data is unavailable", self.held_output.getvalue())

    def test_iteration_4_flip_s3_existence(self):
        from unittest.mock import MagicMock
        s1 = MagicMock()
        s1.song_tags = {}
        del s1.library_tracks
        list_all_tags(s1)
        self.assertIn("Library tracks missing", self.held_output.getvalue())

    def test_iteration_5_flip_content_validity(self):
        from unittest.mock import MagicMock
        s1 = MagicMock()
        s1.song_tags = {"id_01": ["Electronic"], "id_02": ["Electronic", "Ambient"]}
        s1.library_tracks = ["track1", "track2"]

        list_all_tags(s1)
        output = self.held_output.getvalue()
        self.assertIn("--- Custom Tags ---", output)
        self.assertIn("#Electronic (2 songs)", output)
        self.assertIn("#Ambient (1 songs)", output)


if __name__ == '__main__':
    unittest.main()