import unittest
from unittest.mock import MagicMock, patch
import io

# Import the real function
from music_player.playlists_basic import show_current_playlist


# ==============================================================================

class TestSymbolicExecution(unittest.TestCase):
    """
    White-box test suite based on Symbolic Analysis (FILE 1).
    Maps inputs strictly to Path Conditions (PC_1 to PC_5).
    """

    def _target_function(self, state):
        # Use the real imported function
        show_current_playlist(state)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_pc1_state_none(self, mock_stdout):
        """
        PC_1: S1 == None.
        Expects immediate error return.
        """
        state = None
        self._target_function(state)

        output = mock_stdout.getvalue().strip()
        # Real function prints twice due to _ensure_playlists
        self.assertEqual(
            output,
            "[pl] Error: State is None.\n[pl] Error: State is None."
        )

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_pc2_no_playlists_attr(self, mock_stdout):
        """
        PC_2: S1 != None AND NOT S2.
        S1 exists but hasattr(S1, 'playlists') is False.
        """
        class EmptyState:
            pass

        state = EmptyState()
        self.assertFalse(hasattr(state, "playlists"))

        self._target_function(state)

        output = mock_stdout.getvalue().strip()
        # Real function prints twice due to _ensure_playlists
        self.assertEqual(
            output,
            "[pl] Error: State is None.\n[pl] Error: State is None."
        )

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_pc3_index_none(self, mock_stdout):
        """
        PC_3: S1 != None AND S2 AND S3 == None.
        Attributes exist, but active_playlist_index is None.
        """
        state = MagicMock()
        state.playlists = [MagicMock()]
        state.active_playlist_index = None

        self._target_function(state)

        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "[pl] No active playlist. Use /pl.open <name|index>.")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_pc4_playlists_empty(self, mock_stdout):
        """
        PC_4: S1 != None AND S2 AND S3 != None AND NOT S4.
        Index is set, but playlists list is empty (Falsey).
        """
        state = MagicMock()
        state.playlists = []
        state.active_playlist_index = 0

        self._target_function(state)

        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "[pl] No active playlist. Use /pl.open <name|index>.")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_pc5_success_path(self, mock_stdout):
        """
        PC_5: S1 != None AND S2 AND S3 != None AND S4.
        All constraints satisfied.
        """
        state = MagicMock()
        mock_pl = MagicMock()
        mock_pl.name = "Study Beats"

        state.playlists = [mock_pl]
        state.active_playlist_index = 0

        self._target_function(state)

        output = mock_stdout.getvalue().strip()
        self.assertIn("[pl] Current playlist 'Study Beats':", output)


if __name__ == '__main__':
    unittest.main()
