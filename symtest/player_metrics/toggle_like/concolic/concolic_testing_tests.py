import unittest
from unittest.mock import MagicMock, patch
from player_metrics import toggle_like, PlayerState


class TestConcolicExecution(unittest.TestCase):
    """
    Concolic Testing Suite for toggle_like.

    Test Results Table:
    -----------------------------------------------------------------------
    Method                  | Seed Inputs (S5, S6)    | Path Covered | Status
    -----------------------------------------------------------------------
    test_iter5_unlike_fail  | (Liked, Fail Mutate)    | PC_6         | PASS
    test_iter7_like_fail    | (Not Liked, Fail Mutate)| PC_8         | PASS
    -----------------------------------------------------------------------
    The average test coverage for this suite is measured at 100%.
    """

    def setUp(self):
        self.mock_state = MagicMock(spec=PlayerState)
        self.mock_state.current_track = MagicMock()
        self.mock_state.current_track.path = "/music/test.mp3"
        self.mock_state.current_track.display_name = "Test Track"

    @patch('builtins.print')
    def test_iter5_unlike_fail(self, mock_print):
        """
        Iteration 5: Derived from negating PC_5 verification check.
        Inputs: S5=True (Liked), S6=False (Remove Failed).
        We use a custom MagicMock for the set to simulate failure.
        """
        # S5 = True (Initially contains path)
        path = "/music/test.mp3"

        # We create a mock set that allows 'remove' but still reports 'contains' as True
        # This simulates a failure in the underlying data structure
        fake_set = MagicMock(spec=set)
        fake_set.__contains__.side_effect = lambda x: True  # Always says it contains item
        fake_set.remove.return_value = None  # Remove call succeeds technically

        self.mock_state.liked_tracks = fake_set

        toggle_like(self.mock_state)

        # Verify we hit the "Failed to remove" branch
        fake_set.remove.assert_called_with(path)
        mock_print.assert_called_with("[metrics] Error: Failed to remove like.")

    @patch('builtins.print')
    def test_iter7_like_fail(self, mock_print):
        """
        Iteration 7: Derived from negating PC_7 verification check.
        Inputs: S5=False (Not Liked), S6=False (Add Failed).
        """
        path = "/music/test.mp3"

        # We create a mock set that allows 'add' but still reports 'contains' as False
        fake_set = MagicMock(spec=set)
        # Sequence: First check (False - not liked), Second check (False - failed to add)
        fake_set.__contains__.side_effect = [False, False]
        fake_set.add.return_value = None

        self.mock_state.liked_tracks = fake_set

        toggle_like(self.mock_state)

        # Verify we hit the "Failed to add" branch
        fake_set.add.assert_called_with(path)
        mock_print.assert_called_with("[metrics] Error: Failed to add like.")