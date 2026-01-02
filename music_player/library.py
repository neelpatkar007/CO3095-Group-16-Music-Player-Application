
rom __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from music_player.config import MUSIC_DIR, SUPPORTED_EXTENSIONS

# Optional dependency: mutagen for reading audio metadata
# If the user does not have mutagen installed
try:
    import mutagen
    HAS_MUTAGEN = True
except Exception:
    mutagen = None  # type: ignore
    HAS_MUTAGEN = False
    print(
        "[library] mutagen not available – using filename + defaults only."
    )


@dataclass
class Track:
    """
    Simple representation of an audio track.
    Used to pass song information between library, and UI.
    """
    path: Path
    title: str
    artist: str = "Unknown"
    duration_seconds: float | None = None

    @property
    def display_name(self) -> str:
        """
        Return a formatted display name of the track (e.g. "Song Title - Artist").
        """
        # Only show artist if available and not empty
        if self.artist:
            return f"{self.title} – {self.artist}"
        return self.title

#S1-03: Read_metadata function that meets code complexity requirement
def _read_metadata(path: Path) -> Tuple[str, str, float | None]:
    """
    Read title, artist, and duration from audio file metadata.

    Falls back to:
      - filename stem for title
      - "Unknown" for artist
      - None for duration

    if the metadata cannot be retrieved.
    """
    # Defaults based on filename
    title = path.stem
    artist = "Unknown"
    duration: float | None = None

    # If the mutagen library is not available, return defaults
    if not HAS_MUTAGEN:
        return title, artist, duration

    # Attempt to load file using mutagen
    audio = mutagen.File(path)
    if audio is None:
        return title, artist, duration

    # Extract Duration
    info = getattr(audio, "info", None)
    if info is not None and hasattr(info, "length"):
        try:
            duration = float(info.length)
        except Exception:
            # If length is malformed, we leave it as None.
            duration = None

    # Extract Tags (format-dependent)
    tags = getattr(audio, "tags", None)
    if tags:
        # Check for Title ("TIT2")
        if "TIT2" in tags:
            try:
                # Force to string in case of a weird tag types
                title = str(tags["TIT2"])
            except Exception:
                pass

        # Check for Artist
        if "TPE1" in tags:
            try:
                artist = str(tags["TPE1"])
            except Exception:
                pass

    return title, artist, duration


def discover_tracks() -> List[Track]:
    """
    Scan MUSIC_DIR for supported audio files and return a list of Track objects.

    If mutagen is available, then read real metadata

    Otherwise, we fallback to the:
        - title = filename stem
        - artist = "Unknown"
        - duration = 180.0 (3 minutes)
    """
    tracks: List[Track] = []

    # Make sure MUSIC_DIR folder exists
    if not MUSIC_DIR.exists():
        print(
            f"[library] WARNING: MUSIC_DIR '{MUSIC_DIR}' does not exist."
        )
        return tracks

    # Gives all files in the directory
    # They are sorted to ensure consistent order
    for path in sorted(MUSIC_DIR.iterdir()):

        # Skip directories and non-files
        if not path.is_file():
            continue

        # Skip any unsupported file extensions (such as .jpg, .txt, etc)
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        # Extract metadata from file or use defaults
        title, artist, duration = _read_metadata(path)

        # Default duration for Sprint 1 if the scan failed
        if duration is None:
            duration = 180.0 # Default to 3 minutes

        # Create Track object and add to the list
        track = Track(
            path=path,
            title=title,
            artist=artist,
            duration_seconds=duration
        )
        tracks.append(track)

    return tracks