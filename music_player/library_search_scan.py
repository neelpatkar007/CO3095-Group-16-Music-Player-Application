from __future__ import annotations
from collections import defaultdict
from typing import List

from music_player.player_state import PlayerState
from music_player.library import Track, discover_tracks
from music_player.time_utils import format_mm_ss


def _print_tracks_table(tracks: List[Track]) -> None:
    if not tracks:
        print("  (no tracks)")
        return

    print(f"{'No':>3}  {'Title':<30}  {'Artist':<20}  {'Time':>6}")
    print("-" * 65)
    for idx, t in enumerate(tracks, start=1):
        title = (t.title or "")[:30]
        artist = (t.artist or "")[:20]
        dur = format_mm_ss(t.duration_seconds)
        print(f"{idx:3d}  {title:<30}  {artist:<20}  {dur:>6}")


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
    """
    S2-09:
      - Call discover_tracks() to re-scan MUSIC_DIR.
      - Compare paths with current state.tracks.
      - Append any new tracks and print how many were added.
    """
    # TODO: implement
    raise NotImplementedError