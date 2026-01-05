import unittest
from unittest.mock import MagicMock, patch
from music_player.player_time import check_alarms


class TestConcolicExecution(unittest.TestCase):

    def test_iteration_1(self):
        check_alarms(None) # PC_1

    def test_iteration_2(self):
        state = MagicMock(spec=['scheduled_alarms'])
        state.scheduled_alarms = None
        check_alarms(state) # PC_2

    def test_iteration_3(self):
        state = MagicMock(spec=['scheduled_alarms'])
        state.scheduled_alarms = []
        check_alarms(state) # PC_3

    @patch('datetime.datetime')
    def test_iteration_4(self, mock_dt):
        mock_dt.now.return_value.strftime.return_value = "08:00"
        state = MagicMock(scheduled_alarms=["08:00"], is_playing=True)
        check_alarms(state) # PC_5

    @patch('datetime.datetime')
    def test_iteration_5(self, mock_dt):
        mock_dt.now.return_value.strftime.return_value = "09:00"
        state = MagicMock(scheduled_alarms=["09:00"], is_playing=False)

        check_alarms(state)




if __name__ == '__main__':
    unittest.main()