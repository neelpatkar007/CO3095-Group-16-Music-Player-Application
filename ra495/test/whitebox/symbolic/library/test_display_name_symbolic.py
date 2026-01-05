import unittest
from pathlib import Path
from music_player.library import Track


class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        pass

    def test_pc2_artist_evaluates_false(self):
        track = Track(path=Path("test.mp3"), title="Bohemian Rhapsody", artist="", duration_seconds=0.0)
        result = track.display_name
        expected = "Bohemian Rhapsody"
        self.assertEqual(result, expected, "PC_2 failed: Should return title only when artist is empty.")

    def test_pc1_artist_evaluates_true(self):
        track = Track(path=Path("test.mp3"), title="Imagine", artist="Lennon", duration_seconds=0.0)
        result = track.display_name
        expected = "Imagine – Lennon"
        self.assertEqual(result, expected, "PC_1 failed: Should return formatted string when artist is present.")


if __name__ == '__main__':
    unittest.main()