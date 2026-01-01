import unittest
from unittest.mock import MagicMock, patch, mock_open
from music_player import user_data
from music_player.player_state import PlayerState

# Mocks

class MockTrack:
    def __init__(self, path, artist="Unknown", title="Unknown", duration=0):
        self.path = path
        self.artist = artist
        self.title = title
        self.duration_seconds = duration
        self.display_name = title


class MockPlaylist:
    def __init__(self, name, tracks=None):
        self.name = name
        self.tracks = tracks if tracks else []

# Test Class

class TestUserDataStatement(unittest.TestCase):

    """
    White-Box Statement Tests for user_data.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: White-Box Statement Testing
    """

    def setUp(self):
        self.mock_state = MagicMock(spec=PlayerState)
        self.mock_state.profiles = {}
        self.mock_state.active_profile = "default"
        self.mock_state.playlists = []
        self.mock_state.liked_tracks = set()
        self.mock_state.song_ratings = {}
        self.mock_state.library_tracks = []
        self.mock_state.current_track = None

    def test_helpers_serialize_none(self):
        """
        Expected Result: Returns an empty dictionary.
        Actual Result: Passed.
        """
        res = user_data._serialize_current_state(None)
        self.assertEqual(res, {})

    def test_helpers_save_profiles_error(self):
        """
        Expected Result: Catches the OSError/Exception and prints an error message.
        Actual Result: PASSED [100%][profile] Error saving: Disk full
        """
        with patch("builtins.open", mock_open()) as m:
            m.side_effect = OSError("Disk full")
            user_data._save_profiles(self.mock_state)

    def test_helpers_save_current_none(self):
        """
        Expected Result: Returns immediately without error when state is None.
        Actual Result: Passed.
        """
        user_data._save_current_to_profile(None)

    def test_helpers_apply_data_none_or_empty(self):
        """
        Expected Result: If state is None then returns and when data is empty liked_tracks set and playlists list empty.
        Actual Result: Passed.
        """
        # State None
        user_data._apply_profile_data(None, {})

        # Data Empty
        user_data._apply_profile_data(self.mock_state, {})
        self.assertEqual(self.mock_state.liked_tracks, set())
        self.assertEqual(self.mock_state.playlists, [])

    def test_load_profiles_not_exists(self):
        """
        Expected Result: Detected that file does not exist and calls _save_profiles to create a default.
        Actual Result: Passed.
        """
        with patch("pathlib.Path.exists", return_value=False):
            with patch("music_player.user_data._save_profiles") as mock_save:
                user_data.load_profiles_index(self.mock_state)
                mock_save.assert_called_once()

    def test_load_profiles_exception(self):
        """
        Expected Result: Catches JSONDecodeError and prints error message.
        Actual Result: PASSED [100%][profile] Error loading profiles: Expecting value: line 1 column 1 (char 0)
        """
        with patch("pathlib.Path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data="INVALID JSON")):
                user_data.load_profiles_index(self.mock_state)

    def test_create_profile_invalid_state(self):
        """
        Expected Result: Prints error message and returns.
        Actual Result: PASSED [100%][profile] Error: Invalid state.
        """
        user_data.create_profile(None, "new")

    def test_create_profile_invalid_names(self):
        """
        Expected Result: Prints error messages for empty name, reserved name, and duplicate name.
        Actual Result:
            PASSED [100%][profile] Error: Name cannot be empty.
            [profile] 'default' is reserved.
            [profile] Profile 'ex' already exists.
        """
        # Empty Name
        user_data.create_profile(self.mock_state, "")

        # Reserved Name
        user_data.create_profile(self.mock_state, "default")

        # Duplicate Name
        self.mock_state.profiles = {"ex": {}}
        user_data.create_profile(self.mock_state, "ex")

    def test_switch_profile_invalid(self):
        """
        Expected Result: Prints errors for inavlid state and non-existent profiles, switching to current profile message "already on profile".
        Actual Result:
            PASSED [100%][profile] Error: Invalid state.
            [profile] Profile 'non_existent' does not exist.
            [profile] Already on 'default'.
        """
        user_data.switch_profile(None, "p1")  # Invalid state
        user_data.switch_profile(self.mock_state, "non_existent")  # Missing
        user_data.switch_profile(self.mock_state, "default")  # Already active

    def test_advanced_search_invalid_state(self):
        """
        Expected Result: Prints error message.
        Actual Result: PASSED [100%][search] Error: Invalid state.
        """
        user_data.advanced_search(None, "query")

    def test_advanced_search_none_results(self):
        """
        Expected Result: Handles case where library_tracks is None by treating it as empty list.
        Actual Result: PASSED [100%][search] No matches found.
        """
        self.mock_state.library_tracks = None
        user_data.advanced_search(self.mock_state, "query")

    @patch("music_player.time_utils.parse_timecode", return_value=100)
    @patch("music_player.time_utils.format_mm_ss", return_value="01:40")
    def test_advanced_search_branches(self, mock_fmt, mock_parse):
        """
        Expected Result: Filter correctly by artist, duration greater than, and duration less than.
        Actual Result:
            PASSED [100%][search] Found 1 matches:
              1. Song A (01:40)
            [search] Found 1 matches:
              1. Song A (01:40)
            [search] Found 1 matches:
              1. Song B (01:40)
        """
        t1 = MockTrack("/path/1.mp3", artist="The Band", title="Song A", duration=200)
        t2 = MockTrack("/path/2.mp3", artist="Solo Guy", title="Song B", duration=50)
        self.mock_state.library_tracks = [t1, t2]

        user_data.advanced_search(self.mock_state, "artist:Band")
        user_data.advanced_search(self.mock_state, "duration>1:00")
        user_data.advanced_search(self.mock_state, "duration<1:00")

    def test_rate_song_errors(self):
        """
        Expected Result: Return on State None, print "No song playing" when no track is playing, print error when rating not number .
        Actual Result:
            PASSED [100%][rate] No song playing.
            [rate] No song playing.
            [rate] Rating must be a whole number 1-5.
            [rate] Rating must be a whole number 1-5.
        """
        # Invalid state
        user_data.rate_song(None, "5")

        # No track playing
        self.mock_state.current_track = None
        user_data.rate_song(self.mock_state, "5")

        # Invalid input
        self.mock_state.current_track = MockTrack("/p.mp3")
        user_data.rate_song(self.mock_state, "not_a_number")

        # Number out of range
        user_data.rate_song(self.mock_state, "6")

        # Track has no path
        bad_track = MagicMock()
        del bad_track.path
        self.mock_state.current_track = bad_track
        user_data.rate_song(self.mock_state, "3")