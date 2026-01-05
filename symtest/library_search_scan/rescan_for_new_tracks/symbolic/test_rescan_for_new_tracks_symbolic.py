import unittest
from unittest.mock import MagicMock, patch
import sys
import io
from music_player.player_state import PlayerState
from music_player.library_search_scan import rescan_for_new_tracks

class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.held_output = io.StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = self.original_stdout

    def test_pc1_state_none(self):
        state = None
        rescan_for_new_tracks(state)
        output = self.held_output.getvalue()
        self.assertIn("Error: State is None", output)

    @patch('music_player.library_search_scan.discover_tracks')
    def test_pc2_no_files(self, mock_discover):
        mock_audio_engine = MagicMock()
        state = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        mock_discover.return_value = []

        rescan_for_new_tracks(state)

        output = self.held_output.getvalue()
        self.assertIn("Scanning for new tracks...", output)
        self.assertIn("No files found on disk", output)

    @patch('music_player.library_search_scan.discover_tracks')
    def test_pc3_no_new(self, mock_discover):
        mock_audio_engine = MagicMock()
        state = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        t1 = MagicMock()
        t1.path = "song1.mp3"
        state.library_tracks = [t1]
        t2 = MagicMock()
        t2.path = "song1.mp3"
        mock_discover.return_value = [t2]
        rescan_for_new_tracks(state)

        output = self.held_output.getvalue()
        self.assertIn("No new tracks found", output)
        self.assertEqual(len(state.library_tracks), 1)

    @patch('music_player.library_search_scan.discover_tracks')
    def test_pc4_success(self, mock_discover):
        mock_audio_engine = MagicMock()
        state = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        state.library_tracks = []
        new_track = MagicMock()
        new_track.path = "song_new.mp3"
        mock_discover.return_value = [new_track]
        rescan_for_new_tracks(state)

        output = self.held_output.getvalue()
        self.assertIn("Added 1 new tracks", output)
        self.assertEqual(len(state.library_tracks), 1)
        self.assertEqual(state.library_tracks[0].path, "song_new.mp3")


if __name__ == '__main__':
    unittest.main()