import unittest
from unittest.mock import MagicMock, patch
import io
import sys

from music_player.player_ui import print_playlist_with_indicator

class StubTrack:

    def __init__(self, name="Default"):
        self.display_name = name

class TestConcolicExecution(unittest.TestCase):

    def setUp(self):
        self.held_output = io.StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('music_player.player_ui.Track', new=StubTrack)
    @patch('music_player.player_ui._ensure_player_state')
    def test_iteration_4_flip_S3_derive_S6_false(self, mock_ensure):
        real_track = StubTrack("Concolic Track")

        mock_state = MagicMock()
        mock_state.library_tracks = [real_track]
        mock_state.current_track = None

        mock_ensure.return_value = mock_state

        print_playlist_with_indicator(mock_state)
        self.assertIn("  01: Concolic Track", self.held_output.getvalue())

    @patch('music_player.player_ui.Track', new=StubTrack)
    @patch('music_player.player_ui._ensure_player_state')
    def test_iteration_5_flip_S6_derive_S7_true(self, mock_ensure):
        real_track = StubTrack("Concolic Track")

        mock_state = MagicMock()
        mock_state.library_tracks = [real_track]
        mock_state.current_track = real_track
        mock_state.is_playing = True

        mock_ensure.return_value = mock_state

        print_playlist_with_indicator(mock_state)
        self.assertIn("▶ 01: Concolic Track", self.held_output.getvalue())

    @patch('music_player.player_ui.Track', new=StubTrack)
    @patch('music_player.player_ui._ensure_player_state')
    def test_iteration_7_flip_S8_derive_stop(self, mock_ensure):
        real_track = StubTrack("Concolic Track")

        mock_state = MagicMock()
        mock_state.library_tracks = [real_track]
        mock_state.current_track = real_track
        mock_state.is_playing = False
        mock_state.is_paused = False

        mock_ensure.return_value = mock_state

        print_playlist_with_indicator(mock_state)
        self.assertIn("• 01: Concolic Track", self.held_output.getvalue())

    @patch('music_player.player_ui.Track', new=StubTrack)
    @patch('music_player.player_ui._ensure_player_state')
    def test_metadata_and_single_track_warnings(self, mock_ensure):
        real_track = StubTrack("")

        mock_state = MagicMock()
        mock_state.library_tracks = [real_track]
        mock_state.current_track = None

        mock_ensure.return_value = mock_state

        print_playlist_with_indicator(mock_state)
        output = self.held_output.getvalue()

        self.assertIn("Warning: Some tracks have missing titles", output)
        self.assertIn("Note: Only one track in the library", output)

if __name__ == '__main__':
    unittest.main()