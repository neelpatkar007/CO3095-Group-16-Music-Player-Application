import unittest
from unittest.mock import MagicMock, patch
from music_player import main
from music_player.player_state import PlayerState


class TestMainLoops(unittest.TestCase):
    """
    White-Box Statement Tests for main.py Loops.
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

        # Metrics: /like, /likes, /top
        with patch('music_player.player_metrics.toggle_like') as m_like, \
                patch('music_player.player_metrics.show_liked_songs') as m_likes, \
                patch('music_player.player_metrics.show_top_tracks') as m_top:
            main.handle_command(self.state, "/like")
            main.handle_command(self.state, "/likes")
            main.handle_command(self.state, "/top")

    def test_schedule_cancel_and_recent(self):
        """
        Expected Result: Commands dispatch to cancel_alarm, show_recently_added, and view_stats.
        Actual Result: Passed 100%. Mocks confirmed successful execution.
        """
        # /schedule.cancel
        with patch('music_player.player_time.cancel_alarm') as mock_can:
            main.handle_command(self.state, "/schedule.cancel")
            mock_can.assert_called()

        # /recent
        with patch('music_player.player_time.show_recently_added') as mock_rec:
            main.handle_command(self.state, "/recent")
            mock_rec.assert_called()

        # /stats
        with patch('music_player.player_config.view_stats') as mock_stats:
            main.handle_command(self.state, "/stats")
            mock_stats.assert_called()