import unittest
from unittest.mock import MagicMock, patch
from io import StringIO
import sys
from music_player.playlists_basic import list_playlists

class TestConcolicExecution(unittest.TestCase):
    def setUp(self):
        self.captured_output = StringIO()
        sys.stdout = self.captured_output
        self.mock_ensure = patch('music_player.playlists_basic._ensure_playlists').start()
        self.mock_summary = patch('music_player.playlists_basic._get_playlist_summary').start()
        self.mock_format = patch('music_player.playlists_basic.format_mm_ss').start()

    def tearDown(self):
        patch.stopall()
        sys.stdout = sys.__stdout__

    def test_iteration_01_seed_null(self):
        list_playlists(None)
        self.assertIn("State is missing", self.captured_output.getvalue())

    def test_iteration_02_flip_state_existence(self):
        S1 = MagicMock()
        object.__setattr__(S1, 'playlists', None)

        list_playlists(S1)
        self.assertEqual("", self.captured_output.getvalue().strip())

    def test_iteration_03_flip_playlist_existence(self):
        S1 = MagicMock()
        S1.playlists = 12345

        list_playlists(S1)
        self.assertIn("data is corrupted", self.captured_output.getvalue())

    def test_iteration_04_flip_type_check(self):
        S1 = MagicMock()
        S1.playlists = []

        list_playlists(S1)
        self.assertIn("No playlists defined", self.captured_output.getvalue())

    def test_iteration_05_flip_list_content(self):
        S1 = MagicMock()
        S1.playlists = [None]

        list_playlists(S1)
        self.assertIn("Invalid Playlist", self.captured_output.getvalue())

    def test_iteration_06_flip_element_validity(self):
        S1 = MagicMock()
        pl = MagicMock()
        pl.name = "Concolic Hits"
        S1.playlists = [pl]
        S1.active_playlist_index = None

        self.mock_summary.return_value = (10, 600)
        self.mock_format.return_value = "10:00"

        list_playlists(S1)

        output = self.captured_output.getvalue()
        self.assertIn("Concolic Hits", output)
        self.assertNotIn("*", output)
        self.assertIn("songs", output)

    def test_iteration_07_flip_active_and_plurality(self):
        S1 = MagicMock()
        pl = MagicMock()
        pl.name = "Deep Path"
        S1.playlists = [pl]
        S1.active_playlist_index = 0

        self.mock_summary.return_value = (1, 120)
        self.mock_format.return_value = "02:00"

        self.captured_output.truncate(0)
        self.captured_output.seek(0)

        list_playlists(S1)

        output = self.captured_output.getvalue()
        self.assertIn("Deep Path*", output)
        self.assertIn("1 song", output)
