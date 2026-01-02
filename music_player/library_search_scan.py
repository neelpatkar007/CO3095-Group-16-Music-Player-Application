from __future__ import annotations
from collections import defaultdict
from typing import List

from music_player.player_state import PlayerState
from music_player.library import Track, discover_tracks
from music_player.time_utils import format_mm_ss


def _print_tracks_table(tracks: List[Track]) -> None:
    '''
    Prints a clean and formatted table of songs to the console.
    And because of no GUI, this ensures the text is aligned properly.
    '''

    if not tracks:
        print("  (no tracks)")
        return

    # Table headers with spacing
    print(f"{'No':>3}  {'Title':<30}  {'Artist':<20}  {'Time':>6}")
    print("-" * 65)
    for idx, t in enumerate(tracks, start=1):
        if t is None: continue
        # Truncate strings so that they do fit in the table nicely
        title = str(getattr(t, "title", "") or "")[:30]
        artist = str(getattr(t, "artist", "") or "")[:20]
        dur = format_mm_ss(getattr(t, "duration_seconds", None))
        print(f"{idx:3d}  {title:<30}  {artist:<20}  {dur:>6}")


def search_library(state: PlayerState, query: str) -> None:
    '''
    Filters the library tracks based on a users search.
    '''
    if state is None:
        return

    if not query:
        print("[search] Usage: /search <query>")
        return

    if not hasattr(state, "library_tracks"):
        print("[search] Error: Library unavailable.")
        return

    if not isinstance(state.library_tracks, list):
        print("[search] Error: Library corrupted.")
        return

    q = query.lower()
    results = []

    for t in state.library_tracks:
        if t is None:
            continue

        if q in (t.title or "").lower():
            results.append(t)
            continue

        if q in (t.artist or "").lower():
            results.append(t)
            continue

        if t.path and q in t.path.name.lower():
            results.append(t)

    if not results:
        print("[search] No matches found.")
    else:
        print(f"[search] Found {len(results)} matches:")
        _print_tracks_table(results)


def view_songs_table(state: PlayerState) -> None:
    print("[lib] --- All Songs ---")
    if not state or not state.library_tracks:
        print("  (empty library)")
        return
    _print_tracks_table(state.library_tracks)


def view_artists_table(state: PlayerState) -> None:
    '''
    Groups the library by artist and displays a summary table.
    '''
    if state is None:
        return

    if not hasattr(state, "library_tracks"):
        print("[lib] Error: Library unavailable.")
        return

    by_artist = defaultdict(list)

    for t in state.library_tracks:
        if t is None:
            continue

        if not hasattr(t, "artist"):
            by_artist["Unknown"].append(t)
            continue

        if t.artist is None:
            by_artist["Unknown"].append(t)
            continue

        if not str(t.artist).strip():
            by_artist["Unknown"].append(t)
        else:
            by_artist[t.artist].append(t)

    if not by_artist:
        print("  (no artists found)")
        return

    print(f"{'Artist':<25}  {'Tracks':>6}  {'Time':>8}")
    print("-" * 45)

    for artist, tracks in sorted(by_artist.items()):
        total = 0
        for tr in tracks:
            if tr and getattr(tr, 'duration_seconds', None):
                total += tr.duration_seconds

        print(f"{artist:<25}  {len(tracks):6d}  {format_mm_ss(total):>8}")


def view_albums_table(state: PlayerState) -> None:
    '''
    This uses the folder structure as a quick way to organise the music without any complex tagging.
    '''
    if not state or not state.library_tracks:
        return

    by_album: dict[str, List[Track]] = defaultdict(list)
    for t in state.library_tracks:
        album = t.path.parent.name or "(no folder)"
        by_album[album].append(t)

    print(f"{'Album (folder)':<25}  {'Tracks':>6}  {'Time':>8}")
    print("-" * 45)
    for album, tracks in sorted(by_album.items()):
        total = sum((t.duration_seconds or 0) for t in tracks)
        print(f"{album:<25}  {len(tracks):6d}  {format_mm_ss(total):>8}")


def rescan_for_new_tracks(state: PlayerState) -> None:
    '''
    This syncs the internal library with the actual files on disk.
    '''
    if state is None:
        print("[lib] Error: State is None.")
        return

    print("[lib] Scanning for new tracks...")

    if not hasattr(state, "library_tracks"):
        state.library_tracks = []

    if not isinstance(state.library_tracks, list):
        state.library_tracks = []

    current_paths = set()

    for t in state.library_tracks:
        if t and hasattr(t, "path") and t.path:
            current_paths.add(t.path)

    discovered = discover_tracks()

    if not discovered:
        print("[lib] No files found on disk.")
        return

    new_tracks = []

    for t in discovered:
        if t.path not in current_paths:
            new_tracks.append(t)

    if not new_tracks:
        print("[lib] No new tracks found.")
        return

    if new_tracks:
        state.library_tracks.extend(new_tracks)
        print(f"[lib] Added {len(new_tracks)} new tracks.")