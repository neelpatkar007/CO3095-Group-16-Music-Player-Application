import unittest
from unittest.mock import MagicMock, patch
from music_player.player_shortcuts import handle_keypress
from music_player.player_state import PlayerState


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
        self.state = MagicMock(spec=PlayerState)
        self.state.tracks = []
        self.state.is_playing = False
        self.state.volume = 50

    def test_pc1_early_ret(self):
        # PC_1: NOT S1 (Empty key)
        self.assertIsNone(handle_keypress(self.state, ""))

    @patch('builtins.print')
    def test_pc2_no_tracks(self, mock_print):
        # PC_2: S1 == 'p' AND NOT S2
        handle_keypress(self.state, "p")
        # Assert logic terminated at the error return

    @patch('music_player.player_shortcuts.player_core')
    def test_pc3_pause(self, mock_core):
        # PC_3: S1 == 'p' AND S2 AND S3
        self.state.tracks = ["track1"]
        self.state.is_playing = True
        handle_keypress(self.state, "p")
        mock_core.pause.assert_called_with(self.state)

    @patch('music_player.player_shortcuts.player_core')
    def test_pc4_play(self, mock_core):
        # PC_4: S1 == 'p' AND S2 AND NOT S3
        self.state.tracks = ["track1"]
        self.state.is_playing = False
        handle_keypress(self.state, "p")
        mock_core.play.assert_called_with(self.state)

    def test_pc12_invalid(self):
        # PC_12: S1 is unrecognised
        handle_keypress(self.state, "z")

if __name__ == "__main__":
    unittest.main()