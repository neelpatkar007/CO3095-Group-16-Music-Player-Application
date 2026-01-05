import unittest
from unittest.mock import MagicMock, patch
from music_player.player_queue import add_to_queue

class TestConcolicExecution(unittest.TestCase):

    def setUp(self):
        self.patcher_find = patch('music_player.player_queue._find_track')
        self.patcher_decouple = patch('music_player.player_queue._ensure_queue_decoupled')
        self.mock_find = self.patcher_find.start()
        self.mock_decouple = self.patcher_decouple.start()

    def tearDown(self):
        self.patcher_find.stop()
        self.patcher_decouple.stop()

    @patch('builtins.print')
    def test_iter1_seed_null(self, mock_print):
        add_to_queue(None, "song")
        mock_print.assert_called_with("[queue] Error: State is None.")

    @patch('builtins.print')
    def test_iter2_flip_s2(self, mock_print):
        s1 = MagicMock()
        add_to_queue(s1, None)
        mock_print.assert_called_with("[queue] Usage: /q.add <index|name>")

    @patch('builtins.print')
    def test_iter3_flip_s3(self, mock_print):
        s1 = MagicMock()
        s1.library_tracks = None
        add_to_queue(s1, "song")
        mock_print.assert_called_with("[queue] Error: Library is empty or missing.")

    @patch('builtins.print')
    def test_iter4_flip_s5(self, mock_print):
        s1 = MagicMock()
        s1.library_tracks = [True]
        s1.tracks = []
        self.mock_find.return_value = None
        add_to_queue(s1, "song")
        mock_print.assert_called_with("[queue] Song 'song' not found in Library.")

    @patch('builtins.print')
    def test_iter5_flip_s6(self, mock_print):
        s1 = MagicMock()
        s1.library_tracks = [True]
        s1.tracks = []
        s5 = MagicMock()
        s5.display_name = ""
        self.mock_find.return_value = s5
        add_to_queue(s1, "song")
        mock_print.assert_called_with("[queue] Error: Track data corrupted.")

    @patch('builtins.print')
    def test_iter6_flip_exception(self, mock_print):
        s1 = MagicMock()
        s1.library_tracks = [True]

        class FailList(list):
            def append(self, x): raise Exception("Concolic Fail")

        s1.tracks = FailList()
        s5 = MagicMock()
        s5.display_name = "Song"
        self.mock_find.return_value = s5

        add_to_queue(s1, "song")
        mock_print.assert_called_with("[queue] Error appending to queue: Concolic Fail")

    @patch('builtins.print')
    def test_iter7_flip_len_warn(self, mock_print):
        s1 = MagicMock()
        s1.library_tracks = [True]
        s1.tracks = [1] * 501
        s5 = MagicMock()
        s5.display_name = "Song"
        self.mock_find.return_value = s5

        add_to_queue(s1, "song")
        mock_print.assert_any_call("[queue] Warning: Queue is getting very long.")

    @patch('builtins.print')
    def test_iter8_flip_len_norm(self, mock_print):
        s1 = MagicMock()
        s1.library_tracks = [True]
        s1.tracks = []
        s5 = MagicMock()
        s5.display_name = "Song"
        self.mock_find.return_value = s5

        add_to_queue(s1, "song")
        mock_print.assert_called_with("[queue] Added 'Song' to queue.")


if __name__ == '__main__':
    unittest.main()
