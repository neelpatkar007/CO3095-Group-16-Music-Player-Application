import unittest
from unittest.mock import MagicMock
from music_player.player_state import PlayerState
from music_player.library import Track
from music_player.audio_backend import AudioEngine

def _get_tracks_safe(state: PlayerState) -> list:
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
    def setUp(self):
        """Initialise S1 (PlayerState) before each test with real class."""
        self.mock_engine = MagicMock(spec=AudioEngine)

        self.mock_track = MagicMock(spec=Track)
        self.mock_track.path = "/dummy"
        self.mock_track.display_name = "Test Track"
        self.mock_track.duration_seconds = 300

        self.s1 = PlayerState(tracks=[self.mock_track], audio_engine=self.mock_engine)

    def test_pc1_none(self):
        del self.s1.tracks

        result = _get_tracks_safe(self.s1)
        self.assertEqual(result, [], "PC_1 failed: Should return [] when tracks is None")

    def test_pc2_list(self):
        expected_s2 = ["a", "b"]
        self.s1.tracks = expected_s2

        result = _get_tracks_safe(self.s1)

        self.assertIs(result, expected_s2, "PC_2 failed: Should return original list object")

    def test_pc3_iterable(self):
        self.s1.tracks = ("a", "b")

        result = _get_tracks_safe(self.s1)

        self.assertEqual(result, ["a", "b"], "PC_3 failed: Should convert tuple to list")
        self.assertIsInstance(result, list, "PC_3 failed: Output type must be list")

    def test_pc4_exception(self):
        self.s1.tracks = 404

        result = _get_tracks_safe(self.s1)

        self.assertEqual(result, [], "PC_4 failed: Should return [] on exception")


if __name__ == '__main__':
    unittest.main()
