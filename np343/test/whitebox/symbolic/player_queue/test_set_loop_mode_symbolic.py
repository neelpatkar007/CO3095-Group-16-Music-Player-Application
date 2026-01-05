import unittest
from unittest.mock import MagicMock
from io import StringIO
from unittest.mock import patch
from music_player.player_queue import set_loop_mode


class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.mock_state = MagicMock()
        self.mock_state.loop_mode = "none"  # Default state

    def test_pc1_invalid_state(self):
        result = set_loop_mode(None, "off")
        self.assertIsNone(result)

        result = set_loop_mode(12345, "off")
        self.assertIsNone(result)

    def test_pc2_invalid_mode_type(self):
        result = set_loop_mode(self.mock_state, 999)
        self.assertIsNone(result)

    @patch('sys.stdout', new_callable=StringIO)
    def test_pc3_invalid_mode_value(self, mock_stdout):
        set_loop_mode(self.mock_state, "shuffle")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "[queue] Invalid loop mode. Use: off, one, all")

    @patch('sys.stdout', new_callable=StringIO)
    def test_pc4_redundant_check(self, mock_stdout):
        self.mock_state.loop_mode = "off"

        set_loop_mode(self.mock_state, "OFF")

        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "[queue] Loop mode: off")

    @patch('sys.stdout', new_callable=StringIO)
    def test_pc5_success_update(self, mock_stdout):
        self.mock_state.loop_mode = "one"

        set_loop_mode(self.mock_state, "off")  # S2

        self.assertEqual(self.mock_state.loop_mode, "off")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "[queue] Loop mode: off")


if __name__ == '__main__':
    unittest.main()