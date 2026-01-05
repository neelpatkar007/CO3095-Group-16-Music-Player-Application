import unittest
from unittest.mock import MagicMock, patch
from music_player.player_queue import toggle_shuffle

# Dependency injection for context
class PlayerState:
    pass

class TestConcolicIntegration(unittest.TestCase):

    def setUp(self):
        # Patch the helper in its defining module, not __main__
        self.mock_get_tracks = patch('music_player.player_queue._get_tracks_safe').start()
        self.mock_print = patch('builtins.print').start()

    def tearDown(self):
        patch.stopall()

    def test_iteration_1_initial_seed(self):
        """Iteration 1: Concrete Seed (False, False, True). S1 is None."""
        toggle_shuffle(None)
        self.mock_print.assert_called_with("[queue] Error: State is null.")

    def test_iteration_2_derived_valid_obj(self):
        """Iteration 2: Flip (S1 is None) -> Valid Object. Missing tracks."""
        s1 = PlayerState()
        if hasattr(s1, 'tracks'): del s1.tracks

        toggle_shuffle(s1)
        self.mock_print.assert_called_with("[queue] Error: Tracks attribute missing.")

    def test_iteration_3_derived_empty_queue(self):
        """Iteration 3: Flip (hasattr). Valid tracks, Empty (S2=0)."""
        s1 = PlayerState()
        s1.tracks = []
        s1.shuffle_active = False
        self.mock_get_tracks.return_value = []

        toggle_shuffle(s1)
        # Verifies the branch where n == 0
        self.mock_print.assert_any_call("[queue] Note: Shuffle enabled on empty queue.")

    def test_iteration_4_derived_single_track(self):
        """Iteration 4: Flip (S2 == 0). Now S2=1."""
        s1 = PlayerState()
        s1.tracks = ["A"]
        s1.shuffle_active = False
        self.mock_get_tracks.return_value = ["A"]

        toggle_shuffle(s1)
        # Verifies the n=1 special message branch
        self.assertTrue(s1.shuffle_active)
        self.assertIn("(Limited effect: 1 song)", self.mock_print.call_args[0][0])

    def test_iteration_5_derived_boundary_index(self):
        """Iteration 5: Flip (S2 == 1). Now S2=2, S4=3 (Derived Out of Bounds)."""
        s1 = PlayerState()
        s1.tracks = ["A", "B"]
        s1.shuffle_active = False
        s1.current_index = 3  # Derived constraint S4 >= S2
        self.mock_get_tracks.return_value = ["A", "B"]

        toggle_shuffle(s1)
        # Verifies the Critical Safety Logic: Resetting index
        self.assertEqual(s1.current_index, 0)
        self.mock_print.assert_any_call("[queue] Reset index to 0.")

    def test_iteration_6_derived_toggle_off(self):
        """Iteration 6: Flip (NOT S3). Now S3=True (Shuffle already ON)."""
        s1 = PlayerState()
        s1.tracks = ["A", "B"]
        s1.shuffle_active = True  # Starting as True, so it toggles to False
        s1.loop_mode = "off"
        self.mock_get_tracks.return_value = ["A", "B"]

        toggle_shuffle(s1)
        # Verifies the ELSE branch of the main toggle
        self.assertFalse(s1.shuffle_active)
        self.mock_print.assert_any_call("[queue] Shuffle: OFF")

    def test_iteration_7_derived_loop_mode(self):
        """Iteration 7: Flip (S5 != 'one'). Now S5='one'."""
        s1 = PlayerState()
        s1.tracks = ["A", "B"]
        s1.shuffle_active = True
        s1.loop_mode = "one"
        self.mock_get_tracks.return_value = ["A", "B"]

        toggle_shuffle(s1)
        # Verifies the nested loop mode warning logic
        self.mock_print.assert_any_call("[queue] (Loop One remains active)")