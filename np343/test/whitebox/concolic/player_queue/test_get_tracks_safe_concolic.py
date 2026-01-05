import unittest
from unittest.mock import MagicMock
from music_player.player_queue import _get_tracks_safe
from music_player.player_state import PlayerState
from music_player.library import Track
from music_player.audio_backend import AudioEngine

class TestConcolicExecution(unittest.TestCase):

    def setUp(self):
        self.mock_engine = MagicMock(spec=AudioEngine)

        self.mock_track = MagicMock(spec=Track)
        self.mock_track.path = "/dummy"
        self.mock_track.display_name = "Test Track"
        self.mock_track.duration_seconds = 300

        self.s1 = PlayerState(tracks=[self.mock_track], audio_engine=self.mock_engine)
        self.s1.position_seconds = 0
        self.s1.playback_speed = 1.0

    def test_iter1_initial_seed(self):

        del self.s1.tracks

        result = _get_tracks_safe(self.s1)
        self.assertEqual(result, [], "Iteration 1 failed")

    def test_iter2_flip_type_check(self):
        generated_seed = [10, 20]
        self.s1.tracks = generated_seed

        result = _get_tracks_safe(self.s1)
        self.assertEqual(result, generated_seed, "Iteration 2 failed")

    def test_iter3_flip_iterable(self):
        generated_seed = (10, 20)
        self.s1.tracks = generated_seed

        result = _get_tracks_safe(self.s1)
        self.assertEqual(result, [10, 20], "Iteration 3 failed")

    def test_iter4_flip_exception(self):
        generated_seed = 999
        self.s1.tracks = generated_seed

        result = _get_tracks_safe(self.s1)
        self.assertEqual(result, [], "Iteration 4 failed")


if __name__ == '__main__':
    unittest.main()
