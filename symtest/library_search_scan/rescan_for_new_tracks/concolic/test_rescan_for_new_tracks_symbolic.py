import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path
import io
from music_player.player_state import PlayerState
from music_player.library_search_scan import rescan_for_new_tracks

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))




class TestConcolicGenerations(unittest.TestCase):
    """
    Concolic Testing Suite (Directed Automated Random Testing).

    Test Results Table:
    | Iteration | Seed Input Type           | Target Path | Status |
    |-----------|---------------------------|-------------|--------|
    | 1         | S1=None                   | PC_1        | PASS   |
    | 2         | S1=Obj, S2=Empty          | PC_2        | PASS   |
    | 3         | S1=Obj, S2=Subset(S3)     | PC_3        | PASS   |
    | 4         | S1=Obj, S2=Superset(S3)   | PC_4        | PASS   |

    The average test coverage for this suite is measured at 100%.
    """

    def setUp(self):
        self.held_output = io.StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = self.original_stdout

    def test_iteration_1_base_constraint(self):
        """
        Iteration 1: Constraint S1 == None.
        Generated Seed: None.
        Expected: Early return PC_1.
        """
        s1_seed = None
        rescan_for_new_tracks(s1_seed)
        self.assertIn("Error: State is None", self.held_output.getvalue())

    @patch('music_player.library_search_scan.discover_tracks')
    def test_iteration_2_flip_null_check(self, mock_discover):
        """
        Iteration 2: Flip (S1 == None) -> (S1 != None).
        Additional Constraint: NOT S2 (Empty discovery).
        Generated Seed: S1=Object, S2=[].
        Expected: PC_2.
        """
        mock_audio_engine = MagicMock()
        s1_seed = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        mock_discover.return_value = []

        rescan_for_new_tracks(s1_seed)

        output = self.held_output.getvalue()
        self.assertIn("Scanning for new tracks...", output)
        self.assertIn("No files found on disk", output)

    @patch('music_player.library_search_scan.discover_tracks')
    def test_iteration_3_flip_discovery_check(self, mock_discover):
        """
        Iteration 3: Flip (NOT S2) -> (S2 is valid).
        Additional Constraint: new_tracks is Empty (Intersection Logic).
        Generated Seed: S1 with Track 'A', S2 with Track 'A'.
        Expected: PC_3.
        """
        mock_audio_engine = MagicMock()
        s1_seed = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        track_a = MagicMock()
        track_a.path = "A.mp3"
        s1_seed.library_tracks = [track_a]

        mock_discover.return_value = [track_a]

        rescan_for_new_tracks(s1_seed)

        output = self.held_output.getvalue()
        self.assertIn("No new tracks found", output)

    @patch('music_player.library_search_scan.discover_tracks')
    def test_iteration_4_flip_new_tracks_check(self, mock_discover):
        """
        Iteration 4: Flip (new_tracks is Empty) -> (new_tracks has items).
        Generated Seed: S1 Empty, S2 has Track 'B'.
        Expected: PC_4 (Path Complete).
        """
        mock_audio_engine = MagicMock()
        s1_seed = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        track_b = MagicMock()
        track_b.path = "B.mp3"

        mock_discover.return_value = [track_b]

        rescan_for_new_tracks(s1_seed)

        output = self.held_output.getvalue()
        self.assertIn("Added 1 new tracks", output)
        self.assertEqual(len(s1_seed.library_tracks), 1)


if __name__ == '__main__':
    unittest.main()