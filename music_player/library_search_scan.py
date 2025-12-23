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
        if t is None: continue
        title = str(getattr(t, "title", "") or "")[:30]
        artist = str(getattr(t, "artist", "") or "")[:20]
        dur = format_mm_ss(getattr(t, "duration_seconds", None))
        print(f"{idx:3d}  {title:<30}  {artist:<20}  {dur:>6}")


def search_library(state: PlayerState, query: str) -> None:
    if state is None: return
    query = (query or "").strip().lower()
    if not query:
        print("[lib] Usage: /search <text>")
        return

    source_list = state.library_tracks

    results: List[Track] = []
    for t in source_list:
        if t is None: continue
        title = (getattr(t, "title", "") or "").lower()
        artist = (getattr(t, "artist", "") or "").lower()
        filename = ""
        if getattr(t, "path", None) is not None:
            filename = t.path.name.lower()

        if query in title or query in artist or query in filename:
            results.append(t)

    if not results:
        print("[lib] No matches found.")
    else:
        print(f"[lib] Search results for '{query}':")
        _print_tracks_table(results)


def view_songs_table(state: PlayerState) -> None:
    print("[lib] Songs (library):")
    _print_tracks_table(state.library_tracks)


def view_artists_table(state: PlayerState) -> None:
    by_artist: dict[str, List[Track]] = defaultdict(list)
    for t in state.library_tracks:
        if not t or not getattr(t, "artist", None): continue
        by_artist[t.artist].append(t)

    print(f"{'Artist':<25}  {'Tracks':>6}  {'Time':>8}")
    print("-" * 45)
    for artist, tracks in sorted(by_artist.items()):
        total = sum((t.duration_seconds or 0) for t in tracks)
        print(f"{artist:<25}  {len(tracks):6d}  {format_mm_ss(total):>8}")


def view_albums_table(state: PlayerState) -> None:
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
    print("[lib] Scanning for new tracks...")
    current_paths = {t.path for t in state.library_tracks}
    discovered = discover_tracks()

    new_tracks = [t for t in discovered if t.path not in current_paths]

    if not new_tracks:
        print("[lib] No new tracks found.")
        return

    state.library_tracks.extend(new_tracks)


    if state.tracks is state.library_tracks:
        pass

    print(f"[lib] Added {len(new_tracks)} new track(s).")