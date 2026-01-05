import unittest
from unittest.mock import MagicMock, patch
from music_player.player_queue import play_next


# Minimal mocks for list-based fault injection
class FailInsertList(list):
    def insert(self, index, obj):
        raise RuntimeError("Simulated Insertion Failure")


class CorruptInsertList(list):
    def insert(self, index, obj):
        super().insert(index, "WRONG_TRACK")


class TestSymbolicExecution(unittest.TestCase):
    """
    Strict symbolic execution test suite based on FILE 1.
    """

    def setUp(self):
        self.mock_state = MagicMock()
        self.mock_state.tracks = []  # Real list to pass type checks
        self.mock_state.current_index = 0
        self.mock_track = MagicMock()
        self.mock_track.display_name = "Symbolic Song"

    def test_pc1_invalid_state(self):
        """PC_1: S1 is None OR S1 is Primitive."""
        play_next(None, "query")
        play_next(12345, "query")

    def test_pc2_invalid_query(self):
        """PC_2: S2 is Empty OR S2 is NOT str."""
        play_next(self.mock_state, "")
        play_next(self.mock_state, 123)

    @patch('builtins.print')
    def test_pc3_corrupted_queue_fatal(self, mock_print):
        """PC_3: S3 NOT List AND setting S3 raises AttributeError."""
        # Tuple is immutable and passes PC_1 checks (not str/int/float/bool)
        immutable_state = (1, 2)
        play_next(immutable_state, "valid_query")
        mock_print.assert_called_with("[queue] Error: Queue corrupted.")

    @patch('music_player.player_queue._find_track')
    @patch('builtins.print')
    def test_pc4_song_not_found(self, mock_print, mock_find):
        """PC_4: S4 (Found) is None."""
        mock_find.return_value = None
        play_next(self.mock_state, "unknown_song")
        mock_print.assert_called_with("[queue] Song 'unknown_song' not found in Library.")

    @patch('music_player.player_queue._ensure_queue_decoupled')
    @patch('music_player.player_queue._find_track')
    @patch('builtins.print')
    def test_pc5_insertion_exception(self, mock_print, mock_find, mock_decouple):
        """PC_5: S5 raises Exception during insert."""
        mock_find.return_value = self.mock_track
        self.mock_state.tracks = FailInsertList()

        play_next(self.mock_state, "valid_song")
        mock_print.assert_called_with("[queue] Insertion failed: Simulated Insertion Failure")

    @patch('music_player.player_queue._ensure_queue_decoupled')
    @patch('music_player.player_queue._find_track')
    @patch('builtins.print')
    def test_pc6_insertion_verification_fail(self, mock_print, mock_find, mock_decouple):
        """PC_6: S6 is False (verification fails)."""
        mock_find.return_value = self.mock_track
        self.mock_state.tracks = CorruptInsertList(["Existing"])
        self.mock_state.current_index = 0

        play_next(self.mock_state, "valid_song")
        mock_print.assert_called_with("[queue] Error: Track did not insert correctly.")

    @patch('music_player.player_queue._ensure_queue_decoupled')
    @patch('music_player.player_queue._find_track')
    @patch('builtins.print')
    def test_pc7_success(self, mock_print, mock_find, mock_decouple):
        """PC_7: Happy path; S6 True."""
        mock_find.return_value = self.mock_track
        self.mock_state.tracks = ["A", "B"]
        self.mock_state.current_index = 0

        play_next(self.mock_state, "valid_song")

        self.assertEqual(self.mock_state.tracks[1], self.mock_track)
        mock_print.assert_called_with(f"[queue] Queued next: '{self.mock_track.display_name}'.")


if __name__ == '__main__':
    unittest.main()