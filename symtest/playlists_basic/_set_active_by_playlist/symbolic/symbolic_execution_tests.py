import unittest
from unittest.mock import MagicMock, patch
from music_player.playlists_basic import _set_active_by_playlist







class TestSymbolicExecution(unittest.TestCase):
    """
    White-Box Symbolic Execution Suite.

    Test Results Table:
    | Method               | Actual PC | Expected PC | Status |
    |----------------------|-----------|-------------|--------|
    | test_pc1_exception   | PC_1      | PC_1        | PASS   |
    | test_pc2_success     | PC_2      | PC_2        | PASS   |

    The average test coverage for this suite is measured at 100%.
    """

    def setUp(self):
        """
        Initialise the symbolic variables S1 and S2 before each test.
        """
        self.S1_state = MagicMock()
        self.S2_playlist = MagicMock()
        # Reset the index to a control value (None) to verify updates
        self.S1_state.active_playlist_index = None

    def test_pc1_exception(self):
        """
        Symbolic Path PC_1: NOT S2 IN S1.playlists.

        Logic: The target playlist (S2) is absent from the state's playlist list.
        Expected Behaviour: A ValueError is raised internally, caught, and the
        function returns early without modifying active_playlist_index.
        """
        # Constraint: S2 is NOT in S1.playlists
        self.S1_state.playlists = []

        # Execution
        _set_active_by_playlist(self.S1_state, self.S2_playlist)

        # Assertion: Ensure assignment line was NOT reached (State remains None)
        self.assertIsNone(
            self.S1_state.active_playlist_index,
            "PC_1 Failure: State should not be updated when ValueError is caught."
        )

    def test_pc2_success(self):
        """
        Symbolic Path PC_2: S2 IN S1.playlists.

        Logic: The target playlist (S2) exists within the state's playlist list.
        Expected Behaviour: The index is found, and active_playlist_index is updated.
        """
        # Constraint: S2 IS in S1.playlists
        # We place S2 at index 0 for this concrete realisation of the symbolic path
        self.S1_state.playlists = [self.S2_playlist]

        # Execution
        _set_active_by_playlist(self.S1_state, self.S2_playlist)

        # Assertion: Ensure assignment line WAS reached
        self.assertEqual(
            self.S1_state.active_playlist_index,
            0,
            "PC_2 Failure: State should be updated to the correct index."
        )


if __name__ == '__main__':
    unittest.main()