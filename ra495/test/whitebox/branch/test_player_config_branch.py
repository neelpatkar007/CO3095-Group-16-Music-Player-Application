import unittest
from unittest.mock import MagicMock, patch
from music_player import player_config
from music_player.player_state import PlayerState
from music_player.library import Track
from pathlib import Path


class TestPlayerConfigBranch(unittest.TestCase):
    """
    White-Box Branch Testing for player_config.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: Branch Testing (White-Box)
    """

    def setUp(self):
        self.state = PlayerState([], MagicMock())
        self.track1 = Track(Path("a.mp3"), "Song A", "Artist A", 100)
        self.state.library_tracks = [self.track1]

    # Load Settings Tests

    def test_load_settings_branches(self):
        """
        Branches:
         - File exists
         - Audio Engine exists
        """
        # File exists check
        with patch("pathlib.Path.exists", return_value=False):
            player_config.load_settings(self.state)  # False path Return

        # Audio Engine check
        with patch("pathlib.Path.exists", return_value=True), \
                patch("builtins.open", unittest.mock.mock_open(read_data="{}")):
            # Engine exists (True)
            self.state.audio_engine = MagicMock()
            player_config.load_settings(self.state)
            self.state.audio_engine.set_volume.assert_called()

            # Engine missing (False)
            self.state.audio_engine = None
            player_config.load_settings(self.state)

    # Add Tag Tests

    def test_add_tag_branches(self):
        """
        Branches:
         - New and Duplicate tag
         - Tag List initialisation
        """
        path = str(self.track1.path)

        # Init List (True)
        self.state.song_tags = {}
        player_config.add_tag(self.state, "1", "fresh")
        self.assertIn("fresh", self.state.song_tags[path])

        # Duplicate Check (True)
        player_config.add_tag(self.state, "1", "fresh")