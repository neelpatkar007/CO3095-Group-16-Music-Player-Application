import unittest
from unittest.mock import MagicMock, patch, mock_open
import sys
import io
from music_player import player_metrics

# Mock Classes

class MockTrack:
    """Mock object for a track."""
    def __init__(self, path, display_name="Unknown Title"):
        self.path = path
        self.display_name = display_name

class MockState:
    """Mock object for PlayerState."""
    def __init__(self):
        self.liked_tracks = set()
        self.play_counts = {}
        self.library_tracks = []
        self.current_track = None
# Test Class

class TestPlayerMetricsSpecs(unittest.TestCase):
    """
        Black-box specification-based test for player_metrics.py.
        Technique: Category Partition Method
        Tools: Python unittest + unittest.mock
        Source: playerMetrics.txt TSL Generatored Test Frames
    """

    def setUp(self):
        self.mock_state = MockState()
        self.captured_output = io.StringIO()
        self.sys_stdout = sys.stdout
        sys.stdout = self.captured_output

    def tearDown(self):
        sys.stdout = self.sys_stdout

    def get_output(self):
        """Helper to get printed output."""
        return self.captured_output.getvalue().strip()

    def test_case_01_state_none(self):
        """Test Case 1: Player State is None."""
        player_metrics.toggle_like(None)
        self.assertIn("[metrics] Error: State is None.", self.get_output())

        self.captured_output.truncate(0)
        self.captured_output.seek(0)

        player_metrics.show_liked_songs(None)
        self.assertIn("[metrics] Error: State is missing.", self.get_output())

    def test_case_02_liked_tracks_missing(self):
        """Test Case 2: Liked tracks attribute missing or None."""
        del self.mock_state.liked_tracks

        player_metrics.toggle_like(self.mock_state)
        self.assertTrue(hasattr(self.mock_state, 'liked_tracks'), "Should initialise missing liked_tracks")

        del self.mock_state.liked_tracks
        player_metrics.show_liked_songs(self.mock_state)
        self.assertIn("(No liked songs data)", self.get_output())

    def test_case_03_liked_tracks_corrupted(self):
        """Test Case 3: Liked tracks attribute corrupted."""
        self.mock_state.liked_tracks = ["Not", "A", "Set"]

        player_metrics.toggle_like(self.mock_state)
        self.assertIn("[metrics] Error: Liked tracks data corrupted.", self.get_output())

    def test_case_04_liked_tracks_empty(self):
        """Test Case 4: Liked tracks attribute empty set."""
        self.mock_state.liked_tracks = set()

        player_metrics.show_liked_songs(self.mock_state)
        self.assertIn("(No liked songs yet)", self.get_output())

    def test_case_05_play_counts_missing(self):
        """Test Case 5: Play counts attribute missing or None."""
        del self.mock_state.play_counts

        player_metrics.show_top_tracks(self.mock_state)
        self.assertIn("[metrics] No play history data available.", self.get_output())

    def test_case_06_play_counts_corrupted(self):
        """Test Case 6: Play counts attribute corrupted."""
        self.mock_state.play_counts = ["Not", "A", "Dict"]

        player_metrics.show_top_tracks(self.mock_state)
        self.assertIn("[metrics] Error: Play counts corrupted.", self.get_output())

    def test_case_07_play_counts_empty(self):
        """Test Case 7: Play counts dict empty."""
        self.mock_state.play_counts = {}

        player_metrics.show_top_tracks(self.mock_state)
        self.assertIn("[metrics] No play history yet.", self.get_output())

    def test_case_08_library_tracks_missing(self):
        """Test Case 8: Library tracks attribute missing or None."""
        del self.mock_state.library_tracks
        self.mock_state.liked_tracks = {'/some/path'}

        player_metrics.show_liked_songs(self.mock_state)
        self.assertIn("[metrics] Error: Library tracks missing.", self.get_output())

    def test_case_09_library_tracks_corrupted(self):
        """Test Case 9: Library tracks attribute corrupted."""
        self.mock_state.library_tracks = "Not A List"
        self.mock_state.liked_tracks = {'/some/path'}

        player_metrics.show_liked_songs(self.mock_state)
        self.assertIn("[metrics] Error: Library data corrupted.", self.get_output())

    def test_case_10_current_track_none(self):
        """Test Case 10: Current playing track is None."""
        self.mock_state.current_track = None

        player_metrics.toggle_like(self.mock_state)
        self.assertIn("[metrics] No track playing.", self.get_output())

    def test_case_11_track_no_path(self):
        """Test Case 11: Current playing rrack object has no path."""
        self.mock_state.current_track = MagicMock(spec=[])

        player_metrics.toggle_like(self.mock_state)
        self.assertIn("[metrics] Error: Track has no valid path.", self.get_output())

    def test_case_12_track_empty_path(self):
        """Test Case 12: Current playing Track path is empty string."""
        self.mock_state.current_track = MockTrack("")

        player_metrics.toggle_like(self.mock_state)
        self.assertIn("[metrics] Error: Track path is empty.", self.get_output())

    def test_case_13_play_count_logic_limit(self):
        """Test Case 13: Play count top 10 items are displayed."""
        # Generate 15 entries
        self.mock_state.play_counts = {f"/song{i}.mp3": i for i in range(1, 16)}
        self.mock_state.library_tracks = []

        player_metrics.show_top_tracks(self.mock_state)
        output = self.get_output()

        # Count lines generated for top tracks
        lines = [l for l in output.split('\n') if "plays:" in l]
        self.assertEqual(len(lines), 10, "Should strictly display top 10 tracks")

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_case_14_toggle_like_remove(self, mock_dump, mock_file):
        """Test Case 14: Toggle Like when a valid track is already in Likes."""
        path = "/music/song1.mp3"
        self.mock_state.current_track = MockTrack(path, "My Song")
        self.mock_state.liked_tracks = {path}

        player_metrics.toggle_like(self.mock_state)

        self.assertNotIn(path, self.mock_state.liked_tracks)
        self.assertIn("Unliked 'My Song'", self.get_output())
        # Verify save_data was called
        self.assertTrue(mock_dump.called)

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_case_15_toggle_like_add(self, mock_dump, mock_file):
        """Test Case 15: Toggle Like adding a valid track to Likes."""
        path = "/music/song2.mp3"
        self.mock_state.current_track = MockTrack(path, "New Song")
        self.mock_state.liked_tracks = set()

        player_metrics.toggle_like(self.mock_state)

        self.assertIn(path, self.mock_state.liked_tracks)
        self.assertIn("Liked 'New Song'", self.get_output())
        self.assertTrue(mock_dump.called)

    def test_case_16_show_liked_found_in_lib(self):
        """Test Case 16: Show liked songs exist in Library."""
        path = "/music/fav.mp3"
        self.mock_state.liked_tracks = {path}
        self.mock_state.library_tracks = [MockTrack(path, "Favorite Song")]

        player_metrics.show_liked_songs(self.mock_state)
        self.assertIn("♥ Favorite Song", self.get_output())

    def test_case_17_show_liked_missing_from_lib(self):
        """Test Case 17: Show liked song missing from Library."""
        path = "/music/deleted.mp3"
        self.mock_state.liked_tracks = {path}
        self.mock_state.library_tracks = [MockTrack("/music/other.mp3")]

        player_metrics.show_liked_songs(self.mock_state)
        self.assertIn("(Liked songs not found in current library scan)", self.get_output())

    def test_case_18_show_liked_no_display_name(self):
        """Test Case 18: Show liked songs song in Library with a missing display name."""
        path = "/music/unnamed.mp3"
        self.mock_state.liked_tracks = {path}
        self.mock_state.library_tracks = [MockTrack(path, None)]

        player_metrics.show_liked_songs(self.mock_state)
        self.assertIn("♥ Unknown Title", self.get_output())

    def test_case_19_top_tracks_invalid_counts(self):
        """Test Case 19: Show top tracks count is non-integer or negative/zero."""
        self.mock_state.play_counts = {"/song1.mp3": 0, "/song2.mp3": -5, "/song3.mp3": "bad"}
        self.mock_state.library_tracks = []

        player_metrics.show_top_tracks(self.mock_state)
        output = self.get_output()
        self.assertIn("--- Top Played Songs ---", output)
        self.assertNotIn("plays:", output, "Should not display invalid counts")

    def test_case_20_top_tracks_valid_limit(self):
        """Test Case 20: Show top tracks valid counts and less than 10 songs."""
        self.mock_state.play_counts = {"/song1.mp3": 5}
        self.mock_state.library_tracks = []

        player_metrics.show_top_tracks(self.mock_state)
        self.assertIn("5 plays:", self.get_output())

    def test_case_21_top_tracks_invalid_with_lib(self):
        """Test Case 21: Show top tracks invalid counts with library present."""
        path = "/song1.mp3"
        self.mock_state.play_counts = {path: 0}
        self.mock_state.library_tracks = [MockTrack(path, "Song One")]

        player_metrics.show_top_tracks(self.mock_state)
        self.assertNotIn("Song One", self.get_output())

    def test_case_22_top_tracks_invalid_no_lib(self):
        """Test Case 22: Show top tracks invalid counts, library missing."""
        path = "/song1.mp3"
        self.mock_state.play_counts = {path: -1}
        self.mock_state.library_tracks = []

        player_metrics.show_top_tracks(self.mock_state)
        self.assertNotIn("plays:", self.get_output())

    def test_case_23_top_tracks_invalid_no_name(self):
        """Test Case 23: Show top tracks with invalid counts and with no name track."""
        path = "/song1.mp3"
        self.mock_state.play_counts = {path: 0}
        self.mock_state.library_tracks = [MockTrack(path, None)]

        player_metrics.show_top_tracks(self.mock_state)
        self.assertNotIn("plays:", self.get_output())

    def test_case_24_top_tracks_valid_with_lib(self):
        """Test Case 24: Show top tracks with a valid track in library."""
        path = "/song1.mp3"
        self.mock_state.play_counts = {path: 10}
        self.mock_state.library_tracks = [MockTrack(path, "Hit Song")]

        player_metrics.show_top_tracks(self.mock_state)
        self.assertIn("10 plays: Hit Song", self.get_output())

    def test_case_25_top_tracks_valid_no_lib(self):
        """Test Case 25: Show top tracks with a valid track but not in library."""
        path = "/song1.mp3"
        self.mock_state.play_counts = {path: 10}
        self.mock_state.library_tracks = []

        player_metrics.show_top_tracks(self.mock_state)
        self.assertIn(f"10 plays: Unknown (File: {path})", self.get_output())

    def test_case_26_top_tracks_valid_no_name(self):
        """Test Case 26: Show top tracks with a valid track that has no name."""
        path = "/song1.mp3"
        self.mock_state.play_counts = {path: 10}
        self.mock_state.library_tracks = [MockTrack(path, None)]

        player_metrics.show_top_tracks(self.mock_state)
        self.assertIn("10 plays: Unknown", self.get_output())


if __name__ == '__main__':
    unittest.main()