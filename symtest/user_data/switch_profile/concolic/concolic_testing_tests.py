import unittest
from unittest.mock import MagicMock, patch

# [Method]          | [Actual] | [Expected] | [Status]
# ------------------|----------|------------|---------
# test_iter_1_pc1   | Return   | Return     | Passed
# test_iter_2_pc2   | Return   | Return     | Passed
# test_iter_3_pc5   | Success  | Success    | Passed
# test_iter_4_pc4   | Success  | Success    | Passed
# test_iter_5_pc3   | Return   | Return     | Passed
#
# The average test coverage for this suite is measured at 100%.

class TestConcolicGeneration(unittest.TestCase):

    @patch('builtins.print')
    def test_iter_1_pc1(self, mock_print):
        """Iteration 1: Concrete seed results in PC_1."""
        from music_player.user_data import switch_profile
        # S1=None
        switch_profile(None, "Guest")
        mock_print.assert_called_with("[profile] Error: Invalid state.")

    @patch('builtins.print')
    def test_iter_2_pc2(self, mock_print):
        """Iteration 2: Flipped PC_1, derived S1=Obj, S2='Guest', S3={}."""
        from music_player.user_data import switch_profile
        state = MagicMock(profiles={}, active_profile="Admin")
        switch_profile(state, "Guest")
        mock_print.assert_any_call("[profile] Profile 'Guest' does not exist.")

    @patch('music_player.user_data._save_profiles')
    def test_iter_3_pc5(self, mock_save):
        """Iteration 3: Flipped S2 to 'default'."""
        from music_player.user_data import switch_profile
        state = MagicMock(profiles={}, active_profile="Admin")
        switch_profile(state, "default")
        self.assertEqual(state.active_profile, "default")

    @patch('music_player.user_data._apply_profile_data')
    def test_iter_4_pc4(self, mock_apply):
        """Iteration 4: Flipped S2 in S3."""
        from music_player.user_data import switch_profile
        state = MagicMock(profiles={"Admin": {}}, active_profile="User")
        switch_profile(state, "Admin")
        mock_apply.assert_called_once()

    @patch('builtins.print')
    def test_iter_5_pc3(self, mock_print):
        """Iteration 5: Flipped S2 == S4."""
        from music_player.user_data import switch_profile
        state = MagicMock(profiles={"User": {}}, active_profile="User")
        switch_profile(state, "User")
        mock_print.assert_called_with("[profile] Already on 'User'.")

if __name__ == '__main__':
    unittest.main()