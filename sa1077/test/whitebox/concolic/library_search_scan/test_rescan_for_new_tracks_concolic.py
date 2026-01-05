import unittest
from unittest.mock import MagicMock, patch
import sys
import io
from music_player.player_state import PlayerState
from music_player.library_search_scan import rescan_for_new_tracks


class TestConcolicGenerations(unittest.TestCase):

    def setUp(self):
        self.held_output = io.StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = self.original_stdout

    def test_iteration_1_base_constraint(self):
        s1_seed = None
        rescan_for_new_tracks(s1_seed)
        self.assertIn("Error: State is None", self.held_output.getvalue())

    @patch('music_player.library_search_scan.discover_tracks')
    def test_iteration_2_flip_null_check(self, mock_discover):
        mock_audio_engine = MagicMock()
        s1_seed = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        mock_discover.return_value = []

        rescan_for_new_tracks(s1_seed)

        output = self.held_output.getvalue()
        self.assertIn("Scanning for new tracks...", output)
        self.assertIn("No files found on disk", output)

    @patch('music_player.library_search_scan.discover_tracks')
    def test_iteration_3_flip_discovery_check(self, mock_discover):
        mock_audio_engine = MagicMock()
        s1_seed = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        track_a = MagicMock()
        track_a.path = "A.mp3"
        s1_seed.library_tracks = [track_a]
        mock_discover.return_value = [track_a]
        rescan_for_new_tracks(s1_seed)

        output = self.held_output.getvalue()
        self.assertIn("No new tracks found", output)

    @patch('music_player.library_search_scan.discover_tracks')
    def test_iteration_4_flip_new_tracks_check(self, mock_discover):
        mock_audio_engine = MagicMock()
        s1_seed = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        track_b = MagicMock()
        track_b.path = "B.mp3"
        mock_discover.return_value = [track_b]
        rescan_for_new_tracks(s1_seed)

        output = self.held_output.getvalue()
        self.assertIn("Added 1 new tracks", output)
        self.assertEqual(len(s1_seed.library_tracks), 1)


if __name__ == '__main__':
    unittest.main()