import unittest
from unittest.mock import patch
from music_player import player_help


class TestPlayerHelpCoverage(unittest.TestCase):
    """
    Black-Box Specification Testing for player_help.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: Category Partition Method
    Source: TSL Generated Test Cases playerHelp.txt.
    """

    @patch('builtins.print')
    def test_print_help_all_commands(self, mock_print):
        """
        Iterates through every known command in player_help.py to trigger
        specific help blocks.
        """
        # List derived from player_help.py
        commands_to_test = [
            # Menu
            None,
            "",
            "   ",

            # Basic Playback
            "play", "/play",
            "pause",
            "stop",
            "next",
            "prev",
            "seek",
            "rw",
            "ff",

            # Volume Controls
            "volume", "vol",
            "mute",
            "unmute",

            # Queue & Advanced
            "shuffle",
            "loop",
            "queue",
            "q.add",
            "q.remove",
            "playnext",
            "q.clear",
            "speed",
            "sleep",

            # Metrics & Ratings
            "like",
            "likes",
            "top",
            "rate",
            "rated",
            "stats",

            # Playlist Management
            "pl.new",
            "pl.rename",
            "pl.del",
            "pl.list",
            "pl.open",
            "pl.show",
            "pl.play",
            "pl.close",
            "pl.export",
            "pl.sort",

            # Playlist Editing
            "pl.add",
            "pl.remove",
            "pl.move",
            "pl.merge",
            "pl.copy",

            # Library & Tags
            "search",
            "songs",
            "artists",
            "albums",
            "scan",
            "recent",
            "import",
            "edit",
            "tag.add",
            "tags",
            "tag.filter",

            # Profiles & Scheduling
            "profile",
            "profiles",
            "profile.new",
            "profile.switch",
            "schedule",
            "schedule.cancel",

            # UI & System
            "info",
            "progress",
            "bar",
            "list",
            "quit", "exit", "q",

            # Unknown Commands
            "not_a_command",
            "/unknown_cmd"
        ]

        for cmd in commands_to_test:
            with self.subTest(command=cmd):
                # Execute the function
                player_help.print_help(cmd)

                # Verify something was printed
                self.assertTrue(mock_print.called, f"print_help failed to produce output for '{cmd}'")
                mock_print.reset_mock()


if __name__ == '__main__':
    unittest.main()