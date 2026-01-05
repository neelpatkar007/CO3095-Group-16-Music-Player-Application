import unittest
from io import StringIO
import sys
from music_player.player_config import view_stats
from unittest.mock import MagicMock

class MockTrack:
    def __init__(self, path, artist):
        self.path = path
        self.artist = artist

class TestConcolicExecution(unittest.TestCase):

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_iteration_1_seed_none(self):
        seed_S1 = None
        view_stats(seed_S1)
        self.assertIn("Error: State is None", self.held_output.getvalue())

    def test_iteration_2_seed_invalid_dict(self):
        seed_S1 = MagicMock()
        seed_S1.play_counts = None
        view_stats(seed_S1)
        self.assertIn("Error: Play count data is corrupted", self.held_output.getvalue())

    def test_iteration_3_seed_empty_dict(self):
        seed_S1 = MagicMock()
        seed_S1.play_counts = {}
        view_stats(seed_S1)
        self.assertIn("No play history yet", self.held_output.getvalue())

    def test_iteration_4_seed_missing_tracks(self):
        seed_S1 = MagicMock()
        seed_S1.play_counts = {"file": 1}
        seed_S1.library_tracks = []
        view_stats(seed_S1)
        self.assertIn("Error: Library tracks are missing", self.held_output.getvalue())

    def test_iteration_5_seed_bad_time(self):
        seed_S1 = MagicMock()
        seed_S1.play_counts = {"file": 1}
        seed_S1.library_tracks = [MockTrack("file", "art")]
        seed_S1.total_play_time = "Invalid"
        view_stats(seed_S1)
        self.assertIn("Error: Total play time is corrupted", self.held_output.getvalue())

    def test_iteration_6_seed_unmatched_paths(self):
        seed_S1 = MagicMock()
        seed_S1.play_counts = {"path_A": 10}
        seed_S1.library_tracks = [MockTrack("path_B", "ArtistB")]
        seed_S1.total_play_time = 100
        view_stats(seed_S1)
        output = self.held_output.getvalue()
        self.assertIn("Total Songs Played: 10", output)
        self.assertIn("(No data yet)", output)

    def test_iteration_7_seed_matched(self):
        seed_S1 = MagicMock()
        seed_S1.play_counts = {"path_A": 10}
        seed_S1.library_tracks = [MockTrack("path_A", "Queen")]
        seed_S1.total_play_time = 3665
        view_stats(seed_S1)
        output = self.held_output.getvalue()
        self.assertIn("Total Listening Time: 1h 1m", output)
        self.assertIn("Queen: 10 plays", output)


if __name__ == "__main__":
    unittest.main()