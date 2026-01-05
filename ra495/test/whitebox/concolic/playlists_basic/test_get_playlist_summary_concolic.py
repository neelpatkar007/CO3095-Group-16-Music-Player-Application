import unittest
from unittest.mock import Mock
from music_player.playlists_basic import _get_playlist_summary

class Playlist:

    def __init__(self, tracks):
        self.tracks = tracks


class TestConcolicExecution(unittest.TestCase):

    _get_playlist_summary_target = staticmethod(_get_playlist_summary)

    def test_iter_1_base_case(self):
        pl = Playlist(tracks=[])
        result = self._get_playlist_summary_target(pl)
        self.assertEqual(result, (0, 0.0))

    def test_iter_2_flip_structure(self):
        track_mock = Mock(spec=[])
        pl = Playlist(tracks=[track_mock])
        result = self._get_playlist_summary_target(pl)
        self.assertEqual(result, (1, 0.0))

    def test_iter_3_flip_value(self):
        track_mock = Mock()
        track_mock.duration_seconds = -5
        pl = Playlist(tracks=[track_mock])
        result = self._get_playlist_summary_target(pl)
        self.assertEqual(result, (1, 0.0))

    def test_iter_4_path_complete(self):
        track_mock = Mock()
        track_mock.duration_seconds = 180
        pl = Playlist(tracks=[track_mock])
        result = self._get_playlist_summary_target(pl)
        self.assertEqual(result, (1, 180.0))


if __name__ == '__main__':
    unittest.main()
