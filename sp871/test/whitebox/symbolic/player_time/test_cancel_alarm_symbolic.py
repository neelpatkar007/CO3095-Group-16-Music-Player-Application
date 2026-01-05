import unittest
from typing import List, Optional
from music_player.player_time import cancel_alarm

class PlayerState:
    def __init__(self, alarms: Optional[List] = None, add_attr: bool = True):
        if add_attr:
            self.scheduled_alarms = alarms

class TestSymbolicExecution(unittest.TestCase):

    def test_pc1_null_state(self):
        self.assertIsNone(cancel_alarm(None))

    def test_pc2_none_alarms(self):
        state = PlayerState(alarms=None)
        cancel_alarm(state) # Traverses PC_2

    def test_pc3_type_error(self):
        state = PlayerState(alarms=123) # type: ignore
        cancel_alarm(state)

    def test_pc4_empty_list(self):
        state = PlayerState(alarms=[])
        cancel_alarm(state)

    def test_pc5_clear_path(self):
        state = PlayerState(alarms=["Alarm1", "Alarm2"])
        cancel_alarm(state)
        self.assertEqual(len(state.scheduled_alarms), 0)

if __name__ == '__main__':
    unittest.main()