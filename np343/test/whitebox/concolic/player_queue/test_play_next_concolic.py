import unittest
from unittest.mock import MagicMock, patch
from music_player.player_queue import play_next

class TestConcolicExecution(unittest.TestCase):

    def setUp(self):
        self.mock_state = MagicMock()
        self.mock_state.tracks = []
        self.mock_state.current_index = 0
        self.mock_track = MagicMock()
        self.mock_track.display_name = "Concolic Tune"

    def test_iteration_1_null_state(self):
        state = None
        query = "valid"

        play_next(state, query)


    def test_iteration_2_bad_query(self):
        state = self.mock_state
        query = 12345

        play_next(state, query)


    @patch('music_player.player_queue._find_track')
    def test_iteration_3_not_found(self, mock_find):
        mock_find.return_value = None

        play_next(self.mock_state, "ghost_song")

        self.assertEqual(len(self.mock_state.tracks), 0)

    @patch('music_player.player_queue._ensure_queue_decoupled')
    @patch('music_player.player_queue._find_track')
    @patch('builtins.print')
    def test_iteration_5_success(self, mock_print, mock_find, mock_decouple):
        mock_find.return_value = self.mock_track
        self.mock_state.tracks = ["Start"]
        self.mock_state.current_index = 0

        play_next(self.mock_state, "hit_song")

        self.assertEqual(self.mock_state.tracks[1], self.mock_track)
        mock_print.assert_called_with(f"[queue] Queued next: '{self.mock_track.display_name}'.")


if __name__ == '__main__':
    unittest.main()
