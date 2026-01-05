import unittest
from unittest.mock import MagicMock
from music_player.user_data import advanced_search
import io
from contextlib import redirect_stdout

class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        global time_utils
        time_utils = MagicMock()
        time_utils.parse_timecode.return_value = 180
        time_utils.format_mm_ss.return_value = "03:00"

    def test_pc1_invalid_state(self):
        f = io.StringIO()
        with redirect_stdout(f):
            advanced_search(None, "artist:test")
        self.assertIn("[search] Error: Invalid state.", f.getvalue())

    def test_pc3_invalid_query(self):
        state = MagicMock()
        state.library_tracks = []

        f = io.StringIO()
        with redirect_stdout(f):
            advanced_search(state, "")
        self.assertIn("[search] Usage: /advanced.search <query>", f.getvalue())

    def test_pc5_no_results(self):
        state = MagicMock()
        track = MagicMock()
        track.artist = "Real Artist"
        state.library_tracks = [track]

        f = io.StringIO()
        with redirect_stdout(f):
            advanced_search(state, "artist:NonExistent")
        self.assertIn("[search] No matches found.", f.getvalue())

    def test_pc6_successful_filter(self):
        state = MagicMock()
        track = MagicMock()
        track.artist = "Linkin Park"
        track.display_name = "In the End"
        track.duration_seconds = 216
        state.library_tracks = [track]

        f = io.StringIO()
        with redirect_stdout(f):
            advanced_search(state, "artist:Linkin")
        self.assertIn("Found 1 matches:", f.getvalue())


if __name__ == '__main__':
    unittest.main()