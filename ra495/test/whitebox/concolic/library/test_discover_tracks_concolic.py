import unittest
from unittest.mock import MagicMock, patch, PropertyMock
from pathlib import Path
from music_player.library import discover_tracks, Track


class TestConcolicIntegration(unittest.TestCase):

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

        print("\n[Concolic Engine] Executing Seed 1: Null environment")
        self.mock_music_dir.exists.return_value = False

        result = discover_tracks()
        self.assertEqual(result, [], "Failed to handle non-existent directory")

    def test_iteration_2_flip_is_file(self):

        print("[Concolic Engine] Executing Seed 2: Exists=True, Item=Directory")
        self.mock_music_dir.exists.return_value = True

        mock_dir_item = MagicMock(spec=Path)
        mock_dir_item.is_file.return_value = False
        self.mock_music_dir.iterdir.return_value = [mock_dir_item]

        result = discover_tracks()
        self.assertEqual(result, [], "Failed to skip directory items")

    def test_iteration_3_flip_supported_extension(self):

        print("[Concolic Engine] Executing Seed 3: File=True, Suffix=Unsupported")
        self.mock_music_dir.exists.return_value = True

        mock_file = MagicMock(spec=Path)
        mock_file.is_file.return_value = True
        type(mock_file).suffix = PropertyMock(return_value='.jpg')
        self.mock_music_dir.iterdir.return_value = [mock_file]

        result = discover_tracks()
        self.assertEqual(result, [], "Failed to filter unsupported extensions")

    def test_iteration_4_flip_duration_value(self):

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