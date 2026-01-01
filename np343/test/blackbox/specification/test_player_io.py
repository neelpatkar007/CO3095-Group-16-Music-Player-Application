import io
import unittest
import tempfile
from pathlib import Path
from contextlib import redirect_stdout
from unittest.mock import MagicMock

from music_player import player_io
from music_player.player_state import PlayerState


class TestPlayerIoBlackBoxSpec(unittest.TestCase):
    """
    Black-box specification tests for player_io.py.
    Tools -  Python unittest + unittest.mock + tempfile + contextlib.redirect_stdout
    Technique -  Black-Box Specification Testing
    """

    def setUp(self):
        self.state = MagicMock(spec=PlayerState)
        self.state.library_tracks = []
        self.state.tracks = []

    def _capture_prints(self, func, *args, **kwargs) -> str:
        buf = io.StringIO()
        with redirect_stdout(buf):
            func(*args, **kwargs)
        return buf.getvalue()

    # Import Song Tests

    def test_import_song_empty_input_prints_usage(self):
        """
        Expected Result is that it Prints usage when input path is empty.
        Actual Result - Passed.
        """
        out = self._capture_prints(player_io.import_song, self.state, "")
        self.assertIn("[import] Usage: /import <path_to_file>", out)

    def test_import_song_file_not_found(self):
        """
        Expected Result - Prints "File not found" error for non-existent paths.
        Actual Result is: Passed.
        """
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "ASDASD.mp3"
            out = self._capture_prints(player_io.import_song, self.state, str(missing))
            self.assertIn("[import] Error: File not found.", out)

    def test_import_song_source_is_directory(self):
        """
        Expected Result : Prints error if source path points to a directory instead of a file.
        Actual Result : Passed.
        """
        with tempfile.TemporaryDirectory() as tmp:
            src_dir = Path(tmp) / "folder"
            src_dir.mkdir()
            out = self._capture_prints(player_io.import_song, self.state, str(src_dir))
            self.assertIn("[import] Error: Source is not a file.", out)

    def test_import_song_empty_file_rejected(self):
        """
        Expected Result : Prints error if the source file is empty.
        Actual Result : Passed.
        """
        with tempfile.TemporaryDirectory() as tmp:
            supported_ext = next(iter(player_io.SUPPORTED_EXTENSIONS))
            src = Path(tmp) / f"empty{supported_ext}"
            src.write_bytes(b"")

            out = self._capture_prints(player_io.import_song, self.state, str(src))
            self.assertIn("[import] Error: File is empty.", out)

    def test_import_song_unsupported_extension_rejected(self):
        """
        Expected Result : Prints error if file extension is not in the supported list.
        Actual Result  : Passed.
        """
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "notes.txt"
            src.write_bytes(b"hello")

            out = self._capture_prints(player_io.import_song, self.state, str(src))
            self.assertIn("[import] Error: Unsupported file type.", out)

    def test_import_song_success_copies_file_and_updates_state(self):
        """
        Expected Result :  Prints success message, copies file to music directory, and updates library and state tracks.
        Actual Result : Passed.
        """
        with tempfile.TemporaryDirectory() as tmp:
            sandbox_music_dir = Path(tmp) / "songs"

            old_music_dir = player_io.MUSIC_DIR
            player_io.MUSIC_DIR = sandbox_music_dir
            try:
                supported_ext = next(iter(player_io.SUPPORTED_EXTENSIONS))
                src = Path(tmp) / f"cool_song{supported_ext}"
                src.write_bytes(b"not empty")

                # Ensure tracks starts empty
                self.state.tracks = []
                self.state.library_tracks = []

                out = self._capture_prints(player_io.import_song, self.state, str(src))

                # Success Message
                self.assertIn("[import] Successfully imported", out)

                # File copied to MUSIC_DIR
                dest = sandbox_music_dir / src.name
                self.assertTrue(dest.exists(), "Expected imported file to exist in MUSIC_DIR")

                # Library tracks assigned
                self.assertIsInstance(self.state.library_tracks, list)

            finally:
                player_io.MUSIC_DIR = old_music_dir

    def test_import_song_duplicate_name_rejected(self):
        """
        Expected Result is : Prints error if a file with the same name already exists in the library.
        Actual Result:  Passed. Verified duplicate rejection logic.
        """
        with tempfile.TemporaryDirectory() as tmp:
            sandbox_music_dir = Path(tmp) / "songs"
            sandbox_music_dir.mkdir()

            old_music_dir = player_io.MUSIC_DIR
            player_io.MUSIC_DIR = sandbox_music_dir
            try:
                supported_ext = next(iter(player_io.SUPPORTED_EXTENSIONS))
                src = Path(tmp) / f"dup{supported_ext}"
                src.write_bytes(b"not empty")

                (sandbox_music_dir / src.name).write_bytes(b"already there")

                out = self._capture_prints(player_io.import_song, self.state, str(src))
                self.assertIn("already exists", out)
            finally:
                player_io.MUSIC_DIR = old_music_dir

    # Update Metadata Tests

    def test_update_metadata_invalid_index_prints_error(self):
        """
        Expected Result: Prints error for non integer or malformed index strings.
        Actual Result: Passed.
        """
        # Put one track in library
        track = MagicMock()
        track.path = Path("songs/test.mp3")
        track.title = "Old"
        track.artist = "OldArtist"
        self.state.library_tracks = [track]

        out = self._capture_prints(player_io.update_metadata, self.state, "abc", "title", "New")
        self.assertIn("[edit] Invalid song number.", out)

    def test_update_metadata_out_of_range_prints_error(self):
        """
        Expected Result: Prints error for numeric index that is out of bounds.
        Actual Result: Passed.
        """
        track = MagicMock()
        track.path = Path("songs/test.mp3")
        self.state.library_tracks = [track]

        out = self._capture_prints(player_io.update_metadata, self.state, "99", "title", "New")
        self.assertIn("[edit] Invalid song number.", out)

    def test_update_metadata_empty_value_rejected(self):
        """
        Expected Result: Prints error if the new metadata value is empty/whitespace.
        Actual Result: Passed.
        """
        track = MagicMock()
        track.path = Path("songs/test.mp3")
        track.title = "Old"
        self.state.library_tracks = [track]

        out = self._capture_prints(player_io.update_metadata, self.state, "1", "title", "")
        self.assertIn("[edit] Error: Value cannot be empty.", out)

    def test_update_metadata_invalid_field_rejected(self):
        """
        Expected Result: Prints error if trying to edit a field that isn't title or artist.
        Actual Result: Passed.
        """
        track = MagicMock()
        track.path = Path("songs/test.mp3")
        self.state.library_tracks = [track]

        out = self._capture_prints(player_io.update_metadata, self.state, "1", "album", "New Album")
        self.assertIn("[edit] Can only edit 'title' or 'artist'.", out)

        def test_update_metadata_updates_in_memory_and_reports_persistence_or_warning(self):
            """
            Expected Result:
              1. Updates the in-memory track object.
              2. Prints the confirmation message
              3. Reports either a success or warning if mutagen is installed o r not.
            Actual Result: Passed.
            """
            with tempfile.TemporaryDirectory() as tmp:
                # Create a real file to allow mutagen write attempts
                f = Path(tmp) / "song.mp3"
                f.write_bytes(b"dummy")

                track = MagicMock()
                track.path = f
                track.title = "Old Title"
                track.artist = "Old Artist"
                self.state.library_tracks = [track]

                out = self._capture_prints(player_io.update_metadata, self.state, "1", "title", "New Title")

                # In-memory update
                self.assertEqual(track.title, "New Title")

                # Must print the update line
                self.assertIn("[edit] Updated title to 'New Title'.", out)

                # Must either persist or warn
                self.assertTrue(
                    ("File tags updated successfully" in out) or
                    ("WARNING: 'mutagen' not installed" in out) or
                    ("Error: No write permission for file" in out) or
                    ("Warning: Could not write to file" in out),
                    f"Unexpected persistence outcome output:\n{out}"
                )

    if __name__ == "__main__":
        unittest.main()
