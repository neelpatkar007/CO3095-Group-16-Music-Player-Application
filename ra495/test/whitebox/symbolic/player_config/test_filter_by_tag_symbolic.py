import unittest
from unittest.mock import MagicMock
from music_player.player_config import filter_by_tag

class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.valid_track = MagicMock()
        self.valid_track.path = "/music/song1.mp3"
        self.valid_track.display_name = "Song One"

        self.valid_tags = {"/music/song1.mp3": ["rock", "pop"]}
        self.valid_lib = [self.valid_track]

    def test_pc1_state_none(self):
        S1 = None
        S2 = "rock"

        try:
            filter_by_tag(S1, S2)
        except Exception as e:
            self.fail(f"PC_1 failed with exception: {e}")

    def test_pc2_invalid_tags(self):
        S1_a = MagicMock()
        del S1_a.song_tags
        S1_a.library_tracks = []
        S2 = "rock"
        filter_by_tag(S1_a, S2)

        S1_b = MagicMock()
        S1_b.song_tags = "Not a Dict"
        S1_b.library_tracks = []
        filter_by_tag(S1_b, S2)

    def test_pc3_invalid_lib(self):
        S1_a = MagicMock()
        S1_a.song_tags = {}
        del S1_a.library_tracks
        S2 = "rock"
        filter_by_tag(S1_a, S2)

        S1_b = MagicMock()
        S1_b.song_tags = {}
        S1_b.library_tracks = "Not a List"
        filter_by_tag(S1_b, S2)

    def test_pc4_tag_none(self):
        S1 = MagicMock()
        S1.song_tags = self.valid_tags
        S1.library_tracks = self.valid_lib
        S2 = None

        filter_by_tag(S1, S2)

    def test_pc5_no_matches(self):
        S1 = MagicMock()
        S1.song_tags = self.valid_tags
        S1.library_tracks = self.valid_lib
        S1.tracks = []
        S1.current_index = -1
        S2 = "jazz"

        filter_by_tag(S1, S2)

        self.assertEqual(len(S1.tracks), 0)
        self.assertEqual(S1.current_index, -1)

    def test_pc6_success_update(self):
        S1 = MagicMock()
        S1.song_tags = self.valid_tags
        S1.library_tracks = self.valid_lib
        S1.tracks = []
        S1.current_index = -1
        S2 = "#rock "

        filter_by_tag(S1, S2)

        self.assertEqual(len(S1.tracks), 1)
        self.assertEqual(S1.tracks[0].display_name, "Song One")
        self.assertEqual(S1.current_index, 0)


if __name__ == '__main__':
    unittest.main()