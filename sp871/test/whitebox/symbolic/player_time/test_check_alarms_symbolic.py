import unittest
import datetime
from unittest.mock import MagicMock, patch
from music_player.player_time import check_alarms


class TestSymbolicExecution(unittest.TestCase):

    @patch('builtins.print')
    def test_pc_1(self, mock_print):
        check_alarms(None)
        mock_print.assert_not_called()

    @patch('builtins.print')
    def test_pc_2(self, mock_print):
        state = MagicMock(scheduled_alarms=None)
        check_alarms(state)
        mock_print.assert_not_called()

    @patch('builtins.print')
    def test_pc_3(self, mock_print):
        """Path PC_3: len(S2) == 0."""
        state = MagicMock(scheduled_alarms=[])
        check_alarms(state)
        mock_print.assert_not_called()

    @patch('builtins.print')
    @patch('datetime.datetime')
    def test_pc_4(self, mock_date, mock_print):
        mock_date.now.return_value.strftime.return_value = "10:00"
        state = MagicMock(scheduled_alarms=["10:00"], is_playing=False)
        check_alarms(state)
        mock_print.assert_called_with("[alarm] ALARM TRIGGERED")
        self.assertEqual(len(state.scheduled_alarms), 0)

    @patch('builtins.print')
    @patch('datetime.datetime')
    def test_pc_5(self, mock_date, mock_print):
        mock_date.now.return_value.strftime.return_value = "10:00"
        state = MagicMock(scheduled_alarms=["10:00"], is_playing=True)
        check_alarms(state)
        mock_print.assert_not_called()

if __name__ == '__main__':
    unittest.main()
