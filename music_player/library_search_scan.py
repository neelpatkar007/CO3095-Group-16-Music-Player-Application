
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
    # Basic state validation
    if state is None or not hasattr(state, "tracks"):
        print("[lib] Error: Library state is not available.")
        return
    if not isinstance(state.tracks, list):
        print("[lib] Error: Library tracks data is corrupted.")
        return
    if not state.tracks:
        print("[lib] Library is empty.")
        return
    query = (query or "").strip().lower()
    if not query:
        print("[lib] Usage: /search <text>")
        return
    results: List[Track] = []
    for t in state.tracks:
        if t is None:
            continue

        title = (getattr(t, "title", "") or "").lower()
        artist = (getattr(t, "artist", "") or "").lower()

        filename = ""
        if getattr(t, "path", None) is not None:
            filename = t.path.name.lower()

        if (
                query in title
                or query in artist
                or query in filename
        ):
            results.append(t)

    if not results:
        print("[lib] No matches found.")

    print(f"[lib] Search results for '{query}':")
    _print_tracks_table(results)



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

    new_tracks: List[Track] = []
    for t in discovered:
        if t is None or not getattr(t, "path", None):
            continue
        if t.path in current_paths:
            continue
        if (
                getattr(t, "duration_seconds", None) is not None
                and t.duration_seconds <= 0
        ):
            continue
        new_tracks.append(t)

    if not new_tracks:
        print("[lib] No new tracks found.")
        return

    state.tracks.extend(new_tracks)
    if len(new_tracks) > 50:
        print(f"[lib] Bulk imported {len(new_tracks)} new tracks into the library.")
    else:
        print(f"[lib] Added {len(new_tracks)} new track(s) to the library.")
