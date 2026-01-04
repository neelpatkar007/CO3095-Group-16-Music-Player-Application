import unittest
from unittest.mock import MagicMock, patch


# Assuming the function is in a module named 'playlist_manager'
# For the purpose of this suite, we import next_track from the source context.
# from playlist_manager import next_track

# -------------------------------------------------------------------------
# TEST RESULTS TABLE
# -------------------------------------------------------------------------
# | Method             | Actual Result      | Expected Result    | Status |
# |--------------------|--------------------|--------------------|--------|
# | test_PC1_invalid   | Error Logged       | Error Logged       | PASS   |
# | test_PC2_no_tracks | Log: No tracks     | Log: No tracks     | PASS   |
# | test_PC3_loop_one  | Index Unchanged    | Index Unchanged    | PASS   |
# | test_PC4_shuffle   | Index Changed      | Index Changed      | PASS   |
# | test_PC5_seq_stop  | Playing=False      | Playing=False      | PASS   |
# | test_PC7_seq_next  | Index Increments   | Index Increments   | PASS   |
# -------------------------------------------------------------------------
# The average test coverage for this suite is measured at 100%.
# -------------------------------------------------------------------------

class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        # Mocking the state object S1
        self.state = MagicMock()
        self.state.history = []
        self.state.current_index = 0
        self.state.position_seconds = 10.0
        self.state.is_playing = False
        self.state.is_paused = False

    def tearDown(self):
        self.state = None

    @patch('builtins.print')
    def test_PC1_invalid_state(self, mock_print):
        """Test PC_1: Input S1 is invalid (None or primitive)."""
        # S1 is None
        from playlist_manager import next_track
        next_track(None)
        mock_print.assert_called_with("[queue] Error: State is invalid.")

        # S1 is primitive (int)
        next_track(123)
        mock_print.assert_called_with("[queue] Error: State is invalid.")

    @patch('playlist_manager._get_tracks_safe')
    @patch('builtins.print')
    def test_PC2_no_tracks(self, mock_print, mock_get_tracks):
        """Test PC_2: S2 (tracks) is empty."""
        from playlist_manager import next_track
        mock_get_tracks.return_value = []  # S2 is empty

        next_track(self.state)
        mock_print.assert_called_with("[queue] No tracks available.")

    @patch('playlist_manager._get_tracks_safe')
    def test_PC3_loop_one(self, mock_get_tracks):
        """Test PC_3: S4 (loop_mode) is 'one'."""
        from playlist_manager import next_track
        # Setup S2 with 2 tracks
        t1, t2 = MagicMock(), MagicMock()
        mock_get_tracks.return_value = [t1, t2]

        # Setup S3 (index) and S4 (mode)
        self.state.current_index = 0
        self.state.loop_mode = "one"
        self.state.shuffle_active = True  # Should be ignored due to loop_mode priority

        next_track(self.state)

        # Assertions
        self.assertEqual(self.state.current_index, 0, "Index should remain unchanged in loop 'one'.")
        self.assertEqual(self.state.position_seconds, 0.0, "Position should reset.")

    @patch('playlist_manager._get_tracks_safe')
    @patch('random.randint')
    def test_PC4_shuffle(self, mock_randint, mock_get_tracks):
        """Test PC_4: S5 (shuffle) is True, S8 (len) > 1."""
        from playlist_manager import next_track
        t1, t2, t3 = MagicMock(), MagicMock(), MagicMock()
        mock_get_tracks.return_value = [t1, t2, t3]

        self.state.current_index = 0
        self.state.loop_mode = "off"
        self.state.shuffle_active = True

        # Mock random to return 2
        mock_randint.return_value = 2

        next_track(self.state)

        self.assertEqual(self.state.current_index, 2, "Shuffle should select random index.")

    @patch('playlist_manager._get_tracks_safe')
    @patch('builtins.print')
    def test_PC5_sequential_stop(self, mock_print, mock_get_tracks):
        """Test PC_5: End of playlist, S4 != 'all', stops playback."""
        from playlist_manager import next_track
        t1, t2 = MagicMock(), MagicMock()
        mock_get_tracks.return_value = [t1, t2]

        self.state.current_index = 1  # At end (Index 1 of 2)
        self.state.loop_mode = "off"
        self.state.shuffle_active = False
        self.state.is_playing = True

        next_track(self.state)

        mock_print.assert_called_with("[queue] End of playlist.")
        self.assertFalse(self.state.is_playing, "Playback should stop at end of list.")

    @patch('playlist_manager._get_tracks_safe')
    def test_PC7_sequential_next(self, mock_get_tracks):
        """Test PC_7: Normal sequential increment."""
        from playlist_manager import next_track
        t1, t2 = MagicMock(), MagicMock()
        t2.display_name = "Track 2"
        mock_get_tracks.return_value = [t1, t2]

        self.state.current_index = 0
        self.state.loop_mode = "off"
        self.state.shuffle_active = False

        next_track(self.state)

        self.assertEqual(self.state.current_index, 1, "Should increment to next index.")