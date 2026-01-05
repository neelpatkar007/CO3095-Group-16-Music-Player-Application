import unittest
from unittest.mock import MagicMock, patch
from music_player.playlists_basic import play_active_playlist

class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.mock_state = MagicMock()
        self.patcher_ensure = patch('music_player.playlists_basic._ensure_playlists')
        self.patcher_activate = patch('music_player.playlists_basic._activate_playlist_queue')
        self.patcher_print = patch('builtins.print')

        self.mock_ensure = self.patcher_ensure.start()
        self.mock_activate = self.patcher_activate.start()
        self.mock_print = self.patcher_print.start()

    def tearDown(self):
        self.patcher_ensure.stop()
        self.patcher_activate.stop()
        self.patcher_print.stop()

    def test_pc_1_symbolic_s1_is_none(self):
        """
        Path Condition 1: S1 == None.
        Logic: Short-circuit evaluation triggers early return.
        """
        self.mock_state.active_playlist_index = None
        self.mock_state.playlists = ["MockPlaylist"]

        play_active_playlist(self.mock_state)

        self.mock_ensure.assert_called_once_with(self.mock_state)
        self.mock_print.assert_called_once()
        self.mock_activate.assert_not_called()

    def test_pc_2_symbolic_s1_valid_s2_empty(self):

        self.mock_state.active_playlist_index = 0  # S1
        self.mock_state.playlists = []  # S2

        play_active_playlist(self.mock_state)

        self.mock_ensure.assert_called_once_with(self.mock_state)
        self.mock_print.assert_called_once()
        self.mock_activate.assert_not_called()

    def test_pc_3_symbolic_valid_execution(self):

        mock_playlist_obj = MagicMock()
        self.mock_state.active_playlist_index = 0  # S1
        self.mock_state.playlists = [mock_playlist_obj]  # S2

        play_active_playlist(self.mock_state)

        self.mock_ensure.assert_called_once_with(self.mock_state)
        self.mock_print.assert_not_called()
        self.mock_activate.assert_called_once_with(
            self.mock_state,
            mock_playlist_obj,
            auto_play=True
        )


if __name__ == '__main__':
    unittest.main()