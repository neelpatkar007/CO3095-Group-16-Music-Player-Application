import unittest
from unittest.mock import MagicMock
from music_player.playlists_advanced import _get_playlist


class TestConcolicTesting(unittest.TestCase):
    def setUp(self):
        self.p1 = MagicMock()
        self.p1.name = "Chill"
        self.valid_state = MagicMock(playlists=[self.p1])

    def test_iteration_1(self):
        result = _get_playlist(None, "1")
        self.assertIsNone(result)

    def test_iteration_2(self):
        result = _get_playlist(self.valid_state, "")
        self.assertIsNone(result)

    def test_iteration_3(self):
        empty_state = MagicMock(playlists=[])
        result = _get_playlist(empty_state, "1")
        self.assertIsNone(result)

    def test_iteration_4(self):
        result = _get_playlist(self.valid_state, "1")
        self.assertEqual(result, self.p1)

    def test_iteration_5(self):
        result = _get_playlist(self.valid_state, "NonExistent")
        self.assertIsNone(result)

    def test_iteration_6(self):
        result = _get_playlist(self.valid_state, "Chill")
        self.assertEqual(result, self.p1)


if __name__ == "__main__":
    unittest.main()