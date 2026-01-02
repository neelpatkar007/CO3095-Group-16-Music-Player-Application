"""
Backbone: Sprint 2 – playlist_model

Stories:
- S2-01: Create, rename, delete playlists
- S2-05: List all playlists and pick one
- S2-06: Open playlist and show songs with durations
- S2-10: Show number of songs and total play time
- S2-11: Merge playlists
- S2-12: Copy playlists
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Any

from music_player.library import Track
from music_player.time_utils import format_mm_ss


@dataclass
class Playlist:
    """
    Core model for playlist.

    Fields used by:

      - S2-01: name, tracks
      - S2-05/S2-10: num_tracks, total_duration_mm_ss
      - S2-06: iteration over tracks with durations
      - S2-11/S2-12: cloning & merging - lists of tracks
    """
    name: str
    tracks: List[Track] = field(default_factory=list)

    def __post_init__(self) -> None:
        """
        Default initialisation and type normalisation.
        """
        if not isinstance(self.name, str):
            self.name = str(self.name)
        self.name = self.name.strip() or "(unnamed)"

        if self.tracks is None:
            self.tracks = []
        elif not isinstance(self.tracks, list):
            self.tracks = []

    @property
    def num_tracks(self) -> int:
        """
        Total duration as in seconds (S2-05, S2-10).
        """
        return len(self.tracks)

    @property
    def total_duration_seconds(self) -> float:
        """
        Total duration as in seconds (S2-05, S2-10).
        """
        total = 0.0
        for t in self.tracks:
            dur = getattr(t, "duration_seconds", None)
            if isinstance(dur, (int, float)) and dur > 0:
                total += float(dur)
        return total

    @property
    def total_duration_mm_ss(self) -> str:
        """
        Total duration as mm:ss string (S2-05, S2-10).
        """
        if not self.tracks:
            return "00:00"
        return format_mm_ss(self.total_duration_seconds)

    def summary_line(self, index: int | None = None, active: bool = False) -> str:
        """
        Helper for listing playlists (S2-05, S2-10).
        Shows index, name, number of tracks and total time.
        """
        idx_part = f"{index:02d}" if isinstance(index, int) else "--"
        active_marker = "*" if bool(active) else " "
        return (
            f"{active_marker} {idx_part}  {self.name:<20}  "
            f"{self.num_tracks:3d} tracks  {self.total_duration_mm_ss}"
        )