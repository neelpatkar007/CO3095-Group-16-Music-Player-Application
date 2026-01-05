import unittest
from unittest.mock import MagicMock, patch
from music_player.playlists_basic import _activate_playlist_queue
from music_player.playlists_basic import _ensure_playlists
from music_player.playlists_basic import _set_active_by_playlist
class TestConcolicExecution(unittest.TestCase):

    def setUp(self):
        self.ensure_patcher = patch('music_player.playlists_basic._ensure_playlists')
        self.set_active_patcher = patch('music_player.playlists_basic._set_active_by_playlist')
        self.mock_ensure = self.ensure_patcher.start()
        self.mock_set_active = self.set_active_patcher.start()

        self.player_core_patcher = patch('music_player.playlists_basic.player_core', create=True)
        self.mock_player_core = self.player_core_patcher.start()

        self.mock_player_core.play = MagicMock()

    def tearDown(self):
        self.ensure_patcher.stop()
        self.set_active_patcher.stop()
        self.player_core_patcher.stop()

    def test_iter1_flip_s1(self):

        S1 = None
        S2 = None
        S3 = True

        with patch('builtins.print') as mock_print:
            _activate_playlist_queue(S1, S2, S3)
            mock_print.assert_called_with("[pl] Error: State is None.")

    def test_iter2_flip_s2(self):

        S1 = MagicMock()
        S2 = None
        S3 = True

        with patch('builtins.print') as mock_print:
            _activate_playlist_queue(S1, S2, S3)
            mock_print.assert_called_with("[pl] Error: Playlist is None.")

    def test_iter3_flip_attr(self):

        S1 = MagicMock()
        S2 = MagicMock()
        del S2.tracks
        S3 = True

        with patch('builtins.print') as mock_print:
            _activate_playlist_queue(S1, S2, S3)
            mock_print.assert_called_with("[pl] Error: Playlist invalid.")

    def test_iter4_flip_type(self):

        S1 = MagicMock()
        S2 = MagicMock()
        S2.tracks = "Not List"
        S3 = True

        with patch('builtins.print') as mock_print:
            _activate_playlist_queue(S1, S2, S3)
            mock_print.assert_called_with("[pl] Error: Playlist tracks corrupted.")

    def test_iter5_flip_empty(self):

        S1 = MagicMock()
        S2 = MagicMock()
        S2.tracks = []
        S3 = True

        with patch('builtins.print') as mock_print:
            _activate_playlist_queue(S1, S2, S3)
            mock_print.assert_called_with("[pl] Warning: Playlist is empty.")

    def test_iter6_flip_s3(self):

        S1 = MagicMock()
        S2 = MagicMock()
        S2.tracks = ['Item']
        S3 = False

        _activate_playlist_queue(S1, S2, S3)
        self.mock_player_core.play.assert_not_called()

    def test_iter7_flip_s4(self):
        S1 = MagicMock()
        S2 = MagicMock()
        S2.tracks = ['Item']
        S3 = True


        self.mock_player_core.play = MagicMock()

        _activate_playlist_queue(S1, S2, S3)
        self.mock_player_core.play.assert_called_once_with(S1)

    def test_iter8_boundary(self):

        S1 = MagicMock()
        S2 = MagicMock()
        S2.tracks = ['Item']
        S3 = True

        del self.mock_player_core.play

        with patch('builtins.print') as mock_print:
            _activate_playlist_queue(S1, S2, S3)
            mock_print.assert_called_with("[pl] Error: Player core not available.")