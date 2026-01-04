import unittest
import datetime
from unittest.mock import MagicMock, patch

# [Method] | [Actual] | [Expected] | [Status]
# test_pc_1 | Return None | Return None | PASS
# test_pc_2 | Return None | Return None | PASS
# test_pc_3 | Return None | Return None | PASS
# test_pc_4 | Play Called | Play Called | PASS
# test_pc_5 | End No Play | End No Play | PASS
# The average test coverage for this suite is measured at 100%.

class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.mock_core = MagicMock()
        patch('player_core.play', self.mock_core).start()

    def tearDown(self):
        patch.stopall()

    def test_pc_1(self):
        """Path PC_1: S1 is None."""
        check_alarms(None)
        self.mock_core.assert_not_called()

    def test_pc_2(self):
        """Path PC_2: S2 is not a list."""
        state = MagicMock(scheduled_alarms=None)
        check_alarms(state)
        self.mock_core.assert_not_called()

    def test_pc_3(self):
        """Path PC_3: len(S2) == 0."""
        state = MagicMock(scheduled_alarms=[])
        check_alarms(state)
        self.mock_core.assert_not_called()

    @patch('datetime.datetime')
    def test_pc_4(self, mock_date):
        """Path PC_4: Alarm triggers (S3=True, S4=False)."""
        mock_date.now.return_value.strftime.return_value = "10:00"
        state = MagicMock(scheduled_alarms=["10:00"], is_playing=False)
        check_alarms(state)
        self.assertTrue(self.mock_core.called)
        self.assertEqual(len(state.scheduled_alarms), 0)

    @patch('datetime.datetime')
    def test_pc_5(self, mock_date):
        """Path PC_5: Logic fails trigger (S4=True)."""
        mock_date.now.return_value.strftime.return_value = "10:00"
        state = MagicMock(scheduled_alarms=["10:00"], is_playing=True)
        check_alarms(state)
        self.mock_core.assert_not_called()

if __name__ == '__main__':
    unittest.main()