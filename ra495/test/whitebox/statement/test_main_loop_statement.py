import unittest
from unittest.mock import MagicMock, patch
from music_player import main
from music_player.player_state import PlayerState


class TestMainLoops(unittest.TestCase):
    def setUp(self):
        self.state = PlayerState([], MagicMock())

    def test_queue_commands(self):
        main.handle_command(self.state, "/loop")  # Fail
        with patch('music_player.player_queue.set_loop_mode') as mock_loop:
            main.handle_command(self.state, "/loop all")  # Success

        with patch('music_player.player_queue.show_queue') as m_show, \
                patch('music_player.player_queue.add_to_queue') as m_add:
            main.handle_command(self.state, "/queue")
            main.handle_command(self.state, "/q.add 1")
            m_show.assert_called()
            m_add.assert_called()

        with patch('music_player.player_queue.remove_from_queue') as m_rem, \
                patch('music_player.player_queue.play_next') as m_next, \
                patch('music_player.player_queue.clear_queue') as m_clear:
            main.handle_command(self.state, "/q.remove 1")
            main.handle_command(self.state, "/playnext 1")
            main.handle_command(self.state, "/q.clear")

        with patch('music_player.player_metrics.toggle_like') as m_like, \
                patch('music_player.player_metrics.show_liked_songs') as m_likes, \
                patch('music_player.player_metrics.show_top_tracks') as m_top:
            main.handle_command(self.state, "/like")
            main.handle_command(self.state, "/likes")
            main.handle_command(self.state, "/top")

    def test_schedule_cancel_and_recent(self):
        with patch('music_player.player_time.cancel_alarm') as mock_can:
            main.handle_command(self.state, "/schedule.cancel")
            mock_can.assert_called()

        with patch('music_player.player_time.show_recently_added') as mock_rec:
            main.handle_command(self.state, "/recent")
            mock_rec.assert_called()

        with patch('music_player.player_config.view_stats') as mock_stats:
            main.handle_command(self.state, "/stats")
            mock_stats.assert_called()