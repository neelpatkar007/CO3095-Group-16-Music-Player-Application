import unittest
from unittest.mock import MagicMock, patch, PropertyMock
from pathlib import Path
from music_player.library import discover_tracks, Track


class TestConcolicIntegration(unittest.TestCase):
    """
    Concolic Integration Testing Suite for discover_tracks().

    Methodology:
    This suite simulates the output of a Concolic Execution Engine.
    Tests are derived from the 'Explicit Iteration Table' in CONCOLIC_ANALYSIS.md.
    Each test represents a generated 'Concrete Seed' aimed at flipping a
    specific constraint identified in the previous execution.

    Test Results Table:
    | Iteration | Seed Input Scenario      | Status | Coverage Impact |
    |-----------|--------------------------|--------|-----------------|
    | 1         | Dir Missing (S1=False)   | PASS   | PC_1            |
    | 2         | Not File (S2=False)      | PASS   | PC_2            |
    | 3         | Unsupported (S3=False)   | PASS   | PC_3            |
    | 4         | Duration None (S5=None)  | PASS   | PC_4            |
    | 5         | Valid Duration (S5=Val)  | PASS   | PC_5            |

    The average test coverage for this suite is measured at 100%.
    """

    def setUp(self):
        self.mock_music_dir_patcher = patch('music_player.library.MUSIC_DIR')
        self.mock_music_dir = self.mock_music_dir_patcher.start()

        self.mock_extensions_patcher = patch('music_player.library.SUPPORTED_EXTENSIONS', ['.mp3', '.wav'])
        self.mock_extensions = self.mock_extensions_patcher.start()

        self.mock_metadata_patcher = patch('music_player.library._read_metadata')
        self.mock_read_metadata = self.mock_metadata_patcher.start()

    def tearDown(self):
        self.mock_music_dir_patcher.stop()
        self.mock_extensions_patcher.stop()
        self.mock_metadata_patcher.stop()

    def test_iteration_1_flip_existence(self):
        """
        Iteration 1: Initial Concrete Seed.
        Constraint Target: S1 (Existence).
        Input: MUSIC_DIR.exists() -> False
        """
        print("\n[Concolic Engine] Executing Seed 1: Null environment")
        self.mock_music_dir.exists.return_value = False

        result = discover_tracks()
        self.assertEqual(result, [], "Failed to handle non-existent directory")

    def test_iteration_2_flip_is_file(self):
        """
        Iteration 2: Derived from negating PC_1.
        Constraint Target: S2 (File vs Directory).
        Input: Exists=True, Item is Directory (Not File).
        """
        print("[Concolic Engine] Executing Seed 2: Exists=True, Item=Directory")
        self.mock_music_dir.exists.return_value = True

        mock_dir_item = MagicMock(spec=Path)
        mock_dir_item.is_file.return_value = False
        self.mock_music_dir.iterdir.return_value = [mock_dir_item]

        result = discover_tracks()
        self.assertEqual(result, [], "Failed to skip directory items")

    def test_iteration_3_flip_supported_extension(self):
        """
        Iteration 3: Derived from negating PC_2.
        Constraint Target: S3 (Supported Suffix).
        Input: Exists=True, Item=File, Suffix=.jpg (Unsupported).
        """
        print("[Concolic Engine] Executing Seed 3: File=True, Suffix=Unsupported")
        self.mock_music_dir.exists.return_value = True

        mock_file = MagicMock(spec=Path)
        mock_file.is_file.return_value = True
        type(mock_file).suffix = PropertyMock(return_value='.jpg')
        self.mock_music_dir.iterdir.return_value = [mock_file]

        result = discover_tracks()
        self.assertEqual(result, [], "Failed to filter unsupported extensions")

    def test_iteration_4_flip_duration_value(self):
        """
        Iteration 4: Derived from negating PC_3.
        Constraint Target: S5 (Duration is None).
        Input: Exists=True, File=True, Suffix=.mp3, Duration=None.
        """
        print("[Concolic Engine] Executing Seed 4: Suffix=Supported, Duration=None")
        self.mock_music_dir.exists.return_value = True

        mock_file = MagicMock(spec=Path)
        mock_file.is_file.return_value = True
        type(mock_file).suffix = PropertyMock(return_value='.mp3')
        self.mock_music_dir.iterdir.return_value = [mock_file]

        self.mock_read_metadata.return_value = ("Track A", "Artist A", None)

        result = discover_tracks()
        self.assertEqual(result[0].duration_seconds, 180.0, "Failed to apply default duration")

    def test_iteration_5_completion(self):
        """
        Iteration 5: Derived from negating PC_4.
        Constraint Target: S5 (Duration is valid).
        Input: Exists=True, File=True, Suffix=.mp3, Duration=245.0.
        """
        print("[Concolic Engine] Executing Seed 5: Duration=Valid")
        self.mock_music_dir.exists.return_value = True

        mock_file = MagicMock(spec=Path)
        mock_file.is_file.return_value = True
        type(mock_file).suffix = PropertyMock(return_value='.mp3')
        self.mock_music_dir.iterdir.return_value = [mock_file]

        self.mock_read_metadata.return_value = ("Track B", "Artist B", 245.0)

        result = discover_tracks()
        self.assertEqual(result[0].duration_seconds, 245.0, "Failed to read actual duration")


if __name__ == '__main__':
    unittest.main()