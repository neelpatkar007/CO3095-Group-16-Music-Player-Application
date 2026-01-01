import unittest
from unittest.mock import MagicMock, patch, PropertyMock
from music_player import player_queue
from music_player.library import Track
from pathlib import Path


class MockAudioEngine:
    """
    Simulates the AudioBackend for testing playback logic without real audio.
    """

    def __init__(self):
        self.stop_called = False
        self.play_called = False

    def stop(self):
        self.stop_called = True

    def play(self, path, start_pos=0.0):
        self.play_called = True

    def is_busy(self):
        return False

class TestPlayerQueueCoverage(unittest.TestCase):
    """
    Whitebox Branch Testing for player_queue.py.
    Tool: Python unittest + unittest.mock
    Technique: White-Box Branch Testing
    """

    def setUp(self):
        """
        Setup valid PlayerState with 3 tracks for each test.
        """
        self.track1 = Track(Path("song1.mp3"), "Song 1", "Artist 1", 180)
        self.track2 = Track(Path("song2.mp3"), "Song 2", "Artist 2", 200)
        self.track3 = Track(Path("song3.mp3"), "Song 3", "Artist 3", 210)

        self.state = MagicMock()
        self.state.tracks = [self.track1, self.track2, self.track3]
        self.state.library_tracks = [self.track1, self.track2, self.track3]
        self.state.current_index = 0
        self.state.current_track = self.track1
        self.state.history = []
        self.state.audio_engine = MockAudioEngine()
        self.state.is_playing = False
        self.state.is_paused = False
        self.state.loop_mode = "off"
        self.state.shuffle_active = False
        self.state.position_seconds = 0.0
        self.state.playlists = []

    # Helper Function Tests

    def test_get_tracks_safe(self):
        """
        Test _get_tracks_safe helper.
        Branches: List, None, Set, Invalid
        """
        # Normal List
        self.assertEqual(player_queue._get_tracks_safe(self.state), self.state.tracks)

        # None
        self.state.tracks = None
        self.assertEqual(player_queue._get_tracks_safe(self.state), [])

        # Set
        self.state.tracks = {"track1", "track2"}
        result = player_queue._get_tracks_safe(self.state)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)

        # Invalid Type
        self.state.tracks = 123
        self.assertEqual(player_queue._get_tracks_safe(self.state), [])

    def test_ensure_decoupled(self):
        """
        Test -> _ensure_queue_decoupled.
        Branches : Linked to Library, Linked to Playlist
        """
        # Tracks linked to Library
        self.state.tracks = self.state.library_tracks
        player_queue._ensure_queue_decoupled(self.state)
        self.assertIsNot(self.state.tracks, self.state.library_tracks)

        # Tracks linked to Playlist
        pl = MagicMock()
        pl.tracks = [self.track1]
        self.state.playlists = [pl]
        self.state.tracks = pl.tracks
        player_queue._ensure_queue_decoupled(self.state)
        self.assertIsNot(self.state.tracks, pl.tracks)

    # Next + Previous Track Tests

    def test_next_track_logic(self):
        """
        Test next_track navigation.
        Branches: Sequential, End of a List, Loop All, Loop One
        """
        # Standard Next
        player_queue.next_track(self.state)
        self.assertEqual(self.state.current_index, 1)

        # End of Playlist
        self.state.current_index = 2
        player_queue.next_track(self.state)
        self.assertEqual(self.state.current_index, 2)

        # Loop All
        self.state.loop_mode = "all"
        self.state.current_index = 2
        player_queue.next_track(self.state)
        self.assertEqual(self.state.current_index, 0)

        # Loop One
        self.state.loop_mode = "one"
        self.state.current_index = 1
        player_queue.next_track(self.state)
        self.assertEqual(self.state.current_index, 1)

    @patch("random.randint")
    def test_next_track_shuffle(self, mock_rand):
        """
        Test next_track with Shuffle active.
        Branches: Shuffle n=2, Shuffle n>2
        """
        self.state.shuffle_active = True

        # n=2
        self.state.tracks = [self.track1, self.track2]
        self.state.current_index = 0
        player_queue.next_track(self.state)
        self.assertEqual(self.state.current_index, 1)

        # n>2
        self.state.tracks = [self.track1, self.track2, self.track3]
        self.state.current_index = 0
        mock_rand.return_value = 2
        player_queue.next_track(self.state)
        self.assertEqual(self.state.current_index, 2)

    def test_prev_track_logic(self):
        """
        Test previous_track navigation.
        Branches: Sequential, Start of a List, Loop All
        """
        # Standard Prev
        self.state.current_index = 1
        player_queue.previous_track(self.state)
        self.assertEqual(self.state.current_index, 0)

        # Start of Playlist
        self.state.current_index = 0
        player_queue.previous_track(self.state)
        self.assertEqual(self.state.current_index, 0)

        # Loop All
        self.state.loop_mode = "all"
        self.state.current_index = 0
        player_queue.previous_track(self.state)
        self.assertEqual(self.state.current_index, 2)

    def test_prev_track_shuffle_history(self):
        """
        Test previous_track with Shuffle active.
        Branch: Use History Stack
        """
        self.state.shuffle_active = True
        self.state.history = [self.track2]  # Last played was track 2

        player_queue.previous_track(self.state)
        self.assertEqual(self.state.current_index, 1)

    # Playback & Exception Handling

    def test_next_track_playback_exceptions(self):
        """
        Test error handling during playback transition.
        Branches: Stop fails, Play fails, Busy check fails
        """
        self.state.is_playing = True

        # Simulate engine failures
        self.state.audio_engine.stop = MagicMock(side_effect=Exception("Stop fail"))
        self.state.audio_engine.play = MagicMock(side_effect=Exception("Play fail"))

        player_queue.next_track(self.state)
        self.assertFalse(self.state.is_playing)

    def test_next_track_defensive(self):
        """
        Test checks for invalid state/inputs.
        Branches: State is None, Tracks is None, Tracks is Empty
        """
        # Invalid State
        player_queue.next_track(None)

        # Empty List
        self.state.tracks = []
        player_queue.next_track(self.state)

        # None List
        self.state.tracks = None
        player_queue.next_track(self.state)

    # Queue Management Commands

    def test_add_to_queue(self):
        """
        Test /q.add command.
        Branches: Happy Path, Corrupt State Recovery, Not Found
        """
        # Happy Path
        player_queue.add_to_queue(self.state, "Song 2")
        self.assertEqual(len(self.state.tracks), 4)

        # Corrupt State
        self.state.tracks = 123
        player_queue.add_to_queue(self.state, "Song 1")
        self.assertEqual(len(self.state.tracks), 1)

        # Not Found
        player_queue.add_to_queue(self.state, "NonExistent")

    def test_remove_from_queue(self):
        """
        Test /q.remove command.
        Branches: Remove by Index, Remove by Name
        """
        # Remove by Index
        self.state.current_index = 1
        player_queue.remove_from_queue(self.state, "1")  # Remove track at index 1
        self.assertEqual(len(self.state.tracks), 2)
        self.assertEqual(self.state.current_index, 0)

        # Remove by Name
        self.state.tracks = [self.track1, self.track2]
        self.state.current_index = 1
        player_queue.remove_from_queue(self.state, "Song 1")
        self.assertEqual(len(self.state.tracks), 1)
        self.assertEqual(self.state.current_index, 0)

    def test_clear_queue(self):
        """
        Test /q.clear command.
        Branches: Keep Current, Clear Empty, Clear Corrupt
        """
        # Keep Current Song
        self.state.current_index = 1
        player_queue.clear_queue(self.state)
        self.assertEqual(len(self.state.tracks), 1)
        self.assertEqual(self.state.tracks[0], self.track2)

        # Clear Corrupt Type
        self.state.tracks = 123  # Int forces reset
        player_queue.clear_queue(self.state)
        self.assertEqual(self.state.tracks, [])

    # State Toggles & Display

    def test_toggle_shuffle(self):
        """
        Test /shuffle.
        Branches: Toggle On, Reset Index
        """
        # Toggle On
        player_queue.toggle_shuffle(self.state)
        self.assertTrue(self.state.shuffle_active)

        # Reset Index if out of bounds
        self.state.current_index = 10
        player_queue.toggle_shuffle(self.state)  # Off
        player_queue.toggle_shuffle(self.state)  # On
        self.assertEqual(self.state.current_index, 0)

    def test_set_loop_mode(self):
        """
        Test /loop.
        Branches: Valid inputs, Invalid inputs, Defensive Property Check
        """
        # Valid
        player_queue.set_loop_mode(self.state, "one")
        self.assertEqual(self.state.loop_mode, "one")

        # Invalid
        player_queue.set_loop_mode(self.state, "invalid_mode")
        self.assertEqual(self.state.loop_mode, "one")

        # AttributeError
        bad_state = MagicMock()
        p = PropertyMock(side_effect=AttributeError)
        type(bad_state).loop_mode = p
        player_queue.set_loop_mode(bad_state, "all")

    def test_show_queue(self):
        """
        Test /queue display.
        Branches: Playing Marker, Paused Marker, Empty
        """
        # Playing
        self.state.tracks = [self.track1]
        self.state.is_playing = True
        player_queue.show_queue(self.state)

        # Paused
        self.state.is_playing = False
        self.state.is_paused = True
        player_queue.show_queue(self.state)

if __name__ == '__main__':
    unittest.main()