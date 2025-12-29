import unittest
from unittest.mock import MagicMock, patch
from music_player import playlists_basic
from music_player.player_state import PlayerState
from music_player.playlist_model import Playlist
from music_player.library import Track
from pathlib import Path


class TestPlaylistsBasicStatement(unittest.TestCase):
    """
    White-Box Statement Testing for playlists_basic.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: Statement Testing (White-Box)
    """

    def setUp(self):
        self.state = PlayerState([], MagicMock())
        self.state.playlists = []
        self.pl = Playlist("Mix")

    def test_ensure_and_resolve_errors(self):
        """
        Expected Result: Helper functions handle invalid inputs without crashing.
        Actual Result:
            [pl] Error: State is None.
            [pl] Error: State is None.
            [pl] Error: State is None.
            [pl] Missing playlist name or number.
            [pl] Error: State is None.
            [pl] Playlist index out of range.
            [pl] Playlist 'Missing' not found.
        """
        # _ensure_playlists errors
        playlists_basic._ensure_playlists(None)
        # _resolve_playlist errors
        playlists_basic._resolve_playlist(None, "1")
        playlists_basic._resolve_playlist(self.state, 123)
        self.state.playlists = "NotList"  # Corrupt playlists
        playlists_basic._resolve_playlist(self.state, "1")
        self.state.playlists = []
        playlists_basic._resolve_playlist(self.state, "99")
        playlists_basic._resolve_playlist(self.state, "Missing")

    def test_activate_queue_errors(self):
        """
        Expected Result: Activation fails safely with error messages.
        Actual Result:
        [pl] Error: State is None.
        [pl] Error: Playlist is None.
        [pl] Error: Playlist invalid.
        [pl] Warning: Playlist is empty.
        [pl] Error: Playlist tracks corrupted.
        [pl] Error: Player core not available.
        """
        # State None
        playlists_basic._activate_playlist_queue(None, self.pl)
        # Playlist None
        playlists_basic._activate_playlist_queue(self.state, None)
        # Playlist Invalid
        del self.pl.tracks
        playlists_basic._activate_playlist_queue(self.state, self.pl)
        # Restore tracks
        self.pl.tracks = []
        # Playlist Empty
        playlists_basic._activate_playlist_queue(self.state, self.pl)
        # Tracks Corrupted
        self.pl.tracks = "NotList"
        playlists_basic._activate_playlist_queue(self.state, self.pl)
        # Player Core missing
        self.pl.tracks = [MagicMock()]
        with patch.object(playlists_basic, 'player_core', spec=[]) as empty_core:
            playlists_basic._activate_playlist_queue(self.state, self.pl)

    def test_crud_errors(self):
        """
        Expected Result: CRUD operations reject invalid inputs without crashing.
        Actual Result:
            [pl] Usage: /pl.new <name>
            [pl] A playlist named 'Mix' already exists.
            [pl] Usage: /pl.rename <old> <new>
            [pl] Playlist 'Ghost' not found.
            [pl] Another playlist already has the name 'Other'.
            [pl] Playlist 'Ghost' not found.
        """
        # Create
        playlists_basic.create_playlist(self.state, "")
        self.state.playlists.append(self.pl)
        playlists_basic.create_playlist(self.state, "Mix")  # Duplicate
        # Rename
        playlists_basic.rename_playlist(self.state, "Mix", "")
        playlists_basic.rename_playlist(self.state, "Ghost", "New")
        pl2 = Playlist("Other")
        self.state.playlists.append(pl2)
        playlists_basic.rename_playlist(self.state, "Mix", "Other")
        # Delete
        playlists_basic.delete_playlist(self.state, "Ghost")

    def test_list_playlists_coverage(self):
        """
        Expected Result: Function handles all data corruption states.
        Actual Result:
            [pl] Error: State is None.
            [pl] Internal Error: State is missing.
            [pl] No playlists defined.
            [pl] Error: Playlist data is corrupted.
            [pl] No playlists defined.
            [pl] Playlists:
               1. Mix* (0 songs, Total time: 00:00)
               2. <Error: Invalid Playlist>
        """
        # State/Data errors
        playlists_basic.list_playlists(None)
        self.state.playlists = None

        playlists_basic.list_playlists(self.state)

        self.state.playlists = "NotList"
        playlists_basic.list_playlists(self.state)

        self.state.playlists = []
        playlists_basic.list_playlists(self.state)

        # Valid list with None item
        self.state.playlists = [self.pl, None]
        self.state.active_playlist_index = 0
        playlists_basic.list_playlists(self.state)

    def test_play_open_show_close_errors(self):
        """
        Expected Result: Navigation functions handle invalid states safely.
        Actual Result:
            [pl] Error: State is None.
            [pl] Error: State is None.
            [pl] No active playlist. Use /pl.open <name|index>.
            [pl] No active playlist. Use /pl.open or /pl.play <name>.
            [pl] Playlist 'Ghost' not found.
            [pl] No main library to return to.
            [pl] Already in main library.
        """
        # Show Current
        playlists_basic.show_current_playlist(None)
        self.state.active_playlist_index = None
        playlists_basic.show_current_playlist(self.state)
        # Play Active
        playlists_basic.play_active_playlist(self.state)
        # Play Selector
        playlists_basic.play_playlist(self.state, "Ghost")
        # Close
        del self.state.library_tracks
        playlists_basic.close_playlist(self.state)  # No library found
        self.state.library_tracks = []
        self.state.tracks = self.state.library_tracks
        playlists_basic.close_playlist(self.state)  # Already in main library