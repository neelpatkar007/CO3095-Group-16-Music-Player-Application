import unittest
import json
from unittest.mock import MagicMock, patch, mock_open
from pathlib import Path
from music_player import player_time


class TestPlayerTimeSpec(unittest.TestCase):
    """
    Black-Box Specification Testing for player_time.py.
    Tool: Python unittest + unittest.mock
    Test Technique: Category Partition Method
    Source: TSL Generator playerTime.txt.
    """

    def setUp(self):
        # Setup generic mock track
        self.mock_track = MagicMock()
        self.mock_track.path = Path("song.mp3")
        self.mock_track.display_name = "Song A"

        # Setup State
        self.state = MagicMock()
        self.state.current_track = self.mock_track
        self.state.scheduled_alarms = []
        self.state.library_tracks = [self.mock_track]

        # Set numeric values for comparisons
        self.state.position_seconds = 120.0
        # Ensure audio_engine exists
        self.state.audio_engine = MagicMock()

    # Save Resume State
    def test_save_resume_state_spec(self):
        """
        Expected Result:
         - Function handles None inputs without crashing.
         - Valid inputs result in a JSON file write with key "last_track_path" and correct position.
        Actual Result: PASSED [100%][state] Playback saved at 2m 0s.
        """
        # State None
        player_time.save_resume_state(None)

        # Current Track None
        self.state.current_track = None
        player_time.save_resume_state(self.state)

        # Path None
        self.state.current_track = MagicMock()
        self.state.current_track.path = None
        player_time.save_resume_state(self.state)

        # Valid Save
        self.state.current_track = self.mock_track # Reset to valid track

        with patch("builtins.open", mock_open()) as m_file, \
                patch("json.dump") as m_json:
            player_time.save_resume_state(self.state)
            m_json.assert_called_once()

            # Verify data content
            args, _ = m_json.call_args
            data = args[0]
            self.assertEqual(data["last_track_path"], "song.mp3")
            self.assertEqual(data["position"], 120.0)

    # Load Resume State
    def test_load_resume_state_spec(self):
        """
        Covers: State None, File Missing, Corrupt JSON, Valid Load.

        Expected Result:
         - Missing files or corrupt JSON trigger error messages and do not crash.
         - Valid JSON loads successfully and prints "Found resume state".
        Actual Result: Passed. Verified error handling and successful load.
        """
        # State None
        player_time.load_resume_state(None)

        # File Missing
        with patch("pathlib.Path.exists", return_value=False):
            player_time.load_resume_state(self.state)

        # Corrupt JSON
        with patch("pathlib.Path.exists", return_value=True), \
                patch("builtins.open", mock_open(read_data="{invalid")), \
                patch("json.load", side_effect=json.JSONDecodeError("msg", "doc", 0)), \
                patch("builtins.print") as m_print:
            player_time.load_resume_state(self.state)
            self.assertTrue(m_print.called, "Should print error on JSON failure")

        # Valid Load
        valid_json = {"last_track_path": "saved.mp3", "position": 10.0}
        with patch("pathlib.Path.exists", return_value=True), \
                patch("builtins.open", mock_open()), \
                patch("json.load", return_value=valid_json), \
                patch("builtins.print") as m_print:
            player_time.load_resume_state(self.state)

            # Verify success message
            printed_messages = [call.args[0] for call in m_print.call_args_list]
            self.assertTrue(any("Found resume state" in msg for msg in printed_messages))

    # Set Alarm
    def test_set_alarm_spec(self):
        """
        Expected Result:
         - Non-string types, malformed strings, and out-of-range times will produce error messages.
         - Valid HH:MM string updates state.scheduled_alarms.
        Actual Result: Passed. Verified input validation and successful alarm setting.
        """
        # Invalid Input Type
        player_time.set_alarm(self.state, 12345)

        # Invalid Format
        with patch("builtins.print") as m_print:
            player_time.set_alarm(self.state, "999")
            player_time.set_alarm(self.state, "12:000")
            m_print.assert_called()

        # Invalid Range
        with patch("builtins.print") as m_print:
            player_time.set_alarm(self.state, "25:00")
            player_time.set_alarm(self.state, "12:61")
            m_print.assert_called()

        # Invalid Numeric
        with patch("builtins.print") as m_print:
            player_time.set_alarm(self.state, "aa:bb")
            m_print.assert_called()

        # Valid Set
        with patch("builtins.print") as m_print:
            player_time.set_alarm(self.state, "08:30")
            self.assertEqual(self.state.scheduled_alarms, ["08:30"])
            self.assertTrue(any("Alarm set" in str(c) for c in m_print.call_args_list))

    # Cancel & Check Alarms
    def test_alarm_management_spec(self):
        """
        Expected Result:
         - cancel_alarm clears the list.
         - check_alarms triggers only when the mocked system time matches the stored alarm, clearing it when triggered.
        Actual Result: Passed. Verified alarm cancellation and triggering behavior with mocked time.
        """
        # Cancel No Alarms
        self.state.scheduled_alarms = []
        with patch("builtins.print") as m_print:
            player_time.cancel_alarm(self.state)
            m_print.assert_called_with("[alarm] No alarms set.")

        # Cancel Valid
        self.state.scheduled_alarms = ["10:00"]
        with patch("builtins.print") as m_print:
            player_time.cancel_alarm(self.state)
            self.assertEqual(self.state.scheduled_alarms, [])

        # Check No Match
        self.state.scheduled_alarms = ["20:00"]

        with patch("music_player.player_time.datetime") as m_datetime_module:
            m_datetime_module.datetime.now.return_value.strftime.return_value = "10:00"

            player_time.check_alarms(self.state)
            self.assertEqual(self.state.scheduled_alarms, ["20:00"])

        # Check Match Triggered
        with patch("music_player.player_time.datetime") as m_datetime_module, \
                patch("builtins.print") as m_print:
            m_datetime_module.datetime.now.return_value.strftime.return_value = "20:00"

            player_time.check_alarms(self.state)

            self.assertEqual(self.state.scheduled_alarms, [])
            self.assertTrue(any("ALARM TRIGGERED" in str(c) for c in m_print.call_args_list))

    # Recently Added
    def test_show_recently_added_spec(self):
        """
        Expected Result:
         - Returns early/prints message for None/Empty library.
         - Sorts and displays tracks if library is valid.
        Actual Result: Passed. Defensive checks verified, printing logic executed for valid library.
        """
        # Library None
        self.state.library_tracks = None
        with patch("builtins.print") as m_print:
            player_time.show_recently_added(self.state)
            m_print.assert_called()

        # Valid Library
        t_old = MagicMock();
        t_old.display_name = "Old";
        t_old.path = Path("old.mp3")
        t_new = MagicMock();
        t_new.display_name = "New";
        t_new.path = Path("new.mp3")
        self.state.library_tracks = [t_old, t_new]

        with patch("pathlib.Path.exists", return_value=True), \
                patch("pathlib.Path.stat") as m_stat, \
                patch("builtins.print") as m_print:
            player_time.show_recently_added(self.state)
            self.assertTrue(any("Recently Added Songs" in str(c) for c in m_print.call_args_list))