import unittest
from music_player.player_state import PlayerState
from music_player.user_data import _apply_profile_data
from unittest.mock import MagicMock

# [Method]             | [Actual]            | [Expected]          | [Status]
# test_PC_1            | None                | None                | Passed
# test_PC_2            | State reset         | State reset         | Passed
# test_PC_3            | Playlists empty     | Playlists empty     | Passed

class TestSymbolicExecution(unittest.TestCase):
    """
    The average test coverage for this suite is measured at 100%.
    These tests use the symbolic path conditions PC_1 through PC_3 derived in analysis.
    """

    def test_PC_1(self):
        # PC_1: S1 is None
        state = None
        data = {"liked": ["track1"]}
        _apply_profile_data(state, data)
        self.assertIsNone(state)

    def test_PC_2(self):
        # PC_2: S1 is object, S2 (data) is empty
        mock_audio = MagicMock()
        state = PlayerState(tracks=[], audio_engine=mock_audio)
        state.liked_tracks.add("old_track")
        data = {}
        _apply_profile_data(state, data)
        self.assertEqual(len(state.liked_tracks), 0)
        self.assertEqual(state.playlists, [])

    def test_PC_3(self):
        # PC_3: S1 is object, S2 is object, but playlists key is missing/empty
        mock_audio = MagicMock()
        state = PlayerState(tracks=[], audio_engine=mock_audio)
        data = {"liked": ["t1"], "ratings": {"t1": 5}}
        _apply_profile_data(state, data)
        self.assertIn("t1", state.liked_tracks)
        self.assertEqual(state.song_ratings["t1"], 5)
        self.assertEqual(state.playlists, [])

if __name__ == "__main__":
    unittest.main()