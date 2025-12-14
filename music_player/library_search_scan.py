"""
Backbone: Sprint 2 – library_search_scan

Stories:
- S2-03: Search library by title, artist, file name
- S2-04: View songs/albums/artists in clear text tables
- S2-09: Scan music folder for new files
"""

from __future__ import annotations
from collections import defaultdict
from typing import List

from music_player.player_state import PlayerState
from music_player.library import Track, discover_tracks
from music_player.time_utils import format_mm_ss


def _print_tracks_table(tracks: List[Track]) -> None:
    """
    Shared helper to print a table of tracks (S2-04).
    Columns: No, Title, Artist, Time.
    """
    # TODO: implement
    raise NotImplementedError


# S2-03 & S2-04


def search_library(state: PlayerState, query: str) -> None:
    """
    S2-03:
      - Case-insensitive search across title, artist, and file name.
      - Print results using _print_tracks_table.
    """
    # TODO: implement
    raise NotImplementedError


def view_songs_table(state: PlayerState) -> None:
    """
    S2-04:
      - Use _print_tracks_table to show all library tracks.
    """
    # TODO: implement
    raise NotImplementedError


def view_artists_table(state: PlayerState) -> None:
    """
    S2-04:
      - Group tracks by artist.
      - Show artist name, track count, total duration.
    """
    # TODO: implement
    raise NotImplementedError


def view_albums_table(state: PlayerState) -> None:
    """
    S2-04:
      - Approximate album by parent folder name of each track.
      - Show album (folder), number of tracks, total duration.
    """
    # TODO: implement
    raise NotImplementedError


# S2-09


def rescan_for_new_tracks(state: PlayerState) -> None:
    if state is None or not hasattr(state, "tracks"):
        print("[lib] Error: Library state is not available.")
        return
    if not isinstance(state.tracks, list):
        print("[lib] Error: Library tracks data is corrupted.")
        return
    print("[lib] Scanning for new tracks...")

    current_paths = {
        t.path
        for t in state.tracks
        if t is not None and getattr(t, "path", None) is not None
    }
    discovered = discover_tracks()

    if not discovered:
        print("[lib] No tracks found on disk.")
        return
