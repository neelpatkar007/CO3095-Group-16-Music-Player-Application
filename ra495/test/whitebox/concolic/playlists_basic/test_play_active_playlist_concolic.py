import unittest
from unittest.mock import MagicMock, patch
from music_player.playlists_basic import play_active_playlist

class TestConcolicGenerations(unittest.TestCase):

    def setUp(self):
        self.mock_state = MagicMock()
        self.patcher_activate = patch('music_player.playlists_basic._activate_playlist_queue')
        self.patcher_print = patch('builtins.print')
        self.patcher_ensure = patch('music_player.playlists_basic._ensure_playlists')

        self.mock_activate = self.patcher_activate.start()
        self.mock_print = self.patcher_print.start()
        self.mock_ensure = self.patcher_ensure.start()

    def tearDown(self):
        self.patcher_activate.stop()
        self.patcher_print.stop()
        self.patcher_ensure.stop()

    def test_iteration_1_initial_seed(self):
        self.mock_state.active_playlist_index = None
        self.mock_state.playlists = []


        play_active_playlist(self.mock_state)
        self.mock_print.assert_called()
        self.mock_activate.assert_not_called()

    def test_iteration_2_flipped_s1(self):
        self.mock_state.active_playlist_index = 0
        self.mock_state.playlists = []


        play_active_playlist(self.mock_state)

        self.mock_print.assert_called()
        self.mock_activate.assert_not_called()

    def test_iteration_3_flipped_s2(self):
        target_playlist = MagicMock()
        self.mock_state.active_playlist_index = 0
        self.mock_state.playlists = [target_playlist]


        play_active_playlist(self.mock_state)
        self.mock_print.assert_not_called()
        self.mock_activate.assert_called_with(
            self.mock_state,
            target_playlist,
            auto_play=True
        )


if __name__ == '__main__':
    unittest.main()