import unittest
from unittest.mock import MagicMock
from music_player.player_state import PlayerState
from music_player.user_data import _apply_profile_data

class TestConcolicTesting(unittest.TestCase):

    def test_PC_4_iteration(self):
        mock_audio = MagicMock()
        state = PlayerState(tracks=[], audio_engine=mock_audio)
        data = {
            "playlists": [{"name": "Rock", "tracks": ["path/to/song"]}]
        }
        _apply_profile_data(state, data)
        self.assertEqual(len(state.playlists), 1)
        self.assertEqual(state.playlists[0].name, "Rock")

    def test_nested_lookup_logic(self):
        class MockTrack:
            def __init__(self, path):
                self.path = path

        mock_audio = MagicMock()
        t1 = MockTrack("path/1")
        state = PlayerState(tracks=[t1], audio_engine=mock_audio)

        data = {
            "playlists": [{"name": "MyList", "tracks": ["path/1"]}]
        }

        _apply_profile_data(state, data)
        self.assertEqual(len(state.playlists[0].tracks), 1)
        self.assertEqual(state.playlists[0].tracks[0].path, "path/1")


if __name__ == "__main__":
    unittest.main()