import unittest
import datetime
from typing import List
from music_player.player_time import set_alarm

class PlayerState:
    def __init__(self, alarms=None):
        self.scheduled_alarms = alarms if alarms is not None else []


class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.valid_state = PlayerState()

    def test_pc_1(self):

        result = set_alarm(self.valid_state, 123)
        self.assertIsNone(result)

    def test_pc_2(self):
        result = set_alarm(None, "12:00")
        self.assertIsNone(result)

    def test_pc_3(self):

        set_alarm(self.valid_state, "1:0")

    def test_pc_8(self):

        set_alarm(self.valid_state, "14:30")
        self.assertEqual(self.valid_state.scheduled_alarms, ["14:30"])

if __name__ == '__main__':
    unittest.main()