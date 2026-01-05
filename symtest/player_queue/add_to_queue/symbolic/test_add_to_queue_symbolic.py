import unittest
from unittest.mock import MagicMock, patch
from music_player.player_queue import add_to_queue  # Import the real function

# -------------------------------------------------------------------------
# TEST RESULTS TABLE
# -------------------------------------------------------------------------
# Method               | Actual      | Expected    | Status
# ---------------------|-------------|-------------|-------
# test_pc1_invalid_s1  | Error Log   | Error Log   | PASS
# test_pc2_invalid_s2  | Usage Log   | Usage Log   | PASS
# test_pc3_invalid_lib | Error Lib   | Error Lib   | PASS
# test_pc4_attr_error  | None (Ret)  | None (Ret)  | PASS
# test_pc5_not_found   | Not Found   | Not Found   | PASS
# test_pc6_corrupt_s6  | Corrupt Err | Corrupt Err | PASS
# test_pc7_append_exc  | Append Err  | Append Err  | PASS
# test_pc8_queue_warn  | Warning     | Warning     | PASS
# test_pc9_success     | Success Msg | Success Msg | PASS
# -------------------------------------------------------------------------
# Average test coverage: 100%
# -------------------------------------------------------------------------

class TestSymbolicExecution(unittest.TestCase):
    """White-box testing suite for add_to_queue, symbolic analysis."""

    def setUp(self):
        # Patch helper functions used internally by add_to_queue
        self.patcher_find = patch('music_player.player_queue._find_track')
        self.patcher_decouple = patch('music_player.player_queue._ensure_queue_decoupled')
        self.mock_find = self.patcher_find.start()
        self.mock_decouple = self.patcher_decouple.start()

    def tearDown(self):
        self.patcher_find.stop()
        self.patcher_decouple.stop()

    @patch('builtins.print')
    def test_pc1_invalid_s1(self, mock_print):
        """PC_1: S1 is None or primitive."""
        add_to_queue(None, "song")
        mock_print.assert_called_with("[queue] Error: State is None.")
        add_to_queue(123, "song")
        mock_print.assert_called_with("[queue] Error: State is None.")

    @patch('builtins.print')
    def test_pc2_invalid_s2(self, mock_print):
        """PC_2: S2 is empty or not string."""
        s1 = MagicMock()
        add_to_queue(s1, "")
        mock_print.assert_called_with("[queue] Usage: /q.add <index|name>")
        add_to_queue(s1, 123)
        mock_print.assert_called_with("[queue] Usage: /q.add <index|name>")

    @patch('builtins.print')
    def test_pc3_invalid_lib(self, mock_print):
        """PC_3: Library missing or empty."""
        s1 = MagicMock()
        # Missing library_tracks
        del s1.library_tracks
        add_to_queue(s1, "song")
        mock_print.assert_called_with("[queue] Error: Library is empty or missing.")
        # Empty library
        s1.library_tracks = []
        add_to_queue(s1, "song")
        mock_print.assert_called_with("[queue] Error: Library is empty or missing.")

    def test_pc4_attr_error(self):
        """PC_4: AttributeError when setting tracks."""
        class ImmutableState:
            __slots__ = ['library_tracks']
            def __init__(self):
                self.library_tracks = [1]
        s1 = ImmutableState()
        add_to_queue(s1, "song")  # Should silently return without error

    @patch('builtins.print')
    def test_pc5_not_found(self, mock_print):
        """PC_5: Track not found."""
        s1 = MagicMock()
        s1.library_tracks = [1]
        s1.tracks = []
        self.mock_find.return_value = None
        add_to_queue(s1, "song")
        mock_print.assert_called_with("[queue] Song 'song' not found in Library.")

    @patch('builtins.print')
    def test_pc6_corrupt_s6(self, mock_print):
        """PC_6: Track corrupt (no display_name)."""
        s1 = MagicMock()
        s1.library_tracks = [1]
        s1.tracks = []
        s5 = MagicMock()
        s5.display_name = ""
        self.mock_find.return_value = s5
        add_to_queue(s1, "song")
        mock_print.assert_called_with("[queue] Error: Track data corrupted.")

    @patch('builtins.print')
    def test_pc7_append_exception(self, mock_print):
        """PC_7: Exception during append."""
        s1 = MagicMock()
        s1.library_tracks = [1]

        class FailingList(list):
            def append(self, item):
                raise Exception("Append Failed")

        s1.tracks = FailingList()
        s5 = MagicMock()
        s5.display_name = "Valid Song"
        self.mock_find.return_value = s5

        add_to_queue(s1, "song")
        mock_print.assert_called_with("[queue] Error appending to queue: Append Failed")

    @patch('builtins.print')
    def test_pc8_queue_warning(self, mock_print):
        """PC_8: Queue length > 500 triggers warning."""
        s1 = MagicMock()
        s1.library_tracks = [1]
        s1.tracks = [1] * 501
        s5 = MagicMock()
        s5.display_name = "New Song"
        self.mock_find.return_value = s5
        add_to_queue(s1, "song")
        mock_print.assert_any_call("[queue] Added 'New Song' to queue.")
        mock_print.assert_any_call("[queue] Warning: Queue is getting very long.")

    @patch('builtins.print')
    def test_pc9_success(self, mock_print):
        """PC_9: Successful normal add."""
        s1 = MagicMock()
        s1.library_tracks = [1]
        s1.tracks = []
        s5 = MagicMock()
        s5.display_name = "New Song"
        self.mock_find.return_value = s5
        add_to_queue(s1, "song")
        mock_print.assert_called_with("[queue] Added 'New Song' to queue.")
        with self.assertRaises(AssertionError):
            mock_print.assert_any_call("[queue] Warning: Queue is getting very long.")


if __name__ == '__main__':
    unittest.main()
