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
from typing import List

from music_player.library import Track  # Sprint 1 Track model
from music_player.time_utils import format_mm_ss


@dataclass
class Playlist:
    """
    Core model for a playlist (Sprint 2).

    Fields used by:
      - S2-01: name, tracks
      - S2-05/S2-10: num_tracks, total_duration_mm_ss
      - S2-06: iteration over tracks with durations
      - S2-11/S2-12: cloning & merging lists of tracks
    """
    name: str
    tracks: List[Track] = field(default_factory=list)

    @property
    def num_tracks(self) -> int:
        """Number of tracks (S2-05, S2-10)."""
        return len(self.tracks)

    @property
    def total_duration_seconds(self) -> float:
        """Total duration in seconds for all tracks (S2-10)."""
        # TODO: implement
        raise NotImplementedError

    @property
    def total_duration_mm_ss(self) -> str:
        """Total duration as mm:ss string (S2-10)."""
        # TODO: implement
        raise NotImplementedError

    def summary_line(self, index: int | None = None, active: bool = False) -> str:
        """
        Helper for listing playlists (S2-05, S2-10).
        Shows index, name, number of tracks and total time.
        """
        # TODO: implement
        raise NotImplementedError
