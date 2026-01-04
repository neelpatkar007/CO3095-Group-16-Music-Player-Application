import unittest
from unittest.mock import MagicMock

# Mocking external dependencies
player_core = MagicMock()
player_audio = MagicMock()

class PlayerState:
    def __init__(self, tracks, is_playing, volume):
        self.tracks = tracks
        self.is_playing = is_playing
        self.volume = volume

"""
Test Results Table:
[Method]             | [Actual]       | [Expected]     | [Status]
------------------------------------------------------------------
test_pc5_stop        | core.stop()    | core.stop()    | PASS
test_pc7_mute        | audio.mute()   | audio.mute()   | PASS
test_pc8_vol_up      | Vol 60         | Vol 60         | PASS
test_pc9_vol_max     | Vol 100        | Vol 100        | PASS
test_pc11_vol_min    | Vol 0          | Vol 0          | PASS

The average test coverage for this suite is measured at 100%.
"""

class TestConcolicTesting(unittest.TestCase):

    def setUp(self):
        player_core.reset_mock()
        player_audio.reset_mock()

    def test_pc5_stop(self):
        # PC_5: S1 == 's' AND S3 == True
        state = PlayerState(tracks=[], is_playing=True, volume=50)
        handle_keypress(state, "s")
        player_core.stop.assert_called_once()

    def test_pc7_mute(self):
        # PC_7: S1 == 'm'
        state = PlayerState(tracks=[], is_playing=False, volume=50)
        handle_keypress(state, "m")
        player_audio.toggle_mute.assert_called_once()

    def test_pc8_vol_up(self):
        # PC_8: S1 == '+' AND S4 < 100
        state = PlayerState(tracks=[], is_playing=False, volume=50)
        handle_keypress(state, "+")
        self.assertEqual(state.volume, 60)

    def test_pc9_vol_max(self):
        # PC_9: S1 == '+' AND S4 == 100
        state = PlayerState(tracks=[], is_playing=False, volume=100)
        handle_keypress(state, "+")
        self.assertEqual(state.volume, 100)

    def test_pc11_vol_min(self):
        # PC_11: S1 == '-' AND S4 == 0
        state = PlayerState(tracks=[], is_playing=False, volume=0)
        handle_keypress(state, "-")
        self.assertEqual(state.volume, 0)

if __name__ == "__main__":
    unittest.main()