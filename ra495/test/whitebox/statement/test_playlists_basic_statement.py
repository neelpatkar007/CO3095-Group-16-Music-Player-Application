import unittest
from unittest.mock import MagicMock, patch
from music_player import playlists_basic
from music_player.player_state import PlayerState
from music_player.playlist_model import Playlist
from music_player.library import Track
from pathlib import Path


class TestPlaylistsBasicStatement(unittest.TestCase):
    def setUp(self):
        self.state = PlayerState([], MagicMock())
        self.state.playlists = []
        self.pl = Playlist("Mix")

    def test_ensure_and_resolve_errors(self):

        playlists_basic._ensure_playlists(None)
        playlists_basic._resolve_playlist(None, "1")
        playlists_basic._resolve_playlist(self.state, 123)
        self.state.playlists = "NotList"
        playlists_basic._resolve_playlist(self.state, "1")
        self.state.playlists = []
        playlists_basic._resolve_playlist(self.state, "99")
        playlists_basic._resolve_playlist(self.state, "Missing")

    def test_activate_queue_errors(self):

        playlists_basic._activate_playlist_queue(None, self.pl)
        playlists_basic._activate_playlist_queue(self.state, None)
        del self.pl.tracks
        playlists_basic._activate_playlist_queue(self.state, self.pl)
        self.pl.tracks = []
        playlists_basic._activate_playlist_queue(self.state, self.pl)
        self.pl.tracks = "NotList"
        playlists_basic._activate_playlist_queue(self.state, self.pl)
        self.pl.tracks = [MagicMock()]
        with patch.object(playlists_basic, 'player_core', spec=[]) as empty_core:
            playlists_basic._activate_playlist_queue(self.state, self.pl)

    def test_crud_errors(self):
        playlists_basic.create_playlist(self.state, "")
        self.state.playlists.append(self.pl)
        playlists_basic.create_playlist(self.state, "Mix")  # Duplicate
        playlists_basic.rename_playlist(self.state, "Mix", "")
        playlists_basic.rename_playlist(self.state, "Ghost", "New")
        pl2 = Playlist("Other")
        self.state.playlists.append(pl2)
        playlists_basic.rename_playlist(self.state, "Mix", "Other")
        playlists_basic.delete_playlist(self.state, "Ghost")

    def test_list_playlists_coverage(self):
        playlists_basic.list_playlists(None)
        self.state.playlists = None

        playlists_basic.list_playlists(self.state)

        self.state.playlists = "NotList"
        playlists_basic.list_playlists(self.state)

        self.state.playlists = []
        playlists_basic.list_playlists(self.state)

        self.state.playlists = [self.pl, None]
        self.state.active_playlist_index = 0
        playlists_basic.list_playlists(self.state)

    def test_play_open_show_close_errors(self):
        playlists_basic.show_current_playlist(None)
        self.state.active_playlist_index = None
        playlists_basic.show_current_playlist(self.state)
        playlists_basic.play_active_playlist(self.state)
        playlists_basic.play_playlist(self.state, "Ghost")
        del self.state.library_tracks
        playlists_basic.close_playlist(self.state)  # No library found
        self.state.library_tracks = []
        self.state.tracks = self.state.library_tracks
        playlists_basic.close_playlist(self.state)  # Already in main library

    def test_sort_errors_and_exceptions(self):
        playlists_basic.sort_playlist(None, "Mix", "title")
        playlists_basic.sort_playlist(self.state, "", "title")
        playlists_basic.sort_playlist(self.state, "Mix", None)

        playlists_basic.sort_playlist(self.state, "Ghost", "title")

        self.state.playlists = [self.pl]
        del self.pl.tracks
        playlists_basic.sort_playlist(self.state, "Mix", "title")  # Tracks corrupted

        self.pl.tracks = []
        playlists_basic.sort_playlist(self.state, "Mix", "title")  # Empty

        self.pl.tracks = [MagicMock()]
        playlists_basic.sort_playlist(self.state, "Mix", "invalid_criteria")

        exploding_list = MagicMock()
        exploding_list.__len__.return_value = 1
        exploding_list.__bool__.return_value = True
        exploding_list.sort.side_effect = Exception("Sort Failed")

        self.pl.tracks = exploding_list

        playlists_basic.sort_playlist(self.state, "Mix", "title")
        playlists_basic.sort_playlist(self.state, "Mix", "artist")
        playlists_basic.sort_playlist(self.state, "Mix", "duration")