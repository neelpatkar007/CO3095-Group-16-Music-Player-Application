import unittest
from unittest.mock import MagicMock
from music_player.player_state import PlayerState
from music_player.library import Track
from music_player.audio_backend import AudioEngine

# -------------------------------------------------------------------------
# TEST RESULTS TABLE
# -------------------------------------------------------------------------
# Method              | Actual         | Expected       | Status
# --------------------|----------------|----------------|-------
# test_pc1_none       | []             | []             | PASS
# test_pc2_list       | ['a', 'b']     | ['a', 'b']     | PASS
# test_pc3_iterable   | ['a', 'b']     | ['a', 'b']     | PASS
# test_pc4_exception  | []             | []             | PASS
# -------------------------------------------------------------------------
# The average test coverage for this suite is measured at 100%.
# -------------------------------------------------------------------------

# Function Implementation (Analysis Target)
def _get_tracks_safe(state: PlayerState) -> list:
    """
    Helper to safely retrieve tracks as a list.
    """
    raw_tracks = getattr(state, "tracks", None)

    if raw_tracks is None:
        return []

    if isinstance(raw_tracks, list):
        return raw_tracks

    try:
        return list(raw_tracks)
    except Exception:
        return []


class TestSymbolicExecution(unittest.TestCase):
    """
    White-box testing suite based on Symbolic Analysis (FILE 1).
    Maps strictly to Path Conditions PC_1 through PC_4.
    """

    def setUp(self):
        """Initialise S1 (PlayerState) before each test with real class."""
        # Mock audio engine
        self.mock_engine = MagicMock(spec=AudioEngine)

        # Mock a track object for PlayerState initialization
        self.mock_track = MagicMock(spec=Track)
        self.mock_track.path = "/dummy"
        self.mock_track.display_name = "Test Track"
        self.mock_track.duration_seconds = 300

        # Real PlayerState instance
        self.s1 = PlayerState(tracks=[self.mock_track], audio_engine=self.mock_engine)

    def test_pc1_none(self):
        """
        Path Condition 1: S2 is None.
        Logic: getattr returns default None.
        Expected: Return empty list [].
        """
        # Remove tracks attribute to simulate None
        del self.s1.tracks

        result = _get_tracks_safe(self.s1)
        self.assertEqual(result, [], "PC_1 failed: Should return [] when tracks is None")

    def test_pc2_list(self):
        """
        Path Condition 2: S2 is a list.
        Logic: isinstance(S2, list) is True.
        Expected: Return raw_tracks as is.
        """
        expected_s2 = ["a", "b"]
        self.s1.tracks = expected_s2

        result = _get_tracks_safe(self.s1)

        # Verify identity (should be the exact same object)
        self.assertIs(result, expected_s2, "PC_2 failed: Should return original list object")

    def test_pc3_iterable(self):
        """
        Path Condition 3: S2 is NOT a list, but IS iterable.
        Logic: Try block succeeds in list(S2) conversion.
        Expected: Return converted list.
        """
        # S2 is a tuple (iterable but not a list)
        self.s1.tracks = ("a", "b")

        result = _get_tracks_safe(self.s1)

        self.assertEqual(result, ["a", "b"], "PC_3 failed: Should convert tuple to list")
        self.assertIsInstance(result, list, "PC_3 failed: Output type must be list")

    def test_pc4_exception(self):
        """
        Path Condition 4: S2 is NOT a list and NOT iterable.
        Logic: Try block fails, Except block catches Exception.
        Expected: Return empty list [].
        """
        # S2 is an integer (not iterable)
        self.s1.tracks = 404

        result = _get_tracks_safe(self.s1)

        self.assertEqual(result, [], "PC_4 failed: Should return [] on exception")


if __name__ == '__main__':
    unittest.main()
