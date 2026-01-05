import unittest
import datetime
from typing import List
from music_player.player_time import set_alarm

# Mock PlayerState for testing purposes
class PlayerState:
    def __init__(self, alarms=None):
        self.scheduled_alarms = alarms if alarms is not None else []


class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.valid_state = PlayerState()

    def test_pc_1(self):
        # PC_1: S2 is not a string
        # S2 = 123 (int)
        result = set_alarm(self.valid_state, 123)
        self.assertIsNone(result)

    def test_pc_2(self):
        # PC_2: S1 is None
        result = set_alarm(None, "12:00")
        self.assertIsNone(result)

    def test_pc_3(self):
        # PC_3: S2 length != 5
        # S2 = "1:0"
        set_alarm(self.valid_state, "1:0")
        # Function prints and returns None

    def test_pc_8(self):
        # PC_8: Success Path
        # S1 = PlayerState, S2 = "14:30"
        set_alarm(self.valid_state, "14:30")
        self.assertEqual(self.valid_state.scheduled_alarms, ["14:30"])

if __name__ == '__main__':
    unittest.main()