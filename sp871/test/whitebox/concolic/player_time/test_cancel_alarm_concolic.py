import unittest
from typing import List, Optional
from music_player.player_time import cancel_alarm
class PlayerState:
    def __init__(self, alarms=None, has_attr=True):
        if has_attr:
            self.scheduled_alarms = alarms

class TestConcolicSuite(unittest.TestCase):

    def test_iteration_1(self):
        state = None # S1 is None
        cancel_alarm(state)

    def test_iteration_2(self):
        state = PlayerState(alarms=None)
        cancel_alarm(state)

    def test_iteration_3(self):
        state = PlayerState(alarms="InvalidType")
        cancel_alarm(state)

    def test_iteration_4(self):
        state = PlayerState(alarms=[])
        cancel_alarm(state)

    def test_iteration_5(self):
        state = PlayerState(alarms=[1])
        cancel_alarm(state)
        self.assertEqual(len(state.scheduled_alarms), 0)

if __name__ == '__main__':
    unittest.main()