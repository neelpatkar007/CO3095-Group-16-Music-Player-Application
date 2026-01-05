import unittest
from unittest.mock import MagicMock
from music_player.player_seek import seek_to


class Track:
    def __init__(self, duration=None):
        if duration is not None:
            self.duration_seconds = duration


class PlayerState:
    def __init__(self):
        self.current_track = None
        self.position_seconds = 0.0


class TestSymbolicExecution(unittest.TestCase):
    def test_pc1_none_state(self):
        self.assertIsNone(seek_to(None, 10.0))

    def test_pc3_invalid_track_type(self):

        s1 = PlayerState()
        s1.current_track = "Not A Track"
        seek_to(s1, 10.0)
        self.assertEqual(s1.position_seconds, 0.0)

    def test_pc6_successful_seek(self):
        from music_player.library import Track as LibTrack

        s1 = PlayerState()
        track = MagicMock(spec=LibTrack)
        track.duration_seconds = 60.0
        s1.current_track = track
        s1.audio_engine = MagicMock()

        s4 = 15.0  # Symbolic S4
        seek_to(s1, s4)

        self.assertEqual(s1.position_seconds, 15.0)
        s1.audio_engine.seek.assert_called_once_with(15.0)


if __name__ == "__main__":
    unittest.main()