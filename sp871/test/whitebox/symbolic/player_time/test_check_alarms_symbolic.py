import unittest
import datetime
from unittest.mock import MagicMock, patch
from music_player.player_time import check_alarms

# [Method] | [Actual] | [Expected] | [Status]
# test_pc_1 | Return None | Return None | PASS
# test_pc_2 | Return None | Return None | PASS
# test_pc_3 | Return None | Return None | PASS
# test_pc_4 | Alarm Triggered | Alarm Triggered | PASS
# test_pc_5 | End No Play | End No Play | PASS

class TestSymbolicExecution(unittest.TestCase):

    @patch('builtins.print')  # patch print to verify alarm triggering
    def test_pc_1(self, mock_print):
        """Path PC_1: S1 is None."""
        check_alarms(None)
        mock_print.assert_not_called()

    @patch('builtins.print')
    def test_pc_2(self, mock_print):
        """Path PC_2: S2 is not a list (None)."""
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
        """Path PC_4: Alarm triggers (S3=True, S4=False)."""
        mock_date.now.return_value.strftime.return_value = "10:00"
        state = MagicMock(scheduled_alarms=["10:00"], is_playing=False)
        check_alarms(state)
        # Confirm alarm was "triggered"
        mock_print.assert_called_with("[alarm] ALARM TRIGGERED")
        # Confirm alarm removed from scheduled list
        self.assertEqual(len(state.scheduled_alarms), 0)

    @patch('builtins.print')
    @patch('datetime.datetime')
    def test_pc_5(self, mock_date, mock_print):
        """Path PC_5: Logic fails trigger (S4=True)."""
        mock_date.now.return_value.strftime.return_value = "10:00"
        state = MagicMock(scheduled_alarms=["10:00"], is_playing=True)
        check_alarms(state)
        mock_print.assert_not_called()  # No alarm should be triggered

if __name__ == '__main__':
    unittest.main()
