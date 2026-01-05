import unittest
from unittest.mock import MagicMock, patch
from music_player.player_queue import remove_from_queue


class TestConcolicExecution(unittest.TestCase):

    def setUp(self):
        self.patcher = patch('builtins.print')
        self.mock_print = self.patcher.start()
        self.decouple_patcher = patch(f'{__name__}._ensure_queue_decoupled', create=True)
        self.mock_decouple = self.decouple_patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.decouple_patcher.stop()

    def test_iteration_1_invalid_state(self):
        remove_from_queue(None, "test")
        self.mock_print.assert_not_called()

    def test_iteration_2_invalid_structure(self):
        s1 = MagicMock()
        del s1.tracks
        remove_from_queue(s1, "test")
        self.mock_print.assert_called_with("[queue] Queue is empty.")

    def test_iteration_3_empty_queue(self):
        s1 = MagicMock()
        s1.tracks = []
        remove_from_queue(s1, "test")
        self.mock_print.assert_called_with("[queue] Queue is empty.")

    def test_iteration_4_invalid_query(self):
        s1 = MagicMock()
        s1.tracks = [MagicMock()]
        remove_from_queue(s1, None)
        self.mock_print.assert_called_with("[queue] Usage: /q.remove <index|name>")

    def test_iteration_5_digit_success(self):
        s1 = MagicMock()
        track = MagicMock()
        track.display_name = "TargetSong"
        s1.tracks = [track]
        s1.current_index = 0

        remove_from_queue(s1, "1")

        self.mock_print.assert_called_with("[queue] Removed 'TargetSong' from queue.")
        self.assertEqual(len(s1.tracks), 0)

    def test_iteration_6_digit_out_of_range(self):
        s1 = MagicMock()
        s1.tracks = [MagicMock()]

        remove_from_queue(s1, "99")

        self.mock_print.assert_called_with("[queue] Index out of range.")

    def test_iteration_7_string_match(self):
        s1 = MagicMock()
        track = MagicMock()
        track.display_name = "Smooth Jazz"
        s1.tracks = [track]
        s1.current_index = 0

        remove_from_queue(s1, "Jazz")

        self.mock_print.assert_called_with("[queue] Removed 'Smooth Jazz' from queue.")

    def test_iteration_8_string_no_match(self):
        s1 = MagicMock()
        track = MagicMock()
        track.display_name = "Smooth Jazz"
        s1.tracks = [track]

        remove_from_queue(s1, "Rock")

        self.mock_print.assert_called_with("[queue] 'Rock' not found in current queue.")


if __name__ == '__main__':
    unittest.main()