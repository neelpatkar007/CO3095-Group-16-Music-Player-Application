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
    print("[lib] Songs (library):")
    _print_tracks_table(state.tracks)


def view_artists_table(state: PlayerState) -> None:
    if state is None or not hasattr(state, "tracks"):
        print("[lib] Error: Library state is not available.")
        return
    if not isinstance(state.tracks, list):
        print("[lib] Error: Library tracks data is corrupted.")
        return
    if not state.tracks:
        print("[lib] Library is empty.")
        return
    by_artist: dict[str, List[Track]] = defaultdict(list)
    for t in state.tracks:
        if not t or not getattr(t, "artist", None):
            continue
        by_artist[t.artist].append(t)
    if not by_artist:
        print("[lib] No artist information available.")
        return
    print(f"{'Artist':<25}  {'Tracks':>6}  {'Time':>8}")
    print("-" * 45)
    for artist, tracks in sorted(by_artist.items()):
        count = len(tracks)
        total = 0.0
        for t in tracks:
            if t and t.duration_seconds is not None:
                total += t.duration_seconds
        print(f"{artist:<25}  {count:6d}  {format_mm_ss(total):>8}")


def view_albums_table(state: PlayerState) -> None:
    by_album: dict[str, List[Track]] = defaultdict(list)
    for t in state.tracks:
        album = t.path.parent.name or "(no folder)"
        by_album[album].append(t)
    print(f"{'Album (folder)':<25}  {'Tracks':>6}  {'Time':>8}")
    print("-" * 45)
    for album, tracks in sorted(by_album.items()):
        count = len(tracks)
        total = 0.0
        for t in tracks:
            if t.duration_seconds is not None:
                total += t.duration_seconds
        print(f"{album:<25}  {count:6d}  {format_mm_ss(total):>8}")

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