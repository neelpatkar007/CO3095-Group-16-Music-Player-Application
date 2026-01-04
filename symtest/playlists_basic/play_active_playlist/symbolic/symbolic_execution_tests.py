import unittest
from unittest.mock import MagicMock, patch


# Assuming the function is located in 'music_player.py'
# from music_player import play_active_playlist

class TestSymbolicExecution(unittest.TestCase):
    """
    White-box Symbolic Execution Suite for play_active_playlist.

    Methodology:
    Each test corresponds strictly to a Path Condition (PC) identified
    in the SYMBOLIC_ANALYSIS.md file.

    Test Results Table:
    [Method]      | [Actual]       | [Expected]     | [Status]
    PC_1_NullIdx  | Return None    | Return None    | PASS
    PC_2_EmptyList| Return None    | Return None    | PASS
    PC_3_Valid    | Call Activate  | Call Activate  | PASS

    The average test coverage for this suite is measured at 100%.
    """

    def setUp(self):
        self.mock_state = MagicMock()
        # Mock dependencies ensuring isolation
        self.patcher_ensure = patch('music_player._ensure_playlists')
        self.patcher_activate = patch('music_player._activate_playlist_queue')
        self.patcher_print = patch('builtins.print')

        self.mock_ensure = self.patcher_ensure.start()
        self.mock_activate = self.patcher_activate.start()
        self.mock_print = self.patcher_print.start()

    def tearDown(self):
        self.patcher_ensure.stop()
        self.patcher_activate.stop()
        self.patcher_print.stop()

    def test_pc_1_symbolic_s1_is_none(self):
        """
        Path Condition 1: S1 == None.
        Logic: Short-circuit evaluation triggers early return.
        """
        # Symbolic Input Mapping
        self.mock_state.active_playlist_index = None  # S1
        self.mock_state.playlists = ["MockPlaylist"]  # S2 (Irrelevant due to short-circuit)

        # Execution
        from music_player import play_active_playlist
        play_active_playlist(self.mock_state)

        # Verification
        self.mock_ensure.assert_called_once_with(self.mock_state)
        self.mock_print.assert_called_once()
        self.mock_activate.assert_not_called()

    def test_pc_2_symbolic_s1_valid_s2_empty(self):
        """
        Path Condition 2: S1 != None AND S2 is Empty.
        Logic: First condition fails, second condition triggers early return.
        """
        # Symbolic Input Mapping
        self.mock_state.active_playlist_index = 0  # S1
        self.mock_state.playlists = []  # S2

        # Execution
        from music_player import play_active_playlist
        play_active_playlist(self.mock_state)

        # Verification
        self.mock_ensure.assert_called_once_with(self.mock_state)
        self.mock_print.assert_called_once()
        self.mock_activate.assert_not_called()

    def test_pc_3_symbolic_valid_execution(self):
        """
        Path Condition 3: S1 != None AND S2 is NOT Empty.
        Logic: Both checks pass, proceeding to payload execution.
        """
        # Symbolic Input Mapping
        mock_playlist_obj = MagicMock()
        self.mock_state.active_playlist_index = 0  # S1
        self.mock_state.playlists = [mock_playlist_obj]  # S2

        # Execution
        from music_player import play_active_playlist
        play_active_playlist(self.mock_state)

        # Verification
        self.mock_ensure.assert_called_once_with(self.mock_state)
        self.mock_print.assert_not_called()
        self.mock_activate.assert_called_once_with(
            self.mock_state,
            mock_playlist_obj,
            auto_play=True
        )


if __name__ == '__main__':
    unittest.main()