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

    def test_advanced_playlist_branches(self):
        """
        Expected Result: Missing args triggers usage error and valid args triggers backend call.
        Actual Result:
            [main] Usage: /pl.copy <source> <new-name>
            Usage: /pl.sort <playlist> <artist|title|duration>
        """
        # /pl.copy
        main.handle_command(self.state, "/pl.copy Source")  # Fail
        with patch('music_player.playlists_advanced.copy_playlist') as mock_cp:
            main.handle_command(self.state, "/pl.copy Source New")  # Success

        # /scan
        with patch('music_player.library_search_scan.rescan_for_new_tracks') as mock_scan:
            main.handle_command(self.state, "/scan")
            mock_scan.assert_called()

        # /pl.sort
        main.handle_command(self.state, "/pl.sort Mix")  # Fail
        with patch('music_player.playlists_basic.sort_playlist') as mock_sort:
            main.handle_command(self.state, "/pl.sort Mix title")  # Success

    def test_search_and_library_branches(self):
        """
        Expected Result: All view/search commands dispatch to library_search_scan.
        Actual Result: All mocks asserted successfully (100% Passed Test).
        """
        # /search
        with patch('music_player.library_search_scan.search_library') as mock_search:
            main.handle_command(self.state, "/search query")
            mock_search.assert_called()
            main.handle_command(self.state, "/search")  # Empty query

        # View Tables
        with patch('music_player.library_search_scan.view_songs_table') as m_s, \
                patch('music_player.library_search_scan.view_artists_table') as m_a, \
                patch('music_player.library_search_scan.view_albums_table') as m_b:
            main.handle_command(self.state, "/songs")
            m_s.assert_called()
            main.handle_command(self.state, "/artists")
            m_a.assert_called()
            main.handle_command(self.state, "/albums")
            m_b.assert_called()

    def test_sprint_4_branches(self):
        """
        Expected Result:
         - Commands verify and allow only a strict number of accepted arguments where required.
         - Optional arguments are handled properly without crashing/errors.
        Actual Result:
            Usage: /tag.add <song-index> <tag>
            [tags] Usage: /tag.play <tag_name>
            Usage: /edit <index> <title|artist> <value>
        """
        # /tag.add
        main.handle_command(self.state, "/tag.add 1")  # Fail
        with patch('music_player.player_config.add_tag') as mock_tag:
            main.handle_command(self.state, "/tag.add 1 Cool")  # Success

        # /tag.filter
        main.handle_command(self.state, "/tag.filter")  # Fail
        with patch('music_player.player_config.filter_by_tag') as mock_filt:
            main.handle_command(self.state, "/tag.filter Cool")  # Success

        # /edit
        main.handle_command(self.state, "/edit 1 title")  # Fail
        with patch('music_player.player_io.update_metadata') as mock_edit:
            main.handle_command(self.state, "/edit 1 title NewTitle")  # Success

        # /pl.export
        with patch('music_player.player_io.export_playlist') as mock_exp:
            main.handle_command(self.state, "/pl.export Mix csv")  # With format
            main.handle_command(self.state, "/pl.export Mix")  # Without format

        # /rate
        with patch('music_player.user_data.rate_song') as mock_rate:
            main.handle_command(self.state, "/rate 5")  # With arg
            main.handle_command(self.state, "/rate")  # Without arg

        # /profile commands
        with patch('music_player.user_data.create_profile') as m_cp, \
                patch('music_player.user_data.switch_profile') as m_sp, \
                patch('music_player.user_data.list_profiles') as m_lp, \
                patch('music_player.user_data.show_current_profile') as m_scp:
            main.handle_command(self.state, "/profile.new User")
            main.handle_command(self.state, "/profile.switch User")
            main.handle_command(self.state, "/profiles")
            main.handle_command(self.state, "/profile")