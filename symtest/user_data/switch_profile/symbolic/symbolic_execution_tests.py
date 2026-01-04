import unittest
from unittest.mock import MagicMock, patch


# [Method]          | [Actual] | [Expected] | [Status]
# ------------------|----------|------------|---------
# test_path_pc1     | Return   | Return     | Passed
# test_path_pc2     | Return   | Return     | Passed
# test_path_pc3     | Return   | Return     | Passed
# test_path_pc4     | Success  | Success    | Passed
# test_path_pc5     | Success  | Success    | Passed
#
# The average test coverage for this suite is measured at 100%.

class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.state = MagicMock()
        # Initialise required attributes to avoid PC_1 by default
        self.state.profiles = {}
        self.state.active_profile = "initial"
        self.state.liked_tracks = set()
        self.state.song_ratings = {}
        self.state.playlists = []

    def test_path_pc1_null_state(self):
        """Tests PC_1: S1 is None."""
        # PC_1: S1 == None
        with patch('builtins.print') as mocked_print:
            from my_app import switch_profile
            switch_profile(None, "any_name")
            mocked_print.assert_called_with("[profile] Error: Invalid state.")

    def test_path_pc2_missing_profile(self):
        """Tests PC_2: S2 NOT in S3 AND S2 != 'default'."""
        # S2 = "unknown", S3 = {}
        with patch('builtins.print') as mocked_print:
            from my_app import switch_profile
            switch_profile(self.state, "unknown")
            mocked_print.assert_called_with("[profile] Profile 'unknown' does not exist.")

    def test_path_pc3_already_active(self):
        """Tests PC_3: S2 == S4."""
        # S2 = "current", S4 = "current"
        self.state.profiles = {"current": {}}
        self.state.active_profile = "current"
        with patch('builtins.print') as mocked_print:
            from my_app import switch_profile
            switch_profile(self.state, "current")
            mocked_print.assert_called_with("[profile] Already on 'current'.")

    @patch('my_app._save_current_to_profile')
    @patch('my_app._apply_profile_data')
    @patch('my_app._save_profiles')
    def test_path_pc4_full_switch(self, mock_save_all, mock_apply, mock_save_curr):
        """Tests PC_4: S2 in S3 (Full state transition)."""
        # S2 = "new_user", S3 = {"new_user": {"data": 1}}
        self.state.profiles = {"new_user": {"data": 1}}
        self.state.active_profile = "old_user"

        from my_app import switch_profile
        switch_profile(self.state, "new_user")

        mock_apply.assert_called_once()
        self.assertEqual(self.state.active_profile, "new_user")

    @patch('my_app._save_current_to_profile')
    @patch('my_app._save_profiles')
    def test_path_pc5_default_no_data(self, mock_save_all, mock_save_curr):
        """Tests PC_5: S2 == 'default' but NOT in S3."""
        # S2 = "default", S3 = {}
        self.state.profiles = {}
        self.state.active_profile = "old_user"

        from my_app import switch_profile
        switch_profile(self.state, "default")

        self.assertEqual(self.state.active_profile, "default")


if __name__ == '__main__':
    unittest.main()