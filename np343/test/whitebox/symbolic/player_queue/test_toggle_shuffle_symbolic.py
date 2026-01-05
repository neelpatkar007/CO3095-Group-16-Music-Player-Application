import unittest
from unittest.mock import MagicMock, patch
from music_player.player_queue import toggle_shuffle
from music_player.player_queue import PlayerState
from music_player.player_queue import _get_tracks_safe


class PlayerState:
    pass


class TestSymbolicExecution(unittest.TestCase):
    def setUp(self):
        self.mock_get_tracks = patch('music_player.player_queue._get_tracks_safe').start()
        self.mock_print = patch('builtins.print').start()

    def tearDown(self):
        patch.stopall()

    def test_pc_1_invalid_state(self):
        toggle_shuffle(None)
        self.mock_print.assert_called_with("[queue] Error: State is null.")

        toggle_shuffle(12345)
        self.mock_print.assert_called_with("[queue] Error: State is null.")

    def test_pc_2_missing_tracks(self):
        s1 = PlayerState()
        if hasattr(s1, 'tracks'): del s1.tracks

        toggle_shuffle(s1)
        self.mock_print.assert_called_with("[queue] Error: Tracks attribute missing.")

    def test_pc_3_empty_queue_toggle(self):
        s1 = PlayerState()
        s1.tracks = []
        s1.shuffle_active = False
        self.mock_get_tracks.return_value = []

        toggle_shuffle(s1)

        self.assertTrue(s1.shuffle_active)
        self.mock_print.assert_any_call("[queue] Note: Shuffle enabled on empty queue.")

    def test_pc_4_single_track_msg(self):
        s1 = PlayerState()
        s1.tracks = ["song1"]
        s1.shuffle_active = False
        self.mock_get_tracks.return_value = ["song1"]

        toggle_shuffle(s1)

        self.assertTrue(s1.shuffle_active)
        self.mock_print.assert_any_call("[queue] Shuffle: ON (Limited effect: 1 song)")

    def test_pc_5_index_reset_logic(self):
        s1 = PlayerState()
        s1.tracks = ["a", "b"]
        s1.shuffle_active = False
        s1.current_index = 3
        self.mock_get_tracks.return_value = ["a", "b"]

        toggle_shuffle(s1)

        self.assertTrue(s1.shuffle_active)
        self.assertEqual(s1.current_index, 0)
        self.mock_print.assert_any_call("[queue] Reset index to 0.")

    def test_pc_6_valid_index_no_reset(self):
        s1 = PlayerState()
        s1.tracks = ["a", "b"]
        s1.shuffle_active = False  # S3
        s1.current_index = 0  # S4 < S2
        self.mock_get_tracks.return_value = ["a", "b"]

        toggle_shuffle(s1)

        self.assertTrue(s1.shuffle_active)
        self.assertEqual(s1.current_index, 0)
        with self.assertRaises(AssertionError):
            self.mock_print.assert_any_call("[queue] Reset index to 0.")

    def test_pc_7_shuffle_off_loop_one(self):
        s1 = PlayerState()
        s1.tracks = ["a", "b"]
        s1.shuffle_active = True
        s1.loop_mode = "one"
        self.mock_get_tracks.return_value = ["a", "b"]

        toggle_shuffle(s1)

        self.assertFalse(s1.shuffle_active)
        self.mock_print.assert_any_call("[queue] Shuffle: OFF")
        self.mock_print.assert_any_call("[queue] (Loop One remains active)")

    def test_pc_8_shuffle_off_standard(self):
        s1 = PlayerState()
        s1.tracks = ["a", "b"]
        s1.shuffle_active = True
        s1.loop_mode = "off"
        self.mock_get_tracks.return_value = ["a", "b"]

        toggle_shuffle(s1)

        self.assertFalse(s1.shuffle_active)
        self.mock_print.assert_any_call("[queue] Shuffle: OFF")
        with self.assertRaises(AssertionError):
            self.mock_print.assert_any_call("[queue] (Loop One remains active)")