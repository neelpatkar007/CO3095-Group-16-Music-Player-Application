import unittest
from unittest.mock import MagicMock, patch
import threading
import time
from music_player import main
from music_player.player_state import PlayerState


class TestMain(unittest.TestCase):
    """
    Black-Box Specification-based Testing for main.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: Category Partition Method
    Source: mainTSL.txt
    """

    def setUp(self):
        # Mock state and engine
        self.mock_engine = MagicMock()
        self.state = PlayerState([], self.mock_engine)

        # Default state values
        self.state.resume_active = False
        self.state.position_seconds = 0.0
        # Tracks list is empty by default

    # Core Command Handling

    def test_handle_command_empty(self):
        """
        Expected Result: Returns True.
        Actual Result: Input ignored.
        """
        result = main.handle_command(self.state, "   ")
        self.assertTrue(result)

    def test_handle_command_quit(self):
        """
        Expected Result: Returns False and saves metrics.
        Actual Result: Quit command processed.
        """
        with patch("music_player.player_metrics.save_data") as mock_save:
            result = main.handle_command(self.state, "/quit")
            self.assertFalse(result)
            mock_save.assert_called_once()

    def test_handle_command_shortcuts(self):
        """
        Expected Result: Single letters 'p', 's', 'm' dispatch to player_shortcuts.
        Actual Result: Shortcut handler called.
        """
        with patch("music_player.player_shortcuts.handle_keypress") as mock_key:
            main.handle_command(self.state, "p")
            mock_key.assert_called_with(self.state, "p")

    # Sprint 1 Tests (Playback)

    def test_command_play_fresh(self):
        """
        Expected Result: /play calls player_core.play() directly when no resume state exists.
        Actual Result: Core Play called.
        """
        self.state.resume_active = False

        with patch("music_player.player_core.play") as mock_play:
            main.handle_command(self.state, "/play")
            mock_play.assert_called_with(self.state)

    def test_command_play_resume(self):
        """
        Expected Result: /play triggers Seek logic if resume is active and track exists.
        Actual Result: [resume] Seeking to saved position: 45s...
        """
        self.state.resume_active = True
        self.state.position_seconds = 45.0

        # Add a dummy track so state.current_track is valid
        self.state.tracks = [MagicMock()]
        self.state.current_index = 0

        with patch("music_player.player_core.play") as mock_play, \
                patch("music_player.player_seek.seek_to") as mock_seek:
            main.handle_command(self.state, "/play")

            # Verify Resume Logic sequence
            mock_play.assert_called()
            mock_seek.assert_called_with(self.state, "45.0")
            self.assertFalse(self.state.resume_active)

    def test_command_seek_args(self):
        """
        Expected Result: /seek command passes arguments correctly to player_seek.
        Actual Result: Seek to 1:30.
        """
        with patch("music_player.player_seek.seek_to") as mock_seek:
            main.handle_command(self.state, "/seek 1:30")
            mock_seek.assert_called_with(self.state, "1:30")

    def test_command_seek_missing_args(self):
        """
        Expected Result: Prints usage error if arg missing, does not call seek.
        Actual Result: [main] Usage: /seek <mm:ss or seconds>
        """
        with patch("music_player.player_seek.seek_to") as mock_seek:
            main.handle_command(self.state, "/seek")
            mock_seek.assert_not_called()

    # Sprint 2 Tests (Playlists)

    def test_command_playlist_new(self):
        """
        Expected Result: /pl.new dispatches to playlists_basic with name.
        Actual Result: Playlist 'Gym' created.
        """
        with patch("music_player.playlists_basic.create_playlist") as mock_create:
            main.handle_command(self.state, "/pl.new Gym Mix")
            mock_create.assert_called_with(self.state, "Gym Mix")

    def test_command_playlist_list(self):
        """
        Expected Result: /pl.list calls list_playlists.
        Actual Result: Playlists listed.
        """
        with patch("music_player.playlists_basic.list_playlists") as mock_list:
            main.handle_command(self.state, "/pl.list")
            mock_list.assert_called_once()

    def test_command_playlist_merge_args(self):
        """
        Expected Result: /pl.merge parses target, source, and dedupe flag correctly.
        Actual Result: Merge called with dedupe=True.
        """
        with patch("music_player.playlists_advanced.merge_playlists") as mock_merge:
            # Default dedupe (True)
            main.handle_command(self.state, "/pl.merge Target Source")
            mock_merge.assert_called_with(self.state, "Target", "Source", dedupe=True)

            # Selected "all" dedupe=False
            main.handle_command(self.state, "/pl.merge Target Source all")
            mock_merge.assert_called_with(self.state, "Target", "Source", dedupe=False)

    # Sprint 3 Tests (Metrics/Queue)

    def test_command_shuffle_toggle(self):
        """
        Expected Result: /shuffle toggles shuffle mode.
        Actual Result: Shuffle toggled.
        """
        with patch("music_player.player_queue.toggle_shuffle") as mock_shuff:
            main.handle_command(self.state, "/shuffle")
            mock_shuff.assert_called_with(self.state)

    def test_command_playback_speed(self):
        """
        Expected Result: /speed converts arg to float and calls set_speed.
        Actual Result: Speed set to 1.5.
        """
        with patch("music_player.player_core.set_playback_speed") as mock_speed:
            main.handle_command(self.state, "/speed 1.5")
            mock_speed.assert_called_with(self.state, 1.5)

    def test_command_speed_invalid(self):
        """
        Expected Result: Handles non-numeric input without crashing.
        Actual Result: Usage: /speed <0.5 - 2.0>
        """
        with patch("music_player.player_core.set_playback_speed") as mock_speed:
            main.handle_command(self.state, "/speed fast")
            mock_speed.assert_not_called()

    # Sprint 4 Tests (Schedule/User Data)

    def test_command_schedule(self):
        """
        Expected Result: /schedule passes time string to player_time.
        Actual Result: Alarm set for 08:00.
        """
        with patch("music_player.player_time.set_alarm") as mock_alarm:
            main.handle_command(self.state, "/schedule 08:00")
            mock_alarm.assert_called_with(self.state, "08:00")

    def test_command_profiles(self):
        """
        Expected Result: /profile.new creates a new profile and /profile.switch switches to it.
        Actual Result: Profile 'Work' created.
        """
        with patch("music_player.user_data.create_profile") as mock_create, \
                patch("music_player.user_data.switch_profile") as mock_switch:
            main.handle_command(self.state, "/profile.new Work")
            mock_create.assert_called_with(self.state, "Work")

            main.handle_command(self.state, "/profile.switch Home")
            mock_switch.assert_called_with(self.state, "Home")

    def test_command_unknown(self):
        """
        Expected Result: Prints error for unknown commands but keeps loop running.
        Actual Result: Unknown command. Try /help. Returns True.
        """
        result = main.handle_command(self.state, "/notacommand")
        self.assertTrue(result)

    # Playback Worker Logic

    def test_playback_worker_updates(self):
        """
        Expected Result: Worker updates playback time when playing, and checks alarms.
        Actual Result: update_playback called, check_alarms called.
        """
        # Setup thread event to stop loop immediately after one pass
        stop_event = threading.Event()

        self.state.is_playing = True
        self.state.is_paused = False

        with patch("time.time", side_effect=[999.0, 1000.0]), \
                patch("time.sleep", side_effect=lambda *a: stop_event.set()), \
                patch("music_player.player_core.update_playback") as mock_update, \
                patch("music_player.player_time.check_alarms") as mock_alarm:
            # Run worker
            main._playback_worker(self.state, stop_event)

            # Check if playback updated
            mock_update.assert_called()
            # Check if alarms checked
            mock_alarm.assert_called()