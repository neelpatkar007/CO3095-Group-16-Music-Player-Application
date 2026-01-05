import unittest
from pathlib import Path
from music_player.library import Track


class TestConcolicExecution(unittest.TestCase):

    def test_iteration_1_baseline_path(self):
        track = Track(path=Path("test.mp3"), title="Test", artist=None, duration_seconds=0.0)

        if track.artist:
            path_taken = "PC_1"
        else:
            path_taken = "PC_2"

        self.assertEqual(path_taken, "PC_2")
        self.assertEqual(track.display_name, "Test")

    def test_iteration_2_negated_path(self):
        track = Track(path=Path("test.mp3"), title="Test", artist="Artist", duration_seconds=0.0)

        if track.artist:
            path_taken = "PC_1"
        else:
            path_taken = "PC_2"

        self.assertEqual(path_taken, "PC_1")
        self.assertEqual(track.display_name, "Test – Artist")


if __name__ == '__main__':
    unittest.main()