import unittest
from unittest.mock import Mock, MagicMock
from music_player.player_core import play
from music_player.player_state import PlayerState


class TestConcolicGeneration(unittest.TestCase):
    def create_symbolic_state(self):
        track = MagicMock()
        track.path = "/dummy"
        track.display_name = "Dummy Track"
        s = PlayerState(tracks=[track], audio_engine=MagicMock())
        s.current_index = 0
        s.position_seconds = 10
        s.playback_speed = 1.0
        return s

    def test_iteration_1_seed_input(self):
        s1 = None
        play(s1)

    def test_iteration_2_flip_type(self):
        s1 = dict()  # Wrong type
        play(s1)

    def test_iteration_3_flip_engine_attr(self):
        s1 = self.create_symbolic_state()
        del s1.audio_engine
        play(s1)

    def test_iteration_4_flip_engine_method(self):
        s1 = self.create_symbolic_state()
        s1.audio_engine = Mock(spec=[])
        play(s1)

    def test_iteration_5_flip_track_none(self):
        s1 = self.create_symbolic_state()
        s1.tracks = []
        play(s1)

    def test_iteration_6_flip_track_path(self):
        s1 = self.create_symbolic_state()
        del s1.current_track.path
        play(s1)

    def test_iteration_7_flip_is_playing(self):
        s1 = self.create_symbolic_state()
        s1.is_playing = True
        s1.is_paused = False
        play(s1)
        s1.audio_engine.play.assert_not_called()
        s1.audio_engine.resume.assert_not_called()

    def test_iteration_8_flip_is_paused(self):
        s1 = self.create_symbolic_state()
        s1.is_playing = True
        s1.is_paused = True
        play(s1)
        s1.audio_engine.resume.assert_called_once()
        self.assertFalse(s1.is_paused)

    def test_iteration_10_fully_explored(self):
        s1 = self.create_symbolic_state()
        s1.is_playing = False
        s1.is_paused = False
        play(s1)
        s1.audio_engine.play.assert_called()
        self.assertTrue(s1.is_playing)


if __name__ == '__main__':
    unittest.main()
