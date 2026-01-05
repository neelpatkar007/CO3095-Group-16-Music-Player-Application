import unittest
from unittest.mock import MagicMock, patch
from music_player.user_data import _save_current_to_profile

class TestConcolicTesting(unittest.TestCase):

    @patch('music_player.user_data._serialize_current_state')
    def test_concolic_iter1_pc1(self, mock_ser):
        _save_current_to_profile(None)
        mock_ser.assert_not_called()

    @patch('music_player.user_data._save_profiles')
    @patch('music_player.user_data._serialize_current_state')
    def test_concolic_iter2_pc2(self, mock_ser, mock_save):
        state = MagicMock(spec=['profiles', 'active_profile'])
        state.profiles = {}
        state.active_profile = "test"
        mock_ser.return_value = None

        _save_current_to_profile(state)
        mock_save.assert_not_called()

    @patch('music_player.user_data._save_profiles')
    @patch('music_player.user_data._serialize_current_state')
    def test_concolic_iter3_pc3(self, mock_ser, mock_save):
        state = MagicMock(spec=['profiles', 'active_profile'])
        state.profiles = {}
        state.active_profile = "test"
        mock_ser.return_value = {"data": "val"}

        _save_current_to_profile(state)
        self.assertIn("test", state.profiles)
        mock_save.assert_called_once()


if __name__ == '__main__':
    unittest.main()