import unittest
from unittest.mock import MagicMock, patch
import io
import sys

from music_player.player_ui import print_playlist_with_indicator


class StubTrack:


    def __init__(self, name="Default"):
        self.display_name = name



class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.held_output = io.StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('music_player.player_ui._ensure_player_state')
    def test_PC_1_S1_State_Is_None(self, mock_ensure):
        mock_ensure.return_value = None
        print_playlist_with_indicator(MagicMock())
        self.assertEqual(self.held_output.getvalue().strip(), "")

    @patch('music_player.player_ui._ensure_player_state')
    def test_PC_2_S2_Invalid_Library_Type(self, mock_ensure):
        mock_state = MagicMock()
        mock_state.library_tracks = "NotAList"
        mock_ensure.return_value = mock_state

        print_playlist_with_indicator(mock_state)
        self.assertIn("[ui] Warning: Library is in an invalid state.", self.held_output.getvalue())

    @patch('music_player.player_ui._ensure_player_state')
    def test_PC_3_S3_Empty_Library(self, mock_ensure):
        mock_state = MagicMock()
        mock_state.library_tracks = []
        mock_ensure.return_value = mock_state

        print_playlist_with_indicator(mock_state)
        self.assertIn("[ui] Warning: Library is empty.", self.held_output.getvalue())

    @patch('music_player.player_ui.Track', new=StubTrack)
    @patch('music_player.player_ui._ensure_player_state')
    def test_PC_5_S7_Playing_Indicator(self, mock_ensure):
        real_track = StubTrack("Song A")

        mock_state = MagicMock()
        mock_state.library_tracks = [real_track]
        mock_state.current_track = real_track
        mock_state.is_playing = True

        mock_ensure.return_value = mock_state

        print_playlist_with_indicator(mock_state)
        self.assertIn("▶ 01: Song A", self.held_output.getvalue())

    @patch('music_player.player_ui.Track', new=StubTrack)
    @patch('music_player.player_ui._ensure_player_state')
    def test_PC_6_S8_Paused_Indicator(self, mock_ensure):
        real_track = StubTrack("Song B")

        mock_state = MagicMock()
        mock_state.library_tracks = [real_track]
        mock_state.current_track = real_track
        mock_state.is_playing = False
        mock_state.is_paused = True

        mock_ensure.return_value = mock_state

        print_playlist_with_indicator(mock_state)
        self.assertIn("‖ 01: Song B", self.held_output.getvalue())


if __name__ == '__main__':
    unittest.main()