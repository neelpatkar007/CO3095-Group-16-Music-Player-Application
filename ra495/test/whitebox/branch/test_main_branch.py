import unittest
from unittest.mock import MagicMock, patch
from music_player import main
from music_player.player_state import PlayerState


class TestMainBranchExtended(unittest.TestCase):
    """
    White-Box Branch Testing for main.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: Branch Testing (White-Box)
    """

    def setUp(self):
        self.state = PlayerState([], MagicMock())

    def test_playlist_arg_branches(self):
        """
        Expected Result:
         - For missing args print usage and error message
         - For valid args call the logic function.
        Actual Result:
            [main] Usage: /pl.rename <old> <new>
            [main] Usage: /pl.del <name|index>
            [main] Usage: /pl.open <name|index>
            [main] Usage: /pl.remove <playlist> <playlist-index>
        """
        # /pl.rename
        main.handle_command(self.state, "/pl.rename Old")  # Fail
        with patch('music_player.playlists_basic.rename_playlist') as mock_rn:
            main.handle_command(self.state, "/pl.rename Old New")  # Success

        # /pl.del
        main.handle_command(self.state, "/pl.del")  # Fail
        with patch('music_player.playlists_basic.delete_playlist') as mock_del:
            main.handle_command(self.state, "/pl.del Mix")  # Success

        # /pl.open
        main.handle_command(self.state, "/pl.open")  # Fail
        with patch('music_player.playlists_basic.open_playlist') as mock_open:
            main.handle_command(self.state, "/pl.open Mix")  # Success

        # /pl.play
        with patch('music_player.playlists_basic.play_playlist') as mock_pp, \
                patch('music_player.playlists_basic.play_active_playlist') as mock_pa:
            main.handle_command(self.state, "/pl.play Mix")  # Has Args (play_playlist)
            mock_pp.assert_called()

            main.handle_command(self.state, "/pl.play")  # No Args (play_active_playlist)
            mock_pa.assert_called()

        # /pl.remove
        main.handle_command(self.state, "/pl.remove Mix")  # Fail
        with patch('music_player.playlists_edit.remove_track_from_playlist') as mock_rm:
            main.handle_command(self.state, "/pl.remove Mix 1")  # Success

