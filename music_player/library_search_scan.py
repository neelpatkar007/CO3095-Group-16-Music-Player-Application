from __future__ import annotations
from collections import defaultdict
from typing import List

from music_player.player_state import PlayerState
from music_player.library import Track, discover_tracks
from music_player.time_utils import format_mm_ss


def _print_tracks_table(tracks: List[Track]) -> None:
    """
    S2-04: Prints a formatted table of track info (Number, Title, Artist, Time).
    """
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

# S2-03 & S2-04: search & views

def search_library(state: PlayerState, query: str) -> None:
    """
    S2-03: search by title, artist, or filename.
    """
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
    S2-04: view songs in a clear text table.
    """
    print("[lib] Songs (library):")
    _print_tracks_table(state.tracks)


def view_artists_table(state: PlayerState) -> None:
    """
    S2-04: aggregate by artist.
    """
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
    """
    S2-04: approximate album by directory name containing the track.
    """
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

# S2-09: scan for new files


def rescan_for_new_tracks(state: PlayerState) -> None:
    """
    S2-09: scan the music folder for NEW files and add them to the library.
    """
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
