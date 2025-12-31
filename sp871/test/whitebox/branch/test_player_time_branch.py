import unittest
from unittest.mock import MagicMock, patch
from music_player import player_time

class TestPlayerTimeBranch(unittest.TestCase):
    """
    White-Box Branch Tests for player_time.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: White-Box Branch Testing
    """

    def test_save_resume_defensive_branches(self):
        """
        Expected Result: Function returns early and safely without crashes.
        Actual Result: Passed.
        """
        # State None
        player_time.save_resume_state(None)

        # State missing attribute
        empty_state = MagicMock(spec=object)
        player_time.save_resume_state(empty_state)

        # current_track missing path
        state_bad_track = MagicMock()
        state_bad_track.current_track = "I am a string"
        player_time.save_resume_state(state_bad_track)

    def test_load_resume_defensive_branches(self):
        """
        Expected Result: Function returns early.
        Actual Result: PASSED [100%][state] Corrupt resume file.
        """
        # Missing audio_engine
        empty_state = MagicMock(spec=object)
        player_time.load_resume_state(empty_state)

        # JSON valid but missing path
        state = MagicMock()
        state.audio_engine = MagicMock()

        with patch("pathlib.Path.exists", return_value=True), \
                patch("builtins.open", unittest.mock.mock_open(read_data='{"position": 10}')), \
                patch("json.load", return_value={"position": 10}):
            player_time.load_resume_state(state)

    def test_set_alarm_defensive_branches(self):
        """
        Expected Result: Function returns early when input type is invalid or state is malformed.
        Actual Result: Passed. Type checks prevented runtime errors.
        """
        state = MagicMock()
        state.scheduled_alarms = []

        # Not string
        player_time.set_alarm(state, 123)

        # Missing attr
        empty_state = MagicMock(spec=object)
        player_time.set_alarm(empty_state, "10:00")

    def test_cancel_alarm_defensive_branches(self):
        """
        Expected Result: Function returns safely for None or invalid state objects.
        Actual Result: Passed.
        """
        player_time.cancel_alarm(None)

        empty_state = MagicMock(spec=object)
        player_time.cancel_alarm(empty_state)

    def test_check_alarms_defensive_branches(self):
        """
        Expected Result: Function returns early if alarm list is None, invalid type, or empty.
        Actual Result: Passed.
        """
        state = MagicMock()

        # None
        state.scheduled_alarms = None
        player_time.check_alarms(state)

        # Not list
        state.scheduled_alarms = "NotAList"
        player_time.check_alarms(state)

        # Empty
        state.scheduled_alarms = []
        player_time.check_alarms(state)

    def test_show_recent_defensive_branches(self):
        """
        Expected Result: Returns early for invalid inputs. Prints "No valid files found" if list exists but has no valid tracks.
        Actual Result:
            PASSED [100%][recent] Library is empty.
            [recent] Library is empty.
        """
        # Missing attr
        empty_state = MagicMock(spec=object)
        player_time.show_recently_added(empty_state)

        # None
        state = MagicMock()
        state.library_tracks = None
        player_time.show_recently_added(state)

        # Not list
        state.library_tracks = "I am a string"
        player_time.show_recently_added(state)

        # Valid list but no valid tracks
        state.library_tracks = [MagicMock()]
        t = MagicMock()
        t.path = None
        state.library_tracks = [t]

        with patch("builtins.print") as m_print:
            player_time.show_recently_added(state)
            m_print.assert_called_with("[recent] No valid files found.")