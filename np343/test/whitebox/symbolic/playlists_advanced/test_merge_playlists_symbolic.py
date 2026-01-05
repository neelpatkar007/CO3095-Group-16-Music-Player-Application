import unittest
from unittest.mock import MagicMock, patch
from music_player.playlists_advanced import merge_playlists, _get_playlist


class TestSymbolicExecution(unittest.TestCase):
    def setUp(self):
        self.state = MagicMock()

    def test_pc1_target_empty(self):
        merge_playlists(self.state, "", "source", True)

    def test_pc2_source_whitespace(self):
        merge_playlists(self.state, "target", "  ", True)

    def test_pc3_target_not_found(self):
        with patch('music_player.playlists_advanced._get_playlist', side_effect=[None, MagicMock()]):
            merge_playlists(self.state, "target", "source", True)

    def test_pc5_identity_conflict(self):
        playlist_obj = MagicMock()
        with patch('music_player.playlists_advanced._get_playlist', return_value=playlist_obj):
            merge_playlists(self.state, "target", "source", True)

    def test_pc6_empty_source_tracks(self):
        target = MagicMock(tracks=[])
        source = MagicMock(tracks=[], name="EmptySrc")
        with patch('music_player.playlists_advanced._get_playlist', side_effect=[target, source]):
            merge_playlists(self.state, "target", "source", True)

    def test_pc7_full_execution(self):
        target = MagicMock(tracks=[], name="Tgt")
        track_obj = MagicMock(title="Valid Track")
        source = MagicMock(tracks=[track_obj], name="Src")
        with patch('music_player.playlists_advanced._get_playlist', side_effect=[target, source]):
            merge_playlists(self.state, "target", "source", True)
            self.assertIn(track_obj, target.tracks)


if __name__ == '__main__':
    unittest.main()