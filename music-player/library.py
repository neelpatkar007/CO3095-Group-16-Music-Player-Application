from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from config import MUSIC_DIR, SUPPORTED_EXTENSIONS

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
    """Simple representation of an audio track."""
    path: Path
    title: str
    artist: str = "Unknown"
    duration_seconds: float | None = None

    @property
    def display_name(self) -> str:
        """Return formatted display name of the track."""
        if self.artist:
            return f"{self.title} – {self.artist}"
        return self.title


def _read_metadata(path: Path) -> Tuple[str, str, float | None]:
    """
    Read title, artist, and duration from audio file metadata.

    Falls back to:
      - filename stem for title
      - "Unknown" for artist
      - None for duration

    if metadata cannot be retrieved.
    """
    title = path.stem
    artist = "Unknown"
    duration: float | None = None

    if not HAS_MUTAGEN:
        return title, artist, duration

    audio = mutagen.File(path)
    if audio is None:
        return title, artist, duration

    # Duration
    info = getattr(audio, "info", None)
    if info is not None and hasattr(info, "length"):
        try:
            duration = float(info.length)
        except Exception:
            duration = None

    # Tags (format-dependent)
    tags = getattr(audio, "tags", None)
    if tags:
        # Title
        if "TIT2" in tags:
            try:
                title = str(tags["TIT2"])
            except Exception:
                pass

        # Artist
        if "TPE1" in tags:
            try:
                artist = str(tags["TPE1"])
            except Exception:
                pass

    return title, artist, duration


def discover_tracks() -> List[Track]:
    """
    Scan MUSIC_DIR for supported audio files and return a list of Track objects.

    If mutagen is available:
        - read real metadata

    Otherwise fallback to:
        - title = filename stem
        - artist = "Unknown"
        - duration = 180.0 (3 minutes)
    """
    tracks: List[Track] = []

    if not MUSIC_DIR.exists():
        print(
            f"[library] WARNING: MUSIC_DIR '{MUSIC_DIR}' does not exist."
        )
        return tracks

    for path in sorted(MUSIC_DIR.iterdir()):
        if not path.is_file():
            continue

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        title, artist, duration = _read_metadata(path)

        # Default duration for Sprint 1
        if duration is None:
            duration = 180.0

        track = Track(
            path=path,
            title=title,
            artist=artist,
            duration_seconds=duration
        )
        tracks.append(track)

    return tracks