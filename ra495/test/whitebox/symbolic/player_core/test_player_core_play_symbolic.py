import unittest
from unittest.mock import Mock, MagicMock
from music_player.player_core import play
from music_player.player_state import PlayerState


class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.mock_engine = MagicMock()
        self.mock_track = MagicMock()
        self.mock_track.display_name = "Test Track"
        self.mock_track.path = "/music/test.mp3"

    def create_state(self, is_playing=False, is_paused=False, track=None):
        track_list = [track] if track else []
        state = PlayerState(tracks=track_list, audio_engine=self.mock_engine)
        state.current_index = 0
        state.is_playing = is_playing
        state.is_paused = is_paused
        state.position_seconds = 0
        state.playback_speed = 1.0
        return state

    def test_PC_1_state_none(self):
        state = None
        play(state)

    def test_PC_2_invalid_type(self):
        state = "Not a PlayerState"
        play(state)

    def test_PC_3_no_engine(self):
        state = self.create_state(track=self.mock_track)
        del state.audio_engine
        play(state)

    def test_PC_4_engine_no_play(self):
        state = self.create_state(track=self.mock_track)
        state.audio_engine = Mock(spec=[])
        play(state)

    def test_PC_5_track_none(self):
        state = self.create_state(track=None)
        play(state)

    def test_PC_6_track_invalid(self):
        invalid_track = Mock(spec=[])
        state = self.create_state(track=invalid_track)
        play(state)

    def test_PC_7_already_playing(self):
        state = self.create_state(is_playing=True, is_paused=False, track=self.mock_track)
        play(state)
        self.mock_engine.play.assert_not_called()
        self.mock_engine.resume.assert_not_called()

    def test_PC_8_resume_logic(self):
        state = self.create_state(is_playing=True, is_paused=True, track=self.mock_track)
        play(state)
        self.mock_engine.resume.assert_called_once()
        self.assertTrue(state.is_playing)
        self.assertFalse(state.is_paused)

    def test_PC_9_start_fresh(self):
        state = self.create_state(is_playing=False, is_paused=False, track=self.mock_track)
        play(state)
        self.mock_engine.play.assert_called_with(
            "/music/test.mp3",
            start_pos=0,
            speed=1.0
        )
        self.assertTrue(state.is_playing)


if __name__ == '__main__':
    unittest.main()
