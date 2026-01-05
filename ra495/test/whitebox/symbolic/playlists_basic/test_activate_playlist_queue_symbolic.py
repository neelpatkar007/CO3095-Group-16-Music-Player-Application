import unittest
from unittest.mock import MagicMock, patch
from music_player.playlists_basic import _activate_playlist_queue

class TestSymbolicExecution(unittest.TestCase):


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

    def test_pc1_state_none(self):

        with patch('builtins.print') as mock_print:
            _activate_playlist_queue(None, MagicMock(), True)
            mock_print.assert_called_with("[pl] Error: State is None.")

    def test_pc2_playlist_none(self):

        S1 = MagicMock()

        with patch('builtins.print') as mock_print:
            _activate_playlist_queue(S1, None, True)
            mock_print.assert_called_with("[pl] Error: Playlist is None.")

    def test_pc3_playlist_invalid_no_tracks(self):

        S1 = MagicMock()
        S2 = MagicMock()
        del S2.tracks

        with patch('builtins.print') as mock_print:
            _activate_playlist_queue(S1, S2, True)
            mock_print.assert_called_with("[pl] Error: Playlist invalid.")

    def test_pc4_tracks_corrupted(self):

        S1 = MagicMock()
        S2 = MagicMock()
        S2.tracks = "Corrupted Data"

        with patch('builtins.print') as mock_print:
            _activate_playlist_queue(S1, S2, True)
            mock_print.assert_called_with("[pl] Error: Playlist tracks corrupted.")

    def test_pc5_tracks_empty(self):

        S1 = MagicMock()
        S2 = MagicMock()
        S2.tracks = []

        with patch('builtins.print') as mock_print:
            _activate_playlist_queue(S1, S2, True)
            mock_print.assert_called_with("[pl] Warning: Playlist is empty.")

    def test_pc6_valid_execution_no_autoplay(self):

        S1 = MagicMock()
        S1.library_tracks = None
        S2 = MagicMock()
        S2.tracks = ['song1', 'song2']

        S3 = False

        _activate_playlist_queue(S1, S2, S3)


        self.assertEqual(S1.tracks, S2.tracks)
        self.assertEqual(S1.current_index, 0)
        self.assertEqual(S1.position_seconds, 0.0)
        self.assertEqual(S1.library_tracks, [])  # Check the 'None' assignment branch

        self.mock_player_core.play.assert_not_called()

    def test_pc7_valid_execution_autoplay_success(self):


        S1 = MagicMock()
        S1.library_tracks = ['existing']

        S2 = MagicMock()
        S2.tracks = ['song1']

        S3 = True

        self.mock_player_core.play = MagicMock()

        _activate_playlist_queue(S1, S2, S3)

        self.mock_player_core.play.assert_called_once_with(S1)

    def test_pc8_valid_execution_autoplay_error(self):

        S1 = MagicMock()
        S2 = MagicMock()
        S2.tracks = ['song1']
        S3 = True

        del self.mock_player_core.play

        with patch('builtins.print') as mock_print:
            _activate_playlist_queue(S1, S2, S3)
            mock_print.assert_called_with("[pl] Error: Player core not available.")