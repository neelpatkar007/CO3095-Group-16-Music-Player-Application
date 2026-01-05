import unittest
from unittest.mock import Mock
from music_player.playlists_basic import _get_playlist_summary

class Playlist:

    def __init__(self, tracks):
        self.tracks = tracks


class TestSymbolicExecution(unittest.TestCase):

    _get_playlist_summary_target = staticmethod(_get_playlist_summary)

    def test_PC_1_empty_list(self):
        pl = Playlist(tracks=[])
        result = self._get_playlist_summary_target(pl)
        self.assertEqual(result, (0, 0.0), "PC_1 failed: Should return 0 for empty list.")

    def test_PC_2_invalid_duration(self):
        track_mock = Mock()
        track_mock.duration_seconds = -50
        pl = Playlist(tracks=[track_mock])
        result = self._get_playlist_summary_target(pl)
        self.assertEqual(result, (1, 0.0), "PC_2 failed: Negative duration should be ignored.")

    def test_PC_3_valid_track(self):
        track_mock = Mock()
        track_mock.duration_seconds = 120
        pl = Playlist(tracks=[track_mock])
        result = self._get_playlist_summary_target(pl)
        self.assertEqual(result, (1, 120.0), "PC_3 failed: Valid duration should be summed.")


if __name__ == '__main__':
    unittest.main()
