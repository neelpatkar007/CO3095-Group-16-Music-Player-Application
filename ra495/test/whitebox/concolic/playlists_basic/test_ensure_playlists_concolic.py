import unittest
from io import StringIO
import sys
from music_player.playlists_basic import _ensure_playlists

class PlayerState:
    pass

class TestConcolicExecution(unittest.TestCase):

    def setUp(self):
        self.captured_output = StringIO()
        sys.stdout = self.captured_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_iteration_1_base_case(self):
        s1 = None

        _ensure_playlists(s1)

        self.assertIn("[pl] Error", self.captured_output.getvalue())

    def test_iteration_2_negate_s1(self):
        s1 = PlayerState()
        if hasattr(s1, 'playlists'):
            del s1.playlists

        _ensure_playlists(s1)

        self.assertIn("[pl] Error", self.captured_output.getvalue())

    def test_iteration_3_negate_s2(self):
        s1 = PlayerState()
        s1.playlists = None

        _ensure_playlists(s1)

        self.assertEqual(s1.playlists, [])

    def test_iteration_4_negate_s3(self):
        s1 = PlayerState()
        s1.playlists = ["existing_data"]

        _ensure_playlists(s1)

        self.assertEqual(s1.playlists, ["existing_data"])


if __name__ == '__main__':
    unittest.main()