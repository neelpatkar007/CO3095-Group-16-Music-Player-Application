"""
Module: library
Responsible for discovering audio files in the songs folder.

Used in Sprint 1 for:
 - Loading initial list of tracks from /songs (S1-01, S1-02, S1-03, S1-10, S1-12).
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List

from config import MUSIC_DIR, SUPPORTED_EXTENSIONS


@dataclass
class Track:
    path: Path
    title: str
    artist: str = "Unknown"
    duration_seconds: float | None = None

    @property
    def display_name(self) -> str:
        return f"{self.title} – {self.artist}" if self.artist else self.title


def discover_tracks() -> List[Track]:
    """
    Scan MUSIC_DIR for supported audio files and return a list of Track objects.
    """
    tracks: List[Track] = []

    if not MUSIC_DIR.exists():
        print(f"[library] WARNING: MUSIC_DIR '{MUSIC_DIR}' does not exist.")
        return tracks
    # Default values for metadata for testing before implementing search for metadata.
    for path in sorted(MUSIC_DIR.iterdir()):
        if not path.is_file():
            continue
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        title = path.stem
        # Default to 3 minutes so progress bar has a sensible scale.
        tracks.append(Track(path=path, title=title, duration_seconds=180.0))
    return tracks
