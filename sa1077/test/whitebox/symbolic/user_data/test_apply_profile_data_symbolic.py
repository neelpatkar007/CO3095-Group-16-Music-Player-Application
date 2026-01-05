import unittest
from music_player.player_state import PlayerState
from music_player.user_data import _apply_profile_data
from unittest.mock import MagicMock

class TestSymbolicExecution(unittest.TestCase):
    def test_PC_1(self):
        state = None
        data = {"liked": ["track1"]}
        _apply_profile_data(state, data)
        self.assertIsNone(state)

    def test_PC_2(self):
        mock_audio = MagicMock()
        state = PlayerState(tracks=[], audio_engine=mock_audio)
        state.liked_tracks.add("old_track")
        data = {}
        _apply_profile_data(state, data)
        self.assertEqual(len(state.liked_tracks), 0)
        self.assertEqual(state.playlists, [])

    def test_PC_3(self):
        mock_audio = MagicMock()
        state = PlayerState(tracks=[], audio_engine=mock_audio)
        data = {"liked": ["t1"], "ratings": {"t1": 5}}
        _apply_profile_data(state, data)
        self.assertIn("t1", state.liked_tracks)
        self.assertEqual(state.song_ratings["t1"], 5)
        self.assertEqual(state.playlists, [])

if __name__ == "__main__":
    unittest.main()