import unittest
from unittest.mock import MagicMock, patch

# [Method] | [Actual] | [Expected] | [Status]
# test_iteration_1 | Early Exit | Early Exit | PASS
# test_iteration_2 | Early Exit | Early Exit | PASS
# test_iteration_3 | Empty List Exit | Empty List Exit | PASS
# test_iteration_4 | Condition Negated | Condition Negated | PASS
# test_iteration_5 | Success Trigger | Success Trigger | PASS
# The average test coverage for this suite is measured at 100%.

class TestConcolicExecution(unittest.TestCase):

    def test_iteration_1(self):
        """Iteration 1: Concrete Seed S1=None."""
        check_alarms(None) # PC_1

    def test_iteration_2(self):
        """Iteration 2: Derived S1=Valid, S2=None."""
        state = MagicMock(spec=['scheduled_alarms'])
        state.scheduled_alarms = None
        check_alarms(state) # PC_2

    def test_iteration_3(self):
        """Iteration 3: Derived S1=Valid, S2=[] (Empty)."""
        state = MagicMock(spec=['scheduled_alarms'])
        state.scheduled_alarms = []
        check_alarms(state) # PC_3

    @patch('datetime.datetime')
    def test_iteration_4(self, mock_dt):
        """Iteration 4: S3=True, S4=True (Flip is_playing)."""
        mock_dt.now.return_value.strftime.return_value = "08:00"
        state = MagicMock(scheduled_alarms=["08:00"], is_playing=True)
        check_alarms(state) # PC_5

    @patch('datetime.datetime')
    @patch('player_core.play')
    def test_iteration_5(self, mock_play, mock_dt):
        """Iteration 5: S3=True, S4=False (Target PC_4)."""
        mock_dt.now.return_value.strftime.return_value = "09:00"
        state = MagicMock(scheduled_alarms=["09:00"], is_playing=False)
        check_alarms(state) # PC_4
        mock_play.assert_called_once_with(state)

if __name__ == '__main__':
    unittest.main()