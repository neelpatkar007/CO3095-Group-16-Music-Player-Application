import unittest
from unittest.mock import MagicMock, patch
from music_player.player_queue import toggle_shuffle

class PlayerState:
    pass

class TestConcolicIntegration(unittest.TestCase):

    def setUp(self):
        self.mock_get_tracks = patch('music_player.player_queue._get_tracks_safe').start()
        self.mock_print = patch('builtins.print').start()

    def tearDown(self):
        patch.stopall()

    def test_iteration_1_initial_seed(self):
        toggle_shuffle(None)
        self.mock_print.assert_called_with("[queue] Error: State is null.")

    def test_iteration_2_derived_valid_obj(self):
        s1 = PlayerState()
        if hasattr(s1, 'tracks'): del s1.tracks

        toggle_shuffle(s1)
        self.mock_print.assert_called_with("[queue] Error: Tracks attribute missing.")

    def test_iteration_3_derived_empty_queue(self):
        s1 = PlayerState()
        s1.tracks = []
        s1.shuffle_active = False
        self.mock_get_tracks.return_value = []

        toggle_shuffle(s1)
        self.mock_print.assert_any_call("[queue] Note: Shuffle enabled on empty queue.")

    def test_iteration_4_derived_single_track(self):
        s1 = PlayerState()
        s1.tracks = ["A"]
        s1.shuffle_active = False
        self.mock_get_tracks.return_value = ["A"]

        toggle_shuffle(s1)
        # Verifies the n=1 special message branch
        self.assertTrue(s1.shuffle_active)
        self.assertIn("(Limited effect: 1 song)", self.mock_print.call_args[0][0])

    def test_iteration_5_derived_boundary_index(self):
        s1 = PlayerState()
        s1.tracks = ["A", "B"]
        s1.shuffle_active = False
        s1.current_index = 3
        self.mock_get_tracks.return_value = ["A", "B"]

        toggle_shuffle(s1)
        self.assertEqual(s1.current_index, 0)
        self.mock_print.assert_any_call("[queue] Reset index to 0.")

    def test_iteration_6_derived_toggle_off(self):
        s1 = PlayerState()
        s1.tracks = ["A", "B"]
        s1.shuffle_active = True
        s1.loop_mode = "off"
        self.mock_get_tracks.return_value = ["A", "B"]

        toggle_shuffle(s1)
        self.assertFalse(s1.shuffle_active)
        self.mock_print.assert_any_call("[queue] Shuffle: OFF")

    def test_iteration_7_derived_loop_mode(self):
        s1 = PlayerState()
        s1.tracks = ["A", "B"]
        s1.shuffle_active = True
        s1.loop_mode = "one"
        self.mock_get_tracks.return_value = ["A", "B"]

        toggle_shuffle(s1)
        self.mock_print.assert_any_call("[queue] (Loop One remains active)")