import unittest
from unittest.mock import patch
from dataclasses import dataclass, field
from typing import List
from music_player.playlists_basic import create_playlist

@dataclass
class Playlist:
    name: str


@dataclass
class PlayerState:
    playlists: List[Playlist] = field(default_factory=list)
    active_playlist_index: int | None = None


class TestConcolicExecution(unittest.TestCase):

    def test_iteration_1_base_case(self):
        S1 = PlayerState()
        S2 = ""

        with patch("builtins.print") as mocked_print:
            create_playlist(S1, S2)
            mocked_print.assert_called_with("[pl] Usage: /pl.new <name>")

    def test_iteration_2_negate_empty(self):
        S1 = PlayerState()
        S2 = "Jazz"

        with patch("builtins.print") as mocked_print:
            create_playlist(S1, S2)
            mocked_print.assert_called_with("[pl] Created playlist 'Jazz'.")

    def test_iteration_3_negate_existence(self):
        S2 = "Jazz"
        S1 = PlayerState(playlists=[Playlist(name="Jazz")])

        with patch("builtins.print") as mocked_print:
            create_playlist(S1, S2)
            mocked_print.assert_called_with(
                f"[pl] A playlist named '{S2}' already exists."
            )


if __name__ == "__main__":
    unittest.main()
