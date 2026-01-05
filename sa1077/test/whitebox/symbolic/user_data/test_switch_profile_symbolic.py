import unittest
from unittest.mock import MagicMock, patch
from music_player.user_data import switch_profile

class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.state = MagicMock()
        self.state.profiles = {}
        self.state.active_profile = "initial"
        self.state.liked_tracks = set()
        self.state.song_ratings = {}
        self.state.playlists = []

    def test_path_pc1_null_state(self):
        with patch('builtins.print') as mocked_print:
            switch_profile(None, "any_name")
            mocked_print.assert_called_with("[profile] Error: Invalid state.")

    def test_path_pc2_missing_profile(self):
        with patch('builtins.print') as mocked_print:
            switch_profile(self.state, "unknown")
            mocked_print.assert_called_with("[profile] Profile 'unknown' does not exist.")

    def test_path_pc3_already_active(self):
        self.state.profiles = {"current": {}}
        self.state.active_profile = "current"
        with patch('builtins.print') as mocked_print:
            switch_profile(self.state, "current")
            mocked_print.assert_called_with("[profile] Already on 'current'.")

    @patch('music_player.user_data._save_current_to_profile')
    @patch('music_player.user_data._apply_profile_data')
    @patch('music_player.user_data._save_profiles')
    def test_path_pc4_full_switch(self, mock_save_all, mock_apply, mock_save_curr):
        self.state.profiles = {"new_user": {"data": 1}}
        self.state.active_profile = "old_user"

        switch_profile(self.state, "new_user")

        mock_apply.assert_called_once()
        self.assertEqual(self.state.active_profile, "new_user")

    @patch('music_player.user_data._save_current_to_profile')
    @patch('music_player.user_data._save_profiles')
    def test_path_pc5_default_no_data(self, mock_save_all, mock_save_curr):
        self.state.profiles = {}
        self.state.active_profile = "old_user"

        switch_profile(self.state, "default")

        self.assertEqual(self.state.active_profile, "default")


if __name__ == '__main__':
    unittest.main()