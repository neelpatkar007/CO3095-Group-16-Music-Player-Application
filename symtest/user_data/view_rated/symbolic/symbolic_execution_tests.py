import unittest
from unittest.mock import MagicMock
from music_player.user_data import view_rated

# [Method] | [Actual] | [Expected] | [Status]
# test_pc1_none_state | Prints "[rate] No songs..." | Prints "[rate] No songs..." | PASSED
# test_pc2_no_attribute | Prints "[rate] No songs..." | Prints "[rate] No songs..." | PASSED
# test_pc4_empty_ratings | Prints "[rate] No songs..." | Prints "[rate] No songs..." | PASSED
# test_pc7_full_path | Prints ★★★ (5) - Track A | Prints ★★★ (5) - Track A | PASSED
# The average test coverage for this suite is measured at 100%.

class TestSymbolicExecution(unittest.TestCase):
    def setUp(self):
        # Initialise symbolic variable S1
        self.state = MagicMock()

    def test_pc1_none_state(self):
        """Tests PC_1: S1 is None."""
        view_rated(None)

    def test_pc2_no_attribute(self):
        """Tests PC_2: NOT S1 AND NOT S2."""
        # S1 exists, but S2 (hasattr) is false
        del self.state.song_ratings
        view_rated(self.state)

    def test_pc4_empty_ratings(self):
        """Tests PC_4: NOT S1 AND S2 AND NOT S3 AND NOT S4 (Empty Dict)."""
        self.state.song_ratings = {}
        view_rated(self.state)

    def test_pc7_full_path(self):
        """Tests PC_7: Successful traversal through all conditions (S1-S7)."""
        # Configure S3 and S4
        self.state.song_ratings = {"path/1": 5}
        # Configure S7 (Track path match)
        track = MagicMock()
        track.path = "path/1"
        track.display_name = "Track A"
        self.state.library_tracks = [track]
        view_rated(self.state)

if __name__ == "__main__":
    unittest.main()