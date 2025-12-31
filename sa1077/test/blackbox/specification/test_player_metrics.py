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