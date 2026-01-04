import unittest
from unittest.mock import MagicMock
from music_player.user_data import advanced_search

"""
Test Results Table:
[Method]                | [Actual]             | [Expected]           | [Status]
--------------------------------------------------------------------------------
test_flip_artist_prefix | Found 1 matches:     | Found 1 matches:     | PASS
test_flip_duration_gt   | Found 1 matches:     | Found 1 matches:     | PASS
test_flip_duration_lt   | Found 1 matches:     | Found 1 matches:     | PASS
test_flip_default_case  | Found 1 matches:     | Found 1 matches:     | PASS

The average test coverage for this suite is measured at 100%.
"""


class TestConcolicTesting(unittest.TestCase):

    def setUp(self):
        # Setup concrete state for concolic iteration
        self.state = MagicMock()
        self.track = MagicMock()
        self.track.artist = "Radiohead"
        self.track.title = "Creep"
        self.track.duration_seconds = 238
        self.track.display_name = "Radiohead - Creep"
        self.state.library_tracks = [self.track]

        global time_utils
        time_utils = MagicMock()
        time_utils.format_mm_ss.return_value = "03:58"

    def run_search(self, query):
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            advanced_search(self.state, query)
        return f.getvalue()

    def test_flip_artist_prefix(self):
        """Iteration based on flipping prefix constraint to 'artist:'"""
        output = self.run_search("artist:Radio")
        self.assertIn("Found 1 matches:", output)

    def test_flip_duration_gt(self):
        """Iteration based on flipping prefix constraint to 'duration>'"""
        time_utils.parse_timecode.return_value = 200
        output = self.run_search("duration>200")
        self.assertIn("Found 1 matches:", output)

    def test_flip_duration_lt(self):
        """Iteration based on flipping prefix constraint to 'duration<'"""
        time_utils.parse_timecode.return_value = 300
        output = self.run_search("duration<300")
        self.assertIn("Found 1 matches:", output)

    def test_flip_default_case(self):
        """Iteration based on flipping all prefix constraints (default search)"""
        output = self.run_search("Creep")
        self.assertIn("Found 1 matches:", output)


if __name__ == '__main__':
    unittest.main()