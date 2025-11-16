"""
Module: library
Responsible for discovering audio files in the songs folder.

Used in Sprint 1 for:
 - Loading initial list of tracks from /songs (S1-01, S1-02, S1-03, S1-10, S1-12).
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List

from config import MUSIC_DIR, SUPPORTED_EXTENSIONS


@dataclass
class Track:
    path: Path
    title: str
    artist: str = "Unknown"
    duration_seconds: float | None = None  # will be filled in later


def discover_tracks() -> List[Track]:
    """
    Scan MUSIC_DIR for supported audio files and return a list of Track objects.
    """
    # implement file discovery.
    return []
