import unittest
from unittest.mock import MagicMock, patch

from music_player.player_queue import remove_from_queue
from music_player.player_queue import _ensure_queue_decoupled


class TestSymbolicExecution(unittest.TestCase):

    def _ensure_queue_decoupled(state):
        pass
    
    def setUp(self):
        self.patcher = patch('builtins.print')
        self.mock_print = self.patcher.start()

        self.decouple_patcher = patch(f'{__name__}._ensure_queue_decoupled')
        self.mock_decouple = self.decouple_patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.decouple_patcher.stop()

    def test_pc1_invalid_s1(self):
        remove_from_queue(None, "query")
        self.mock_print.assert_not_called()

        remove_from_queue(12345, "query")
        self.mock_print.assert_not_called()

    def test_pc2_no_tracks(self):
        s1 = MagicMock()
        del s1.tracks

        remove_from_queue(s1, "query")
        self.mock_print.assert_called_with("[queue] Queue is empty.")

    def test_pc3_empty_tracks(self):
        s1 = MagicMock()
        s1.tracks = []

        remove_from_queue(s1, "query")
        self.mock_print.assert_called_with("[queue] Queue is empty.")

    def test_pc4_invalid_s2(self):
        s1 = MagicMock()
        s1.tracks = [MagicMock()]


        remove_from_queue(s1, None)
        self.mock_print.assert_called_with("[queue] Usage: /q.remove <index|name>")


        remove_from_queue(s1, 123)
        self.mock_print.assert_called_with("[queue] Usage: /q.remove <index|name>")

    def test_pc5_valid_digit_removal(self):
        s1 = MagicMock()
        track_1 = MagicMock()
        track_1.display_name = "Song A"
        s1.tracks = [track_1]
        s1.current_index = 0

        remove_from_queue(s1, "1")

        self.assertEqual(len(s1.tracks), 0)
        self.mock_print.assert_called_with("[queue] Removed 'Song A' from queue.")

    def test_pc6_index_out_of_range(self):
        s1 = MagicMock()
        s1.tracks = [MagicMock()]

        remove_from_queue(s1, "99")

        self.assertEqual(len(s1.tracks), 1)
        self.mock_print.assert_called_with("[queue] Index out of range.")

    def test_pc7_valid_string_match(self):
        s1 = MagicMock()
        track_1 = MagicMock()
        track_1.display_name = "Bohemian Rhapsody"
        s1.tracks = [track_1]
        s1.current_index = 0

        remove_from_queue(s1, "rhapsody")

        self.assertEqual(len(s1.tracks), 0)
        self.mock_print.assert_called_with("[queue] Removed 'Bohemian Rhapsody' from queue.")

    def test_pc8_valid_string_no_match(self):
        s1 = MagicMock()
        track_1 = MagicMock()
        track_1.display_name = "Bohemian Rhapsody"
        s1.tracks = [track_1]

        remove_from_queue(s1, "Stairway")

        self.assertEqual(len(s1.tracks), 1)
        self.mock_print.assert_called_with("[queue] 'Stairway' not found in current queue.")


if __name__ == '__main__':
    unittest.main()