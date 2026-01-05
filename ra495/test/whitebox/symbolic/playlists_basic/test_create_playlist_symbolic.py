import unittest
import unittest.mock
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


class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.S1 = PlayerState()

    def test_pc1_empty_input(self):

        S2 = ""

        with unittest.mock.patch("builtins.print") as mocked_print:
            create_playlist(self.S1, S2)
            mocked_print.assert_called_with("[pl] Usage: /pl.new <name>")

    def test_pc2_duplicate_found(self):

        S2 = "RockContext"
        self.S1.playlists.append(Playlist(name="RockContext"))

        with unittest.mock.patch("builtins.print") as mocked_print:
            create_playlist(self.S1, S2)
            mocked_print.assert_called_with(
                f"[pl] A playlist named '{S2}' already exists."
            )

    def test_pc3_success_path(self):

        S2 = "UniqueName"

        with unittest.mock.patch("builtins.print") as mocked_print:
            create_playlist(self.S1, S2)
            mocked_print.assert_called_with(
                "[pl] Created playlist 'UniqueName'."
            )


if __name__ == "__main__":
    unittest.main()
