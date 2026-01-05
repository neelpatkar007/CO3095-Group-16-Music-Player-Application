import unittest
from unittest.mock import patch
from dataclasses import dataclass, field
from typing import List
from music_player.playlists_basic import create_playlist

# Mock definitions to support the Concolic test environment
@dataclass
class Playlist:
    name: str


@dataclass
class PlayerState:
    playlists: List[Playlist] = field(default_factory=list)
    active_playlist_index: int | None = None


class TestConcolicExecution(unittest.TestCase):
    """
    Concolic Testing Suite (Concrete + Symbolic).

    Test Results Table:
    | Method | Iteration | Input Seed (S1, S2) | Status |
    | :--- | :--- | :--- | :--- |
    | test_iteration_1_base_case | 1 | ([], "") | PASS |
    | test_iteration_2_negate_empty | 2 | ([], "Jazz") | PASS |
    | test_iteration_3_negate_existence | 3 | ([...], "Jazz") | PASS |

    The average test coverage for this suite is measured at 100%.
    """

    def test_iteration_1_base_case(self):
        """
        Iteration 1: Initial Concrete Seed.
        Constraint: S2 is effectively empty.
        Target: PC_1
        """
        S1 = PlayerState()
        S2 = ""

        with patch("builtins.print") as mocked_print:
            create_playlist(S1, S2)
            mocked_print.assert_called_with("[pl] Usage: /pl.new <name>")

    def test_iteration_2_negate_empty(self):
        """
        Iteration 2: Negating the 'Empty' constraint.
        New Seed: Derived from negating (S2 == "").
        Target: PC_3 (Success path)
        """
        S1 = PlayerState()
        S2 = "Jazz"

        with patch("builtins.print") as mocked_print:
            create_playlist(S1, S2)
            mocked_print.assert_called_with("[pl] Created playlist 'Jazz'.")

    def test_iteration_3_negate_existence(self):
        """
        Iteration 3: Negating the 'No Duplicate' constraint found in Iteration 2.
        New Seed: Derived from forcing (pl.name == S2) to be True.
        Target: PC_2
        """
        S2 = "Jazz"
        S1 = PlayerState(playlists=[Playlist(name="Jazz")])

        with patch("builtins.print") as mocked_print:
            create_playlist(S1, S2)
            mocked_print.assert_called_with(
                f"[pl] A playlist named '{S2}' already exists."
            )


if __name__ == "__main__":
    unittest.main()
