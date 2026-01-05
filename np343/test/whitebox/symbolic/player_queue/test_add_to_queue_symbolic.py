import unittest
from unittest.mock import MagicMock, patch
from music_player.player_queue import add_to_queue

class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.patcher_find = patch('music_player.player_queue._find_track')
        self.patcher_decouple = patch('music_player.player_queue._ensure_queue_decoupled')
        self.mock_find = self.patcher_find.start()
        self.mock_decouple = self.patcher_decouple.start()

    def tearDown(self):
        self.patcher_find.stop()
        self.patcher_decouple.stop()

    @patch('builtins.print')
    def test_pc1_invalid_s1(self, mock_print):
        add_to_queue(None, "song")
        mock_print.assert_called_with("[queue] Error: State is None.")
        add_to_queue(123, "song")
        mock_print.assert_called_with("[queue] Error: State is None.")

    @patch('builtins.print')
    def test_pc2_invalid_s2(self, mock_print):
        s1 = MagicMock()
        add_to_queue(s1, "")
        mock_print.assert_called_with("[queue] Usage: /q.add <index|name>")
        add_to_queue(s1, 123)
        mock_print.assert_called_with("[queue] Usage: /q.add <index|name>")

    @patch('builtins.print')
    def test_pc3_invalid_lib(self, mock_print):
        s1 = MagicMock()
        del s1.library_tracks
        add_to_queue(s1, "song")
        mock_print.assert_called_with("[queue] Error: Library is empty or missing.")
        s1.library_tracks = []
        add_to_queue(s1, "song")
        mock_print.assert_called_with("[queue] Error: Library is empty or missing.")

    def test_pc4_attr_error(self):
        class ImmutableState:
            __slots__ = ['library_tracks']
            def __init__(self):
                self.library_tracks = [1]
        s1 = ImmutableState()
        add_to_queue(s1, "song")

    @patch('builtins.print')
    def test_pc5_not_found(self, mock_print):
        s1 = MagicMock()
        s1.library_tracks = [1]
        s1.tracks = []
        self.mock_find.return_value = None
        add_to_queue(s1, "song")
        mock_print.assert_called_with("[queue] Song 'song' not found in Library.")

    @patch('builtins.print')
    def test_pc6_corrupt_s6(self, mock_print):
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
