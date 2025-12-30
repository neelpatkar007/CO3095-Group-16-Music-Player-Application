import unittest
from unittest.mock import MagicMock, patch
from music_player import main
from music_player.player_state import PlayerState


class TestMainLoops(unittest.TestCase):
    """
    White-Box Statement Coverage for main.py Loops.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: Statement Testing (White-Box)
    """

    def setUp(self):
        self.state = PlayerState([], MagicMock())

    def test_queue_commands(self):
        """
        Expected Result:
         - /loop forces an argument check.
         - Queue/Metric commands dispatch to their backend functions.
        Actual Result: PASSED [100%][main] Usage: /loop <off|one|all>
        """
        # /loop
        main.handle_command(self.state, "/loop")  # Fail
        with patch('music_player.player_queue.set_loop_mode') as mock_loop:
            main.handle_command(self.state, "/loop all")  # Success

        # Queue: /queue, /q.add
        with patch('music_player.player_queue.show_queue') as m_show, \
                patch('music_player.player_queue.add_to_queue') as m_add:
            main.handle_command(self.state, "/queue")
            main.handle_command(self.state, "/q.add 1")
            m_show.assert_called()
            m_add.assert_called()

        # /q.remove, /playnext, /q.clear
        with patch('music_player.player_queue.remove_from_queue') as m_rem, \
                patch('music_player.player_queue.play_next') as m_next, \
                patch('music_player.player_queue.clear_queue') as m_clear:
            main.handle_command(self.state, "/q.remove 1")
            main.handle_command(self.state, "/playnext 1")
            main.handle_command(self.state, "/q.clear")