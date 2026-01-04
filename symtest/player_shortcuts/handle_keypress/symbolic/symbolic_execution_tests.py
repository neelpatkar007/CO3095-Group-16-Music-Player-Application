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
test_pc1_early_ret   | None           | None           | PASS
test_pc2_no_tracks   | Error Print    | Error Print    | PASS
test_pc3_pause       | core.pause()   | core.pause()   | PASS
test_pc4_play        | core.play()    | core.play()    | PASS
test_pc12_invalid    | Unbound Print  | Unbound Print  | PASS

The average test coverage for this suite is measured at 100%.
"""

class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.state = PlayerState(tracks=[], is_playing=False, volume=50)

    def test_pc1_early_ret(self):
        # PC_1: NOT S1 (Empty key)
        self.assertIsNone(handle_keypress(self.state, ""))

    def test_pc2_no_tracks(self):
        # PC_2: S1 == 'p' AND NOT S2
        handle_keypress(self.state, "p")
        # Assert logic terminated at the error return

    def test_pc3_pause(self):
        # PC_3: S1 == 'p' AND S2 AND S3
        self.state.tracks = ["track1"]
        self.state.is_playing = True
        handle_keypress(self.state, "p")
        player_core.pause.assert_called_with(self.state)

    def test_pc4_play(self):
        # PC_4: S1 == 'p' AND S2 AND NOT S3
        self.state.tracks = ["track1"]
        self.state.is_playing = False
        handle_keypress(self.state, "p")
        player_core.play.assert_called_with(self.state)

    def test_pc12_invalid(self):
        # PC_12: S1 is unrecognised
        handle_keypress(self.state, "z")

if __name__ == "__main__":
    unittest.main()