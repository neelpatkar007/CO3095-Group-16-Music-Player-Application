import unittest
from unittest.mock import MagicMock
from music_player.player_seek import seek_to


class TestConcolicTesting(unittest.TestCase):
    def test_pc1_iteration1_flip(self):
        seek_to(None, 20.0)

    def test_pc5_iteration4_no_engine(self):
        from music_player.library import Track

        class State:
            pass

        s1 = State()
        mock_track = MagicMock(spec=Track)
        mock_track.duration_seconds = 50.0
        s1.current_track = mock_track

        seek_to(s1, 10.0)
        self.assertFalse(hasattr(s1, "audio_engine"))
        self.assertFalse(hasattr(s1, "position_seconds"))

    def test_pc6_clamping_logic(self):
        """Derived input to test boundary: new_pos > duration"""
        from music_player.library import Track

        class State:
            pass

        s1 = State()
        mock_track = MagicMock(spec=Track)
        mock_track.duration_seconds = 50.0
        s1.current_track = mock_track
        s1.audio_engine = MagicMock()

        seek_to(s1, 100.0)  # S4 > S3

        self.assertEqual(s1.position_seconds, 50.0)
        s1.audio_engine.seek.assert_called_once_with(50.0)


if __name__ == "__main__":
    unittest.main()