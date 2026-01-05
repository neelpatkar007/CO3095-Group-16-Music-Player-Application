import unittest
from unittest.mock import MagicMock, patch
from music_player.player_queue import previous_track, _get_tracks_safe


class PlayerState:
    def __init__(self):
        self.current_index = 0
        self.loop_mode = "off"
        self.shuffle_active = False
        self.history = []
        self.is_playing = False
        self.is_paused = False
        self.position_seconds = 0.0
        self.audio_engine = MagicMock()


class Track:
    def __init__(self, name="Track", path="path/to/file"):
        self.display_name = name
        self.path = path

    def __eq__(self, other):
        return self.display_name == other.display_name


class TestConcolicExecution(unittest.TestCase):

    def setUp(self):
        self.state = PlayerState()
        self.track1 = Track("Track 1")
        self.track2 = Track("Track 2")
        self.tracks = [self.track1, self.track2]

    @patch('music_player.player_queue._get_tracks_safe')
    def test_iter_3_loop_one_logic(self, mock_get_tracks):

        mock_get_tracks.return_value = self.tracks
        self.state.loop_mode = "one"
        self.state.current_index = 0

        previous_track(self.state)

        self.assertEqual(self.state.current_index, 0)

    @patch('music_player.player_queue._get_tracks_safe')
    def test_iter_4_shuffle_logic(self, mock_get_tracks):

        mock_get_tracks.return_value = self.tracks
        self.state.shuffle_active = True
        self.state.history = [self.track2]
        self.state.current_index = 0

        previous_track(self.state)

        self.assertEqual(self.state.current_index, 1)
        self.assertEqual(len(self.state.history), 0)

    @patch('music_player.player_queue._get_tracks_safe')
    def test_iter_5_wrap_logic(self, mock_get_tracks):

        mock_get_tracks.return_value = self.tracks
        self.state.loop_mode = "all"
        self.state.current_index = 0

        previous_track(self.state)

        self.assertEqual(self.state.current_index, 1)

    @patch('music_player.player_queue._get_tracks_safe')
    def test_iter_6_start_boundary_logic(self, mock_get_tracks):

        mock_get_tracks.return_value = self.tracks
        self.state.loop_mode = "off"
        self.state.current_index = 0

        previous_track(self.state)

        self.assertEqual(self.state.current_index, 0)


if __name__ == '__main__':
    unittest.main()
